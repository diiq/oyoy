"""
An interpreter for a code-as-object version of Oyster, as opposed to code-as-list.
"""
# builtin functions take an environment as an argument; okie?
# types: builtin call number symbol etc

current = ""

def eval(code, env):
    # Function call
    if isinstance(code, Call):
        
        function = eval(code.call, env)

        # Evaluate arguments
        new_env = copy_env(function.bindings)
        for arg in function.lambda_list:
            new_env[arg.name] = eval_arg(arg, code.args[arg.name], env)

        # If it's a built-in, apply it
        if isinstance(function, Builtin):
            return function.function(new_env)

        # if it's user-defined, execute the body
        elif isinstance(function, Lambda):
            ret = FAIL
            for c in function.body:
                ret = eval(c, new_env)
            return ret

        else:
            return FAIL 

    # Self-valued Atom
    elif (isinstance(code, Builtin) or
          isinstance(code, Number)):
        return code

    # Symbol
    elif isinstance(code, Symbol):
        return env[code.symbol]

    else:
        return FAIL

def eval_arg(arg, code, env):
    if arg.code:
        return arg 
    else:
        return eval(code, env)

def copy_env(env):
    ret = {}
    for k, v in env.iteritems():
        ret[k] = v
    return ret

# That's the whole evaluator; here are the types to go with it:

class OyO(object):
    type = "oyster"

class Number(OyO):
    def __init__(self, value):
        self.type = "number"
        self.number = value

class Symbol(OyO):
    def __init__(self, value):
        self.type = "symbol"
        self.symbol = value

class Arg(OyO):
    def __init__(self, name):
        self.type = "arg"
        self.name = name
        self.code = False

class Call(OyO):
    def __init__(self, call, kwargs):
        self.type = "call"
        self.call = call
        self.args = kwargs

class Lambda(OyO):
    def __init__(self, args, body, env):
        assert isinstance(body, list)
        assert isinstance(body[0], OyO)
        self.type = "lambda"
        self.lambda_list = args
        self.body = body
        self.bindings = env

class Builtin(OyO):
    def __init__(self, function, args):
        self.type = "builtin"
        self.lambda_list = args
        self.function = function
        self.bindings = {}

def builtin_plus(env):
    x = env["x"].number
    y = env["y"].number
    return Number(x+y)

FAIL = Symbol("Fail")



def entry_point(argv):
    # For now, entry_point just runs a test, applying a user-defined
    # function that wraps a built-in 'add'.

    iplus = Builtin(builtin_plus, [Arg("x"), Arg("y")])

    plus = Lambda([Arg("x"), Arg("y")], 
                  [Call(iplus, {"x":Symbol("x"), "y":Symbol("y")})], 
                  {})

    testcode = Call(Symbol("+"), 
                    {"x" : Number(2), 
                     "y" : Call(Symbol("+"),
                             {"x" : Number(3), 
                              "y" : Number(5)})})

    print eval(testcode, {"Fail":FAIL, "+":plus}).number
    return 0
    
def target(*args):
    return entry_point, None

if __name__ == "__main__":
    entry_point("")
