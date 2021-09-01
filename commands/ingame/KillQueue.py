import sqlite3

from discord.ext import commands

import globvars
from config import ALIVE_ROLE_ID, DEAD_ROLE_ID, SERVER_ID
from mafia.util import PlayerConverter, check_if_is_host


class KillQueue(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name='killqueue',
        aliases=[
            'kill_queue',
            'killq',
            'kq'
        ]
    )
    @commands.check(check_if_is_host)
    async def killqueue(self, ctx):
        if ctx.invoked_subcommand is None:
            with sqlite3.connect('database.sqlite3') as connection:
                data = connection.execute("""
                SELECT user_id, nick FROM player_data
                """).fetchall()

            id_to_nick = {row[0]: row[1] for row in data if row[1]}

            # Send current kill queue
            game = globvars.state_manager.game

            formatted = ' - ' + ('\n - '.join([(id_to_nick[p.id] if p.id in id_to_nick else p.display_name) for p in game.kill_queue]) if game.kill_queue else 'Queue empty')
            await ctx.send(f"""```
Current Kill queue:

{formatted}
            ```""")

    @killqueue.command(
        name='add',
        aliases=[
            'a',
            '+'
        ]
    )
    async def killqueue_add(self, ctx, targets: 'commands.Greedy[PlayerConverter]'):
        current_killqueue = globvars.state_manager.game.kill_queue

        for target in targets:
            if target in current_killqueue:
                await ctx.send(f'⛔ **{target.display_name}** is already in the kill queue!')
            else:
                current_killqueue.add(target)
                await ctx.send(f'✅ **{target.display_name}** added to the kill queue!')

    @killqueue.command(
        name='remove',
        aliases=[
            'r',
            '-',
            'rm'
        ]
    )
    async def killqueue_remove(self, ctx, targets: 'commands.Greedy[PlayerConverter]'):
        current_killqueue = globvars.state_manager.game.kill_queue

        for target in targets:
            if target not in current_killqueue:
                await ctx.send(f'⛔ **{target.display_name}** is already not in the kill queue!')
            else:
                current_killqueue.remove(target)
                await ctx.send(f'✅ **{target.display_name}** removed from the kill queue!')

    @killqueue.command(
        name='exec',
        aliases=[
            'e'
        ]
    )
    async def killqueue_exec(self, ctx):
        guild = globvars.client.get_guild(SERVER_ID)

        alive_role = guild.get_role(ALIVE_ROLE_ID)
        dead_role = guild.get_role(DEAD_ROLE_ID)

        for player in globvars.state_manager.game.kill_queue:
            if alive_role in player.roles:
                await player.remove_roles(alive_role)
            if dead_role not in player.roles:
                await player.add_roles(dead_role)

            if player in globvars.state_manager.game.alive_players:
                globvars.state_manager.game.alive_players.remove(player)
            if player not in globvars.state_manager.game.dead_players:
                globvars.state_manager.game.dead_players.add(player)

        globvars.state_manager.game.kill_queue.clear()

        await ctx.send(f'✅ Kill queue executed')

    @killqueue.command(
        name='clear',
        aliases=[
            'reset'
        ]
    )
    async def killqueue_clear(self, ctx):
        globvars.state_manager.game.kill_queue.clear()
        await ctx.send('✅ Cleared kill queue!')

    @commands.command(
        name='kill'
    )
    @commands.check(check_if_is_host)
    async def kill(self, ctx, targets: 'commands.Greedy[PlayerConverter]'):
        guild = globvars.client.get_guild(SERVER_ID)

        alive_role = guild.get_role(ALIVE_ROLE_ID)
        dead_role = guild.get_role(DEAD_ROLE_ID)

        for player in targets:
            if alive_role in player.roles:
                await player.remove_roles(alive_role)
            if dead_role not in player.roles:
                await player.add_roles(dead_role)

            if player in globvars.state_manager.game.alive_players:
                globvars.state_manager.game.alive_players.remove(player)
            if player not in globvars.state_manager.game.dead_players:
                globvars.state_manager.game.dead_players.add(player)

        await ctx.send(f'✅ Killed player{"s" if len(targets) != 1 else ""}!')

    @commands.command(
        name='revive',
        aliases=[
            'rv'
        ]
    )
    @commands.check(check_if_is_host)
    async def revive(self, ctx, targets: 'commands.Greedy[PlayerConverter]'):
        guild = globvars.client.get_guild(SERVER_ID)

        alive_role = guild.get_role(ALIVE_ROLE_ID)
        dead_role = guild.get_role(DEAD_ROLE_ID)

        for player in targets:
            if alive_role not in player.roles:
                await player.add_roles(alive_role)
            if dead_role in player.roles:
                await player.remove_roles(dead_role)

            if player not in globvars.state_manager.game.alive_players:
                globvars.state_manager.game.alive_players.add(player)
            if player in globvars.state_manager.game.dead_players:
                globvars.state_manager.game.dead_players.remove(player)

        await ctx.send(f'✅ Revived player{"s" if len(targets) != 1 else ""}!')
