from code_objects import *


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
                        [Call(iplus, {"x": Symbol("x"), "y": Symbol("y")})],
                        Env(None, None)))

    # Lambda:
    def builtin_lambda(env):
        args = env.lookup("args")
        body = env.lookup("body")
        return Lambda(args.items, body.items, env.dynamic)

    env.set("fn",
            Builtin(builtin_lambda, [Arg("args", True),
                                     Arg("body", True)]))

    # Lambda:
    def builtin_set(env):
        sym = env.lookup("symbol")
        val = env.lookup("value")
        env.dynamic.set(sym.symbol, val)
        return val

    env.set("set", Builtin(builtin_set, [Arg("symbol", True), Arg("value")]))

    return env
