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
            self.assertEqual(actual.number, expected)

        else:
            assert False, "Unknown type: %s" % actual.__class__.__name__

    def assertParsesTo(self, code, expected):
        file = StringIO(dedent(code))
        tokens = OysterScanner(file, "test").read_all()
        statements = OysterParser.parse(tokens)
        print "DEEP MATCHING", statements, expected
        for statement in zip(statements, expected):
            self.assertDeepMatch(*statement)


    def xtest_one_line_colon_no_call(self):
        code = """
        (pr: foo)
        """
        self.assertParsesTo(code, [["pr", "foo"]])

    def test_one_line_parens(self):
        code = """
        (pr (foo))
        """
        self.assertParsesTo(code, [["pr", ["foo"]]])

    def xtest_one_line_colon(self):
        code = """
        pr bing: foo bar
        """
        self.assertParsesTo(code, [["pr", "bing", ["foo", "bar"]]])

    def xtest_multiline_colon(self):
        code = """
        pr bing:
            foo bar
        """
        self.assertParsesTo(code, [["pr", "bing", ["foo", "bar"]]])

    def xtest_one_line_colon_redundant_parens(self):
        code = """
        (pr: (foo bar))
        """
        self.assertParsesTo(code, [["pr", ["foo", "bar"]]])

    def xtest_multiline_colon_smorgasbord(self):
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
        self.assertParsesTo(code, [
            ["set", "my-plus", ["λ", ["x", "y"],
                 ["+", "x", "y"]]],
            ["my-plus", 2, ["+", 3, 5]]])

    def test_nested_parens_plus(self):
        code = """
        (set my-plus (λ (a b) (a + b)))
        (my-plus 2 (3 + 5))
        """
        self.assertParsesTo(code, [
            ["set", "my-plus", ["λ", ["a", "b"],
                 ["plus", "a", "b"]]],
            ["my-plus", 2, ["plus", 3, 5]]])

    def test_prefix(self):
        code="""
        -my-symbol
        """
        self.assertParsesTo(code, [
            ["negative", "my-symbol"]])

    def test_infix(self):
        code="""
        my-symbol + five
        """
        self.assertParsesTo(code, [
            ["plus", "my-symbol", "five"]])

    def test_deep_infix(self):
        code="""
        dig inbroom my-symbol + two five seven
        """
        self.assertParsesTo(code, [
            ["plus",
             ["dig", "inbroom", "my-symbol"],
             ["two", "five", "seven"]]])

    def test_calls(self):
        code="""
        tremble barf fob
        """
        self.assertParsesTo(code, [
            ["tremble", "barf", "fob"]])

    def test_prefix_call(self):
        code="""
        -tremble barf
        """
        self.assertParsesTo(code, [
            [["negative", "tremble"], "barf"]])

    def test_parens(self):
        code="""
        (tremble barf)
        """
        self.assertParsesTo(code, [
            ["tremble", "barf"]])

    def test_nested_parens(self):
        code="""
        (tremble (organic barf))
        """
        self.assertParsesTo(code, [
            ["tremble", ["organic", "barf"]]])
