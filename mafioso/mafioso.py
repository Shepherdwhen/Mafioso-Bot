import logging

import discord
from redbot.core import Config, commands
from redbot.core import Config
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


# This part was made by phenom4n4n


class Mafioso(commands.Cog):
    """
    Cog Description

    Less important information about the cog
    """

    def __init__(self, bot: Red):
        super().__init__()
        self.players = {}
        self.killqueue = []
        self.nosu = 0
        self.bot = bot
        self.signed_up_role = 810988151476453477
        self.spectator_role = 797155577154633728
        self.backup_role = 797377006659436576
        self.alive_role = 796806682344161320
        self.dead_role = 796806821490589796
        self.moderator_role = 856971152978608188
        self.admin_role = 796806958329495624
        self.mod_ingame_role = 847850195366707310
        self.admin_ingame_role = 796808073129623553
        self.config = Config.get_conf(self, identifier=6, force_registration=True)
        self.default_player = {"obj": None, "emoji": 'None', "alive": False, "role": None}

        default_global = {"players": {}, "nosu": 0, "guild_id": 0}

        self.config.register_global(**default_global)

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    async def load_from_config(self):
        guild_id = await self.config.guild_id()
        guild = self.bot.get_guild(int(guild_id))
        if guild is None:
            log.warning("Failed to load guild from config")
            return
        self.nosu = await self.config.nosu()
        config_players = await self.config.players()
        for member_id, this_player in config_players.items():
            emoji_id = this_player['emoji']
            alive = this_player['alive']
            role = this_player['role']

            emoji = emoji_id if not isistance(emoji_id, int) else self.bot.get_emoji(emoji_id)
            member_id = int(member_id)  # Converts string back to int

            member = guild.get_member(member_id)
            if member is not None:  # None is failed to get the user.
                # (Quit the server, programming error)
                self.players[member_id] = {"obj": member, "emoji": emoji, "alive": alive, "role": role}
            else:
                log.warning(f"Failed to get id: {member_id}")

    async def save_to_config(self):
        await self.config.nosu.set(self.nosu)
        saveable_players = {}
        guild_id = 0
        for member_id, player_dict in self.players.items():
            member = player_dict["obj"]
            emoji = player_dict["emoji"]
            log.info(f"{type(emoji)}")
            guild_id = member.guild.id  # Fetch the guild ID for this batch of members
            if isisntance(emoji, discord.Emoji):
                log.info(f"{emoji} is discord.Emoji")
                emoji = emoji.id  # Save the custom emoji ID

            # This is the structure of the config file now. Only emoji (as id), alive status, and role (tbd)
            this_player = {"emoji": emoji, "alive": player_dict["alive"], "role": player_dict["role"]}

            saveable_players[member.id] = this_player
        log.info(saveable_players)
        await self.config.players.set(saveable_players)
        await self.config.guild_id.set(guild_id)  # Save the guild_id

    def check_for_duplicates(self, new_member, new_emote):
        if new_member.id in self.players:
            return False
        if new_emote in [player_dict['emoji'] for player_dict in self.players.values()]:
            return False
        return True

    @commands.command()
    async def signup(self, ctx: commands.Context, emoji: RealEmojiConverter):
        if not self.check_for_duplicates(ctx.author, emoji):
            await ctx.send(":x: Duplicate emoji or player found")
            return

        player_dict = self.default_player.copy()
        player_dict['obj'] = ctx.author
        player_dict['emoji'] = emoji

        self.players[ctx.author.id] = player_dict
        self.nosu = self.nosu + 1
        role = ctx.guild.get_role(self.signed_up_role)
        spec = ctx.guild.get_role(self.spectator_role)
        back = ctx.guild.get_role(self.backup_role)
        await ctx.author.remove_roles(back, reason="Signed up")
        await ctx.author.remove_roles(spec, reason="Signed up")
        await ctx.author.add_roles(role, reason="Signed up")
        await self.save_to_config()
        await ctx.send(f"Successfully Signed Up with {emoji}")
        # signup command takes name and emoji and stores it in players list

    @commands.command()
    async def signout(self, ctx: commands.Context):
        del self.players[ctx.author.id]
        self.nosu = self.nosu - 1
        role = ctx.guild.get_role(self.signed_up_role)
        await ctx.author.remove_roles(role, reason="Signed out")
        await self.save_to_config()
        await ctx.send(f"Successfully Signed Out")
        # Signout command

    @commands.command()
    async def spectate(self, ctx: commands.Context):
        spec = ctx.guild.get_role(self.spectator_role)
        back = ctx.guild.get_role(self.backup_role)
        await ctx.author.remove_roles(back, reason="Spectating")
        await ctx.author.add_roles(spec, reason="Spectating")
        await ctx.send(f"You are now Spectating the Game")
        # spectate command

    @commands.command()
    async def backup(self, ctx: commands.Context):
        spec = ctx.guild.get_role(self.spectator_role)
        back = ctx.guild.get_role(self.backup_role)
        await ctx.author.add_roles(back, reason="Backup")
        await ctx.author.remove_roles(spec, reason="Backup")
        await ctx.send(f"You are now a Substitute for the game")
        # backup command

    @commands.command()
    async def resetlist(self, ctx: commands.Context):
        for player_dict in self.players.values():
            member = player_dict['obj']
            role = ctx.guild.get_role(self.signed_up_role)
            self.nosu = self.nosu - 1
            await member.remove_roles(role, reason="Resetting")
            await ctx.send(f"Signing out {member.display_name}")
        self.players = {}
        await self.save_to_config()
        await ctx.send("Signed out all players successfully")

    # command to reset the list of signed up players

    @commands.command()
    async def debuglist(self, ctx: commands.Context):
        self.players = {}
        self.nosu = 0
        await self.save_to_config()
        await ctx.send("Debugged List")

    # command to debug the list of signed up players

    @commands.group()
    async def list(self, ctx):
        """This is the base command for the lists"""
        pass  # Does nothing on it's own, call the sub commands

    @list.command()
    async def signed_up(self, ctx: commands.Context):

        to_print = f"**Signed up** | {self.nosu}\n"  # title for the list

        for player_dict in self.players.values():
            emoji = player_dict["emoji"]
            member = player_dict["obj"]
            to_print += f'{emoji}  {member.mention}  ({member.name})\n'

        message = await ctx.send(".")
        await message.edit(content=to_print)
        # lists all signed up players in players list

    @list.command()
    async def alive(self, ctx: commands.Context):
        alive_count = sum(player_dict["alive"] for player_dict in self.players.values())
        to_print = f"**Alive** | {alive_count}\n"  # title for the list
        for member_id, player_dict in self.players.items():
            if not player_dict["alive"]:  # Checks if they're dead
                log.debug(player_dict)
                continue  # Skips this entry
            emoji = player_dict["emoji"]
            member = player_dict["obj"]
            to_print += f'{emoji}  {member.mention}  ({member.name})\n'

        message = await ctx.send(".")
        await message.edit(content=to_print)
        # lists all signed up players in players list

    @commands.command()
    async def startgame(self, ctx: commands.Context):
        for player_dict in self.players.values():
            member = player_dict['obj']
            role = ctx.guild.get_role(self.signed_up_role)
            alive = ctx.guild.get_role(self.alive_role)
            await member.remove_roles(role, reason="starting game")
            await member.add_roles(alive, reason="starting game")
            player_dict['alive'] = True
            await ctx.send(f"Adding alive role to {member.display_name}")
        await self.save_to_config()
        await ctx.send("Game started")
        # the command to make all players alive and start the game

    @commands.group()
    async def killq(self, ctx):
        """This is the base command for the kill queue"""
        pass  # Does nothing on it's own, call the sub commands

    @killq.command()
    async def add(self, ctx, member: discord.Member):
        self.killqueue.append(member)
        await ctx.send(f"Added {member.display_name} to the Kill Queue")

    @killq.command()
    async def clear(self, ctx, member: discord.Member):
        self.killqueue = []
        await ctx.send(f"Kill Queue Cleared")

    @killq.command()
    async def execute(self, ctx: commands.Context):
        for member in self.killqueue:
            dead = ctx.guild.get_role(self.dead_role)
            alive = ctx.guild.get_role(self.alive_role)
            await member.remove_roles(alive, reason="killed")
            await member.add_roles(dead, reason="killed")
            self.players[member.id]['alive'] = False
            await ctx.send(f"Killing {member.display_name}")
        self.killqueue = []
        await ctx.send("Everyone killed")

    @commands.command()
    async def sheet(self, ctx: commands.Context):
        sheet_list = f"```\n"  # start
        for player_dict in self.players.values():
            member = player_dict["obj"]
            sheet_list += f'=SPLIT({member.name},{member.id}, ,)\n'
        sheet_list += f"```"  # end

        await ctx.send(f'{sheet_list}')
        # lists all signed up players in players list

    @commands.command()
    async def demote(self, ctx: commands.Context):
        mod = ctx.guild.get_role(self.moderator_role)
        mod_ig = ctx.guild.get_role(self.mod_ingame_role)
        admin = ctx.guild.get_role(self.admin_role)
        admin_ig = ctx.guild.get_role(self.admin_ingame_role)
        if "856971152978608188" in [role.id for role in ctx.message.author.roles]:
            await member.remove_roles(mod, reason="demote")
            await member.add_roles(mod_ig, reason="demote")
            await ctx.send("Demoted from moderator")
        if "796806958329495624" in [role.id for role in ctx.message.author.roles]:
            await member.remove_roles(admin, reason="demote")
            await member.add_roles(admin_ig, reason="demote")
            await ctx.send("Demoted from admin")
        else:
            await ctx.send(":x: you do not have the permissions for that")

    @commands.command()
    async def promote(self, ctx: commands.Context):
        mod = ctx.guild.get_role(self.moderator_role)
        mod_ig = ctx.guild.get_role(self.mod_ingame_role)
        admin = ctx.guild.get_role(self.admin_role)
        admin_ig = ctx.guild.get_role(self.admin_ingame_role)
        if "847850195366707310" in [role.id for role in ctx.message.author.roles]:
            await member.remove_roles(mod_ig, reason="promote")
            await member.add_roles(mod, reason="promote")
            await ctx.send("Promoted to moderator")
        if "796808073129623553" in [role.id for role in ctx.message.author.roles]:
            await member.remove_roles(admin_ig, reason="promote")
            await member.add_roles(admin, reason="promote")
            await ctx.send("Promoted to admin")
        else:
            await ctx.send(":x: you do not have the permissions for that")