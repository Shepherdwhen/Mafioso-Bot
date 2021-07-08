from .mafioso import Mafioso


async def setup(bot):
    cog = Mafioso(bot)
    await cog.load_from_config()
    bot.add_cog(cog)