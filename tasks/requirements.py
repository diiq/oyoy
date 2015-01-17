from fabric.api import task, local


@task
def requirements():
    """Installs python packages from requirements.txt"""
    local("pip install -r requirements.txt")
    local("pip install -r requirements_dev.txt")
