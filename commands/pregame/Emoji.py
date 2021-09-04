import sqlite3

from discord.ext import commands
from emoji import UNICODE_EMOJI_ENGLISH


class Emoji(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='emoji'
    )
    async def emoji(self, ctx, emoji: 'str'):
        emoji = emoji.strip()

        has_variation_selector = False
        if emoji.endswith(u'\U0000FE0F'):
            has_variation_selector = True
            emoji = emoji[:-1] # Strip variation selector


        if emoji not in UNICODE_EMOJI_ENGLISH:
            raise commands.BadArgument()

        with sqlite3.connect('database.sqlite3') as connection:
            connection.execute("""
            REPLACE INTO
                player_data (user_id, emoji, nick)
                VALUES (
                    :id,
                    :emoji,
                    (SELECT nick FROM player_data WHERE user_id=:id)
                )
            """, {
                'id': ctx.author.id,
                'emoji': emoji + (u'\U0000FE0F' if has_variation_selector else '')
            })
        
        await ctx.send('✅ Set your emoji!')
