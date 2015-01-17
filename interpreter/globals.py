from code_objects import *


def populate_globals(env):
    # Builtin *functions* take an environment, rather than individual
    # args.
    def builtin_plus(env):
        x = env.lookup("x").number
        y = env.lookup("y").number
        return Number(x+y)

    # Builtin *objects* have arglists, though.
    iplus = Builtin(builtin_plus, [Symbol("x"), Symbol("y")])

    env.set("builtin+", iplus)

    # And lambda objects have an environtment to close over.
    env.set("+", Lambda([Symbol("x"), Symbol("y")],
                        [Call(iplus, [Symbol("x"), Symbol("y")])],
                        Env(None, None)))

    # Lambda:
    def builtin_lambda(env):
        args = env.lookup("args")
        body = env.lookup("body")
        return Lambda(args.items, body.items, env.calling_environment)

    env.set("fn",
            Builtin(builtin_lambda, [Arg("args", True),
                                     Arg("body", True)]))

    # Lambda:
    def builtin_set(env):
        sym = env.lookup("symbol")
        val = env.lookup("value")
        env.calling_environment.set(sym.symbol, val)
        return val

    env.set("set", Builtin(builtin_set, [Arg("symbol", True), Symbol("value")]))

    return env
