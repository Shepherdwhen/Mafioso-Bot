from .on_command_error import on_command_error
from .on_ready import on_ready


def setup(bot):
    bot.add_cog(on_ready(bot))
    bot.add_cog(on_command_error(bot))