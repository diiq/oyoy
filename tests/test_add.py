from test_case import TestCase
from interpreter.code_objects import *
from interpreter.interpreter import Instruction


class AddTests(TestCase):
    def test_add(self):

        make_lam = Call(Symbol("fn"),
                        {"args": List([Arg("a"), Arg("b")]),
                         "body": List([Call(Symbol("+"),
                                            {"x": Symbol("a"),
                                             "y": Symbol("b")})])})

        setter = Call(Symbol("set"),
                      {"symbol": Symbol("my-plus"),
                       "value": make_lam})

        testcode = Call(Symbol("my-plus"),
                        {"a": Number(2),
                         "b": Call(Symbol("+"),
                                   {"x": Number(3),
                                    "y": Number(5)})})

        ins = [Instruction(Instruction.CODE, testcode),
               Instruction(Instruction.CODE, setter)]

        result = self.run_program(ins)
        print result
        self.assertIsInstance(result, Number)
        self.assertEqual(result.number, 10)
