from unittest import TestCase as TC
from cStringIO import StringIO
from textwrap import dedent
from pprint import pformat

from interpreter.interpreter import eval, Frame, Instruction
from interpreter.environment import Env
from interpreter.code_objects import *
from interpreter.globals import populate_globals
from oyster.oyster_parser import OysterParser
from oyster.oyster_scanner import OysterScanner

class TestCase(TC):
    def setUp(self):
        self.env = populate_globals(Env(None, None))

    def run_program(self, filename):
        with open(filename) as file:
            tokens = OysterScanner(file, filename).read_all()
        instructions = [Instruction(Instruction.CODE, statement)
                        for statement in OysterParser.parse(tokens)]

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


class ParserTestCase(TC):

    def assertDeepMatch(self, actual, expected):
        print actual, expected
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
        print statements
        self.assertDeepMatch(statements, expected)
        print statements
