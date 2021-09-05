from discord.ext import commands

from mafia.data import roles


class Roles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='roles'
    )
    async def roles(self, ctx, filter: 'str' = ''):
        filter = filter.lower()

        messages = ["__Roles__:"]

        for role in roles.values():
            if not filter \
                or filter in role['power'].lower() \
                or filter in role['alignment'].lower():
                messages.append(f"`{role['name']}` - {role['alignment']}")

        message = ""
        for m in messages:
            if len(message) + len(m) > 2000:
                await ctx.send(message)
                message = ""
            message += m + '\n'

        await ctx.send(message)
