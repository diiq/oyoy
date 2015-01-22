# -*- coding: utf-8 -*-
from lib.parsing.scanner import Token, Tokenizer, Scanner, DITTO
from lib.parsing import readers as re

#####################################
# Readers:
#

digit = re.SingleCharacterReader("1234567890")
# this is a terrible idea:
letter = re.SingleNotCharacterReader("0987654321-+?!$~<>_():\n\r #")
valid_symbol_char = re.SingleNotCharacterReader(".:()[] \n\r#")
symbol = re.SequenceReader([letter, re.RepeatReader(valid_symbol_char)])
operator = re.PickAStringReader(
    ['...', '-', '!', '*', '+', '/', '==', '!=', '<=', '>=',
     '<', '>', '&&', '||'])
number = re.RepeatReader(re.SingleCharacterReader("1234567890"), 1)
open = re.SingleCharacterReader("(")
close = re.SingleCharacterReader(")")
colon = re.SingleCharacterReader(":")
space = re.SingleCharacterReader(" ")
lineterm = re.SingleCharacterReader("\n")
colondent = re.SimpleStringReader(":\n")
indentation = re.RepeatReader(space)
comment = re.SequenceReader([re.SingleCharacterReader("#"),
                             re.RepeatReader(
                                 re.SingleNotCharacterReader("\n"))])
blank_line = re.SequenceReader([indentation,
                                re.RepeatReader(comment),
                                lineterm])


####################################
# Tokenizers:
#

symbol_tokenizer = Tokenizer(symbol, "symbol")
operator_tokenizer = Tokenizer(operator, DITTO)
number_tokenizer = Tokenizer(number, "number")
open_tokenizer = Tokenizer(open, "open")
close_tokenizer = Tokenizer(close, "close")
colon_tokenizer = Tokenizer(colon, "colon")
space_tokenizer = Tokenizer(space, "")
lineterm_tokenizer = Tokenizer(lineterm, "")
colondent_tokenizer = Tokenizer(colondent, "colondent")
indentation_tokenizer = Tokenizer(indentation, "")
comment_tokenizer = Tokenizer(comment, "")
blank_line_tokenizer = Tokenizer(blank_line, "")



####################################
# Scanner:
#


class OysterScanner(Scanner):
    def __init__(self, string):
        # The indendation stack stores the current indendation depth
        # in characters
        self.indentation_stack = [0]

        # The paren stack stores how far back into the indentation
        # stack to pop when we close the next paren.
        self.paren_stack = [0]

        self.state = self.default_state
        self.initialize_scan(string)

    def tokenize(self):
        while self.tokenize_one():
            pass
        return self.tokens[1:-1]

    def current_indentation(self):
        return self.indentation_stack[-1]

    def indent_to(self, new_level):
        self.indentation_stack.append(new_level)
        self.produce(Token('indent', ''))
        self.produce(Token('line', ''))

    def dedent_to(self, new_level):
        self.produce(Token('endline', ''))
        while new_level < self.current_indentation():
            self.indentation_stack.pop()
            self.produce(Token('dedent', ''))
            self.produce(Token('endline', ''))
        self.produce(Token('line', ''))

    def eof(self):
        self.dedent_to(0)

    def default_action(self, token):
        self.produce(token)

    def ignore_action(self, token):
        return

    def indentation_action(self, token):
        current_indentation = self.current_indentation()
        new_indentation = len(token.text)
        if new_indentation > current_indentation:
            self.indent_to(new_indentation)
        elif new_indentation < current_indentation:
            self.dedent_to(new_indentation)
        else:
            self.produce(Token('endline', ''))
            self.produce(Token('line', ''))

        self.state = self.default_state

    def open_action(self, token):
        position = self.stream.position()
        self.indentation_stack.append(position + 1)
        self.paren_stack.append(len(self.indentation_stack))
        self.produce(token)

    def close_action(self, token):
        ind = self.paren_stack.pop() or 0

        while len(self.indentation_stack) > ind:
            self.produce(Token('dedent', ''))
            self.indentation_stack.pop()
        self.indentation_stack.pop()

        self.produce(token)

    def lineterm_action(self, token):
        self.state = self.new_line_state

    def colondent_action(self, token):
        self.state = self.new_line_state
        self.produce(Token("colondent", ""))

    def operator_action(self, token):
        self.produce(token)

    default_state = [
        (operator_tokenizer,    operator_action),
        (symbol_tokenizer,      default_action),
        (number_tokenizer,      default_action),
        (open_tokenizer,        open_action),
        (close_tokenizer,       close_action),
        (colondent_tokenizer,   colondent_action),
        (colon_tokenizer,       default_action),
        (space_tokenizer,       ignore_action),
        (comment_tokenizer,     ignore_action),
        (lineterm_tokenizer,    lineterm_action),
    ]

    new_line_state = [
        (blank_line_tokenizer,  ignore_action),
        (indentation_tokenizer, indentation_action),
    ]
