import enum
import sqlite3
from importlib import import_module

from discord.ext.commands.errors import ExtensionNotLoaded

import globvars
from mafia.Game import Game
from mafia.Pregame import Pregame


class State(enum.Enum):
    ingame = 'ingame'
    pregame = 'pregame'

class StateManager:

    def __init__(self):
        self.state: 'State' = None

        self.pregame: 'Pregame' = None
        self.game: 'Game' = None

    def init_pregame(self):
        self.state = State.pregame
        self.pregame = Pregame()
        self.game = None

        with sqlite3.connect('database.sqlite3') as connection:
            connection.execute("""
            DELETE
                FROM data
                WHERE key LIKE "game.%"
            """)

            connection.execute("""
            INSERT OR REPLACE
                INTO data (key, value)
                VALUES ("state", "pregame")
            """)

        import_module('commands.global.Poll').poll_power.clear()

        # commands.ingame will not be loaded when the bot is first
        # started, so the initial transition might throw an error
        try:
            globvars.client.unload_extension('commands.ingame')
        except ExtensionNotLoaded:
            pass

        globvars.client.load_extension('commands.pregame')

    def init_game(self):
        self.state = State.ingame
        if self.pregame:
            self.game = self.pregame.transition_to_game()
        else:
            self.game = Game(set(), set())
        self.pregame = None

        with sqlite3.connect('database.sqlite3') as connection:
            connection.execute("""
            DELETE
                FROM data
                WHERE key LIKE "pregame.%"
            """)

            connection.execute("""
            INSERT OR REPLACE
                INTO data (key, value)
                VALUES ("state", "ingame")
            """)

        import_module('commands.global.Poll').poll_power.clear()

        try:
            globvars.client.unload_extension('commands.pregame')
        except ExtensionNotLoaded:
            pass

        globvars.client.load_extension('commands.ingame')
