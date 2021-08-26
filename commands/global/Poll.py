from discord.ext import commands
import discord

from mafia.util import check_if_is_host_or_admin

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

active_polls: dict[int, tuple[discord.Message, str, list[str]]] = dict()

class Poll(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        @bot.event
        async def on_reaction_add(reaction, member):
            if member.id == reaction.message.guild.me.id:
                return

            if reaction.message in [el[0] for el in active_polls.values()]:
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

        id = 1
        while id in active_polls:
            id = id + 1

        description_str = ""
        count = 0
        for option in options:
            count = count + 1
            description_str += f'{NUMBER_EMOJIS[count]} - {option}\n'

        embed = discord.Embed(
            title=prompt,
            description=description_str
        )

        embed.set_footer(text=f"Poll #{id}")

        msg = await ctx.send(embed=embed)

        active_polls[id] = (msg, prompt, options)

        for i in range(1, len(options) + 1):
            await msg.add_reaction(NUMBER_EMOJIS[i])

    @poll.command(
        name='end',
        aliases=[
            'stop'
        ]
    )
    async def poll_stop(self, ctx, id: int):
        if id not in active_polls:
            return await ctx.send(f'⛔ Poll #{id} does not exist!')

        target_poll = active_polls[id]
        message = await target_poll[0].channel.fetch_message(target_poll[0].id) # Refetch message for up-to-date reaction counts

        summary = ''

        i = 0
        for option in target_poll[2]:
            i = i + 1
            # reactions = discord.utils.get(target_poll[0].reactions, emoji=NUMBER_EMOJIS[i]).count
            reactions = discord.utils.find(lambda r: str(r.emoji).strip() == NUMBER_EMOJIS[i], message.reactions).count

            summary += f'{option} - {reactions - 1} vote{"s" if reactions - 2 else ""}\n' # Bot will add one vote to the actual numberd

        embed = discord.Embed(
            title=f"Poll results: {target_poll[1]}",
            description=summary
        )

        await ctx.send(embed=embed)
        del active_polls[id]

