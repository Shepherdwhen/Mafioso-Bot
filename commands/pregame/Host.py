"""Contains commands related to hosting a game
"""

import discord
from discord.ext import commands

import globvars
from config import ADMIN_ROLE_ID, SERVER_ID
from mafia.errors import NotAdmin
from mafia.util import check_if_can_host, check_if_is_host_or_admin


class Host(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='host',
        aliases = [
            "h"
        ]
    )
    @commands.check(check_if_can_host)
    async def host(self, ctx):
        globvars.state_manager.pregame.register_host(ctx.author)
        await ctx.send('✅ You are now a host!')

    @commands.command(
        name='unhost'
    )
    @commands.check(check_if_is_host_or_admin)
    async def unhost(self, ctx, target: discord.Member = None):
        if target:
            admin_role = globvars.client.get_guild(SERVER_ID).get_role(ADMIN_ROLE_ID)
            if admin_role not in ctx.author.roles:
                raise NotAdmin()
        else:
            target = ctx.author
        globvars.state_manager.pregame.unregister_host(target)

        await ctx.send('✅ You are now no longer a host!')
