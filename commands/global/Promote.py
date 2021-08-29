from discord.ext import commands

import globvars
from config import (ADMIN_ROLE_ID, INGAME_ADMIN_ROLE_ID, INGAME_MOD_ROLE_ID,
                    MOD_ROLE_ID, SERVER_ID)


class Promote(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='promote',
        aliases=[
            '^'
        ]
    )
    async def promote(self, ctx):
        guild = globvars.client.get_guild(SERVER_ID)

        admin_role = guild.get_role(ADMIN_ROLE_ID)
        mod_role = guild.get_role(MOD_ROLE_ID)
        inagme_admin_role = guild.get_role(INGAME_ADMIN_ROLE_ID)
        inagme_mod_role = guild.get_role(INGAME_MOD_ROLE_ID)

        success = False
        if inagme_admin_role in ctx.author.roles:
            await ctx.author.remove_roles(inagme_admin_role)
            await ctx.author.add_roles(admin_role)
            success = True

        if inagme_mod_role in ctx.author.roles:
            await ctx.author.remove_roles(inagme_mod_role)
            await ctx.author.add_roles(mod_role)
            success = True

        if success:
            await ctx.send('✅ Successfully promoted!')
        else:
            await ctx.send('⛔ You cannot promote!')

    @commands.command(
        name='demote',
        aliases=[
            'v'
        ]
    )
    async def demote(self, ctx):
        guild = globvars.client.get_guild(SERVER_ID)

        admin_role = guild.get_role(ADMIN_ROLE_ID)
        mod_role = guild.get_role(MOD_ROLE_ID)
        inagme_admin_role = guild.get_role(INGAME_ADMIN_ROLE_ID)
        inagme_mod_role = guild.get_role(INGAME_MOD_ROLE_ID)

        success = False
        if admin_role in ctx.author.roles:
            await ctx.author.add_roles(inagme_admin_role)
            await ctx.author.remove_roles(admin_role)
            success = True

        if mod_role in ctx.author.roles:
            await ctx.author.add_roles(inagme_mod_role)
            await ctx.author.remove_roles(mod_role)
            success = True

        if success:
            await ctx.send('✅ Successfully demoted!')
        else:
            await ctx.send('⛔ You cannot demote!')
