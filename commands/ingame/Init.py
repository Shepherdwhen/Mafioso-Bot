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
        try:
            await ctx.send('✅ Initialized channels and roles!')
        except Exception:
            pass

    @commands.command(
        name="cleanup",
        aliases=[
            "clean_up",
            "clup"
        ]
    )
    @commands.check(check_if_is_host_or_admin)
    async def cleanup(self, ctx):
        await globvars.state_manager.game.clean_up()
        try:
            await ctx.send('✅ Removed channels and roles!')
        except Exception:
            pass

    @commands.command(
        name='reload',
        aliases=[
            'rl'
        ]
    )
    @commands.check(check_if_is_host_or_admin)
    async def reload(self, ctx):
        await self.cleanup(ctx)
        await self.init(ctx)


