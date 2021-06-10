import logging

import discord
from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.commands import BadArgument
from typing import Union

log = logging.getLogger("red.Mafioso-Bot.mafioso")

class RealEmojiConverter(commands.EmojiConverter):
    async def convert(self, ctx: commands.Context, argument: str) -> Union[discord.Emoji, str]:
        try:
            emoji = await super().convert(ctx, argument)
        except BadArgument:
            try:
                await ctx.message.add_reaction(argument)
            except discord.HTTPException:
                raise commands.EmojiNotFound(argument)
            else:
                emoji = argument
        return emoji

#This part was made by phenom4n4n

class Mafioso(commands.Cog):
    """
    Cog Description

    Less important information about the cog
    """

    def __init__(self, bot: Red):
        super().__init__()
        self.current_game = []
        self.bot = bot
        self.config = Config.get_conf(self, identifier=0, force_registration=True)

        default_guild = {}

        self.config.register_guild(**default_guild)

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    @commands.command()
    async def mafioso(self, ctx: commands.Context):
        await ctx.send("Hello world")

    @commands.command()
    async def signup(self, ctx: commands.Context, emoji: RealEmojiConverter):
        self.current_game.append( (ctx.author, emoji) )
        await ctx.send(f"Successfully Signed Up with {emoji}")
        
    @commands.command()
    async def signedup(self, ctx: commands.Context):
        await ctx.send(self.current_game)
        
