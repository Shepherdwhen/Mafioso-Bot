from .Info import Info
from .Ping import Ping
from .Poll import Poll


def setup(bot):
    bot.add_cog(Ping(bot))
    bot.add_cog(Info(bot))
    bot.add_cog(Poll(bot))
