import sqlite3
from discord.ext import commands

import globvars
from mafia.errors import NotPlayer
from mafia.util import PlayerConverter, RoleConverter, check_if_is_host_or_admin


class Role(commands.Cog):

    def __init__(self, bot):
        self.bot  = bot

    @commands.group(
        name="role"
    )
    async def role(self, ctx):
        pass

    @role.command(
        name="set"
    )
    @commands.check(check_if_is_host_or_admin)
    async def role_set(self, ctx, target: PlayerConverter, *, role: RoleConverter):
        if target not in globvars.state_manager.game.players:
            raise NotPlayer()

        globvars.state_manager.game.roles[target] = role
        await ctx.send(f'✅ Set **{target.display_name}**\'s role!')

    @role.command(
        name='list'
    )
    @commands.check(check_if_is_host_or_admin)
    async def role_list(self, ctx):
        with sqlite3.connect('database.sqlite3') as connection:
            data = connection.execute("""
            SELECT user_id, nick, emoji FROM player_data
            """).fetchall()

        id_to_nick = {row[0]: row[1] for row in data if row[1]}
        id_to_emoji = {row[0]: row[2] for row in data if row[2]}

        players = globvars.state_manager.game.players
        roles = globvars.state_manager.game.roles

        role_str = ' - ' + ('\n - '.join(
            ((id_to_nick[p.id] if p.id in id_to_nick else p.display_name) + (' (' + id_to_emoji[p.id] + ')' if p.id in id_to_emoji else '') + ' : ' + (roles[p]['name'] if p in roles else 'No role')) \
            for p in players \
        ) if players else 'No players')

        await ctx.send(f'```{role_str}```')

