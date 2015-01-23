from environment import Env


class OyO(object):
    def __init__():
        pass


class Number(OyO):
    def __init__(self, value):
        self.number = value

    def __str__(self):
        return "<num: %s>" % self.number


class Symbol(OyO):
    code = False

    def __init__(self, value):
        self.symbol = value

    def __str__(self):
        return "<sym: %s>" % self.symbol


class Arg(OyO):
    def __init__(self, symbol, code=False):
        self.symbol = symbol
        self.code = code


class Lambda(OyO):
    def __init__(self, args, body, env):
        self.lambda_list = args
        self.body = body
        self.bindings = env


class Builtin(OyO):
    def __init__(self, function, args):
        self.function = function
        self.lambda_list = args
        self.bindings = Env(None, None)


class List(OyO):
    def __init__(self, items):
        self.items = items
        self.call = items[0]
        self.args = items[1:]

    def __str__(self):
        return "(%s)" % ", ".join([item.__str__() for item in self.items])


##################################################################
# The following classes and constructors used during parsing only:


class PartialList(List):
    pass


def make_number(str):
    return Number(int(str, 10))


def make_symbol(str):
    return Symbol(str)


def close_partial_lists(obj):
    if isinstance(obj, PartialList):
        return List(obj.items)
    return obj


def ensure_partial_list(obj):
    if not isinstance(obj, PartialList):
        return PartialList([obj])
    return obj


def enforce_list(obj):
    if isinstance(obj, PartialList):
        return List(obj.items)
    else:
        return List([obj])
