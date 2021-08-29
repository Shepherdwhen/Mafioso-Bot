from discord.ext import commands

import globvars
from config import SERVER_ID, SPECTATOR_ROLE_ID
from mafia.State import State


class Spectate(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='spectate',
        aliases=[
            's'
        ]
    )
    async def spectate(self, ctx):
        if globvars.state_manager.state == State.pregame:
            queue_and_hosts = globvars.state_manager.pregame.queue \
                              | globvars.state_manager.pregame.hosts
            if ctx.author in queue_and_hosts:
                return await ctx.send('⛔ You cannot spectate and be in a game!')
        else:
            queue_and_hosts = globvars.state_manager.game.alive_players \
                              | globvars.state_manager.game.hosts
            if ctx.author in queue_and_hosts:
                return await ctx.send('⛔ You cannot spectate and be in a game!')

        if globvars.state_manager.state == State.ingame:
            globvars.state_manager.game.cannot_backup.add(ctx.author)

        spectator_role = globvars.client.get_guild(SERVER_ID).get_role(SPECTATOR_ROLE_ID)

        await ctx.author.add_roles(spectator_role)
        await ctx.send('✅ You are now a spectator!')

    @commands.command(
        name='unspectate',
        aliases=[
            'us'
        ]
    )
    async def unspectate(self, ctx):
        spectator_role = globvars.client.get_guild(SERVER_ID).get_role(SPECTATOR_ROLE_ID)

        if spectator_role not in ctx.author.roles:
            return await ctx.send('⛔ You are already not a spectator!')

        await ctx.author.remove_roles(spectator_role)
        await ctx.send('✅ You are no longer a spectator!')
