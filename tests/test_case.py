from unittest import TestCase as TC
from interpreter.interpreter import eval, Frame
from interpreter.environment import Env
from interpreter.globals import populate_globals


class TestCase(TC):
    def setUp(self):
        self.env = populate_globals(Env(None, None))

    def run_program(self, instructions):
        cur = None
        stack = [Frame(instructions, self.env)]
        while stack:
            cur = eval(stack, cur)
        return cur
