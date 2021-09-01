from discord.ext import commands

from mafia.util import RoleConverter

TEMPLATE = """
**{name}** | {alignment} {power}

{description}
"""

class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='info',
        aliases=[
            'i'
        ]
    )
    async def info(self, ctx, role: 'RoleConverter'):
        description_str = '\n'.join(role['description'])

        await ctx.send(TEMPLATE.format(
            name=role['name'],
            alignment=role['alignment'],
            power=role['power'],
            description=description_str
        ))
