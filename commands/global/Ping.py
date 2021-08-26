from discord.ext import commands

class Ping(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='ping',
        aliases=[
            'pong'
        ]
    )
    async def ping(self, ctx):
        await ctx.send(f'Pong! The bot\'s latency is **{round(self.bot.latency, 2)}** seconds')
