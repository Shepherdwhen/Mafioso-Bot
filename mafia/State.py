import enum

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

        # commands.ingame will not be loaded when the bot is first
        # started, so the initial transition might throw an error
        try:
            globvars.client.unload_extension('commands.ingame')
        except ExtensionNotLoaded:
            pass

        globvars.client.load_extension('commands.pregame')

    def init_game(self):
        self.state = State.ingame
        self.game = self.pregame.transition_to_game()
        self.pregame = None

        globvars.client.unload_extension('commands.pregame')
        globvars.client.load_extension('commands.ingame')
