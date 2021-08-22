from discord.ext import commands

import globvars
from mafia.util import check_if_is_host


class Start(commands.Cog):
    """Contains commands related to starting the game
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='start'
    )
    @commands.check(check_if_is_host)
    async def start(self, ctx):
        globvars.state_manager.init_game()
        await ctx.send('✅ Transitioned to game state!')