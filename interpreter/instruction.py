class Instruction():
    ARGUMENT, CODE, CALL, APPLY, LITERAL = range(5)

    def __init__(self, typ, code=None, args=None, symbol=""):
        self.type = typ
        self.code = code
        self.symbol = symbol
        self.args = args
