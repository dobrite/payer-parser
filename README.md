# Script to convert a human-readable email back into a CSV

NOTE: Permission was granted by client to make this script public.
All data has been sanitzed.

Client would receive an email detailing payment information in a
multi-lined human readable format (see sanitzed.txt). Each email
was for a single check, but contained payments for hundreds of line
items. The email was manually converted into a csv format for further
data processing.

The script uses [Parsley][pa], a [PEG][pg] based parser library
to take the input email and output a csv.

The script was compiled into a windows .exe using [py2exe][p2]
and the user drags and drops a copy of the email.
An output file is produced.

[pa]: http://parsley.readthedocs.org/en/latest/index.html
[pg]: http://en.wikipedia.org/wiki/Parsing_expression_grammar
[p2]: http://www.py2exe.org/

## Approximate time savings: 5 hours of work per week.


