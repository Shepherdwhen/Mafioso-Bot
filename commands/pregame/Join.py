"""Contains commands related to joining/leaving a lobby
"""

import discord
from discord.ext import commands

import globvars
from mafia.errors import AlreadyJoined, NotJoined, PlayerCannotHost
from mafia.util import check_if_is_host_or_admin


class Join(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='join',
        aliases=['j']
    )
    async def join(self, ctx):
        globvars.state_manager.pregame.register_player(ctx.author)
        await ctx.send('✅ Joined the game!')

    @commands.command(
        name='fjoin',
        aliases=['fj']
    )
    @commands.check(check_if_is_host_or_admin)
    async def fjoin(self, ctx, targets: commands.Greedy[discord.Member]):
        targets = set(targets)
        for target in targets:
            try:
                globvars.state_manager.pregame.register_player(target)
            except AlreadyJoined:
                await ctx.send(f'⛔ Cannot join {target.mention} because they are already in the game!')
            except PlayerCannotHost:
                await ctx.send('⛔ You cannot host and play at the same time!')
        await ctx.send('✅ Users are now joined!')

    @commands.command(
        name='quit',
        aliases=['q']
    )
    async def quit(self, ctx):
        globvars.state_manager.pregame.unregister_player(ctx.author)
        await ctx.send('✅ Left the game.')

    @commands.command(
        name='fquit',
        aliases=['fq']
    )
    @commands.check(check_if_is_host_or_admin)
    async def fquit(self, ctx, targets: commands.Greedy[discord.Member]):
        targets = set(targets)
        for target in targets:
            try:
                globvars.state_manager.pregame.unregister_player(target)
            except NotJoined:
                await ctx.send(f'⛔ Cannot quit {target.mention} because they are not in the game!')
        await ctx.send('✅ Users are no longer joined!')
