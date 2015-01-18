# -*- coding: utf-8 -*-

from cStringIO import StringIO
from textwrap import dedent
from pprint import pformat

from test_case import TestCase
from interpreter.code_objects import *
from parser.parser import OysterParser
from parser.scanner import OysterScanner


class ParserTests(TestCase):
    def assertDeepMatch(self, actual, expected):
        print actual, expected
        if isinstance(actual, List):
            self.assertEqual(len(actual.items), len(expected))
            for item in zip(actual.items, expected):
                self.assertDeepMatch(*item)

        elif isinstance(actual, Symbol):
            self.assertEqual(actual.symbol, expected)

        elif isinstance(actual, Number):
            self.assertEqual(acutal.number, expected)

        else:
            assert False, "Unknown type: %s" % actual.__class__.__name__

    def assertParsesTo(self, code, expected):
        file = StringIO(dedent(code))
        tokens = OysterScanner(file, "test").read_all()
        statements = OysterParser.parse(tokens)
        self.assertEqual(len(statements), len(expected))
        for statement in zip(statements, expected):
            self.assertDeepMatch(*statement)


    def test_one_line_colon_no_call(self):
        code = "(pr: foo)"
        self.assertParsesTo(code, [["pr", "foo"]])

    def test_one_line_parens(self):
        code = "(pr (foo))"
        self.assertParsesTo(code, [["pr", ["foo"]]])

    def test_one_line_colon(self):
        code = "(pr: foo bar)"
        self.assertParsesTo(code, [["pr", ["foo", "bar"]]])

    def test_one_line_colon_redundant_parens(self):
        code = "(pr: (foo bar))"
        self.assertParsesTo(code, [["pr", ["foo", "bar"]]])

    def test_multiline_colon(self):
        code = """
        pr:
            foo # Variable
            (foo) # Function call
            foo bar # Implied function call
            (foo bar) # Function call
        """
        expected = [
            ["pr",
             "foo",
             ["foo"],
             ["foo", "bar"],
             ["foo", "bar"]]]

        self.assertParsesTo(code, expected)

    def xtest_plus(self):
        code = """
        set my-plus: λ(x y):
            # commentary goes here
            + x y

        my-plus 2 (+ 3 5)

        """
        self.assertParsesTo(code, [])
