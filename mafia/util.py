import globvars
from config import ADMIN_ROLE_ID, MOD_ROLE_ID, SERVER_ID
from mafia.errors import CannotHost, NotAdmin, NotHost


def check_if_is_host(ctx):
    if ctx.author in globvars.state_manager.pregame.hosts:
        return True
    raise NotHost()

def check_if_is_admin(ctx):
    admin_role = globvars.client.get_guild(SERVER_ID).get_role(ADMIN_ROLE_ID)

    if admin_role in ctx.author.roles:
        return True
    raise NotAdmin()

def check_if_is_host_or_admin(ctx):
    admin_role = globvars.client.get_guild(SERVER_ID).get_role(ADMIN_ROLE_ID)

    if ctx.author in globvars.state_manager.pregame.hosts:
        return True
    if admin_role in ctx.author.roles:
        return True
    raise NotHost()

def check_if_can_host(ctx):
    mod_role = globvars.client.get_guild(SERVER_ID).get_role(MOD_ROLE_ID)

    if mod_role in ctx.author.roles:
        return True
    raise CannotHost()
