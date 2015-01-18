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
        parts, rest = self.parse_until(["close"], rest)
        return code_objects.List(parts), rest[1:]

    def nodent(self, text, rest):
        parts, rest = self.parse_until(["nodent", "dedent"], rest)
        if len(parts) == 0:
            parts = None
        elif len(parts) == 1:
            parts = parts[0]
        else:
            parts = code_objects.List(parts)

        return parts, rest

    def colon(self, text, rest):
        if rest[0][0] == "indent":
            parts, rest = self.parse_until(["dedent"], rest)
            return parts, rest
        else:
            return self.nodent(text, rest)

    def dedent(self, text, rest):
        return self.nodent(text, rest)

    def indent(self, text, rest):
        return self.nodent(text, rest)

    def close(self, test, rest):
        return None, rest

    def parse_one(self, rest):
        token = rest[0]
        value, rest = getattr(self, token[0])(token[1], rest[1:])
        return value, rest

    def parse_until(self, ends, rest):
        parts = []
        while (rest[0][0] and rest[0][0] not in ends):
            value, rest = self.parse_one(rest)
            if value:
                if isinstance(value, list):
                    parts.extend(value)
                else:
                    parts.append(value)
        return parts, rest

    def parse_all(self, rest):
        parts = []
        while (rest and rest[0][0]):
            value, rest = self.parse_one(rest)
            if value:
                parts.append(value)
        return parts
