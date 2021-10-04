from .Info import Info
from .Nick import Nick
from .Ping import Ping
from .Poll import Poll
from .Promote import Promote
from .Roles import Roles
from .Spectate import Spectate
from .ChannelVis import ChannelVis


def setup(bot):
    bot.add_cog(Ping(bot))
    bot.add_cog(Info(bot))
    bot.add_cog(Poll(bot))
    bot.add_cog(Spectate(bot))
    bot.add_cog(Nick(bot))
    bot.add_cog(Promote(bot))
    bot.add_cog(Roles(bot))
    bot.add_cog(ChannelVis(bot))
