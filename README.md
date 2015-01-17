Oyster is a programming language. It's heavily lisp-influenced (though
it becomes less lisp-like with each iteration in its production).

This particular project is an attempt at producting an interpreter for
Oyster in RPython, for translation and JIT-generation by pypy.

Because I'm just playing around, the best way to learn what I'm doing,
and what you can do, is to send me an email: [s@diiq.org](mailto:s@diiq.org)

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

Get set up by running:

    fab db.reset
    fab server

You're now running a development server! Yay!

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
