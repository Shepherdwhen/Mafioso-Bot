import sqlite3
import discord
from discord.ext import commands
from mafia.util import PlayerConverter, check_if_is_host, check_if_is_player
import globvars
import math

whisper_ratelimit: dict[discord.Member, int] = dict()
max_whispers = math.inf

class Whisper(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name='whisper',
        aliases=[
            'w'
        ]
    )
    async def whisper(self, ctx):
        pass

    @whisper.command(
        name='send'
    )
    @commands.check(check_if_is_player)
    async def whisper_send(self, ctx, target: PlayerConverter, *, message: str):
        with sqlite3.connect('database.sqlite3') as connection:
            nick = connection.execute("""
            SELECT nick, user_id FROM player_data WHERE user_id = :id
            """, {
                'id': ctx.author.id
            }).fetchone()

        if ctx.author not in whisper_ratelimit:
            whisper_ratelimit[ctx.author] = 0
        whisper_ratelimit[ctx.author] += 1

        if whisper_ratelimit[ctx.author] > max_whispers:
            return await ctx.send('⛔ You have sent the maximum amount of whispers!')

        channel = globvars.state_manager.game.player_to_private_channel[target]

        await channel.send(f'From **{nick[0] if nick else ctx.author.display_name}**: {message}')
        await ctx.send('✅ Whisper sent!')

    @whisper.command(
        name='set',
        aliases=[
            'setmax'
        ]
    )
    @commands.check(check_if_is_host)
    async def whisper_max(self, ctx, max: int):
        global max_whispers
        max_whispers = max
        await ctx.send('✅ Set maximum whispers per day!')

    @whisper.command(
        name='clear',
        aliases=[
            'reset'
        ]
    )
    @commands.check(check_if_is_host)
    async def whisper_clear(self, ctx):
        global whisper_ratelimit
        whisper_ratelimit.clear()
        await ctx.send('✅ Cleared whisper limit!')
