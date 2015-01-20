from fabric.api import local, hide, task

@task
def build():
    """Compiles the project using PyPy's RPython."""
    with hide("running"):
        local("python ../pypy/rpython/bin/rpython pypy_target.py")
