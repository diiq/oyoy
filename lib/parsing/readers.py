class Reader(object):
    def read(self, stream):
        i = stream.index

        try:
            if self.recognize(stream):
                return True

            stream.set_index(i)
            return False

        except EOFError:
            stream.set_index(i)
            return False

class SingleCharacterReader(Reader):
    def __init__(self, characters):
        self.characters = characters

    def recognize(self, stream):
        c = stream.get()
        if c in self.characters:
            return True
        return False


class SingleNotCharacterReader(Reader):
    def __init__(self, characters):
        self.characters = characters

    def recognize(self, stream):
        c = stream.get()
        if c not in self.characters:
            return True
        return False


class SimpleStringReader(Reader):
    def __init__(self, string):
        self.string = string

    def recognize(self, stream):
        chars = stream.get_n(len(self.string))
        if chars == self.string:
            return True
        return False


class RepeatReader(Reader):
    def __init__(self, reader, minimum=0):
        self.reader = reader
        self.minimum = minimum

    def recognize(self, stream):
        count = 0
        while self.reader.read(stream):
            count += 1

        if count >= self.minimum:
            return True
        return False


class SequenceReader(Reader):
    def __init__(self, readers):
        self.readers = readers

    def recognize(self, stream):
        for reader in self.readers:
            if not reader.read(stream):
                return False

        return True


class PickAStringReader(Reader):
    def __init__(self, strings):
        self.operators = map(SimpleStringReader, strings)

    def read(self, stream):
        for operator in self.operators:
            if operator.read(stream):
                return True
        return False
