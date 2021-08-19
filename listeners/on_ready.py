from discord.ext import commands


class on_ready(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        from globvars import client, state_manager
        
        print(f"Logged in as {client.user.name}#{client.user.discriminator}")

        state_manager.init_pregame()