from unittest import TestCase as TC
from textwrap import dedent

from oyster.interpreter import eval
from oyster.stack_frame import StackFrame
from oyster.instruction import Instruction
from oyster.environment import Env
from oyster.list import List, PartialList
from oyster.symbol import Symbol
from oyster.number import Number
from oyster.globals import populate_globals
from oyster.oyster_parser import OysterParser
from oyster.oyster_scanner import OysterScanner


class TestCase(TC):
    def setUp(self):
        self.env = populate_globals(Env(None, None))

    def run_program(self, filename):
        with open(filename) as file:
            tokens = OysterScanner(file.read()).tokenize()
        statements = OysterParser().parse(tokens).items
        instructions = [Instruction(Instruction.CODE, statement)
                        for statement in statements]
        instructions.reverse()
        stack = [StackFrame(instructions, self.env)]
        cur = None
        while stack:
            cur = eval(stack, cur)
        return cur

    def run_snippet(self, code):
        tokens = OysterScanner(dedent(code)).read_all()
        instructions = OysterParser.parse(tokens).items
        stack = [StackFrame(instructions, self.env)]
        cur = None
        while stack:
            cur = eval(stack, cur)
        return cur

    def run_parsed_code(self, code):
        stack = [StackFrame(code, self.env)]
        cur = None
        while stack:
            cur = eval(stack, cur)
        return cur


class ParserTestCase(TC):

    def assertDeepMatch(self, actual, expected):
        assert not isinstance(actual, PartialList)
        if isinstance(actual, List):
            self.assertEqual(len(actual.items), len(expected))
            for item in zip(actual.items, expected):
                self.assertDeepMatch(*item)

        elif isinstance(actual, Symbol):
            self.assertEqual(actual.symbol, expected)

        elif isinstance(actual, Number):
            self.assertEqual(actual.number, expected)

        else:
            assert False, "Unknown type: %s" % actual.__class__.__name__

    def assertParsesTo(self, code, expected):
        tokens = OysterScanner(dedent(code)).tokenize()
        statements = OysterParser().parse(tokens)
        self.assertDeepMatch(statements, expected)
