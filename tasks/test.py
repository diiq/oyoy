from fabric.api import local, settings, hide, task


@task
def style():
    """Runs pep8 to check python standard style"""
    with hide("running", "warnings"):
        local("flake8 ./ --max-complexity 10 --exclude \".git,.#*\"")


@task
def unit(args=""):
    """Runs unit tests"""
    with hide("running"):
        local("honcho run -e .env.test nosetests --rednose %s" % args)


@task(default=True)
def all():
    """Runs all tests; style, unit, and integration."""
    with settings(warn_only=True):
        print "Testing style..."
        style()
        print "Testing units..."
        unit()


@task
def auto(args=None):
    """Runs unit tests continuously, re-running when files have changed."""
    #    with hide("running"):
    if args:
        local("honcho run -e .env.test sniffer -x --rednose -x%s" % args)
    else:
        local("honcho run -e .env.test sniffer -x --rednose")
