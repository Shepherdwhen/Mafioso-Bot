import sqlite3

from discord.ext import commands


class on_ready(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        from globvars import client, state_manager
        
        print(f"Logged in as {client.user.name}#{client.user.discriminator}")

        with sqlite3.connect('database.sqlite3') as connection:
            connection.execute("""
            CREATE TABLE IF NOT EXISTS player_data (
                user_id INTEGER PRIMARY KEY NOT NULL,
                nick    TEXT,
                emoji   TEXT
            )
            """)

        state_manager.init_pregame()
