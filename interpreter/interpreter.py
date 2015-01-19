from environment import Env
from code_objects import *


Log = []


class Instruction():
    ARGUMENT, CODE, CALL, APPLY = range(4)

    def __init__(self, typ, code=None, args=None, symbol=""):
        self.type = typ
        self.code = code
        self.symbol = symbol
        self.args = args


class Frame():
    def __init__(self, instructions, env):
        self.instructions = instructions
        self.env = env
        self.new_env = None

    def next(self):
        if self.instructions == []:
            return None
        return self.instructions.pop()

    def push(self, instruction):
        self.instructions.append(instruction)


FAIL = Symbol("Fail")


def eval(stack, current):
    # stack is a list of Frames.
    frame = stack[-1]
    instruction = frame.next()

    if instruction is None:
        stack.pop()
        return current

    elif instruction.type is Instruction.ARGUMENT:
        print "Argument", instruction.symbol
        frame.new_env.set(instruction.symbol, current)
        return current

    elif instruction.type is Instruction.CALL:
        print "Call", instruction.code
        eval_args(stack, current, instruction.code)
        return current

    elif instruction.type is Instruction.APPLY:
        print "Apply", instruction.code
        ret = eval_apply(stack, instruction.code)
        return ret or current

    elif instruction.type is Instruction.CODE:
        code = instruction.code
        print "CODE", code

        # Function call
        if isinstance(code, List):
            return eval_fn(stack, code)

        # Self-valued Atom
        elif (isinstance(code, Builtin) or
              isinstance(code, Number)):
            return code

        # Symbol
        elif isinstance(code, Symbol):
            Log.append(frame)
            return frame.env.lookup(code.symbol)

    return FAIL


def eval_fn(stack, code):
    frame = stack[-1]
    frame.push(Instruction(Instruction.CALL, code))
    frame.push(Instruction(Instruction.CODE, code.call))


def eval_args(stack, function, code):
    # Evaluate arguments
    args = code.args

    frame = Frame([], stack[-1].env)
    stack.append(frame)
    frame.new_env = Env(function.bindings, frame.env)

    frame.push(Instruction(Instruction.APPLY, function))

    for index, arg in enumerate(function.lambda_list):
        if isinstance(arg, List):
            if arg.items[0].symbol == "quote":
                frame.new_env.set(arg.items[1].symbol, args[index])
            else:
                print "OH NO BAD LIST ARG", arg
        else:
            frame.push(Instruction(Instruction.ARGUMENT, symbol=arg.symbol))
            frame.push(Instruction(Instruction.CODE, args[index]))


def eval_apply(stack, function):
    # If it's a built-in, apply it
    frame = stack[-1]
    frame.env = frame.new_env

    if isinstance(function, Builtin):
        ret = function.function(frame.env)
        print "RETURNED", ret
        return ret

    # if it's user-defined, execute the body
    elif isinstance(function, Lambda):
        frame.push(Instruction(Instruction.CODE, function.body))
        stack.append(frame)
        return None
