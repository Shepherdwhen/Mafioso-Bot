import globvars
from config import ADMIN_ROLE_ID, SERVER_ID
from mafia.errors import NotAdmin, NotHost


def check_if_is_host(ctx):
    if globvars.state_manager.pregame.host == ctx.author:
        return True
    raise NotHost()

def check_if_is_admin(ctx):
    admin_role = globvars.client.get_guild(SERVER_ID).get_role(ADMIN_ROLE_ID)

    if admin_role in ctx.author.roles:
        return True
    raise NotAdmin()

def check_if_is_host_or_admin(ctx):
    admin_role = globvars.client.get_guild(SERVER_ID).get_role(ADMIN_ROLE_ID)

    if globvars.state_manager.pregame.host == ctx.author:
        return True
    if admin_role in ctx.author.roles:
        return True
    raise NotHost()
