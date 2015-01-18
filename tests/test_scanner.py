# -*- coding: utf-8 -*-
from unittest import TestCase
from cStringIO import StringIO
from textwrap import dedent
from pprint import pformat

from parser.scanner import OysterScanner


class ScannerTests(TestCase):
    def assertScansTo(self, scanner, expected):
        res = [t[0] for t in scanner.read_all()]
        pairs = zip(expected, res)
        if not all([pair[0] == pair[1] for pair in pairs]):
            raise AssertionError(
                "Scan failed to match:\n%s" % pformat(pairs, 4))

    def test_symbol(self):
        file = StringIO("a-symbol")
        scanner = OysterScanner(file, "test_symbol")
        expected = ["line", "symbol", "endline"]

        self.assertScansTo(scanner, expected)

    def test_number(self):
        file = StringIO("242")
        scanner = OysterScanner(file, "test_number")
        expected = ["line", "number", "endline"]

        self.assertScansTo(scanner, expected)

    def test_chain(self):
        file = StringIO("(a-symbol 3 b)")
        scanner = OysterScanner(file, "test_close")
        expected = ["line", "open", "symbol",
                    "number", "symbol", "close", "endline"]

        self.assertScansTo(scanner, expected)

    def test_indentation(self):
        code = """
        this:
            is
        sparta
        """
        file = StringIO(dedent(code))
        scanner = OysterScanner(file, "test_indentation")
        expected = ["line", "symbol", "colon", "indent",
                    "line", "symbol", "endline",
                    "dedent", "endline",
                    "line", "symbol", "endline"]

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
        expected = ["line", "open", "symbol", "endline",
                    "line", "symbol", "colon", "indent",
                    "line", "symbol", "dedent", "close",
                    "number", "endline",
                    "line", "symbol", "endline"]

        self.assertScansTo(scanner, expected)

    def xtest_plus_program(self):
        code = """
        set my-plus: λ(x y):
            # commentary goes here
            + x y

        my-plus 2 (+ 3 5)
        """
        file = StringIO(dedent(code))
        scanner = OysterScanner(file, "test_plus")
        expected = ['nodent', 'symbol', 'symbol', 'colon',
                    'symbol', 'open', 'symbol', 'symbol', 'close', 'colon',
                    'indent', 'symbol', 'symbol', 'symbol',
                    'dedent', 'symbol', 'number',
                    'open', 'symbol', 'number', 'number', 'close',
                    'nodent', None]

        self.assertScansTo(scanner, expected)
