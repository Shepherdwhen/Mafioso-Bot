from discord.ext import commands
from discord.permissions import PermissionOverwrite
from config import DEAD_ROLE_ID, SERVER_ID, SPECTATOR_ROLE_ID

import globvars
from mafia.State import State
from mafia.util import check_if_is_host_or_admin

class ChannelVis(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='channelvis',
        aliases=[
            'cv',
            'channel_vis'
        ]
    )
    @commands.check(check_if_is_host_or_admin)
    async def channel_vis(self, ctx, arg: bool):
        globvars.private_channel_vis = arg

        if globvars.state_manager.state == State.ingame:

            guild = globvars.client.get_guild(SERVER_ID)

            dead_role = guild.get_role(DEAD_ROLE_ID)
            spectator_role = guild.get_role(SPECTATOR_ROLE_ID)

            for channel in globvars.state_manager.game.managed_channels:
                await channel.set_permissions(dead_role, overwrite=PermissionOverwrite(read_messages=arg))
                await channel.set_permissions(spectator_role, overwrite=PermissionOverwrite(read_messages=arg))


        await ctx.send('✅ Updated private channel visibility')
