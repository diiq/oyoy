from oyster_object import OysterObject
from environment import Env


class Builtin(OysterObject):
    def __init__(self, function, args):
        self.function = function
        self.lambda_list = args
        self.bindings = Env(None, None)
