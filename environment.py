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
    def __init__(self, lexical, dynamic):
        self.active = {} # active is where local variables are set
        self.lexical = lexical # the lexical environment
        self.dynamic = dynamic # the leak environment
        self.leaks = {}
        
    def set(self, symbol, value):
        if symbol in self.leaks:
            if self.leaks[symbol] == Env.LEAK:
                self.dynamic.set(symbol, value)
            elif self.leaks[symbol] == Env.ALTER:
                self.lexical.set(symbol, value)
        else:
            self.active[symbol] = value
            
    def lookup(self, symbol):
        if symbol in self.leaks and self.leaks[symbol] == Env.LEAK:
            return self.dynamic.lookup(symbol)
        if symbol in self.active:
            return self.active[symbol]
        elif self.lexical:
            return self.lexical.lookup(symbol)
        else:
            raise LookupError, symbol 

    def leak(self, symbol):
        self.leaks[symbol] = Env.LEAK

    def alter(self, symbol):
        self.leaks[symbol] = Env.ALTER

        
def test_env():
    lexical = Env(None, None)
    dynamic = Env(None, None)
    local = Env(lexical, dynamic)

    local.set("a", 5)
    assert local.lookup("a") == 5
    assert local.active["a"] == 5

    dynamic.set("b", 6)
    local.leak("b")
    
    assert local.lookup("b") == 6
    local.set("b", 10)
    assert dynamic.active["b"] == 10

    lexical.set("g", 15)
    assert local.lookup("g") == 15
        
    local.alter("g")
    local.set("g", 20)
    assert local.lookup("g") == 20
    assert lexical.active["g"] == 20


if __name__ == "__main__":
    test_env()
    
