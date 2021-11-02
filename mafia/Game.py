import asyncio
import sqlite3

import discord
from discord import PermissionOverwrite
from discord.errors import NotFound

import globvars
from config import (ALIVE_ROLE_ID, DEAD_ROLE_ID, HOST_ROLE_ID,
                    MAIN_CATEGORY_ID, MOD_ROLE_ID, SERVER_ID,
                    SPECTATOR_ROLE_ID)

from .data import Role, channels, roles
from .errors import MafiaException, NoRoles


class Game:
    """Represents the game state of the bot
    Keeps track of players, hosts, channels and roles
    """

    def __init__(self, hosts, players):
        self.hosts: 'set[discord.Member]' = hosts
        self.alive_players: 'set[discord.Member]' = players
        self.dead_players: 'set[discord.Member]' = set()

        self.roles: 'dict[discord.Member, Role]' = dict()

        self.kill_queue: 'set[discord.Member]' = set()

        self.managed_channels: 'set[discord.TextChannel]' = set()
        self.player_to_private_channel: 'dict[discord.Member, discord.TextChannel]' = dict()
        self.player_to_multi_channels: 'dict[discord.Member, set[discord.TextChannel]]' = dict()
        self.main_category: 'discord.CategoryChannel' = globvars.client.get_guild(SERVER_ID).get_channel(MAIN_CATEGORY_ID)

        # Players who have been spectators are not eligible to be backups
        # so we keep track of who has spectated this game
        # Also contains players who left the game after a back up
        self.cannot_backup: 'set[discord.Member]' = set()

        asyncio.create_task(self._init_from_db())

    async def _init_from_db(self):
        with sqlite3.connect('database.sqlite3') as connection:
            res = connection.execute("""
            SELECT key, value FROM data
            """)

            data = {key: value for (key, value) in res}

        guild = globvars.client.get_guild(SERVER_ID)

        for id in data.get('game.hosts', '').split(','):
            if id:
                self.hosts.add(await guild.fetch_member(id))

        for id in data.get('game.alive_players', '').split(','):
            if id:
                self.alive_players.add(await guild.fetch_member(id))

        for id in data.get('game.dead_players', '').split(','):
            if id:
                self.dead_players.add(await guild.fetch_member(id))

        for (id, role) in map(lambda s: s.split(':'), data.get('game.roles', ':').split(',')):
            if id:
                self.roles[await guild.fetch_member(id)] = roles[role]

        for id in data.get('game.kill_queue', '').split(','):
            if id:
                self.kill_queue.add(await guild.fetch_member(id))

        for (member_id, channel_id) in map(lambda s: s.split(':'), data.get('game.private_channels', ':').split(',')):
            if member_id:
                self.player_to_private_channel[await guild.fetch_member(member_id)] = await globvars.client.fetch_channel(channel_id)

        for ch_data in data.get('game.multi_channels', '').split(','):
            member_split = ch_data.split(':')
            member_id = member_split[0]

            if member_id:
                channel_ids = member_split[1].split(';')

                channels = [await globvars.client.fetch_channel(channel_id) for channel_id in channel_ids]
                self.player_to_multi_channels[await guild.fetch_member(member_id)] = set(channels)
        
        for channel in self.player_to_private_channel.values():
            self.managed_channels.add(channel)
        for channels in self.player_to_multi_channels.values():
            for channel in channels:
                self.managed_channels.add(channel)

        for id in data.get('game.cannot_backup', '').split(','):
            if id:
                self.cannot_backup.add(await guild.fetch_member(id))

        self._push_to_db()

    def _push_to_db(self):
        with sqlite3.connect('database.sqlite3') as connection:
            connection.execute("""
            INSERT OR REPLACE
                INTO data (key, value)
                VALUES (:key, :value)
            """, {
                'key': 'game.hosts',
                'value': ','.join([str(m.id) for m in self.hosts])
            })

            connection.execute("""
            INSERT OR REPLACE
                INTO data (key, value)
                VALUES (:key, :value)
            """, {
                'key': 'game.alive_players',
                'value': ','.join([str(m.id) for m in self.alive_players])
            })

            connection.execute("""
            INSERT OR REPLACE
                INTO data (key, value)
                VALUES (:key, :value)
            """, {
                'key': 'game.dead_players',
                'value': ','.join([str(m.id) for m in self.dead_players])
            })

            roles_as_id = {str(m.id): self.roles[m]['id'] for m in self.roles}
            roles_string = [f"{m}:{roles_as_id[m]}" for m in roles_as_id]

            connection.execute("""
            INSERT OR REPLACE
                INTO data (key, value)
                VALUES (:key, :value)
            """, {
                'key': 'game.roles',
                'value': ','.join(roles_string)
            })

            connection.execute("""
            INSERT OR REPLACE
                INTO data (key, value)
                VALUES (:key, :value)
            """, {
                'key': 'game.kill_queue',
                'value': ','.join([str(m.id) for m in self.kill_queue])
            })

            private_channels_as_id = {m.id: self.player_to_private_channel[m].id for m in self.player_to_private_channel}
            private_channels_string = [f"{m}:{private_channels_as_id[m]}" for m in private_channels_as_id]

            connection.execute("""
            INSERT OR REPLACE
                INTO data (key, value)
                VALUES (:key, :value)
            """, {
                'key': 'game.private_channels',
                'value': ','.join(private_channels_string)
            })

            multi_channels_as_id = {m.id: [str(c.id) for c in self.player_to_multi_channels[m]] for m in self.player_to_multi_channels}
            multi_channels_string = [f"{m}:{';'.join(multi_channels_as_id[m])}" for m in multi_channels_as_id]

            connection.execute("""
            INSERT OR REPLACE
                INTO data (key, value)
                VALUES (:key, :value)
            """, {
                'key': 'game.multi_channels',
                'value': ','.join(multi_channels_string)
            })

            connection.execute("""
            INSERT OR REPLACE
                INTO data (key, value)
                VALUES (:key, :value)
            """, {
                'key': 'game.cannot_backup',
                'value': ','.join([str(m.id) for m in self.cannot_backup])
            })

    @property
    def players(self) -> 'set[discord.Member]':
        return self.alive_players | self.dead_players

    async def start(self):
        """Starts the game
        - Gives all required roles
        - Creates all needed channels
        """

        players_without_role = self.alive_players - set(self.roles.keys())
        if players_without_role:
            raise NoRoles(*players_without_role)

        # Spectators can join during pregame, load all current spectators
        # TODO: Issue with members intent?
        spectator_role = globvars.client.get_guild(SERVER_ID).get_role(SPECTATOR_ROLE_ID)
        self.cannot_backup = set(spectator_role.members)

        await self.give_init_roles()
        await self.create_channels()
        await self.send_role_messages()

        self._push_to_db()

    async def clean_up(self):
        for channel in self.managed_channels.copy():
            try:
                await channel.delete()
            except NotFound:
                pass # Channel already deleted
            finally:
                self.managed_channels.remove(channel)
        self.player_to_private_channel.clear()

        guild = globvars.client.get_guild(SERVER_ID)

        host_role = guild.get_role(HOST_ROLE_ID)
        for host in self.hosts:
            await host.remove_roles(host_role)

        alive_role = guild.get_role(ALIVE_ROLE_ID)
        dead_role = guild.get_role(DEAD_ROLE_ID)
        for player in self.players:
            await player.remove_roles(alive_role, dead_role)
        
        self._push_to_db()

    async def give_init_roles(self):
        """Give the initial roles to the players on game start
        """
        
        guild = globvars.client.get_guild(SERVER_ID)
        spectator_role = guild.get_role(SPECTATOR_ROLE_ID)

        host_role = guild.get_role(HOST_ROLE_ID)
        for host in self.hosts:
            await host.add_roles(host_role)
            await host.remove_roles(spectator_role)

        alive_role = guild.get_role(ALIVE_ROLE_ID)
        for player in self.alive_players: # All players will be alive initially
            await player.add_roles(alive_role)
            await player.remove_roles(spectator_role)

    async def create_channels(self):
        """Create all the channels with the needed permissions
        """

        guild = globvars.client.get_guild(SERVER_ID)
        target_category = self.main_category

        host_role = guild.get_role(HOST_ROLE_ID)
        spectator_role = guild.get_role(SPECTATOR_ROLE_ID)
        mod_role = guild.get_role(MOD_ROLE_ID)
        dead_role = guild.get_role(DEAD_ROLE_ID)

        async def create_individual_channel(channel, member, *, send_description=True):
            created_channel = await guild.create_text_channel(
                name=channel['name'],
                category=target_category,
                overwrites={
                    guild.default_role: PermissionOverwrite(read_messages=False),
                    spectator_role: PermissionOverwrite(read_messages=globvars.private_channel_vis, send_messages=False),
                    dead_role: PermissionOverwrite(read_messages=globvars.private_channel_vis, send_messages=False),

                    # Dead players talking in their private channels isnt a big
                    # deal and it may be enforced by category inheritance anyways,
                    # so don't bother restricting dead players from talking

                    guild.me: PermissionOverwrite(read_messages=True),
                    host_role: PermissionOverwrite(read_messages=True),
                    mod_role: PermissionOverwrite(read_messages=True, send_messages=True),
                    member: PermissionOverwrite(read_messages=True)
                }
            )

            self.managed_channels.add(created_channel)
            self.player_to_private_channel[member] = created_channel

            if send_description:
                description = '\n'.join(self.roles[member]['description'])

                msg = await created_channel.send(f"`{self.roles[member]['name']}`\n\n{description}")
                await msg.pin()

        async def create_multi_channel(channel, members):
            dead_role = guild.get_role(DEAD_ROLE_ID)

            overwrites = {member: PermissionOverwrite(read_messages=True) for member in members}
            overwrites[guild.default_role] = PermissionOverwrite(read_messages=False)
            overwrites[spectator_role] =  PermissionOverwrite(read_messages=globvars.private_channel_vis, send_messages=False)
            overwrites[guild.me] = PermissionOverwrite(read_messages=True)
            overwrites[host_role] = PermissionOverwrite(read_messages=True)
            overwrites[dead_role] = PermissionOverwrite(read_messages=globvars.private_channel_vis, send_messages=False)
            overwrites[mod_role] = PermissionOverwrite(read_messages=True, send_messages=True)

            created_channel = await guild.create_text_channel(
                name=channel['name'].format(
                    num_players=len(members)
                ),
                category=target_category,
                overwrites=overwrites
            )

            self.managed_channels.add(created_channel)
            for member in members:
                if member not in self.player_to_multi_channels:
                    self.player_to_multi_channels[member] = set()
                self.player_to_multi_channels[member].add(created_channel)

            if 'start_message' in channel and channel['start_message']:
                await created_channel.send(channel['start_message'].format(
                    num_players=len(members)
                ))

        for channel in channels.values():
            if channel['type'] == 'multi':
                members = []
                for player in self.players:
                    if self.roles[player]['id'] in channel['members']:
                        members.append(player)

                if members:
                    await create_multi_channel(channel, members)
            elif channel['type'] == 'single':
                players = []
                for player in self.players:
                    if self.roles[player]['id'] in channel['members']:
                        players.append(player)

                for player in players:
                    await create_multi_channel({
                        'name': channel['name']
                    }, [player])

            else:
                raise MafiaException(f"Channels must be of type 'multi' or 'single', not {channel['type']!r}")

        for player in self.players:
            await create_individual_channel({
                'name': self.roles[player]['name']
            }, player, send_description=True)

        self._push_to_db()

    async def send_role_messages(self):
        for player in self.players:
            try:
                await player.send(f"""
    Your role for this upcoming game is:

    `{self.roles[player]['name']}`

    Please do not copy or screenshot this message.
                """)
            except discord.Forbidden:
                pass # User blocked
