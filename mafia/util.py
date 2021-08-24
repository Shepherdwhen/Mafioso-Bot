from discord.ext import commands
from discord.ext.commands.errors import BadArgument, CommandError

import globvars
from config import ADMIN_ROLE_ID, MOD_ROLE_ID, SERVER_ID
from mafia.errors import CannotHost, NotAdmin, NotHost
from mafia.State import State

from .data import roles


def check_if_is_host(ctx):
    if globvars.state_manager.state == State.pregame:
        if ctx.author in globvars.state_manager.pregame.hosts:
            return True
    else:
        if ctx.author in globvars.state_manager.game.hosts:
            return True
    raise NotHost()

def check_if_is_admin(ctx):
    admin_role = globvars.client.get_guild(SERVER_ID).get_role(ADMIN_ROLE_ID)

    if admin_role in ctx.author.roles:
        return True
    raise NotAdmin()

def check_if_is_host_or_admin(ctx):
    admin_role = globvars.client.get_guild(SERVER_ID).get_role(ADMIN_ROLE_ID)

    if globvars.state_manager.state == State.pregame:
        if ctx.author in globvars.state_manager.pregame.hosts:
            return True
    else:
        if ctx.author in globvars.state_manager.game.hosts:
            return True
    if admin_role in ctx.author.roles:
        return True
    raise NotHost()

def check_if_can_host(ctx):
    mod_role = globvars.client.get_guild(SERVER_ID).get_role(MOD_ROLE_ID)

    if mod_role in ctx.author.roles:
        return True
    raise CannotHost()

class RoleConverter(commands.Converter):

    def __init__(self):
        pass

    async def convert(self, ctx, argument: str):
        try:
            argument = argument.lower()

            if argument in roles: # ID match
                return roles[argument]

            for role in roles.values():
                if argument == role['name'].lower(): # Name match
                    return role

            found = None

            for role in roles.values(): # Part name match
                if argument in role['name'].lower():
                    if found:
                        found = None
                        break
                    found = role

            if found:
                return found
            raise BadArgument

        except BadArgument:
            raise # Don't catch raw BadArguments
        except Exception as e:
            raise CommandError from e
