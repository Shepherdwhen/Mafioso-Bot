import sqlite3
import discord
from discord.ext import commands

from mafia.util import MemberConverter, check_if_is_host_or_admin

class Nick(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='nick'
    )
    @commands.check(check_if_is_host_or_admin)
    async def nick(self, ctx, target: MemberConverter, *, nick: str):
        with sqlite3.connect('database.sqlite3') as connection:
            connection.execute("""
            REPLACE INTO
                player_data (user_id, nick, emoji)
                VALUES (
                    :id,
                    :nick,
                    (SELECT emoji FROM player_data WHERE user_id=:id)
                )
            """, {
                'id': target.id,
                'nick': nick.strip()
            })
        await ctx.send(f'✅ Set **{target.display_name}**\'s nickname!')
        try:
            target.edit(nick=nick.strip())
        except discord.Forbidden:
            pass
