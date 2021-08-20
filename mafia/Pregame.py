import discord

from .errors import (AlreadyHost, AlreadyJoined, NotHost, NotHosted, NotJoined,
                     PlayerCannotHost)


class Pregame:
    """Represents the Pregame state of the bot.
    A pregame has the following properties
     - A queue of players in the lobby
     - A queue of hosts

    At least one host is required to transition to the game state.
    """
    
    def __init__(self):
        self.hosts: set[discord.Member] = set()
        self.queue: set[discord.Member] = set()

    def register_host(self, host: discord.Member):
        """Register a host for this pregame.
        If the host is currently in the queue, `PlayerCannotHost()`
        is raised.
        """

        if host in self.queue:
            raise PlayerCannotHost()
        if host in self.hosts:
            raise AlreadyHost()
        self.hosts.add(host)

    def unregister_host(self, target: discord.Member):
        """Unregister a host.
        If the target is not a host, `NotHost()` is raised.
        """

        if target not in self.hosts:
            raise NotHost()
        self.hosts.remove(target)

    def register_player(self, player: discord.Member):
        """Registers a player for this pregame.
        If the player is already in the queue, `AlreadyJoined()`
        is raised.
        If the player is also this pregame's host, `PlayerCannotHost()`
        is raised.
        """

        if player in self.queue:
            raise AlreadyJoined()
        if player in self.hosts:
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

        if not self.hosts:
            raise NotHosted()

        raise NotImplemented()

