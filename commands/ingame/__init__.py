from .Init import Init
from .Role import Role


def setup(bot):
    bot.add_cog(Role(bot))
    bot.add_cog(Init(bot))
