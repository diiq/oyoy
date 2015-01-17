# TODO parse
# nodent symbol *dent -> symbol
# nodent stuff+ *dent -> (stuff+)
# nodent stuff+  stuff+ dedent -> (stuff+ stuff+)
from interpreter import code_objects


class OysterParser(object):
    @classmethod
    def parse(Cls, tokens):
        return Cls().parse_all(tokens)

    def symbol(self, text, rest):
        return code_objects.Symbol(text), rest

    def number(self, text, rest):
        return code_objects.Number(int(text)), rest

    def open(self, text, rest):
        list, rest = self.parse_until(["close"], rest)
        return code_objects.List(list), rest

    def nodent(self, text, rest):
        list, rest = self.parse_until(["nodent", "dedent"], rest)
        if len(list) == 0:
            return None, rest
        if len(list) == 1:
            return list[0], rest
        else:
            return code_objects.List(list), rest

    def colon(self, text, rest):
        if rest[0][0] == "indent":
            rest = rest[1:]
            list, rest = self.parse_until(["dedent"], rest)
            return code_objects.List(list), rest
        else:
            return self.nodent(text, rest)

    def dedent(self, text, rest):
        return self.nodent(text, rest)

    def close(self, test, rest):
        return None, rest

    def parse_one(self, rest):
        token = rest[0]
        value, rest = getattr(self, token[0])(token[1], rest[1:])
        return value, rest

    def parse_until(self, ends, rest):
        list = []
        while (rest[0][0] and rest[0][0] not in ends):
            value, rest = self.parse_one(rest)
            if value:
                list.append(value)
        return list, rest

    def parse_all(self, rest):
        list = []
        while (rest and rest[0][0]):
            value, rest = self.parse_one(rest)
            if value:
                list.append(value)
        return list
