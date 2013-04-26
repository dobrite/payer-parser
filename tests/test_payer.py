#nosetests --with-cov --cov-report term-missing --cov payer tests/

import unittest
from nose.tools import eq_
from decimal import Decimal

from payer import parse
from payer import output
from payer import read_file
from payer import split_duplicates
from payer import duplicates_equal


class TestUnitCollections(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_settle_date(self):
        # test to ensure invoice numbers with 'CA' in the front are left
        eq_(parse("settle date      :12/3/2012")[0], '12/3/2012')

    def test_ca_invoice_name(self):
        # test to ensure invoice numbers with 'ca' in the front are left
        eq_(parse("invoice number   :ca54592")[0], 'CA54592')

    def test_ne_invoice_name(self):
        # test to ensure invoice numbers without 'CA' in the front have 'NE' added
        eq_(parse("invoice number   :54592")[0], 'NE54592')

    def test_invoice_total(self):
        # test to ensure the invoice total is returned as the correct Decimal
        eq_(parse("invoice total    :27.00")[0], Decimal('27.00'))

    def test_invoice_payment(self):
        # test to ensure the invoice total is returned as the correct Decimal
        eq_(parse("invoice payment amount   :27.96")[0], Decimal('27.96'))

    def test_invoice_discount(self):
        # test to ensure the invoice total is returned as the correct Decimal
        eq_(parse("invoice discount :8.50")[0], Decimal('-8.50'))

    def test_invoice_discount_one(self):
        # test to ensure the invoice total is returned as the correct Decimal
        eq_(parse("invoice discount :1.00")[0], Decimal('-1.00'))

    def test_invoice_discount_zero(self):
        # test to ensure the invoice total is returned as the correct Decimal
        eq_(parse("invoice discount :0.00")[0], Decimal('0.00'))

    def test_money_conversion(self):
        # test to ensure the commas in invoice total are returned as the correct Decimal
        eq_(parse("invoice total :8.50")[0], Decimal('8.50'))
        eq_(parse("invoice total :98.97")[0], Decimal('98.97'))
        eq_(parse("invoice total :198.44")[0], Decimal('198.44'))
        eq_(parse("invoice total :6,198.44")[0], Decimal('6198.44'))
        eq_(parse("invoice total :56,198.44")[0], Decimal('56198.44'))
        eq_(parse("invoice total :956,198.44")[0], Decimal('956198.44'))
        eq_(parse("invoice total :1,956,198.44")[0], Decimal('1956198.44'))
        eq_(parse("invoice total :71,956,198.44")[0], Decimal('71956198.44'))
        eq_(parse("invoice total :371,956,198.44")[0], Decimal('371956198.44'))
        eq_(parse("invoice total :5,371,956,198.44")[0], Decimal('5371956198.44'))
        eq_(parse("invoice total :15,371,956,198.44")[0], Decimal('15371956198.44'))
        eq_(parse("invoice total :105,371,956,198.44")[0], Decimal('105371956198.44'))
        eq_(parse("invoice total :3,105,371,956,198.44")[0], Decimal('3105371956198.44'))

    def test_date_conversion(self):
        # test to ensure dates with 4 digit year are return correctly
        eq_(parse("settle date      :12/3/2012")[0], '12/3/2012')
        eq_(parse("settle date      :2/3/2012")[0], '2/3/2012')
        eq_(parse("settle date      :10/31/2012")[0], '10/31/2012')
        eq_(parse("settle date      :1/31/2012")[0], '1/31/2012')

    def test_date_2_digit_year(self):
        # test to ensure dates with 2 digit years are return correctly
        eq_(parse("settle date      :12/3/12")[0], '12/3/2012')
        eq_(parse("settle date      :2/3/12")[0], '2/3/2012')
        eq_(parse("settle date      :10/31/12")[0], '10/31/2012')
        eq_(parse("settle date      :1/31/12")[0], '1/31/2012')

    def test_ws_colon_ws(self):
        # test to ensure whitespace colon whitespace in parser works correctly
        eq_(parse("settle date:12/3/2012")[0], '12/3/2012')
        eq_(parse("settle date :12/3/2012")[0], '12/3/2012')
        eq_(parse("settle date: 12/3/2012")[0], '12/3/2012')
        eq_(parse("settle date : 12/3/2012")[0], '12/3/2012')
        eq_(parse("settle date               :              12/3/2012")[0], '12/3/2012')

    def test_split_duplicates(self):
        s = "your payment processed blah your payment processed blah your payment processed blah"
        eq_(split_duplicates(s), ['blah', 'blah', 'blah'])

    def test_duplicates_equal_true(self):
        eq_(duplicates_equal(['blah', 'blah', 'blah']), True)

    def test_duplicates_equal_false(self):
        eq_(duplicates_equal(['blah', 'blah', 'clah']), False)


class TestIntegrationCollections(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_integration_split_duplicates(self):
        s = read_file("./tests/files/email.txt")
        eq_(len(split_duplicates(s)), 6)

    def test_email_count(self):
        # integration test to ensure all lines are parsed
        eq_(len(parse(read_file("./tests/files/email_split.txt"))), 1523)

    def test_email_all(self):
        # complete integration test
        original = open("./tests/files/output.csv", 'U').read()
        parsed = parse(read_file("./tests/files/email_split.txt"))[3:]
        output_csv = output(parsed, '12/3/2012')
        eq_(output_csv, original)

if __name__ == '__main__':
    unittest.main()
