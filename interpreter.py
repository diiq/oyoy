"""
An interpreter for a code-as-object version of Oyster, as opposed to code-as-list.
"""
# builtin functions take an environment as an argument; okie?
# types: builtin call number symbol etc

current = ""

def eval(code, env):
    if code.type == "call":
        
        function = eval(code.call, env)

        new_env = dict(function.bindings)
        for arg in function.args:
            new_env[arg.name] = eval_arg(arg, code.__dict__[arg.name], env)

        return apply_fn(function, new_env)
        
    elif (code.type == "builtin" or
          code.type == "number"):
        return code

    elif code.type == "symbol":
        return lookup(env, code)

def eval_arg(arg, code, env):
    if arg.code:
        return arg 
    else:
        return eval(code, env)

def lookup(env, symbol):
    return env[symbol.value]

def apply_fn(function, env):
    if function.type == "builtin":
        return function.function(env)
    else:
        return eval(function.body, env)


# That's all, folks!

# This is floppy, like wet spaghetti. Don't call it; wrap it in a
# function call, like you see below. Should perhaps be replaced by
# separate classes, but those are so *verbose*...

class Code(object):
    def __init__(self, type, **kwargs):
        self.type = typ
        for k, v in kwargs.iteritems():
            self.__dict__[k] = v

def Arg(name, code=False):
    return Code("arg", name=name, code=code)

def Builtin(function, args):
    return Code("builtin", function=function, args=args)

def Atom(typ, value):
    return Code(type, value=value)

def Call(call, **kwargs):
    return Code("call", **kwargs)

def Lambda(args, body, env):
    return Code("lambda", args=args, body=body, bindings=env)

def builtin_plus(env):
    x = env["x"].value
    y = env["y"].value
    return Atom("number", x+y)
    
plus = Builtin(builtin_plus, [Arg("x"), Arg("y")], {})
testcode = Call(plus, x=Atom("number", 2), y=Atom("number", 3))
testcode = Call(plus, x=Atom("number", 2), y=Call(plus, x=Atom("number", 3), y=Atom("number", 5)))
print eval(testcode, {})


