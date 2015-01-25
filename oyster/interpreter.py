from environment import Env
from instruction import Instruction
from list import List
from symbol import Symbol
from number import Number
from builtin import Builtin
from oyster_lambda import Lambda
from stack_frame import StackFrame


FAIL = Symbol("Fail")


def eval(stack, current):
    # stack is a list of Frames.
    frame = stack[-1]
    instruction = frame.next()

    if instruction is None:
        stack.pop()
        return current

    elif instruction.type is Instruction.ARGUMENT:
        frame.new_env.set(instruction.symbol, current)
        return current

    elif instruction.type is Instruction.CALL:
        eval_args(stack, current, instruction.code)
        return current

    elif instruction.type is Instruction.APPLY:
        ret = eval_apply(stack, instruction.code)
        return ret or current

    elif instruction.type is Instruction.CODE:
        code = instruction.code

        if code.env:
            stack.append(StackFrame(
                [Instruction(Instruction.CODE, code=code.dup())],
                code.env))
            return current

        # Function call
        if isinstance(code, List):
            return eval_fn(stack, code)

        # Self-valued Atom
        elif (isinstance(code, Builtin) or
              isinstance(code, Number)):
            return code

        # Symbol
        elif isinstance(code, Symbol):
            return frame.env.lookup(code.symbol)

    return FAIL


def eval_fn(stack, code):
    frame = stack[-1]
    frame.push(Instruction(Instruction.CALL, code))
    frame.push(Instruction(Instruction.CODE, code.call))


def eval_args(stack, function, code):
    # Evaluate arguments
    args = code.args

    frame = StackFrame([], stack[-1].env)
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
        return ret

    # if it's user-defined, execute the body
    elif isinstance(function, Lambda):
        frame.push(Instruction(Instruction.CODE, function.body))
        stack.append(frame)
        return None
