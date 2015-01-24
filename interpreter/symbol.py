from oyster_object import OysterObject


class Symbol(OysterObject):
    code = False

    def __init__(self, value):
        self.symbol = value

    def __str__(self):
        return "<sym: %s>" % self.symbol

    def dup(self):
        return Symbol(self.symbol)


def make_symbol(str):
    return Symbol(str)
