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
        self.players = {}
        self.nosu = (0)
        self.bot = bot
        self.signed_up_role = 810988151476453477
        self.config = Config.get_conf(self, identifier=0, force_registration=True)

        default_guild = {}

        self.config.register_guild(**default_guild)


    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    def check_for_duplicates(self, new_member, new_emote):
        if new_member.id in self.players:
            return False
        if new_emote in [emoji for member, emoji in self.players.values()]:
            return False
        return True

    @commands.command()
    async def mafioso(self, ctx: commands.Context):
        await ctx.send("Hello world")
        #hello world command to test bot

    @commands.command()
    async def signup(self, ctx: commands.Context, emoji: RealEmojiConverter):
        if not self.check_for_duplicates(ctx.author, emoji):
            await ctx.send("Member or emote invalid")
            return
        self.players[ctx.author.id] = (ctx.author, emoji)
        self.nosu = (self.nosu+1)
        role = ctx.guild.get_role(self.signed_up_role)
        await ctx.author.add_roles(role, reason="Signed up")
        await ctx.send(f"Successfully Signed Up with {emoji}")
        #signup command takes name and emoji and stores it in players list

    @commands.command()
    async def signout(self, ctx: commands.Context):
        del self.players[ctx.author.id]
        self.nosu = (self.nosu-1)
        role = ctx.guild.get_role(self.signed_up_role)
        await ctx.author.remove_roles(role, reason="Signed out")
        await ctx.send(f"Successfully Signed Out")
        #Signout command
        
    @commands.command()
    async def resetsl(self, ctx: commands.Context):    
        for member, emoji in self.players.values():
            role = ctx.guild.get_role(self.signed_up_role)
            await member.remove_roles(role, reason="Resetting")
            await ctx.send(f"Signing out {member.display_name}")
        await ctx.send("Signed out all players successfully")
    #command to reset the list of signed up players

    @commands.command()
    async def sl(self, ctx: commands.Context):

        to_print = f'**Signed up** | {self.nosu}\n' #title for the list

        to_print += '\n'.join(f'{member.mention}  ({member.display_name})  {emoji}' for member, emoji in self.players.values())
        message = await ctx.send('.')
        await message.edit(content=to_print)
        #lists all signed up players in players list
