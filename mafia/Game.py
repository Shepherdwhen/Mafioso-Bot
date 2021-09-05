import discord
from discord import PermissionOverwrite
from discord.errors import NotFound

import globvars
from config import (ALIVE_ROLE_ID, DEAD_ROLE_ID, HOST_ROLE_ID,
                    MAIN_CATEGORY_ID, MOD_ROLE_ID, SERVER_ID, SPECTATOR_ROLE_ID)

from .data import Role, channels
from .errors import MafiaException, NoRoles


class Game:
    """Represents the game state of the bot
    Keeps track of players, hosts, channels and roles
    """

    def __init__(self, hosts, players):
        self.hosts: 'set[discord.Member]' = hosts
        self.alive_players: 'set[discord.Member]' = players
        self.dead_players: 'set[discord.Member]' = set()

        self.roles: 'dict[discord.Member, Role]' = dict()

        self.kill_queue: 'set[discord.Member]' = set()

        self.managed_channels: 'set[discord.TextChannel]' = set()
        self.player_to_private_channel: 'dict[discord.Member, discord.TextChannel]' = dict()
        self.player_to_multi_channels: 'dict[discord.Member, set[discord.TextChannel]]' = dict()
        self.main_category: 'discord.CategoryChannel' = globvars.client.get_guild(SERVER_ID).get_channel(MAIN_CATEGORY_ID)

        # Players who have been spectators are not eligible to be backups
        # so we keep track of who has spectated this game
        # Also contains players who left the game after a back up
        self.cannot_backup: 'set[discord.Member]' = set()

    @property
    def players(self) -> 'set[discord.Member]':
        return self.alive_players | self.dead_players

    async def start(self):
        """Starts the game
        - Gives all required roles
        - Creates all needed channels
        """

        players_without_role = self.alive_players - set(self.roles.keys())
        if players_without_role:
            raise NoRoles(*players_without_role)

        # Spectators can join during pregame, load all current spectators
        # TODO: Issue with members intent?
        spectator_role = globvars.client.get_guild(SERVER_ID).get_role(SPECTATOR_ROLE_ID)
        self.cannot_backup = set(spectator_role.members)

        await self.give_init_roles()
        await self.create_channels()
        await self.send_role_messages()

    async def clean_up(self):
        for channel in self.managed_channels.copy():
            try:
                await channel.delete()
            except NotFound:
                pass # Channel already deleted
            finally:
                self.managed_channels.remove(channel)
        self.player_to_private_channel.clear()

        guild = globvars.client.get_guild(SERVER_ID)

        host_role = guild.get_role(HOST_ROLE_ID)
        for host in self.hosts:
            await host.remove_roles(host_role)

        alive_role = guild.get_role(ALIVE_ROLE_ID)
        dead_role = guild.get_role(DEAD_ROLE_ID)
        for player in self.players:
            await player.remove_roles(alive_role, dead_role)

    async def give_init_roles(self):
        """Give the initial roles to the players on game start
        """
        
        guild = globvars.client.get_guild(SERVER_ID)
        spectator_role = guild.get_role(SPECTATOR_ROLE_ID)

        host_role = guild.get_role(HOST_ROLE_ID)
        for host in self.hosts:
            await host.add_roles(host_role)
            await host.remove_roles(spectator_role)

        alive_role = guild.get_role(ALIVE_ROLE_ID)
        for player in self.alive_players: # All players will be alive initially
            await player.add_roles(alive_role)
            await player.remove_roles(spectator_role)

    async def create_channels(self):
        """Create all the channels with the needed permissions
        """

        guild = globvars.client.get_guild(SERVER_ID)
        target_category = self.main_category

        host_role = guild.get_role(HOST_ROLE_ID)
        spectator_role = guild.get_role(SPECTATOR_ROLE_ID)
        mod_role = guild.get_role(MOD_ROLE_ID)
        dead_role = guild.get_role(DEAD_ROLE_ID)

        async def create_individual_channel(channel, member):
            created_channel = await guild.create_text_channel(
                name=channel['name'],
                category=target_category,
                overwrites={
                    guild.default_role: PermissionOverwrite(read_messages=False),
                    spectator_role: PermissionOverwrite(read_messages=True, send_messages=False),
                    dead_role: PermissionOverwrite(read_messages=True, send_messages=False),

                    # Dead players talking in their private channels isnt a big
                    # deal and it may be enforced by category inheritance anyways,
                    # so don't bother restricting dead players from talking

                    guild.me: PermissionOverwrite(read_messages=True),
                    host_role: PermissionOverwrite(read_messages=True),
                    mod_role: PermissionOverwrite(read_messages=True),
                    member: PermissionOverwrite(read_messages=True)
                }
            )

            self.managed_channels.add(created_channel)
            self.player_to_private_channel[member] = created_channel

        async def create_multi_channel(channel, members):
            dead_role = guild.get_role(DEAD_ROLE_ID)

            overwrites = {member: PermissionOverwrite(read_messages=True) for member in members}
            overwrites[guild.default_role] = PermissionOverwrite(read_messages=False)
            overwrites[spectator_role] =  PermissionOverwrite(read_messages=True, send_messages=False)
            overwrites[guild.me] = PermissionOverwrite(read_messages=True)
            overwrites[host_role] = PermissionOverwrite(read_messages=True)
            overwrites[dead_role] = PermissionOverwrite(send_messages=False)

            created_channel = await guild.create_text_channel(
                name=channel['name'].format(
                    num_players=len(members)
                ),
                category=target_category,
                overwrites=overwrites
            )

            self.managed_channels.add(created_channel)
            for member in members:
                if member not in self.player_to_multi_channels:
                    self.player_to_multi_channels[member] = set()
                self.player_to_multi_channels[member].add(created_channel)

            if 'start_message' in channel and channel['start_message']:
                await created_channel.send(channel['start_message'].format(
                    num_players=len(members)
                ))

        for channel in channels.values():
            if channel['type'] == 'multi':
                members = []
                for player in self.players:
                    if self.roles[player]['id'] in channel['members']:
                        members.append(player)

                if members:
                    await create_multi_channel(channel, members)

            else:
                raise MafiaException(f"Channels must be of type 'multi', not {channel['type']!r}")

        for player in self.players:
            await create_individual_channel({
                'name': self.roles[player]['name']
            }, player)

    async def send_role_messages(self):
        for player in self.players:
            try:
                await player.send(f"""
    Your role for this upcoming game is:

    `{self.roles[player]['name']}`

    Please do not copy or screenshot this message.
                """)
            except discord.Forbidden:
                pass # User blocked
