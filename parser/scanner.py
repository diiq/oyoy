# -*- coding: utf-8 -*-

import plex


# Here's a mighty dangerous game, to allow λ, unicode and other
# foolishness. I will regret this definition:
letter = plex.AnyBut("0987654321-+?!$~<>_()\t\n :.")

digit = plex.Range("09")
valid_punctuation = plex.Any("-+?!$~<>_")
valid_symbol_char = letter | digit | valid_punctuation
symbol = letter + plex.Rep(valid_symbol_char) | valid_punctuation
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
        self.lineterm_action('')

    def read_all(self):
        # We'll want to make this into a generator, probs.
        res = []
        token = self.read()
        while token[0]:
            res.append(token)
            token = self.read()

        # Cheat to get rid of inital "endline" and terminating "line"
        return res[1:-1]

    def current_level(self):
        return self.indentation_stack[-1]

    def open_action(self, text):
        """Handles open parens.

        This is complicated by indentation. If we have an open paren,
        the next newline should be indented to the character following
        that paren.

        """
        position = self.position()[2]
        self.indentation_stack.append(position + 1)
        self.paren_stack.append(len(self.indentation_stack))
        return "open"

    def close_action(self, text):
        """Handles close parens.

        A close paren necessarily closes all indented blocks contained
        between it and its matching open.

        """
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
            self.produce('endline', '')
            self.produce('line', '')

        self.begin('')

    def indent_to(self, new_level):
        self.indentation_stack.append(new_level)
        self.produce('indent', '')
        self.produce('line', '')

    def dedent_to(self, new_level):
        self.produce('endline', '')
        while new_level < self.current_level():
            self.indentation_stack.pop()
            self.produce('dedent', '')
            self.produce('endline', '')
        self.produce('line', '')

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
