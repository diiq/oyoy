# -*- coding: utf-8 -*-
from code_objects import *


def populate_globals(env):
    # Builtin *functions* take an environment, rather than individual
    # args.
    def builtin_add(env):
        x = env.lookup("x").number
        y = env.lookup("y").number
        return Number(x+y)

    # Builtin *objects* have arglists, though.
    iplus = Builtin(builtin_add, [Symbol("x"), Symbol("y")])

    env.set("add", iplus)

    # Lambda:
    def builtin_lambda(env):
        args = env.lookup("args")
        body = env.lookup("body")
        return Lambda(args.items, body, env.calling_environment)

    fn = Builtin(builtin_lambda,
                    [List([Symbol("quote"), Symbol("args")]),
                     List([Symbol("quote"), Symbol("body")])])
    env.set("fn", fn)
    env.set("λ", fn)



    # Lambda:
    def builtin_set(env):
        sym = env.lookup("symbol")
        val = env.lookup("value")
        env.calling_environment.set(sym.symbol, val)
        return val

    env.set("set", Builtin(builtin_set,
                           [List([Symbol("quote"), Symbol("symbol")]),
                            Symbol("value")]))

    return env
