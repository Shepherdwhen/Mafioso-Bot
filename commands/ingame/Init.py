from discord.ext import commands

import globvars
from mafia.util import check_if_is_host_or_admin


class Init(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="init",
        aliases=[
            "setup"
        ]
    )
    @commands.check(check_if_is_host_or_admin)
    async def init(self, ctx):
        await globvars.state_manager.game.start()
