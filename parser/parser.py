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
        return code_objects.List(parts), rest

    def nodent(self, text, rest):
        parts, rest = self.parse_until(["nodent", "dedent"], rest)
        if len(parts) > 1:
            parts = code_objects.List(parts)
        return parts, rest

    def colon(self, text, rest):
        if rest[0][0] == "indent":
            rest = rest[1:]
            parts, rest = self.parse_until(["dedent"], rest)
            return parts, rest
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
        parts = []
        while (rest[0][0] and rest[0][0] not in ends):
            value, rest = self.parse_one(rest)
            if value:
                if isinstance(value, list):
                    parts.extend(value)
                else:
                    parts.append(value)
        if parts:
            parts = PrattParser.parse(parts)
        return parts, rest

    def parse_all(self, rest):
        parts = []
        while (rest and rest[0][0]):
            value, rest = self.parse_one(rest)
            if value:
                parts.append(value)
        return parts
