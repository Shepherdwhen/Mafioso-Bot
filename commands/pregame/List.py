"""Contains the list command
"""

from discord.ext import commands

import globvars

TEMPLATE = """```
Host:
{hosts}

Players:
{players}
```"""

class List(commands.Cog):

    def __init__(self, bot):
        self.bot = bool

    @commands.command(
        name='list',
        aliases=['l', 'stats']
    )
    async def list(self, ctx):
        hosts = globvars.state_manager.pregame.hosts
        hosts_str = ' - ' + ('\n - '.join(p.display_name for p in hosts) if hosts else 'No host')

        players = globvars.state_manager.pregame.queue
        player_str = ' - ' + ('\n - '.join(p.display_name for p in players) if players else 'No players')

        await ctx.send(TEMPLATE.format(
            hosts=hosts_str,
            players=player_str
        ))