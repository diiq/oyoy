# -*- coding: utf-8 -*-
from unittest import TestCase
from textwrap import dedent
from pprint import pformat

from oyster.oyster_scanner import *
from lib.parsing.stream import Stream


class ScannerTests(TestCase):
    def assertMatch(self, reader, string):
        stream = Stream(string)
        assert reader.read(stream)

    def assertNotMatch(self, reader, string):
        stream = Stream(string)
        assert not reader.read(stream)

    def test_letter(self):
        self.assertMatch(letter, "f")
        self.assertNotMatch(letter, "?")

    def test_digit(self):
        self.assertMatch(digit, "5")
        self.assertNotMatch(digit, "F")

    def test_operator(self):
        self.assertMatch(operator, "...")
        self.assertMatch(operator, "== s")
        self.assertNotMatch(operator, "FAQ")

    def test_symbol(self):
        self.assertMatch(symbol, "hello-there ")
        self.assertMatch(symbol, "sw$en$y+toad ")
        self.assertNotMatch(symbol, "?barf ")

    def assertScansTo(self, code, expected):
        scanner = OysterScanner(dedent(code))
        res = [t.purpose for t in scanner.tokenize()]
        pairs = zip(expected, res)
        if not all([pair[0] == pair[1] for pair in pairs]):
            raise AssertionError(
                "Scan failed to match:\n%s" % pformat(pairs, 4))

    def test_lone_symbol(self):
        code = """
        a-symbol
        """
        expected = ["line", "symbol", "endline"]

        self.assertScansTo(code, expected)

    def test_lone_number(self):
        code = """
        242
        """
        expected = ["line", "number", "endline"]

        self.assertScansTo(code, expected)

    def test_chain(self):
        code = """
        (a-symbol 3 b)
        """
        expected = ["line", "open", "symbol",
                    "number", "symbol", "close", "endline"]

        self.assertScansTo(code, expected)

    def test_indentation(self):
        code = """
        this:
            is
        sparta
        """
        expected = ["line", "symbol", "colondent", "indent",
                    "line", "symbol", "endline",
                    "dedent", "endline",
                    "line", "symbol", "endline"]

        self.assertScansTo(code, expected)

    def test_parens_and_indentation(self):
        code = """
        (this
         is:
             mine) 5
        sparta
        """
        expected = ["line", "open", "symbol", "endline",
                    "line", "symbol", "colondent", "indent",
                    "line", "symbol", "dedent", "close",
                    "number", "endline",
                    "line", "symbol", "endline"]

        self.assertScansTo(code, expected)

    def test_plus_program(self):
        code = """
        set my-plus: λ(x y):
            # commentary goes here
            x + y

        my-plus 2 (3 + 5)
        """
        expected = ['line', 'symbol', 'symbol', 'colon',
                    'symbol', 'open', 'symbol', 'symbol', 'close',
                    'colondent', 'indent',
                    'line', 'symbol', '+', 'symbol', 'endline',
                    'dedent', 'endline',
                    'line', 'symbol', 'number',
                    'open', 'number', '+', 'number', 'close',
                    'endline']

        self.assertScansTo(code, expected)
