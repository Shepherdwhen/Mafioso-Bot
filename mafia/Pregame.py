import asyncio
import sqlite3
import discord

import globvars

from mafia.Game import Game

from .errors import (AlreadyHost, AlreadyJoined, NotHost, NotHosted, NotJoined,
                     PlayerCannotHost)
from config import SERVER_ID


class Pregame:
    """Represents the Pregame state of the bot.
    A pregame has the following properties
     - A queue of players in the lobby
     - A queue of hosts

    At least one host is required to transition to the game state.
    """
    
    def __init__(self):
        self.hosts: 'set[discord.Member]' = set()
        self.queue: 'set[discord.Member]' = set()

        asyncio.create_task(self._init_from_db())

    async def _init_from_db(self):
        with sqlite3.connect('database.sqlite3') as connection:
            res = connection.execute("""
            SELECT key, value FROM data
            """)

            data = {key: value for (key, value) in res}

        guild = globvars.client.get_guild(SERVER_ID)

        for id in data.get('pregame.hosts', '').split(','):
            if id:
                self.hosts.add(await guild.fetch_member(id))

        for id in data.get('pregame.queue', '').split(','):
            if id:
                self.queue.add(await guild.fetch_member(id))

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

        with sqlite3.connect('database.sqlite3') as connection:
            connection.execute("""
            INSERT OR REPLACE
                INTO data (key, value)
                VALUES (:key, :value)
            """, {
                'key': 'pregame.hosts',
                'value': ','.join([str(member.id) for member in self.hosts])
            })

    def unregister_host(self, target: 'discord.Member'):
        """Unregister a host.
        If the target is not a host, `NotHost()` is raised.
        """

        if target not in self.hosts:
            raise NotHost()
        self.hosts.remove(target)

        with sqlite3.connect('database.sqlite3') as connection:
            connection.execute("""
            INSERT OR REPLACE
                INTO data (key, value)
                VALUES (:key, :value)
            """, {
                'key': 'pregame.hosts',
                'value': ','.join([str(member.id) for member in self.hosts])
            })

    def register_player(self, player: 'discord.Member'):
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

        with sqlite3.connect('database.sqlite3') as connection:
            connection.execute("""
            INSERT OR REPLACE
                INTO data (key, value)
                VALUES (:key, :value)
            """, {
                'key': 'pregame.queue',
                'value': ','.join([str(member.id) for member in self.queue])
            })

    def unregister_player(self, player: 'discord.Member'):
        """Removes a player from the pregame queue.
        If the player is already not in the queue, `NotJoined()`
        is raised.
        """

        if player not in self.queue:
            raise NotJoined()
        self.queue.remove(player)

        with sqlite3.connect('database.sqlite3') as connection:
            connection.execute("""
            INSERT OR REPLACE
                INTO data (key, value)
                VALUES (:key, :value)
            """, {
                'key': 'pregame.queue',
                'value': ','.join([str(member.id) for member in self.queue])
            })

    def transition_to_game(self):
        """Converts this `Pregame` object into a `Game` object,
        that can then be used as the game object for the bot state.
        """

        if not self.hosts:
            raise NotHosted()

        return Game(self.hosts, self.queue)

