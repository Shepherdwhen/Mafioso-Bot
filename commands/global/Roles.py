from discord.ext import commands

from mafia.data import roles


class Roles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='roles',
        aliases=[
            'r'
        ]
    )
    async def roles(self, ctx, filter: 'str' = ''):
        filter = filter.lower()

        messages = ["__Roles__:"]

        for role in roles.values():
            if not filter \
                or role['power'].lower().startswith(filter) \
                or role['alignment'].lower().startswith(filter):
                messages.append(f"`{role['name']}` - {role['alignment']}")

        message = ""
        for m in messages:
            if len(message) + len(m) > 2000:
                await ctx.send(message)
                message = ""
            message += m + '\n'

        await ctx.send(message)
