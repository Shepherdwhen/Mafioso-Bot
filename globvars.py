"""Contains global variables
"""

from discord.ext import commands

from mafia.State import StateManager

# The Bot instance. Initialized by main.py
client: commands.Bot = None

# The state manager
state_manager: StateManager = StateManager()
