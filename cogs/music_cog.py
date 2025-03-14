import discord
from discord.ext import commands
from discord import Interaction, app_commands

from cogs.music.music_server import MusicServer

class MusicCog(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot : commands.Bot = bot
        self.servers : dict = {}

    #-------------- Servers -------------------------------------------#
    @app_commands.command(name = "setup_music", description = "Starts the Music Bot functionality.")
    async def setup_musicserver(self, interaction : Interaction):
        await self.__get_server(interaction = interaction)     

    async def __get_server(self, interaction : Interaction) -> MusicServer:
        server_id = str(interaction.guild.id)
        if server_id not in self.servers.keys():
            self.servers[server_id] = MusicServer(bot = self.bot)
            await self.servers[server_id].setup(interaction = interaction)
        return self.servers[server_id]
    
    async def __get_server_by_id(self, server_id : int) -> MusicServer:
        server_id = str(server_id)
        assert server_id in self.servers.keys()

        return self.servers[server_id]

async def setup(bot):
    await bot.add_cog(MusicCog(bot))
