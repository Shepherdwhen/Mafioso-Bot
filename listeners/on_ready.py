import sqlite3

from discord.ext import commands

import globvars


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

            connection.execute("""
            CREATE TABLE IF NOT EXISTS polls (
                id            TEXT    PRIMARY KEY NOT NULL,
                channel_id    INTEGER             NOT NULL,
                message_id    INTEGER             NOT NULL,
                prompt        TEXT                NOT NULL,
                options_map   TEXT                NOT NULL,
                restrict_dead INTEGER             NOT NULL
            )
            """)

            connection.execute("""
            CREATE TABLE IF NOT EXISTS poll_power (
                id    INTEGER PRIMARY KEY NOT NULL,
                power INTEGER             NOT NULL
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
        
        globvars.client.load_extension('commands.global')
