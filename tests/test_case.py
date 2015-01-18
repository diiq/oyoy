from unittest import TestCase as TC
from interpreter.interpreter import eval, Frame, Instruction
from interpreter.environment import Env
from interpreter.globals import populate_globals
from parser.parser import OysterParser
from parser.scanner import OysterScanner

class TestCase(TC):
    def setUp(self):
        self.env = populate_globals(Env(None, None))

    def run_program(self, filename):
        with open(filename) as file:
            tokens = OysterScanner(file, filename).read_all()
        instructions = [Instruction(Instruction.CODE, statement) for statement in OysterParser.parse(tokens)]
        print "--- INSTRUCTIONS ---"
        for instruction in instructions:
            print instruction.code
        instructions.reverse()
        print "--- END INSTRUCTIONS ---"
        stack = [Frame(instructions, self.env)]
        cur = None
        while stack:
            cur = eval(stack, cur)
        return cur

    def run_snippet(self, code):
        file = StringIO(dedent(code))
        tokens = OysterScanner(file, "snippet").read_all()
        instructions = OysterParser.parse(tokens)
        stack = [Frame(instructions, self.env)]
        cur = None
        while stack:
            cur = eval(stack, cur)
        return cur

    def run_parsed_code(self, code):
        stack = [Frame(code, self.env)]
        cur = None
        while stack:
            cur = eval(stack, cur)
        return cur
