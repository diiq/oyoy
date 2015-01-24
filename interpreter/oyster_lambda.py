from oyster_object import OysterObject


class Lambda(OysterObject):
    def __init__(self, args, body, env):
        self.lambda_list = args
        self.body = body
        self.bindings = env


class Argument(object):
    # This is the symbol to which the arugment should be bound:
    argument_name = None

    # This is the function list to apply to the argument before
    # binding.
    function_list = None

    # If the function of the function list is a "prefix" symbol --
    # quote, enclose, or ellipsis, we mark that here
    prefix = None

    def __init__(self, clause):
        if isinstance(clause, List):
            self.set_argument_name(clause[1])
            self.function_list = clause.items
            self.set_prefix(self.function_list)

        else:
            set_argument_name(self, clause)

    def set_argument_name(self, symbol):
        if not isinstance(symbol, Symbol):
            raise StandardError("Bad argument name")
        self.argument_name = argument_symbol.value

    def set_prefix(self, function_list):
        function = function_list[0]
        if (isinstance(function, Symbol) and
            function.value in ["quote", "enclose", "ellipse"]):
            self.prefix = function.value

    def build_instruction(self, code):
        if self.prefix == "quote":
            pass
        elif self.prefix == "enclose":
            pass
        elif self.prefix == "ellipse":
            pass
        elif self.function_list:
            return List(self.function_list[0],
                        code,
                        self.function_list[2:])
