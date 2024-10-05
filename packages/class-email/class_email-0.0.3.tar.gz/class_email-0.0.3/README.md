# A tool for spitting out .eml files from a template and a CSV file

Built for UNSW COMP6[48]41 tutors, because we don't get to use SMTP with Outlook, since we can't add OAuth applications.

Defaults are tailored to the COMP6[48]41 marking spreadsheet for 24T3.

```
Usage: class-email [OPTIONS] DATAFILE TEMPLATE SUBJECT

  Creates .eml files for each row in DATAFILE. The email body is generated
  from TEMPLATE, which is a Jinja2 template. Each email's subject will be
  SUBJECT.

Options:
  --filter TEXT            An allowed value for the column specified by
                           --filter-column. Not compatible with --filter-file.
  --filter-file FILENAME   A file with allowed values for the column specified
                           by --filter-column. Values should be separated by
                           newlines. Not compatible with --filter-file.
  --filter-column INTEGER  The column to filter on. First column is column 0.
                           Defaults to 0 when using --filter-file and 3 when
                           using --filter.
  --sender TEXT            If specified, the From header is added to .eml
                           files - useful if you have multiple sending
                           addresses configured in your email client.
  --email-column INTEGER   The column to use as the email address. First
                           column is column 0. Defaults to 4.
  --header-count INTEGER   Number of header rows. Defaults to 2.
  --outdir DIRECTORY       A directory where .eml files should be output to.
  --yes                    Auto-open all output email files without prompting.
  --no                     Skips the file open prompt without opening.
  --help                   Show this message and exit.
```