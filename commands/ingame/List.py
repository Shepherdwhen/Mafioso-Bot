"""Contains the list command
"""

import sqlite3

from discord.ext import commands

import globvars

TEMPLATE = """```
Hosts:
{hosts}

Alive Players:
{alive_players}

Dead Players:
{dead_players}
```"""

class List(commands.Cog):

    def __init__(self, bot):
        self.bot = bool

    @commands.command(
        name='list',
        aliases=['l', 'stats']
    )
    async def list(self, ctx):
        with sqlite3.connect('database.sqlite3') as connection:
            data = connection.execute("""
            SELECT user_id, nick, emoji FROM player_data
            """).fetchall()

        id_to_nick = {row[0]: row[1] for row in data if row[1]}
        id_to_emoji = {row[0]: row[2] for row in data if row[2]}


        hosts = globvars.state_manager.game.hosts
        hosts_str = ' - ' + ('\n - '.join(
            ((id_to_nick[p.id] if p.id in id_to_nick else p.display_name) + (' (' + id_to_emoji[p.id] + ')' if p.id in id_to_emoji else '')) \
            for p in hosts \
        ) if hosts else 'No host')

        alive_players = globvars.state_manager.game.alive_players
        alive_player_str = ' - ' + ('\n - '.join(
            ((id_to_nick[p.id] if p.id in id_to_nick else p.display_name) + (' (' + id_to_emoji[p.id] + ')' if p.id in id_to_emoji else '')) \
            for p in alive_players \
        ) if alive_players else 'No players')
        
        dead_players = globvars.state_manager.game.dead_players
        dead_player_str = ' - ' + ('\n - '.join(
            ((id_to_nick[p.id] if p.id in id_to_nick else p.display_name) + (' (' + id_to_emoji[p.id] + ')' if p.id in id_to_emoji else '')) \
            for p in dead_players \
        ) if dead_players else 'No players')

        await ctx.send(TEMPLATE.format(
            hosts=hosts_str,
            alive_players=alive_player_str,
            dead_players=dead_player_str
        ))