# -*- coding: utf-8 -*-

from cStringIO import StringIO
from textwrap import dedent
from pprint import pformat

from test_case import TestCase
from interpreter.code_objects import *
from parser.scanner import OysterScanner


class ScannerTests(TestCase):
    def assertScansTo(self, scanner, expected):
        res = (scanner.read()[0] for i in xrange(10000))
        pairs = zip(expected, res)
        if not all([pair[0] == pair[1] for pair in pairs]):
            raise AssertionError(
                "Scan failed to match:\n%s" % pformat(pairs, 4))

    def test_symbol(self):
        file = StringIO("a-symbol")
        scanner = OysterScanner(file, "test_symbol")
        res = scanner.read()
        self.assertEqual(res[0], "Symbol")
        self.assertEqual(res[1], "a-symbol")

    def test_number(self):
        file = StringIO("242")
        scanner = OysterScanner(file, "test_number")
        res = scanner.read()
        self.assertEqual(res[0], "Number")
        self.assertEqual(res[1], "242")

    def test_chain(self):
        file = StringIO("(a-symbol 3 b)")
        scanner = OysterScanner(file, "test_close")
        expected = ["open",
                    "Symbol",
                    "Number",
                    "Symbol",
                    "close"]

        self.assertScansTo(scanner, expected)

    def test_indentation(self):
        code = """
        this:
            is
        sparta
        """
        file = StringIO(dedent(code))
        scanner = OysterScanner(file, "test_indentation")
        expected = ["nodent", "Symbol", "colon",
                    "indent", "Symbol",
                    "dedent", "Symbol", "nodent", None]

        self.assertScansTo(scanner, expected)

    def test_parens_and_indentation(self):
        code = """
        (this
         is:
             mine) 5
        sparta
        """
        file = StringIO(dedent(code))
        scanner = OysterScanner(file, "test_parens_and_indentation")
        expected = ["nodent", "open", "Symbol",
                    "nodent", "Symbol", "colon",
                    "indent", "Symbol", "dedent", "close", "Number",
                    "nodent", "Symbol", "nodent", None]

        self.assertScansTo(scanner, expected)

    def test_plus_program(self):
        code = """
        set my-plus: λ(x y):
            # commentary goes here
            + x y

        my-plus 2 (+ 3 5)
        """
        file = StringIO(dedent(code))
        scanner = OysterScanner(file, "test_plus")
        expected = ['nodent', 'Symbol', 'Symbol', 'colon',
                      'Symbol', 'open', 'Symbol', 'Symbol', 'close', 'colon',
                    'indent', 'Symbol', 'Symbol', 'Symbol',
                    'dedent', 'Symbol', 'Number',
                      'open', 'Symbol', 'Number', 'Number', 'close',
                    'nodent', None]

        self.assertScansTo(scanner, expected)
