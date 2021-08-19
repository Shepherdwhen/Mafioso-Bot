from discord.ext import commands


# Inherits from CommandError to be caught in command_error
# events
class MafiaException(commands.CommandError):
    """Base class for all Mafia exceptions
    """

class AlreadyHosted(MafiaException):
    """Exception raised when a game is already hosted
    and a player attempts to become host
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
