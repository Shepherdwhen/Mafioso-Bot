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

            connection.execute("""
            CREATE TABLE IF NOT EXISTS data (
                key   TEXT PRIMARY KEY NOT NULL,
                value TEXT
            )
            """)

            res = connection.execute("""
            SELECT key, value FROM data
            """)

            data = {key: value for (key, value) in res}

        state = data.get('state', 'pregame')

        if state == 'pregame':
            state_manager.init_pregame()
        else:
            state_manager.init_game()
