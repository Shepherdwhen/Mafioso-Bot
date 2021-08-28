import sqlite3

from discord.ext import commands
from emoji import UNICODE_EMOJI_ENGLISH

class Emoji(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='emoji'
    )
    async def emoji(self, ctx, emoji: str):
        if emoji.strip() not in UNICODE_EMOJI_ENGLISH:
            raise commands.BadArgument()

        with sqlite3.connect('database.sqlite3') as connection:
            connection.execute("""
            REPLACE INTO
                player_data (user_id, emoji)
                VALUES (
                    :id,
                    :emoji
                )
            """, {
                'id': ctx.author.id,
                'emoji': emoji.strip()
            })
        
        await ctx.send('✅ Set your emoji!')
