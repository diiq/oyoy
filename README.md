Oyster is a programming language. It's heavily lisp-influenced (though
it becomes less lisp-like with each iteration).

## Oyster

Oyster is lisp-like; but rather than being built around cons cells,
it's built around rather Frankensteinian data structures that have
three parts. There each one has a list-y bit, which can be iterated
over; a hash-y bit, which supports key-value lookups, and a 'metadata'
bit, for, uh, metadata about the object (its class, its lexical
environment, etc).

Oyster's syntax is based on Psychotic Bastard. Much of the development
of the PB syntax for lisp is documented in [this
gist](https://gist.github.com/diiq/1087830).

Here's a very simple sample that currently runs:

    set my-plus: fn (a b):
        + a b

    my-plus 2 (+ 3 5)

(It returns 10.)

Oyster is unique largely because of its extensive use of
[fexprs](http://en.wikipedia.org/wiki/Fexpr). This is almost
universally considered a bad idea, and made Oyster's [ancestor
languages](https://github.com/diiq/eight) painfully slow. It is my
hope that [PyPy](http://pypy.org/) will be able to host Oyster and use
its JIT-generator to win back the speed lost to fexprs.

Fexprs have astonishing expressive power. My goal with Oyster is to
demonstrate and explore that power, even if the resulting language
proves impractical.

Because I'm just playing around, the best way to learn what I'm doing is to contact me. Twitter ([@diiq](https://twitter.com/diiq), and email ([s@diiq.org](mailto:s@diiq.org)) both work great.

## Installation

To start, you'll need python and pip installed. Use the package manager of your choice.

1. Install [virtualenv](http://virtualenv.readthedocs.org/en/latest/) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/).

        pip install virtualenv virtualenvwrapper

2. Setup your shell to work with virtualenvwrapper. [Here](http://virtualenvwrapper.readthedocs.org/en/latest/install.html#shell-startup-file) are the full instructions. For reference, here's roughly what you need in your `.bashrc` or `.zshrc`:

        export WORKON_HOME=$HOME/.virtualenvs
        source /usr/local/bin/virtualenvwrapper.sh

3. Run `install.sh` to setup the virtualenv:

        source scripts/install.sh

## Developing

Activate the virtual environment (if you just installed, it's already active; see [Time Savers] for how to have this happen automatically when you cd into the project directory).

    workon oyoy

Use `fab` to do things:

    fab test.auto
    fab test.style

You're now running a dev setup! Yay!

## Time savers

To automatically activate the virualenv when you cd into the project directory, put https://gist.github.com/clneagu/7990272#file-bashrc-L22 in your .profile, .bashrc or .zshrc.

## Contributing

### Style:

Set up your editor to use:

- 4-space tabs.
- No trailing whitespace.
- One trailing newline at the end of the file.

Try to keep lines < 80 characters; DEFINITELY keep lines < 120 characters.

One space should be the largest number of spaces between characters within a single line.

The test suite will check source for any styles contrary to those defined in PEP8 (https://www.python.org/dev/peps/pep-0008).
