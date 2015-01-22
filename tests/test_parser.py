# -*- coding: utf-8 -*-
from test_case import ParserTestCase


class OneLineParserTests(ParserTestCase):

    def test_one_line_parens(self):
        code = """
        (pr (foo))
        """
        self.assertParsesTo(code, [["pr", ["foo"]]])

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
            ["add", "my-symbol", "five"]])

    def test_infix_precedence(self):
        code="""
        my-symbol + five * 4 + 2
        """
        self.assertParsesTo(code, [
            ["add", ["add", "my-symbol",
                      ["multiply", "five", 4]], 2]])

    def test_deep_infix(self):
        code="""
        dig inbroom my-symbol + two five seven
        """
        self.assertParsesTo(code, [
            ["add",
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


class OneLineColonParserTests(ParserTestCase):

    def test_no_call(self):
        code = """
        (pr: foo)
        """
        self.assertParsesTo(code, [["pr", "foo"]])

    def test_colon(self):
        code = """
        pr bing: foo bar
        """
        self.assertParsesTo(code, [["pr", "bing", ["foo", "bar"]]])

    def test_redundant_parens(self):
        code = """
        (pr: (foo bar))
        """
        self.assertParsesTo(code, [["pr", ["foo", "bar"]]])

    def test_double_colon(self):
        code = """
        pr: foo bar: baz bing
        """
        self.assertParsesTo(code, [["pr", ["foo", "bar", ["baz", "bing"]]]])

    def test_double_colon_parens(self):
        code = """
        (pr: foo bar: baz bing)
        """
        self.assertParsesTo(code, [["pr", ["foo", "bar", ["baz", "bing"]]]])


class MultiLineParserTests(ParserTestCase):

    def test_multiline_colon(self):
        code = """
        pr bing:
            foo bar
        """
        self.assertParsesTo(code, [["pr", "bing", ["foo", "bar"]]])


    def test_multiline_colon_smorgasbord(self):
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

    def test_multiline_colon_parens(self):
        code = """
        sing (hello there:
                 neighbor boy) I am 5

        """
        self.assertParsesTo(code, [["sing", ["hello", "there",
                                            ["neighbor", "boy"]],
                                    "I", "am", 5]])

    def test_plus(self):
        code = """
        set my-plus: λ(x y):
            # commentary goes here
            x + y

        my-plus 2 (3 + 5)

        """
        self.assertParsesTo(code, [
            ["set", "my-plus", ["λ", ["x", "y"],
                 ["add", "x", "y"]]],
            ["my-plus", 2, ["add", 3, 5]]])

    def test_nested_parens_plus(self):
        code = """
        (set my-plus (λ (a b) (a + b)))
        (my-plus 2 (3 + 5))
        """
        self.assertParsesTo(code, [
            ["set", "my-plus", ["λ", ["a", "b"],
                 ["add", "a", "b"]]],
            ["my-plus", 2, ["add", 3, 5]]])

    def test_operator_before_colon(self):
        code = """
        if (x == y):
            x + y
        """
        self.assertParsesTo(code, [
            ["if", ["equal?", "x", "y"],
                 ["add", "x", "y"]]])
