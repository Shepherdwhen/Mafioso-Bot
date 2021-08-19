from .Host import Host
from .Join import Join
from .List import List


def setup(bot):
    bot.add_cog(Join(bot))
    bot.add_cog(Host(bot))
    bot.add_cog(List(bot))