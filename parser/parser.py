from interpreter.code_objects import *


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


# a b + c d e
# a b + (c d) e

class LiteralPrefixOperator(object):
    precedence = -1
    def __init__(self, constructor):
        self.constructor = constructor

    def parse(self, item, right, parser):
        return self.constructor(item[1]), right


class InfixOperator(object):
    def __init__(self, symbol, precedence):
        self.symbol = symbol
        self.precedence = precedence

    def representation(self):
        return Symbol(self.symbol)

    def parse(self, item, left, right, parser):
        right, far_right = parser.expression(self.precedence, right)

        if isinstance(left, list):
            left = List(left)


        if isinstance(right, list):
            right = List(right)

        return [self.representation(), left, right], far_right


class NullInfix(object):
    precedence = 9

    def parse(self, item, left, right, parser):
        right, far_right = parser.expression(self.precedence, right)
        if isinstance(left, list):
            if isinstance(right, list):
                return left + right, far_right
            return left + [right], far_right
        if isinstance(right, list):
            return [left] + right
        return [left, right], far_right


class OysterParser(object):
    prefixes = {
        "symbol": LiteralPrefixOperator(Symbol), # -1
        "number": LiteralPrefixOperator(Number), # -1
        "open": ParenOperator(0),
        "line": NewlineOperator(0),
        "-": PrefixOperator("negative", 10),
    }

    infixes = {
        "*": InfixOperator("mult", 7),
        "/": InfixOperator("divide", 7),

        "+": InfixOperator("plus", 6),
        "-": InfixOperator("minus", 6),

        "==": InfixOperator("equal", 4),
        "!=": InfixOperator("not-equal", 4),

        "null": NullInfix()
    }

    @classmethod
    def parse(Cls, tokens):
        ret, tokens = Cls().expression(-1, tokens)
        if not isinstance(ret, list):
            ret = [ret]
        return ret

    def expressions_until(self, right, stop):
        expressions = []
        while not right[0][0] == stop:
            print "Will stop at", stop
            expr, right = self.expression(0, right)
            expressions.append(expr)
        return expressions, right

    def expression(self, prev_precedence, right):
        print "EXPRESSION", prev_precedence, right
        current = right[0]
        right = right[1:]
        left, right = self.fill(current, None, right)
        while (right and
               not self.is_closing(right[0])
               and self.precedence(self.peek_token(right)) > prev_precedence):
            current, right = self.next_token(right)
            left, right = self.fill(current, left, right)

        return left, right

    def next_token(self, right):
        if right[0][0] not in self.infixes:
            current = ("null", '')
        else:
            current = right[0]
            right = right[1:]
        return current, right

    def peek_token(self, right):
        if right[0][0] not in self.infixes:
            return ("null", '')
        else:
            return right[0]

    def is_closing(self, token):
        return token[0] in ["close", "endline", "dedent"]

    def precedence(self, token):
        if token[0] in self.prefixes:
            return self.prefixes[token[0]].precedence

        if token[0] in self.infixes:
            return self.infixes[token[0]].precedence

        return -1

    def fill(self, item, left, right):
        print "FILL:", item, left, right
        if not left:
            assert item[0] in self.prefixes, "%s is not a prefix operator" % item[0]

            ret, right = self.prefixes[item[0]].parse(item, right, self)
        else:
            assert item[0] in self.infixes, "%s is not an infix operator" % item[0]

            ret, right = self.infixes[item[0]].parse(item, left, right, self)

        print "I RETURNED", ret, right
        return ret, right
