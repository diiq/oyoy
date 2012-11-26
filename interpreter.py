"""
An interpreter for a code-as-object version of Oyster, as opposed to code-as-list.
"""

class OyO(object):
    pass

class Number(OyO):
    def __init__(self, value):
        self.number = value

class Symbol(OyO):
    def __init__(self, value):
        self.symbol = value

class Arg(OyO):
    def __init__(self, name, code=False):
        self.name = name
        self.code = code

class Call(OyO):
    def __init__(self, call, kwargs):
        self.call = call
        self.args = kwargs

class Lambda(OyO):
    def __init__(self, args, body, env):
        self.lambda_list = args
        self.body = body
        self.bindings = env

class Builtin(OyO):
    def __init__(self, function, args, bindings={}):
        self.function = function
        self.lambda_list = args
        self.bindings = bindings

class List(OyO):
    def __init__(self, items):
        self.items = items

#class Frame():
#    def __init__(self,  
        
FAIL = Symbol("Fail")

def eval(code, env):
    ret = FAIL
    # Function call
    if isinstance(code, Call):
        
        function = eval(code.call, env)
        
        # Evaluate arguments
        new_env = function.bindings
        for arg in function.lambda_list:
            new_env[arg.name] = [eval_arg(arg, code.args[arg.name], env)]

        # If it's a built-in, apply it
        if isinstance(function, Builtin):
            ret =function.function(new_env, env)

        # if it's user-defined, execute the body
        elif isinstance(function, Lambda):
            for c in function.body:
                ret = eval(c, new_env)

    # Self-valued Atom
    elif (isinstance(code, Builtin) or
          isinstance(code, Number)):
        ret = code

    # Symbol
    elif isinstance(code, Symbol):
        ret = env[code.symbol][0]

    return ret

def eval_arg(arg, code, env):
    if arg.code:
        return code
    else:
        return eval(code, env)



def populate_globals(env):
    # Builtin *functions* take an environment, rather than individual
    # args.
    def builtin_plus(env, _):
        x = env["x"][0].number
        y = env["y"][0].number
        return Number(x+y)

    # Builtin *objects* have arglists, though.
    iplus = Builtin(builtin_plus, [Arg("x"), Arg("y")])

    env["builtin+"] = iplus
    
    # And lambda objects have an environtment to close over.
    env["+"] = [Lambda([Arg("x"), Arg("y")], 
                      [Call(iplus, {"x":Symbol("x"), "y":Symbol("y")})], 
                      {})] # <-- environment


    # Lambda:
    def builtin_lambda(env, benv):
        args = env["args"][0]
        body = env["body"][0]
        return Lambda(args.items, body.items, benv)

    env["fn"] = [Builtin(builtin_lambda, [Arg("args", True), Arg("body", True)])]
    return env

def entry_point(argv):
    # For now, entry_point just runs a test, applying a user-defined
    # function that wraps a built-in addition function.

    # A call takes a dictionary of arguments; all args are keyword
    # args.
    env = populate_globals({})
    make_lam = Call(Symbol("fn"),
                    {"args" : List([Arg("a"), Arg("b")]),
                     "body" : List([Call(Symbol("+"), 
                                         {"x":Symbol("a"),
                                          "y":Symbol("b")})])})
    testcode = Call(make_lam, 
                    {"a" : Number(2), 
                     "b" : Call(Symbol("+"),
                             {"x" : Number(3), 
                              "y" : Number(5)})})

    print eval(testcode, env).number
    return 0
    
def target(*args):
    return entry_point, None

if __name__ == "__main__":
    entry_point("")
