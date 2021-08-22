import discord

import globvars
from config import ALIVE_ROLE_ID, HOST_ROLE_ID, LOBBY_CHANNEL_ID, SERVER_ID
from mafia.errors import NoRoles


class Game:
    """Represents the game state of the bot
    Keeps track of players, hosts, channels and roles
    """

    def __init__(self, hosts, players):
        self.hosts: set[discord.Member] = hosts
        self.alive_players: set[discord.Member] = players
        self.dead_players: set[discord.Member] = set()

        self.roles: dict[discord.Member, str] = dict()

        self.kill_queue: set[discord.Member] = set()

        self.managed_channels: set[discord.TextChannel] = set()
        self.lobby_channel: discord.TextChannel = globvars.client.get_guild(SERVER_ID).get_channel(LOBBY_CHANNEL_ID)

    async def start(self):
        """Starts the game
        - Gives all required roles
        - Creates all needed channels
        """

        players_without_role = self.alive_players - set(self.roles.keys())
        if players_without_role:
            raise NoRoles(players_without_role)

        await self.give_init_roles()
        await self.create_channels()

    async def give_init_roles(self):
        """Give the initial roles to the players on game start
        """
        
        guild = globvars.client.get_guild(SERVER_ID)

        host_role = guild.get_role(HOST_ROLE_ID)
        for host in self.hosts:
            host.add_roles(host_role)

        alive_role = guild.get_role(ALIVE_ROLE_ID)
        for player in self.alive_players: # All players will be alive initially
            player.add_roles(alive_role)

    async def create_channels(self):
        """Create all the channels with the needed permissions
        """

        raise NotImplemented()
