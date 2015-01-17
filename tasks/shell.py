from fabric.api import task


@task()
def pyshell():
    """Starts an interactive python shell"""
    # TODO import some stuff here
    context = dict()  # and add it to the environment here
    banner = "~~~ Oyster Shell ~~~"
    try:
        # 0.10.x
        from IPython.Shell import IPShellEmbed
        ipshell = IPShellEmbed(banner=banner)
        ipshell(global_ns=dict(), local_ns=context)
    except ImportError:
        # 0.12+
        from IPython import embed
        embed(banner1=banner, user_ns=context)
