from discord.ext import commands
from discord.ext.commands.converter import TextChannelConverter
from discord.permissions import PermissionOverwrite

import globvars
from mafia.util import PlayerConverter, check_if_is_host

class Channel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name='channel'
    )
    async def channel(self, ctx):
        pass

    @channel.command(
        name='add'
    )
    @commands.check(check_if_is_host)
    async def channel_add(self, ctx, channel: 'TextChannelConverter', player: 'PlayerConverter'):
        if channel in globvars.state_manager.game.managed_channels:
            await channel.set_permissions(player, overwrite=PermissionOverwrite(read_messages=True))

            await ctx.send(f'✅ Added **{player.display_name}** to channel!')
        else:
            await ctx.send(f'⛔ Channel is not a game channel.')

    @channel.command(
        name='remove',
        aliases=[
            'rm'
        ]
    )
    @commands.check(check_if_is_host)
    async def channel_remove(self, ctx, channel: TextChannelConverter, player: PlayerConverter):
        if channel in globvars.state_manager.game.managed_channels:
            await channel.set_permissions(player, overwrite=PermissionOverwrite(read_messages=False))

            await ctx.send(f'✅ Removed **{player.display_name}** from channel!')
        else:
            await ctx.send(f'⛔ Channel is not a game channel.')
