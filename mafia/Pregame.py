import asyncio

import discord

import globvars
from config import LOBBY_CHANNEL_ID

from .errors import (AlreadyHosted, AlreadyJoined, NotHosted, NotJoined,
                     PlayerCannotHost)


async def auto_unhost_task():
    from config import AUTO_UNHOST_TIMEOUT
    
    await asyncio.sleep(AUTO_UNHOST_TIMEOUT)

    await globvars.client.get_channel(LOBBY_CHANNEL_ID).send(f'{globvars.state_manager.pregame.host.mention} You have been unhosted because the game took too long to start.')
    globvars.state_manager.pregame.unregister_host()

class Pregame:
    """Represents the Pregame state of the bot.
    A pregame has the following properties
     - A queue of players in the lobby
     - An (optional) host

    The host is required to transition to the game state.
    """
    
    def __init__(self):
        self.host: discord.Member = None
        self.queue: set[discord.Member] = set()
        self.auto_unhost_task = None

    def register_host(self, host: discord.Member):
        """Register a host for this pregame.
        If this pregame is already hosted, `AlreadyHosted()` is
        raised.
        If the host is currently in the queue, `PlayerCannotHost()`
        is raised.
        """

        if self.host:
            raise AlreadyHosted()
        if host in self.queue:
            raise PlayerCannotHost()
        self.host = host
        self.auto_unhost_task = asyncio.create_task(auto_unhost_task())

    def unregister_host(self):
        """Unregister the current host.
        If there is no host, `NotHosted()` is raised.
        """

        if not self.host:
            raise NotHosted()
        self.host = None
        self.auto_unhost_task.cancel()

    def transfer_host(self, new_host: discord.Member):
        """Transfer host priviliges from one player to another.
        If `new_host` is currently in the queue, `PlayerCannotHost()`
        is raised.
        """

        if new_host in self.queue:
            raise PlayerCannotHost()
        self.host = new_host
        
        self.auto_unhost_task.cancel()
        self.auto_unhost_task = asyncio.create_task(auto_unhost_task())

    def register_player(self, player: discord.Member):
        """Registers a player for this pregame.
        If the player is already in the queue, `AlreadyJoined()`
        is raised.
        If the player is also this pregame's host, `PlayerCannotHost()`
        is raised.
        """

        if player in self.queue:
            raise AlreadyJoined()
        if player == self.host:
            raise PlayerCannotHost()
        self.queue.add(player)

    def unregister_player(self, player: discord.Member):
        """Removes a player from the pregame queue.
        If the player is already not in the queue, `NotJoined()`
        is raised.
        """

        if player not in self.queue:
            raise NotJoined()
        self.queue.remove(player)

    def transition_to_game(self):
        """Converts this `Pregame` object into a `Game` object,
        that can then be used as the game object for the bot state.
        """

        if not self.host:
            raise NotHosted()
        self.auto_unhost_task.cancel()
        raise NotImplemented()

