import random
from functools import reduce
import sqlite3

import discord
from discord.ext import commands

import globvars
from mafia.State import State
from mafia.util import MemberConverter, check_if_is_host_or_admin

NUMBER_EMOJIS = {
    1:  '1️⃣',
    2:  '2️⃣',
    3:  '3️⃣',
    4:  '4️⃣',
    5:  '5️⃣',
    6:  '6️⃣',
    7:  '7️⃣',
    8:  '8️⃣',
    9:  '9️⃣',
    10: '🔟',
    11 :'🔴',
    12 :'🟠',
    13 :'🟡',
    14 :'🟢',
    15 :'🔵',
    16 :'🟥',
    17 :'🟧',
    18 :'🟨',
    19 :'🟩',
    20 :'🟦',
}

active_polls: 'dict[int, tuple[discord.Message, str, dict[str, str]], bool]' = dict()
poll_power: 'dict[discord.Member, int]' = dict()

class Poll(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        @bot.event
        async def on_reaction_add(reaction, member):
            if member.id == reaction.message.guild.me.id:
                return

            if reaction.message in [el[0] for el in active_polls.values()]:
                restrict_dead_votes = active_polls[[k for k, v in active_polls.items() if v[0].id == reaction.message.id][0]][3]
                if restrict_dead_votes:
                    if globvars.state_manager.state == State.ingame:
                        if member in globvars.state_manager.game.dead_players:
                            await reaction.message.remove_reaction(reaction, member)
                            return


                for r in reaction.message.reactions:
                    if r.emoji != reaction.emoji:
                        async for m in r.users():
                            if m.id == member.id:
                                await reaction.message.remove_reaction(r, member)

    @commands.group(
        name='poll'
    )
    @commands.check(check_if_is_host_or_admin)
    async def poll(self, ctx):
        pass

    @poll.command(
        name='create',
        aliases=[
            'new'
        ]
    )
    async def poll_create(self, ctx, prompt: str, *options):
        if len(options) < 1 or len(options) > len(NUMBER_EMOJIS.keys()):
            return await ctx.send(f'⛔ There is a maximum of twenty options and a minimum of one!')

        id = random.randint(0, 9999)
        while id in active_polls:
            id = random.randint(0, 9999)

        option_to_emoji = {}

        description_str = ""
        count = 0
        for option in options:
            count = count + 1
            description_str += f'{NUMBER_EMOJIS[count]} - {option}\n'
            option_to_emoji[option] = NUMBER_EMOJIS[count]

        embed = discord.Embed(
            title=prompt,
            description=description_str
        )

        embed.set_footer(text=f"Poll #{id}")

        msg = await ctx.send(embed=embed)

        active_polls[id] = (msg, prompt, option_to_emoji, False)

        for i in range(1, len(options) + 1):
            await msg.add_reaction(NUMBER_EMOJIS[i])

    @poll.command(
        name='ask'
    )
    async def poll_ask(self, ctx, *, question: 'str'):
        embed = discord.Embed(
            title=question,
            description='👍 - Yes\n👎 - No'
        )

        id = random.randint(0, 9999)
        while id in active_polls:
            id = random.randint(0, 9999)

        embed.set_footer(text=f"Poll #{id}")

        msg = await ctx.send(embed=embed)

        active_polls[id] = (msg, question, {'Yes': '👍', 'No': '👎'}, False)

        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

    @poll.command(
        name='alive'
    )
    async def poll_alive(self, ctx, *, question: 'str'):
        with sqlite3.connect('database.sqlite3') as connection:
            data = connection.execute("""
            SELECT user_id, emoji FROM player_data
            """)

            player_emojis = {item[0]: item[1] for item in data}

        if globvars.state_manager.state == State.pregame:
            players = globvars.state_manager.pregame.queue
        else:
            players = globvars.state_manager.game.alive_players

        if len(players) < 1:
            return await ctx.send('⛔ Cannot perform an alive poll with no alive players!')
        elif len(players) > 20:
            return await ctx.send('⛔ Cannot perform an alive poll with more than twenty alive players!')

        id = random.randint(0, 9999)
        while id in active_polls:
            id = random.randint(0, 9999)

        player_to_emoji = {}
        description_str = ""

        count = 0
        emojis = []

        for player in players:
            if player.id in player_emojis:
                emoji = player_emojis[player.id]
            else:
                count += 1
                emoji = NUMBER_EMOJIS[count]

            emojis.append(emoji)

            description_str += f"{emoji} - {player.mention}\n"
            player_to_emoji[player.mention] = emoji

        embed = discord.Embed(
            title=question,
            description=description_str
        )
        embed.set_footer(text=f"Poll #{id}")

        msg = await ctx.send(embed=embed)

        active_polls[id] = (msg, question, player_to_emoji, True)

        for emoji in emojis:
            await msg.add_reaction(emoji)

    @poll.command(
        name='end',
        aliases=[
            'stop'
        ]
    )
    async def poll_stop(self, ctx, id: 'int'):
        if id not in active_polls:
            return await ctx.send(f'⛔ Poll #{id} does not exist!')

        target_poll = active_polls[id]
        message = await target_poll[0].channel.fetch_message(target_poll[0].id) # Refetch message for up-to-date reaction counts

        summary = ''

        i = 0
        for (option, emoji) in target_poll[2].items():
            i = i + 1
            members = await discord.utils.find(lambda r: str(r.emoji).strip() == emoji, message.reactions).users().flatten()

            reactions = reduce(lambda count, user:
                count + (poll_power[user] if user in poll_power else 1)
            , members, 0)

            summary += f'{option} - {reactions - 1} vote{"s" if reactions - 2 else ""}\n' # Bot will add one vote to the actual numberd

        embed = discord.Embed(
            title=f"Poll results: {target_poll[1]}",
            description=summary
        )

        await ctx.send(embed=embed)
        del active_polls[id]

    @poll.command(
        name="power"
    )
    @commands.check(check_if_is_host_or_admin)
    async def poll_power(self, ctx, target: 'MemberConverter', power: 'int'):
        poll_power[target] = power
        await ctx.send(f'✅ Set **{target.display_name}**\'s voting power!')

