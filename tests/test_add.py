from test_case import TestCase
from interpreter.code_objects import *
from interpreter.interpreter import Instruction


class AddTests(TestCase):
    def test_add(self):

        make_lam = Call(Symbol("fn"),
                        [List(Symbol("a"), Symbol("b")),
                         List(Call(Symbol("+"),
                                   [Symbol("a"), Symbol("b")]))])

        setter = Call(Symbol("set"),
                      [Symbol("my-plus"), make_lam])

        testcode = Call(Symbol("my-plus"),
                        [Number(2),
                         Call(Symbol("+"), [Number(3), Number(5)])])

        ins = [Instruction(Instruction.CODE, testcode),
               Instruction(Instruction.CODE, setter)]

        result = self.run_program(ins)

        self.assertIsInstance(result, Number)
        self.assertEqual(result.number, 10)
