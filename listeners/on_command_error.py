import traceback

from discord.ext import commands
from discord.ext.commands.errors import (BadArgument, CheckFailure,
                                         CommandNotFound,
                                         MissingRequiredArgument)

from mafia.errors import (AlreadyHost, AlreadyJoined, CannotBackup, CannotHost,
                          MafiaException, NoRoles, NotAdmin, NotHost,
                          NotHosted, NotJoined, NotPlayer, NotPrivateChannel,
                          PlayerCannotHost)


class on_command_error(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = error.original if hasattr(error, 'original') else error # error might be a CommandInvokeException

        if isinstance(error, PlayerCannotHost):
            return await ctx.send('⛔ You cannot host and play at the same time!\nLeave the lobby first and try again.')
        elif isinstance(error, AlreadyJoined):
            return await ctx.send('⛔ You are already in the game!')
        elif isinstance(error, NotJoined):
            return await ctx.send('⛔ You are already not in the game!')
        elif isinstance(error, NotHosted):
            return await ctx.send('⛔ This game doesn\'t have a host!')
        elif isinstance(error, NotHost):
            return await ctx.send('⛔ You must be the host to perform this action!')
        elif isinstance(error, NotAdmin):
            return await ctx.send('⛔ You must be an administrator to perform this action!')
        elif isinstance(error, CannotHost):
            return await ctx.send('⛔ You cannot host games!')
        elif isinstance(error, AlreadyHost):
            return await ctx.send('⛔ You are already a host!')
        elif isinstance(error, NoRoles):
            users = "**, **".join([user.display_name for user in error.missing_roles])
            return await ctx.send(f'⛔ Some members have no roles: **{users}**')
        elif isinstance(error, NotPlayer):
            return await ctx.send('⛔ This action requries a player!')
        elif isinstance(error, CannotBackup):
            return await ctx.send('⛔ That user cannot be a backup!')
        elif isinstance(error, NotPrivateChannel):
            return await ctx.send('⛔ This command can only be run in prirvate channels!')
        elif isinstance(error, CommandNotFound):
            return
        elif isinstance(error, CheckFailure):
            return
        elif isinstance(error, BadArgument):
            return await ctx.send('⛔ An invalid or incomplete argument was provided!')
        elif isinstance(error, MissingRequiredArgument):
            return await ctx.send('⛔ You are missing arguments!')
        elif isinstance(error, MafiaException):
            await ctx.send(f'⛔ An unhandled error has occured: {error}')

            try:
                raise error
            except Exception:
                traceback.print_exc()
        else:
            await ctx.send(f'⛔ An unexpected error has occured: {error}')

            try:
                raise error
            except Exception:
                traceback.print_exc()

    @commands.Cog.listener(name='on_error')
    async def on_error(self, *args, **kwargs):
        print(args)