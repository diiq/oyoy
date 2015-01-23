from stream import Stream

DITTO = "DITTO"


class Token(object):
    def __init__(self, purpose, text, line, character):
        self.purpose = purpose
        self.text = text
        self.line = line
        self.character = character

    def __repr__(self):
        if self.text != "":
            return "<%s:%s>" % (self.purpose, self.text)
        return "<%s>" % (self.purpose)


class Tokenizer(object):
    def __init__(self, reader, purpose):
        self.reader = reader
        self.purpose = purpose

    def applies(self, stream):
        return self.reader.read(stream)

    def token(self, stream, i, j):
        text = stream.string[i:j]
        if self.purpose == DITTO:
            return Token(text, text,
                         stream.line(),
                         stream.position())
        else:
            return Token(self.purpose, text,
                         stream.line(),
                         stream.position())


class Scanner(object):
    def initialize_scan(self, string):
        self.tokens = []
        self.stream = Stream(string)

    def produce(self, token):
        self.tokens.append(token)

    def tokenize(self):
        while self.tokenize_one():
            pass
        return self.tokens

    def tokenize_one(self):
        i = self.stream.index

        if self.stream.eof():
            self.eof()
            return False

        for tokenizer_pair in self.state:
            tokenizer = tokenizer_pair[0]
            action = tokenizer_pair[1]
            if tokenizer.applies(self.stream):
                j = self.stream.index
                action(self, tokenizer.token(self.stream, i, j))
                return True

        raise StandardError("No tokenizer applied.")
