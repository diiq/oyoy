import sys
import os
from oyster.oyster_scanner import OysterScanner
from oyster.oyster_parser import OysterParser
from interpreter.interpreter import eval, Frame, Instruction
from interpreter.globals import populate_globals
from interpreter.environment import Env

def run_string(string):
    tokens = OysterScanner(string).tokenize()
    statements = OysterParser().parse(tokens)
    instructions = [Instruction(Instruction.CODE, statement)
                        for statement in OysterParser().parse(tokens).items]
    instructions.reverse()
    env = populate_globals(Env(None, None))
    stack = [Frame(instructions, env)]
    cur = None
    while stack:
        cur = eval(stack, cur)

    print "Result is", cur.__str__()


def run(fp):
    program_contents = ""
    while True:
        read = os.read(fp, 4096)
        if len(read) == 0:
            break
        program_contents += read
    os.close(fp)
    run_string(program_contents)

def entry_point(argv):
    try:
        filename = argv[1]
    except IndexError:
        print "You must supply a filename"
        return 1

    run(os.open(filename, os.O_RDONLY, 0777))
    return 0

def target(*args):
    return entry_point, None

if __name__ == "__main__":
    entry_point(sys.argv)
