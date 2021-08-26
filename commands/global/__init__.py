from .Info import Info
from .Ping import Ping


def setup(bot):
    bot.add_cog(Ping(bot))
    bot.add_cog(Info(bot))
