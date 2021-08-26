from .Init import Init
from .Role import Role
from .End import End
from .KillQueue import KillQueue

def setup(bot):
    bot.add_cog(Role(bot))
    bot.add_cog(Init(bot))
    bot.add_cog(End(bot))
    bot.add_cog(KillQueue(bot))
