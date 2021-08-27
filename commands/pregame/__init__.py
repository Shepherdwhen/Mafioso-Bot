from .Emoji import Emoji
from .Host import Host
from .Join import Join
from .List import List
from .Start import Start


def setup(bot):
    bot.add_cog(Join(bot))
    bot.add_cog(Host(bot))
    bot.add_cog(List(bot))
    bot.add_cog(Start(bot))
    bot.add_cog(Emoji(bot))
