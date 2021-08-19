import globvars
from mafia.errors import NotHost


def check_if_is_host(ctx):
    if globvars.state_manager.pregame.host == ctx.author:
        return True
    raise NotHost()
