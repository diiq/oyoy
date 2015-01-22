from interpreter.code_objects import *
from oyster_scanner import Token


class TokenStream(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def peek(self):
        return self.tokens[self.index]

    def next(self):
        ret = self.tokens[self.index]
        self.index += 1
        return ret

    def eof(self):
        return self.index >= len(self.tokens)


class OysterParser(object):
    def __init__(self):
        self.prefixes = {
            "symbol": LiteralPrefixOperator(make_symbol, -1),
            "number": LiteralPrefixOperator(make_number, -1),
            "open":   ParenOperator(-1),
            "line":   NewlineOperator(0),
            "-":      PrefixOperator("negative", 10),
            "!":      PrefixOperator("not", 10),
            "...":    PrefixOperator("ellipsis", 10),
            "'":      PrefixOperator("quote", 10),
            "colon":  ColonOperator(1),
        }

        self.infixes = {
            "null": NullInfix(10),

            "colondent": ColondentOperator(2),

            "*":  InfixOperator("multiply", 7),
            "/":  InfixOperator("divide", 7),

            "+":  InfixOperator("add", 6),
            "-":  InfixOperator("subtract", 6),

            "==": InfixOperator("equal?", 4),
            "!=": InfixOperator("not-equal?", 4),
            ">=": InfixOperator("greater-than-or-equal?", 4),
            "<=": InfixOperator("less-than-or-equal?", 4),
            ">":  InfixOperator("greater-than?", 4),
            "<":  InfixOperator("less-than?", 4),

            "&&": InfixOperator("and", 3),
            "||": InfixOperator("or", 2),

        }

        self.closers = ["close", "endline", "dedent"]

    def parse(self, tokens):
        self.right = TokenStream(tokens)
        ret = self.expression(-1)
        # ENSURE LIST
        return enforce_list(ret)

    def expression(self, prev_precedence):
        left = self.build_left(self.right.next())

        while (not self.right.eof() and
               not self.next_is_closing()
               and self.precedence(self.peek_or_null()) > prev_precedence):
            token = self.next_or_null()
            left = self.fill_right(left, token)

        return left

    def peek_or_null(self):
        if self.right.peek().purpose in self.infixes:
            return self.right.peek()
        else:
            return Token("null", '')

    def next_or_null(self):
        if self.right.peek().purpose in self.infixes:
            return self.right.next()
        else:
            return Token("null", '')

    def next_is_closing(self):
        return self.right.peek().purpose in self.closers

    def precedence(self, token):
        if token.purpose in self.infixes:
            return self.infixes[token.purpose].precedence
        else:
            return -1

    def build_left(self, token):
        assert token.purpose in self.prefixes, \
            "%s is not a prefix operator" % token.purpose

        operator = self.prefixes[token.purpose]
        return operator.parse(token, self.right, self)

    def fill_right(self, left, token):
        assert token.purpose in self.infixes, \
            "%s is not an infix operator" % token.purpose

        operator = self.infixes[token.purpose]
        return operator.parse(left, token, self.right, self)


###################
# Prefix Operators
#

class PrefixOperator(object):
    def __init__(self, symbol, precedence):
        self.symbol = symbol
        self.precedence = precedence

    def representation(self):
        return Symbol(self.symbol)

    def parse(self, token, right, parser):
        within = parser.expression(self.precedence)
        within = close_partial_lists(within)
        return List([self.representation(), within])


class NewlineOperator(PrefixOperator):
    def __init__(self, precedence):
        self.precedence = precedence

    def parse(self, token, right, parser):
        within = parser.expression(self.precedence)
        if right.peek().purpose == "endline":
            right.next()

        return close_partial_lists(within)


class ParenOperator(PrefixOperator):
    def __init__(self, precedence):
        self.precedence = precedence

    def parse(self, token, right, parser):
        within = parser.expression(self.precedence)
        right.next()
        # Todo assertion

        within = enforce_list(within)

        return within


class LiteralPrefixOperator(PrefixOperator):
    def __init__(self, constructor, precedence):
        self.precedence = precedence
        self.constructor = constructor

    def parse(self, token, right, parser):
        return self.constructor(token.text)


class ColonOperator(PrefixOperator):
    def __init__(self, precedence):
        self.precedence = precedence

    def parse(self, token, right, parser):
        within = parser.expression(self.precedence)
        within = close_partial_lists(within)

        return PartialList([within])


###################
# Infix Operators
#

class InfixOperator(object):
    def __init__(self, symbol, precedence):
        self.symbol = symbol
        self.precedence = precedence

    def representation(self):
        return Symbol(self.symbol)

    def parse(self, left, token, right, parser):
        right_side = parser.expression(self.precedence)

        return PartialList([self.representation(),
                            close_partial_lists(left),
                            close_partial_lists(right_side)])


class NullInfix(InfixOperator):
    def __init__(self, precedence):
        self.precedence = precedence

    def parse(self, left, token, right, parser):
        right_side = parser.expression(self.precedence)

        left = ensure_partial_list(left)
        right_side = ensure_partial_list(right_side)

        return PartialList(left.items + right_side.items)


class ColondentOperator(InfixOperator):
    def __init__(self, precedence):
        self.precedence = precedence

    def parse(self, left, token, right, parser):
        right.next() # Todo assert
        right_side = parser.expression(self.precedence)
        right.next() # Todo assert

        # ensure both are lists
        left = ensure_partial_list(left)
        right_side = ensure_partial_list(right_side)

        return PartialList(left.items + right_side.items)
