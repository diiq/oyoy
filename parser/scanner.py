# -*- coding: utf-8 -*-

import plex


lmbda = plex.Str("λ")
# Here's a mighty dangerous game:
letter = plex.AnyBut("0987654321-+?!$~<>_()\t\n :")
digit = plex.Range("09")
valid_punctuation = plex.Any("-+?!$~<>_")
symbol = (letter + plex.Rep(letter | digit | valid_punctuation) |
          valid_punctuation)
number = plex.Rep1(digit)
open = plex.Str("(")
close = plex.Str(")")
space = plex.Any(" \t")
colon = plex.Str(":")
indentation = plex.Rep(plex.Str(" "))
lineterm = plex.Str("\n") | plex.Eof
comment = plex.Str("#") + plex.Rep(plex.AnyBut("\n"))
blank_line = indentation + plex.Opt(comment) + plex.Str("\n")


class OysterScanner(plex.Scanner):
    def __init__(self, file, name):
        # The indendation stack stores the current indendation depth
        # in characters
        self.indentation_stack = [0]

        # The paren stack stores how far back into the indentation
        # stack to pop when we close the next paren.
        self.paren_stack = [0]

        plex.Scanner.__init__(self, self.lexicon, file, name)

    def read_all(self):
        res = []
        token = self.read()
        res.append(token)
        while token[0]:
            token = self.read()
            res.append(token)
        return res

    def current_level(self):
        return self.indentation_stack[-1]

    def open_action(self, text):
        position = self.position()[2]
        self.indentation_stack.append(position + 1)
        self.paren_stack.append(len(self.indentation_stack))
        return "open"

    def close_action(self, text):
        ind = self.paren_stack.pop()
        while len(self.indentation_stack) > ind:
            self.produce('dedent', '')
            self.indentation_stack.pop()
        self.indentation_stack.pop()

        return "close"

    def indentation_action(self, text):
        current_level = self.current_level()
        new_level = len(text)
        if new_level > current_level:
            self.indent_to(new_level)
        elif new_level < current_level:
            self.dedent_to(new_level)
        else:
            self.produce('nodent', '')
        self.begin('')

    def indent_to(self, new_level):
        self.indentation_stack.append(new_level)
        self.produce('indent', '')

    def dedent_to(self, new_level):
        while new_level < self.current_level():
            self.indentation_stack.pop()
            self.produce('dedent', '')

    def eof(self):
        self.dedent_to(0)

    def lineterm_action(self, text):
        self.begin('new_line')

    lexicon = plex.Lexicon([
        (symbol,        "symbol"),
        (number,        "number"),
        (open,          open_action),
        (close,         close_action),
        (colon,         "colon"),
        (space,         plex.IGNORE),
        (comment,         plex.IGNORE),
        (lineterm,      lineterm_action),
        plex.State('new_line', [
            (blank_line,    plex.IGNORE),
            (indentation,   indentation_action),
        ]),
    ])
