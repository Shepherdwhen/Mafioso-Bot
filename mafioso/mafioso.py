import logging

import discord
from redbot.core import Config, commands
from redbot.core.bot import Red

log = logging.getLogger("red.Mafioso-Bot.mafioso")


class Mafioso(commands.Cog):
    """
    Cog Description

    Less important information about the cog
    """

    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot
        self.config = Config.get_conf(self, identifier=0, force_registration=True)

        default_guild = {}

        self.config.register_guild(**default_guild)

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    @commands.command() #here is the problem
    async def mafioso(self, ctx: commands.Context):
        await ctx.send("Hello world")

    @commands.command()
    async def signup(self, ctx: commands.Context, emoji):
        await ctx.send(f"Successfully Signed Up with {emoji}")
