from parser.scanner import OysterScanner
from parser.parser import OysterParser
from interpreter.interpreter import Instruction, Frame, eval
from interpreter.environment import Env
from interpreter.globals import populate_globals

def run_string():
    #file = StringIO(code)
    tokens = OysterScanner(file, "snippet").read_all()
#    tokens = [('line', ''), ('symbol', 'set'), ('symbol', 'my-plus'), ('colon', ':'), ('symbol', 'fn'), ('open', '('), ('symbol', 'a'), ('symbol', 'b'), ('close', ')'), ('colondent', ':\n'), ('indent', ''), ('line', ''), ('symbol', 'a'), ('+', '+'), ('symbol', 'b'), ('endline', ''), ('dedent', ''), ('endline', ''), ('line', ''), ('symbol', 'my-plus'), ('number', '2'), ('open', '('), ('number', '3'), ('+', '+'), ('number', '5'), ('close', ')'), ('endline', '')]
    print tokens
    # statements = OysterParser().farse(tokens)
    # instructions = [Instruction(Instruction.CODE, statement)
    #                 for statement in statements]
    # env = populate_globals(Env(None, None))
    # stack = [Frame(instructions, env)]
    # cur = None

    # print "--- INSTRUCTIONS ---"
    # for instruction in instructions:
    #     print instruction
    # instructions.reverse()
    # print "--- END INSTRUCTIONS ---"


    # while stack:
    #     cur = eval(stack, cur)
    # print "OK I DID", cur
