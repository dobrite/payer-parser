import sys
from os import path

from tmobile import read_file
from tmobile import duplicates_equal
from tmobile import split_duplicates
from tmobile import parse
from tmobile import grouper
from tmobile import output
from tmobile import write_file

VERSION = "0.13"

if __name__ == "__main__":
    print "T-Mobile collections email parser v{}".format(VERSION)
    assert not len(sys.argv) > 2, (
        "Too many arguments supplied, "
        "please drag and drop email file onto this program "
        "or supple a single file-name as a command line argument"
    )

    assert len(sys.argv) == 2, (
        "Please drag and drop email file onto this program "
        "or supply the file-name as an command line argument"
    )

    HERE = path.dirname(sys.argv[0])
    text = read_file(sys.argv[1])

    split = split_duplicates(text)
    assert duplicates_equal(split), "A section is different"
    print "All sections are equal"

    result = parse(split[0])

    total_num, total_amt, settle_date = result[:3]
    invoices = result[3:]

    assert total_num == len(invoices) / 4, (
        "The 'Number of remittance lines' does not equal "
        "the amount of invoices processed {}, {}"
        .format(total_num, len(invoices) / 4)
    )

    total_total = sum(t[1] for t in grouper(4, invoices))
    total_payment = sum(t[2] for t in grouper(4, invoices))
    total_discount = sum(t[3] for t in grouper(4, invoices))
    output_csv = output(invoices, settle_date)

    print "Number of invoices: {}".format(total_num)
    print "Sum of invoice payment amount: {}".format(total_amt)
    print "Sum of invoice discount: {}".format(total_discount)
    print "Sum of invoice total: {}".format(total_total)
    print "Invoice total less discount: {}".format(
        total_total + total_discount
    )

    assert total_amt == total_payment, (
        "Total of all 'invoice payment amount' does not equal "
        "'payment amount'"
    )

    assert total_amt == total_total + total_discount, (
        "'Payment Amount' does not equal 'Invoice total less discount' amount"
    )

    write_file(HERE, output_csv)

    print "File written to disk with no errors"
    raw_input("Press return to exit")
