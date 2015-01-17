from environment import Env


class OyO(object):
    pass


class Number(OyO):
    def __init__(self, value):
        self.number = value


class Symbol(OyO):
    def __init__(self, value):
        self.symbol = value


class Arg(OyO):
    def __init__(self, name, code=False):
        self.name = name
        self.code = code


class Call(OyO):
    def __init__(self, call, kwargs):
        self.call = call
        self.args = kwargs


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
