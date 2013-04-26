import parsley
from os import path
from decimal import Decimal
from itertools import izip_longest


def split_duplicates(text):
    """Splits email into its duplicate chunks"""

    #string at index 0 will be ''
    split_text = text.split("your payment processed")[1:]
    return [section.strip() for section in split_text]


def duplicates_equal(split_text):
    """Returns if all sections of a split email are equal"""

    for section in split_text[1:]:
        if split_text[0] != section:
            return False

    return True


def read_file(filename):
    """Convenience function to read in a file"""

    with open(filename) as ap_file:
        full_text = ap_file.read().lower()

    return full_text


def write_file(directory, output_csv):
    """Convenience function to write file to output.csv"""

    with open(path.join(directory, 'output.csv'), 'w') as f:
        f.write(output_csv)


def grouper(n, iterable, fillvalue=None):
    """Take from itertools documentation
    Collect data into fixed-length chunks or blocks
    grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx

    """

    args = [iter(iterable)] * n

    return izip_longest(fillvalue=fillvalue, *args)


def to_dec(s):
    """Returns a string as a Decimal"""

    return Decimal(s.replace(',', ''))


def parse(text):
    """Performs the parse using the defined grammar"""

    return [tokens for tokens in G(text).summarize() if tokens is not None]


def date_format(d):
    """Returns a consistent MM/DD/YYYY format"""

    month, day, year = d.split('/')
    year = '20' + year if len(year) == 2 else year

    return "{}/{}/{}".format(month, day, year)


def add_line(num, discount, total, settle_date):
    """Returns a line of csv using the input args"""

    discount = '' if discount == Decimal('-0.00') else discount

    return ",{},,,,{},,{},{}\n".format(num, discount, total, settle_date)


def output(invoices, settle_date):
    """Creates the csv"""

    output_csv = ''
    for inv_num, total, payment, discount in grouper(4, invoices):
        output_csv += add_line(inv_num, discount, total, settle_date)

    return output_csv


G = parsley.makeGrammar("""
    skip = anything:s ?(type(s) is str) -> None
    ws = ' '*
    ws_colon_ws = ws ':' ws
    digit = anything:x ?(x in '0123456789') -> x
    money = <(digit{1,3} ','*)+ '.' digit{2}>
    date = <digit{1, 2} '/' digit{1, 2} '/' (digit{4} | digit{2})>:d -> date_format(d)
    inv_num_format = <'ca' digit+ | digit+>:n -> n.replace('ca', 'CA') if n.startswith('ca') else 'NE' + n

    num_inv = 'number of remittance lines' ws_colon_ws <digit+>:n -> int(n)
    settle_date = 'settle date' ws_colon_ws date
    payment_amount = 'total amount deposited' ws ':usd' ws money:m -> to_dec(m)
    inv_number = 'invoice number' ws_colon_ws inv_num_format
    inv_total = 'invoice total' ws_colon_ws money:m -> to_dec(m)
    inv_payment = 'invoice payment amount' ws_colon_ws money:m -> to_dec(m)
    inv_discount = 'invoice discount' ws_colon_ws money:m -> to_dec(m) * -1

    summarize = (
        num_inv
        | settle_date
        | payment_amount
        | inv_number
        | inv_total
        | inv_payment
        | inv_discount
        | skip
    )+
    """, {
            "to_dec": to_dec,
            "date_format": date_format
    }
)
