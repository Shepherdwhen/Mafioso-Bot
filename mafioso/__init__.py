from .mafioso import Mafioso


async def setup(bot):
    bot.add_cog(Mafioso(bot))
