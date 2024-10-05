import os
import platform
import subprocess
from csv import reader
from pathlib import Path
from typing import TextIO

import click
from jinja2 import DictLoader, Environment, select_autoescape


@click.command(
    help="Creates .eml files for each row in DATAFILE. The email body is generated from TEMPLATE, which is a Jinja2 template. Each email's subject will be SUBJECT."
)
@click.option(
    "--filter",
    help="An allowed value for the column specified by --filter-column. Not compatible with --filter-file.",
)
@click.option(
    "--filter-file",
    type=click.File("r"),
    help="A file with allowed values for the column specified by --filter-column. Values should be separated by newlines. Not compatible with --filter-file.",
)
@click.option(
    "--filter-column",
    type=int,
    help="The column to filter on. First column is column 0. Defaults to 0 when using --filter-file and 3 when using --filter.",
)
@click.option(
    "--sender",
    help="If specified, the From header is added to .eml files - useful if you have multiple sending addresses configured in your email client.",
)
@click.option(
    "--email-column",
    type=int,
    default=4,
    help="The column to use as the email address. First column is column 0. Defaults to 4.",
)
@click.option("--header-count", default=2, help="Number of header rows. Defaults to 2.")
@click.option(
    "--outdir",
    type=click.Path(file_okay=False, writable=True, resolve_path=True, path_type=Path),
    default="./out",
    help="A directory where .eml files should be output to.",
)
@click.option(
    "--yes",
    "open_files",
    flag_value="yes",
    help="Auto-open all output email files without prompting.",
)
@click.option(
    "--no",
    "open_files",
    flag_value="no",
    help="Skips the file open prompt without opening.",
)
@click.argument("datafile", type=click.File("r"))
@click.argument(
    "template",
    type=click.File("r"),
)
@click.argument("subject")
def main(
    open_files: bool | None,
    header_count: int,
    filter: str | None,
    filter_file: TextIO | None,
    filter_column: int | None,
    email_column: int,
    sender: str | None,
    outdir: Path,
    datafile: TextIO,
    template: TextIO,
    subject: str,
):
    if filter_file and filter:
        raise click.BadArgumentUsage(
            "--filter and --filter-file cannot be used together."
        )
    elif filter:
        allowed_values = [filter.strip()]
        if filter_column is None:
            filter_column = 3
    elif filter_file:
        allowed_values = [
            line.strip() for line in filter_file.readlines() if line.strip()
        ]
        if filter_column is None:
            filter_column = 0
    else:
        allowed_values = None

    csv = reader(datafile)
    data = []
    for i, row in enumerate(csv):
        if i < header_count or (
            filter_column is not None
            and allowed_values is not None
            and row[filter_column].strip() not in allowed_values
        ):
            continue
        data.append(row)

    loader = DictLoader({"template.html": template.read()})
    env = Environment(loader=loader, autoescape=select_autoescape())
    t = env.get_template("template.html")

    if not outdir.exists():
        outdir.mkdir(parents=True)

    files = []
    for row in data:
        target = row[email_column].split("@")[0]
        file = outdir / f"{target}.eml"
        with open(file, "w") as f:
            if sender:
                f.write(f"From: <{sender}>\r\n")
            f.write(f"To: {row[email_column]}\r\n")
            f.write(f"Subject: {subject}\r\n")
            f.write("X-Unsent: 1\r\n")
            f.write("Content-Type: text/html\r\n")
            f.write("\r\n\r\n")
            f.write(t.render(data=row))
        files.append(file)

    click.echo(
        f"{len(data)} .eml files have been output to ./{outdir.relative_to(Path().resolve())}."
    )
    if open_files != "no" and (
        open_files == "yes"
        or click.confirm(
            f"Do you want to open the email files in your preferred email client?"
        )
    ):
        for fn in files:
            fn = fn.resolve()
            if platform.system() == "Darwin":  # macOS
                subprocess.call(("open", str(fn)))
            elif platform.system() == "Windows":  # Windows
                os.startfile(str(fn))  # type: ignore
            else:  # Linux
                subprocess.call(("xdg-open", str(fn)))
