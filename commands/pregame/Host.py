"""Contains commands related to hosting a game
"""

import discord
from discord.ext import commands

import globvars
from mafia.util import check_if_is_host_or_admin


class Host(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='host'
    )
    async def host(self, ctx):
        globvars.state_manager.pregame.register_host(ctx.author)
        await ctx.send('✅ You are now the host!')

    @commands.command(
        name='unhost'
    )
    @commands.check(check_if_is_host_or_admin)
    async def unhost(self, ctx):
        globvars.state_manager.pregame.unregister_host()
        await ctx.send('✅ You are now no longer the host!')

    @commands.command(
        name='transfer_host',
        aliases=['thost', 'transferhost', 'changehost', 'change_host', 'swaphost', 'swap_host']
    )
    @commands.check(check_if_is_host_or_admin)
    async def transfer_host(self, ctx, new_host: discord.Member):
        globvars.state_manager.pregame.transfer_host(new_host)
        await ctx.send(f'✅ Transferred host from {ctx.author.mention} to {new_host.mention}')
