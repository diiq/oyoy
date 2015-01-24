from test_case import TestCase
from interpreter.list import List
from interpreter.symbol import Symbol
from interpreter.number import Number
from interpreter.interpreter import Instruction


class AddTests(TestCase):
    def test_add(self):

        make_lam = List([Symbol("fn"),
                         List([Symbol("a"), Symbol("b")]),
                         List([Symbol("add"),
                               Symbol("a"), Symbol("b")])])

        setter = List([Symbol("set"), Symbol("my-plus"), make_lam])

        testcode = List([Symbol("my-plus"),
                         Number(2),
                         List([Symbol("add"), Number(3), Number(5)])])

        ins = [Instruction(Instruction.CODE, testcode),
               Instruction(Instruction.CODE, setter)]

        result = self.run_parsed_code(ins)
        self.assertIsInstance(result, Number)
        self.assertEqual(result.number, 10)

    def test_add_from_file(self):
        result = self.run_program("oyster_code/test_add.oy")

        self.assertIsInstance(result, Number)
        self.assertEqual(result.number, 10)
