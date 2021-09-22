from discord.ext import commands
from discord.permissions import PermissionOverwrite

import globvars
from config import ALIVE_ROLE_ID, DEAD_ROLE_ID, SERVER_ID
from mafia.errors import CannotBackup
from mafia.util import MemberConverter, PlayerConverter, check_if_is_host


class Backup(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='backup',
        aliases=[
            'substitute',
            'sub',
            'swap'
        ]
    )
    @commands.check(check_if_is_host)
    async def backup(self, ctx, target: 'PlayerConverter', swap: 'MemberConverter'):
        if swap in globvars.state_manager.game.cannot_backup \
        or swap in globvars.state_manager.game.players \
        or swap in globvars.state_manager.game.hosts:
            raise CannotBackup()

        game = globvars.state_manager.game
        guild = globvars.client.get_guild(SERVER_ID)

        fetched_target = guild.get_member(target.id)

        # Swap player state

        if target in game.alive_players:
            alive_role = guild.get_role(ALIVE_ROLE_ID)

            game.alive_players.remove(target)
            if fetched_target:
                await target.remove_roles(alive_role)
            
            game.alive_players.add(swap)
            await swap.add_roles(alive_role)
        elif target in game.dead_players:
            dead_role = guild.get_role(DEAD_ROLE_ID)

            game.dead_players.remove(target)
            if fetched_target:
                await target.remove_roles(dead_role)
            
            game.dead_players.add(swap)
            await swap.add_roles(dead_role)
        if target in game.kill_queue:
            game.kill_queue.remove(target)
            game.kill_queue.add(swap)

        # Swap roles

        game.roles[swap] = game.roles[target]
        del game.roles[target]

        # Swap channels

        game.player_to_private_channel[swap] = game.player_to_private_channel[target]
        del game.player_to_private_channel[target]

        channel = game.player_to_private_channel[swap]


        if fetched_target:
            await channel.set_permissions(target, overwrite=None)
        await channel.set_permissions(swap, overwrite=PermissionOverwrite(read_messages=True))

        if target in game.player_to_multi_channels:
            game.player_to_multi_channels[swap] = game.player_to_multi_channels[target]
            del game.player_to_multi_channels[target]

            for channel in game.player_to_multi_channels[swap]:
                if fetched_target:
                    await channel.set_permissions(target, overwrite=None)
                await channel.set_permissions(swap, overwrite=PermissionOverwrite(read_messages=True))

        # Prevent player from acting as backup
        game.cannot_backup.add(target)

        await ctx.send(f'✅ Swapped **{target.display_name}** with **{swap.display_name}**')

        game._push_to_db()
