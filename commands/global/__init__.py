from .Info import Info
from .Ping import Ping
from .Poll import Poll
from .Spectate import Spectate
from .Nick import Nick
from .Promote import Promote


def setup(bot):
    bot.add_cog(Ping(bot))
    bot.add_cog(Info(bot))
    bot.add_cog(Poll(bot))
    bot.add_cog(Spectate(bot))
    bot.add_cog(Nick(bot))
    bot.add_cog(Promote(bot))
