from .Init import Init
from .Role import Role
from .End import End

def setup(bot):
    bot.add_cog(Role(bot))
    bot.add_cog(Init(bot))
    bot.add_cog(End(bot))
