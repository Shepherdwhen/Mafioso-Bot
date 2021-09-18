import sqlite3
from operator import indexOf

from discord.ext import commands
from discord.ext.commands.errors import (BadArgument, CommandError,
                                         MemberNotFound)

import globvars
from config import ADMIN_ROLE_ID, MOD_ROLE_ID, SERVER_ID
from mafia.errors import CannotHost, NotAdmin, NotHost, NotPlayer
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

def check_if_is_player(ctx):
    if ctx.author not in globvars.state_manager.game.players:
        raise NotPlayer()
    return True

class RoleConverter(commands.Converter):

    def __init__(self):
        pass

    async def convert(self, ctx, argument: 'str'):
        try:
            argument = argument.lower().strip('" ')

            if argument in roles: # ID match
                return roles[argument]

            for role in roles.values():
                if argument == role['name'].lower(): # Name match
                    return role
                if 'aliases' in role and argument in role['aliases']: # Alias match
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

class MemberConverter(commands.MemberConverter):

    async def convert(self, ctx, argument: 'str'):
        result = None
        try:
            result = await super().convert(ctx, argument)
        except MemberNotFound:
            # Look up by emoji
            with sqlite3.connect('database.sqlite3') as connection:
                data = connection.execute("""
                SELECT user_id, emoji, nick FROM player_data
                """).fetchall()

                emoji_to_id = {row[1]: row[0] for row in data}

                emojis = [row[1] for row in data]
                conflicting_emojis = [emoji for emoji in emojis if emojis.count(emoji) > 1]

            argument = argument.strip().lower()
            id = emoji_to_id.get(argument, None)

            if not id:
                # Look up by nickname
                nick_to_id = {row[2].lower(): row[0] for row in data if row[2]}

                if argument in nick_to_id:
                    id = nick_to_id[argument]
                else:
                    found = None
                    for nick in nick_to_id:
                        if argument in nick:
                            if found:
                                found = None # Conflict, cancel found member
                                break
                            found = nick
                    
                    if found:
                        id = nick_to_id[found]

            if id:
                member = await globvars.client.get_guild(SERVER_ID).fetch_member(id)
                if member:
                    result =  member
                if argument in conflicting_emojis:
                    result = None # Conflict, cancel found member

        if not result:
            raise MemberNotFound(argument)

        return result

class PlayerConverter(MemberConverter):

    async def convert(self, ctx, argument: 'str'):
        result = await super().convert(ctx, argument)

        if result not in globvars.state_manager.game.players:
            raise NotPlayer()

        return result
