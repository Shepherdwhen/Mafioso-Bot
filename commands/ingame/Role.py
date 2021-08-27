import discord
from discord.ext import commands

import globvars
from mafia.errors import NotPlayer
from mafia.util import PlayerConverter, RoleConverter, check_if_is_host_or_admin


class Role(commands.Cog):

    def __init__(self, bot):
        self.bot  = bot

    @commands.group(
        name="role"
    )
    async def role(self, ctx):
        pass

    @role.command(
        name="set"
    )
    @commands.check(check_if_is_host_or_admin)
    async def role_set(self, ctx, target: PlayerConverter, *, role: RoleConverter):
        if target not in globvars.state_manager.game.players:
            raise NotPlayer()

        globvars.state_manager.game.roles[target] = role
        await ctx.send(f'✅ Set **{target.display_name}**\'s role!')

