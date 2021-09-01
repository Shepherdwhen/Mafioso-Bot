import discord
from discord.ext import commands


# Inherits from CommandError to be caught in command_error
# events
class MafiaException(commands.CommandError):
    """Base class for all Mafia exceptions
    """

class PlayerCannotHost(MafiaException):
    """Exception raised when a player attempts to host
    a game while already being in the queue for the game
    """

class AlreadyJoined(MafiaException):
    """Exception raised when a player attempts to join a
    game they are already in the queue for 
    """

class NotJoined(MafiaException):
    """Exception raised when a player attempts to leave
    a game they are not part of
    """

class NotHosted(MafiaException):
    """Exception raised when a host-less game attempts to perform
    a host-related action
    """

class NotHost(MafiaException):
    """Exception raised when a player that is not the host
    attempts to perform a host-restricted action.
    """

class NotAdmin(MafiaException):
    """Exception raised when a player that is not an admin
    attempts to perform an admin-related action
    """

class CannotHost(MafiaException):
    """Exception raised when a player that cannot host games
    attempts to do so
    """

class AlreadyHost(MafiaException):
    """Exception raised when a player attempts to become host
    when they are already host
    """

class NoRoles(MafiaException):
    """Exception raised when a game without a role for one or
    more players is started
    """

    def __init__(self, *players):
        self.missing_roles: 'set[discord.Member]' = set(players)

class NotPlayer(MafiaException):
    """Exception raised when a user that is not a player attempts
    to perform a player restricted action or is targeted by a
    player-restricted operation
    """

class CannotBackup(MafiaException):
    """Exception raised when a player that is already joined or
    hosting attempts to backup
    """
