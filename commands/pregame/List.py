"""Contains the list command
"""

from discord.ext import commands

import globvars

TEMPLATE = """```
Host:
 - {host}

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
        host = globvars.state_manager.pregame.host
        host_str = host.display_name if host else 'No host'

        players = globvars.state_manager.pregame.queue
        player_str = ' - ' + ('\n - '.join(p.display_name for p in players) if players else 'No players')

        await ctx.send(TEMPLATE.format(
            host=host_str,
            players=player_str
        ))