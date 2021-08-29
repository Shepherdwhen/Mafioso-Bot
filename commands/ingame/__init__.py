from .End import End
from .Init import Init
from .KillQueue import KillQueue
from .Role import Role
from .List import List
from .Whisper import Whisper
from .Backup import Backup

def setup(bot):
    bot.add_cog(Role(bot))
    bot.add_cog(Init(bot))
    bot.add_cog(End(bot))
    bot.add_cog(KillQueue(bot))
    bot.add_cog(List(bot))
    bot.add_cog(Whisper(bot))
    bot.add_cog(Backup(bot))
