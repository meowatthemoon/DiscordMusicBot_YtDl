import asyncio

import discord
from discord import Interaction
from discord.ui import  Modal, TextInput
import yt_dlp

from config import SEARCH_SONG_ITEMS_PER_PAGE, NUMBER_SONGS_PER_SEARCH, YDL_OPTIONS
from cogs.music.pagination_menu import PaginationMenu



async def search_ytdlp_async(query, ydl_opts):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: _extract(query, ydl_opts))

def _extract(query, ydl_opts):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(query, download=False)

class SongSearchModal(Modal, title = "What song do you want to search for?"):
    def __init__(self, callback : callable):
        super().__init__(timeout = None)
        self.callback_fn : callable = callback

    song_name = TextInput(
        style = discord.TextStyle.short,
        label = "Song Name",
        required = True,
        placeholder = "Name"
    )

    async def on_submit(self, interaction : Interaction):
        await interaction.response.send_message("Processing...")

        user = interaction.user
        query = self.song_name.value

        results = await search_ytdlp_async(f"ytsearch{NUMBER_SONGS_PER_SEARCH}: {query}", YDL_OPTIONS)
        tracks = results.get("entries", [])

        if len(tracks) == 0:
            return await interaction.edit_original_response(f"<@{user.id}>  I did not find any songs that match your query.", ephemeral = True, delete_after = 5)
        
        pagination_menu = PaginationMenu(tracks = tracks, items_per_page = SEARCH_SONG_ITEMS_PER_PAGE, callback = self.callback_fn)
        await interaction.edit_original_response(content = pagination_menu.get_page(), view = pagination_menu)

    async def on_error(self, interaction : Interaction, error):
        print("MODAL error", error)

    async def on_timeout(self, interaction : Interaction):
        print("MODAL tiemout")