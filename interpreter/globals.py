# -*- coding: utf-8 -*-
from list import List
from symbol import Symbol
from number import Number
from builtin import Builtin
from oyster_lambda import Lambda


def populate_globals(env):
    # Builtin *functions* take an environment, rather than individual
    # args.

    ##
    # Add:
    #
    def builtin_add(env):
        x = env.lookup("x").number
        y = env.lookup("y").number
        return Number(x+y)

    # Builtin *objects* have arglists, though.
    iplus = Builtin(builtin_add, [Symbol("x"), Symbol("y")])

    env.set("add", iplus)

    ##
    # Lambda:
    #
    def builtin_lambda(env):
        args = env.lookup("args")
        body = env.lookup("body")
        return Lambda(args.items, body, env.calling_environment)

    fn = Builtin(builtin_lambda,
                 [List([Symbol("quote"), Symbol("args")]),
                  List([Symbol("quote"), Symbol("body")])])
    env.set("fn", fn)
    env.set("λ", fn)

    ##
    # Set:
    #
    def builtin_set(env):
        sym = env.lookup("symbol")
        val = env.lookup("value")
        env.calling_environment.set(sym.symbol, val)
        return val

    env.set("set", Builtin(builtin_set,
                           [List([Symbol("quote"), Symbol("symbol")]),
                            Symbol("value")]))

    return env
