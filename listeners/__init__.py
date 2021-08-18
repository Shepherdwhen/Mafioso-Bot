from .on_ready import on_ready


def setup(bot):
    bot.add_cog(on_ready(bot))