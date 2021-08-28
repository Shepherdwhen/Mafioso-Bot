import sqlite3
from discord.ext import commands
from mafia.util import PlayerConverter, check_if_is_player
import globvars

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

        channel = globvars.state_manager.game.player_to_private_channel[target]

        await channel.send(f'From **{nick[0] if nick else ctx.author.display_name}**: {message}')
        await ctx.send('✅ Whisper sent!')
