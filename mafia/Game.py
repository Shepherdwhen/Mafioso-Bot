import discord
from discord import PermissionOverwrite
from discord.errors import NotFound

import globvars
from config import (ALIVE_ROLE_ID, DEAD_ROLE_ID, HOST_ROLE_ID,
                    LOBBY_CHANNEL_ID, SERVER_ID)

from .data import Role, channels
from .errors import MafiaException, NoRoles


class Game:
    """Represents the game state of the bot
    Keeps track of players, hosts, channels and roles
    """

    def __init__(self, hosts, players):
        self.hosts: set[discord.Member] = hosts
        self.alive_players: set[discord.Member] = players
        self.dead_players: set[discord.Member] = set()

        self.roles: dict[discord.Member, Role] = dict()

        self.kill_queue: set[discord.Member] = set()

        self.managed_channels: set[discord.TextChannel] = set()
        self.lobby_channel: discord.TextChannel = globvars.client.get_guild(SERVER_ID).get_channel(LOBBY_CHANNEL_ID)

    @property
    def players(self) -> set[discord.Member]:
        return self.alive_players | self.dead_players

    async def start(self):
        """Starts the game
        - Gives all required roles
        - Creates all needed channels
        """

        players_without_role = self.alive_players - set(self.roles.keys())
        if players_without_role:
            raise NoRoles(*players_without_role)

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

        host_role = guild.get_role(HOST_ROLE_ID)
        for host in self.hosts:
            await host.add_roles(host_role)

        alive_role = guild.get_role(ALIVE_ROLE_ID)
        for player in self.alive_players: # All players will be alive initially
            await player.add_roles(alive_role)

    async def create_channels(self):
        """Create all the channels with the needed permissions
        """

        guild = globvars.client.get_guild(SERVER_ID)
        target_category = guild.get_channel(LOBBY_CHANNEL_ID).category

        host_role = guild.get_role(HOST_ROLE_ID)

        async def create_individual_channel(channel, member, role):
            created_channel = await guild.create_text_channel(
                name=channel['name'].format(
                    player_name=member.display_name,
                    role_name=role['name']
                ),
                category=target_category,
                overwrites={
                    guild.default_role: PermissionOverwrite(read_messages=False),

                    guild.me: PermissionOverwrite(read_messages=True),
                    host_role: PermissionOverwrite(read_messages=True),
                    member: PermissionOverwrite(read_messages=True)
                }
            )

            self.managed_channels.add(created_channel)

            if 'start_message' in channel and channel['start_message']:
                await created_channel.send(channel['start_message'].format(
                    player_name=member.display_name,
                    role_name=role['name']
                ))

        async def create_multi_channel(channel, members):
            overwites = {member: PermissionOverwrite(read_messages=True) for member in members}
            overwites[guild.default_role] = PermissionOverwrite(read_messages=False)
            overwites[guild.me] = PermissionOverwrite(read_messages=True)
            overwites[host_role] = PermissionOverwrite(read_messages=True)

            created_channel = await guild.create_text_channel(
                name=channel['name'].format(
                    num_players=len(members)
                ),
                category=target_category,
                overwrites=overwites
            )

            self.managed_channels.add(created_channel)

            if 'start_message' in channel and channel['start_message']:
                await created_channel.send(channel['start_message'].format(
                    num_players=len(members)
                ))

        for channel in channels.values():
            if channel['type'] == 'single':
                for player in self.players:
                    if self.roles[player]['id'] in channel['members']:
                        await create_individual_channel(channel, player, self.roles[player])

            elif channel['type'] == 'multi':
                members = []
                for player in self.players:
                    if self.roles[player]['id'] in channel['members']:
                        members.append(player)

                if members:
                    await create_multi_channel(channel, members)

            else:
                raise MafiaException(f"Channels must be of type 'single' or 'multi', not {channel['type']!r}")

    async def send_role_messages(self):
        for player in self.players:
            await player.send(f"""
Your role for this upcoming game is:

`{self.roles[player]['name']}`

Please do not copy or screenshot this message.
            """)