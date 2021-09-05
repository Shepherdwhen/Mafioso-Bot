import sqlite3

from discord.ext import commands
from emoji import UNICODE_EMOJI_ENGLISH


class Emoji(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name='emoji',
        invoke_without_command=True
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

    @emoji.command(
        name='clear'
    )
    async def nick_clear(self, ctx):
        with sqlite3.connect('database.sqlite3') as connection:
            connection.execute("""
            UPDATE player_data
                SET emoji = :emoji
                WHERE user_id = :id
            """, {
                'emoji': None,
                'id': ctx.author.id
            })
        await ctx.send(f'✅ Cleared **{ctx.author.display_name}**\'s nickname!')
