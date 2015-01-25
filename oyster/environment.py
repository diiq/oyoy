"""
Environment class for Oyster.

Oyster has two ways to lookup symbol bindings, and three ways to bind
symbols.

The default lookup looks in lexical scope. If a symbol has been
"leaked" from the current scope, it is looked for in the dynamic scope.

The default setting behavior is to bind symbols locally only.
If a symbol has been leaked, it is set in dynamic scope.
If a symbol has been altered, it is set in lexical scope.

This behavior means no `let`, `let*` or `with` is necessary.

It also means pure functions can be identified by simple, local static
analysis.

"""


class Env():
    LEAK, ALTER = range(2)

    def __init__(self, lexical_environment, calling_environment):
        self.this_environment = {}
        self.lexical_environment = lexical_environment
        self.calling_environment = calling_environment
        self.leaks = {}

    def set(self, symbol, value):
        if symbol in self.leaks:
            if self.leaks[symbol] == Env.LEAK:
                self.calling_environment.set(symbol, value)
            elif self.leaks[symbol] == Env.ALTER:
                self.lexical_environment.set(symbol, value)
        else:
            self.this_environment[symbol] = value

    def lookup(self, symbol):
        if symbol in self.leaks and self.leaks[symbol] == Env.LEAK:
            return self.calling_environment.lookup(symbol)
        if symbol in self.this_environment:
            return self.this_environment[symbol]
        elif self.lexical_environment:
            return self.lexical_environment.lookup(symbol)
        else:
            raise LookupError(symbol)

    def leak(self, symbol):
        self.leaks[symbol] = Env.LEAK

    def alter(self, symbol):
        self.leaks[symbol] = Env.ALTER
