from test_case import TestCase
from interpreter.code_objects import *
from interpreter.interpreter import Instruction


class AddTests(TestCase):
    def xtest_add(self):

        make_lam = List([Symbol("fn"),
                         List([Symbol("a"), Symbol("b")]),
                         List([Symbol("+"),
                               Symbol("a"), Symbol("b")])])

        setter = List([Symbol("set"), Symbol("my-plus"), make_lam])

        testcode = List([Symbol("my-plus"),
                         Number(2),
                         List([Symbol("+"), Number(3), Number(5)])])

        ins = [Instruction(Instruction.CODE, testcode),
               Instruction(Instruction.CODE, setter)]

        result = self.run_parsed_code(ins)
        self.assertIsInstance(result, Number)
        self.assertEqual(result.number, 10)

    def xtest_add_from_file(self):
        result = self.run_program("oyster_code/test_add.oy")

        self.assertIsInstance(result, Number)
        self.assertEqual(result.number, 10)
