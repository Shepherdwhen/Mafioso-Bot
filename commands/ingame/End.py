from discord.ext import commands

from mafia.util import check_if_is_host_or_admin

import globvars

class End(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='endgame',
        aliases=[
            'end_game',
            'endg',
            'end',
            'stop'
        ]
    )
    @commands.check(check_if_is_host_or_admin)
    async def end_game(self, ctx):
        globvars.state_manager.init_pregame()
        await ctx.send('✅ Ended game and transitioned to pregame!')
