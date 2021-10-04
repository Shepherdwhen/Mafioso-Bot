"""Contains global variables
"""

from discord.ext import commands

from mafia.State import StateManager

# The Bot instance. Initialized by main.py
client: commands.Bot = None

# The state manager
state_manager: StateManager = StateManager()

# Whether dead players and spectators can see private player channels
private_channel_vis: bool = True
