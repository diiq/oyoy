from oyster_object import OysterObject


class Number(OysterObject):
    def __init__(self, value):
        self.number = value

    def __str__(self):
        return "<num: %s>" % self.number

    def dup(self):
        return Number(self.number)


def make_number(str):
    return Number(int(str, 10))
