import enum

from discord.ext.commands.errors import ExtensionNotLoaded

from mafia.Pregame import Pregame


class State(enum.Enum):
    ingame = 'ingame'
    pregame = 'pregame'

class StateManager:

    def __init__(self):
        self.state: State = None

        self.pregame: Pregame = None

    def init_pregame(self):
        self.state = State.pregame
        self.pregame = Pregame()

        import globvars

        globvars.client.load_extension('commands.pregame')
        
        try:
            globvars.client.unload_extension('commands.ingame')
        except ExtensionNotLoaded:
            pass
