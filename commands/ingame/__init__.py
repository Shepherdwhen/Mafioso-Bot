from .Backup import Backup
from .End import End
from .Export import Export
from .Init import Init
from .KillQueue import KillQueue
from .List import List
from .Role import Role
from .Whisper import Whisper
from .Channel import Channel


def setup(bot):
    bot.add_cog(Role(bot))
    bot.add_cog(Init(bot))
    bot.add_cog(End(bot))
    bot.add_cog(KillQueue(bot))
    bot.add_cog(List(bot))
    bot.add_cog(Whisper(bot))
    bot.add_cog(Backup(bot))
    bot.add_cog(Export(bot))
    bot.add_cog(Channel(bot))
