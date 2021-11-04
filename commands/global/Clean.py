import math
import asyncio
from discord.ext import commands

from mafia.util import check_if_is_admin

class Clean(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        'clean',
        aliases=[
            'purge'
        ]
    )
    @commands.check(check_if_is_admin)
    async def purge(self, ctx:commands.Context):
        await ctx.send('Purge:\n>This will delete all non-bot messages in this channel!\nAre you sure? [y/n]')

        res = ""
        
        try:
            res = (await ctx.bot.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)).content
        except asyncio.TimeoutError:
            res = "n"

        if res == "y" or res == "Y":
            await ctx.channel.purge(limit=math.inf, check=lambda m: m.author.id != ctx.bot.user.id)
        else:
            await ctx.send("Aborted clean.")
