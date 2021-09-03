import sqlite3

from discord.ext import commands

import globvars
from mafia.util import check_if_is_host_or_admin


class Export(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='export',
        aliases=[
            'sheet'
        ]
    )
    @commands.check(check_if_is_host_or_admin)
    async def export(self, ctx):
        with sqlite3.connect('database.sqlite3') as connection:
            data = connection.execute("""
            SELECT user_id, nick FROM player_data
            """).fetchall()

        id_to_nick = {row[0]: row[1] for row in data if row[1]}

        string = ''
        for player in globvars.state_manager.game.players:
            string += f'=SPLIT("{id_to_nick[player.id] if player.id in id_to_nick else player.display_name},{player.id}", ",")\n'

        await ctx.send(f"```{string}```")
