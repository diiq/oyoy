"""
An interpreter for a code-as-object version of Oyster, as opposed to code-as-list.
"""
# builtin functions take an environment as an argument; okie?
# types: builtin call number symbol etc

current = ""

def eval(code, env):
    if code["type"] == "call":
        
        function = eval(code["call"], env)

        new_env = dict(function["bindings"])
        for arg in function["args"]:
            new_env[arg["name"]] = eval_arg(arg, code["args"][arg["name"]], env)

        return apply_fn(function, new_env)
        
    elif (code["type"] == "builtin" or
          code["type"] == "number"):
        return code

    elif code["type"] == "symbol":
        return lookup(env, code)

def eval_arg(arg, code, env):
    if arg["code"]:
        return arg 
    else:
        return eval(code, env)

def lookup(env, symbol):
    return env[symbol["id"]]

def apply_fn(function, env):
    if function["type"] == "builtin":
        return function["function"](env)
    else:
        return eval(function["body"], env)


# That's all, folks!

# This is floppy, like wet spaghetti. Don't call it; wrap it in a
# function call, like you see below. Should perhaps be replaced by
# separate classes, but those are so *verbose*...


def Atom(typ, value):
    self = {}
    self["type"] = typ
    self["value"] = value
    return self
    
def Arg(name):
    self = {}
    self["type"] = "arg"
    self["name"] = name
    self["code"] = False
    return self
    
def Call(call, kwargs):
    self = {}
    self["type"] = "call"
    self["call"] = call
    self["args"] = kwargs
    return self
    
def Lambda(args, body, env):
    self = {}
    self["type"] = "lambda"
    self["args"] = args
    self["body"] = body
    self["bindings"] = env
    return self
    
def Builtin(function, args):
    self = {}
    self["type"] = "builtin"
    self["args"] = args
    self["function"] = function
    self["bindings"] = {}
    return self
    
def builtin_plus(env):
    x = env["x"]["value"]
    y = env["y"]["value"]
    return Atom("number", x+y)
    
plus = Builtin(builtin_plus, [Arg("x"), Arg("y")])


def entry_point(argv):
    #    testcode = Call(plus, x=Atom("number", 2), y=Atom("number", 3))
    testcode = Call(plus, 
                    {"x" : Atom("number", 2), 
                     "y" : Call(plus, 
                             {"x" : Atom("number", 3), 
                              "y" : Atom("number", 5)})})
    print eval(testcode, {})["value"]
    return 0
    
def target(*args):
    return entry_point, None

if __name__ == "__main__":
    entry_point("")
