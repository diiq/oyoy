from interpreter.code_objects import *


class OysterParser(object):
    def __init__(self):
        self.prefixes = {
            "symbol": LiteralPrefixOperator(Symbol), # -1
            "number": LiteralPrefixOperator(Number), # -1
            "open": ParenOperator(0),
            "line": NewlineOperator(0),
            "-": PrefixOperator("negative", 10),
        }

        self.infixes = {
            "*": InfixOperator("mult", 7),
            "/": InfixOperator("divide", 7),

            "+": InfixOperator("plus", 6),
            "-": InfixOperator("minus", 6),

            "==": InfixOperator("equal", 4),
            "!=": InfixOperator("not-equal", 4),

            "colon": ColonOperator(8),
            "colondent": ColondentOperator(9),

            "null": NullInfix(10)
        }

    @classmethod
    def parse(Cls, tokens):
        ret, tokens = Cls().expression(-1, tokens)
        if not isinstance(ret, list):
            ret = [ret]
        return ret

    def expression(self, prev_precedence, right):
        print "EXPRESSION", prev_precedence, right

        left, right = self.build_left(*self.next(right))

        while (right and
               not self.is_closing(right[0])
               and self.precedence(self.peek_or_null(right)) > prev_precedence):

            left, right = self.fill_right(
                left, *self.next_or_null(right))

        return left, right

    def next(self, right):
        current = right[0]
        right = right[1:]
        return current, right

    def next_or_null(self, right):
        if right[0][0] not in self.infixes:
            return ("null", ''), right
        else:
            return self.next(right)

    def peek_or_null(self, right):
        if right[0][0] not in self.infixes:
            return ("null", '')
        else:
            return right[0]

    def is_closing(self, token):
        return token[0] in ["close", "endline", "dedent"]

    def precedence(self, token):
        if token[0] in self.infixes:
            return self.infixes[token[0]].precedence
        else:
            return -1

    def build_left(self, item, right):
        assert item[0] in self.prefixes, \
            "%s is not a prefix operator" % item[0]

        return self.prefixes[item[0]].parse(item, right, self)

    def fill_right(self, left, item, right):
        assert item[0] in self.infixes, \
            "%s is not an infix operator" % item[0]

        return self.infixes[item[0]].parse(left, item, right, self)


###################
# Prefix Operators
#

class PrefixOperator(object):
    def __init__(self, symbol, precedence):
        self.symbol = symbol
        self.precedence = precedence

    def representation(self):
        return Symbol(self.symbol)

    def parse(self, item, right, parser):
        within, right = parser.expression(self.precedence, right)
        return List([self.representation(), within]), right


class NewlineOperator(object):
    def __init__(self, precedence):
        self.precedence = precedence

    def parse(self, item, right, parser):
        within, right = parser.expression(self.precedence, right)
        print "This line contains", within, right
        right = right[1:]
        if isinstance(within, list):
            within = List(within)
        return within, right


class ParenOperator(object):
    def __init__(self, precedence):
        self.precedence = precedence

    def parse(self, item, right, parser):
        within, right = parser.expression(self.precedence, right)
        print "These parens contain", within, right
        right = right[1:]
        if not isinstance(within, list):
            within = [within]
        return List(within), right


class LiteralPrefixOperator(object):
    precedence = -1
    def __init__(self, constructor):
        self.constructor = constructor

    def parse(self, item, right, parser):
        return self.constructor(item[1]), right

###################
# Infix Operators
#

class InfixOperator(object):
    def __init__(self, symbol, precedence):
        self.symbol = symbol
        self.precedence = precedence

    def representation(self):
        return Symbol(self.symbol)

    def parse(self, left, item, right, parser):
        right, far_right = parser.expression(self.precedence, right)

        if isinstance(left, list):
            left = List(left)

        if isinstance(right, list):
            right = List(right)

        return [self.representation(), left, right], far_right


class NullInfix(object):
    def __init__(self, precedence):
        self.precedence = precedence

    def parse(self, left, item, right, parser):
        right, far_right = parser.expression(self.precedence, right)

        if not isinstance(left, list):
            left = [left]

        if not isinstance(right, list):
            right = [right]

        return left + right, far_right


class ColonOperator(object):
    def __init__(self, precedence):
        self.precedence = precedence

    def parse(self, left, item, right, parser):
        right, far_right = parser.expression(self.precedence, right)

        if not isinstance(left, list):
            left = [left]

        if isinstance(right, list):
            right = List(right)

        return left + [right], far_right


class ColondentOperator(object):
    def __init__(self, precedence):
        self.precedence = precedence

    def parse(self, left, item, right, parser):
        right = right[1:]
        right, far_right = parser.expression(self.precedence, right)

        if not isinstance(left, list):
            left = [left]

        if not isinstance(right, list):
            right = [right]

        far_right = far_right[1:]

        return left + right, far_right
