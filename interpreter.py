"""
An interpreter for a code-as-object version of Oyster, as opposed to code-as-list.
"""

from environment import Env
from code_objects import *

Log = []

class Instruction():
    ARGUMENT, CODE, CALL, APPLY = range(4)
    def __init__(self, typ, code=None, args=None, name=""):
        self.type = typ
        self.code = code
        self.name = name
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
        frame.new_env.set(instruction.name, current)
        return current

    elif instruction.type is Instruction.CALL:
        eval_args(stack, current, instruction.code)
        return current

    elif instruction.type is Instruction.APPLY:
        ret = eval_apply(stack, instruction.code)
        return ret or current
    
    elif instruction.type is Instruction.CODE:
        code = instruction.code
        
        # Function call
        if isinstance(code, Call):
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
    
    for arg in function.lambda_list:
        if arg.code:
            frame.new_env.set(arg.name, args[arg.name])
        else:
            frame.push(Instruction(Instruction.ARGUMENT, name=arg.name))
            frame.push(Instruction(Instruction.CODE, args[arg.name]))

def eval_apply(stack, function):
    # If it's a built-in, apply it
    frame = stack[-1]
    frame.env = frame.new_env
    
    if isinstance(function, Builtin):
        return function.function(frame.env)

    # if it's user-defined, execute the body
    elif isinstance(function, Lambda):
        for i in range(len(function.body)-1, -1, -1):
            frame.push(Instruction(Instruction.CODE, function.body[i]))
        stack.append(frame)
        return None

def populate_globals(env):
    # Builtin *functions* take an environment, rather than individual
    # args.
    def builtin_plus(env):
        x = env.lookup("x").number
        y = env.lookup("y").number
        return Number(x+y)

    # Builtin *objects* have arglists, though.
    iplus = Builtin(builtin_plus, [Arg("x"), Arg("y")])

    env.set("builtin+", iplus)
    
    # And lambda objects have an environtment to close over.
    env.set("+", Lambda([Arg("x"), Arg("y")], 
                        [Call(iplus, {"x":Symbol("x"), "y":Symbol("y")})], 
                        Env(None, None))) # <-- environment


    # Lambda:
    def builtin_lambda(env):
        args = env.lookup("args")
        body = env.lookup("body")
        return Lambda(args.items, body.items, env.dynamic)

    env.set("fn", Builtin(builtin_lambda, [Arg("args", True), Arg("body", True)]))


    
    # Lambda:
    def builtin_set(env):
        sym = env.lookup("symbol")
        val = env.lookup("value")
        env.dynamic.set(sym.symbol, val)
        return val

    env.set("set", Builtin(builtin_set, [Arg("symbol", True), Arg("value")]))

    return env
    

def entry_point(argv):
    # For now, entry_point just runs a test, applying a user-defined
    # function that wraps a built-in addition function.

    # A call takes a dictionary of arguments; all args are keyword
    # args.
    env = populate_globals(Env(None, None))
    
    make_lam = Call(Symbol("fn"),
                    {"args" : List([Arg("a"), Arg("b")]),
                     "body" : List([Call(Symbol("+"), 
                                         {"x":Symbol("a"),
                                          "y":Symbol("b")})])})
    setter = Call(Symbol("set"), 
                  {"symbol" : Symbol("my-plus"),
                   "value" : make_lam})
    testcode = Call(Symbol("my-plus"), 
                    {"a" : Number(2), 
                     "b" : Call(Symbol("+"),
                             {"x" : Number(3), 
                              "y" : Number(5)})})

    ins = [Instruction(Instruction.CODE, testcode),
           Instruction(Instruction.CODE, setter)]
    stack = [Frame(ins, env)]
    cur = None
    #    try:
    while stack:
        cur = eval(stack, cur)
            #except Exception as e:
            #for f in stack:
            #print f.env.lexical and f.env.dynamic.active
            #raise e
    if cur:
        print cur.number
    return 0
    
def target(*args):
    return entry_point, None

if __name__ == "__main__":
    entry_point("")
