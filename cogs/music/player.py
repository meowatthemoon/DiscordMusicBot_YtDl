import asyncio

import discord
from discord import ButtonStyle, Interaction, Member, Message, VoiceClient
from discord.ui import View
from cogs.music.queue import Queue
from config import FFMPEG_OPTIONS, HISTORY_SIZE

class PlayerMenu(View):
    def __init__(self, bot):
        super().__init__(timeout = None)
        self.__bot = bot

        self.__queue : Queue = Queue()
        self.__history : Queue = Queue(max_length = HISTORY_SIZE)

        self.__display_message : Message = None
        self.__vc : VoiceClient = None

    def set_message(self, message : Message):
        self.__display_message = message

    async def __display(self, text : str):
        await self.__display_message.edit(content = text)

    async def queue_track(self, track : dict, user : Member) -> bool:
        joined = await self.__join_voice_channel(user = user)
        if not joined:
            return False
     
        self.__queue.add_track_end(track = track)

        return await self.__play()

    async def __play(self) -> bool:
        if self.__vc.is_playing():
            return True

        return await self.__play_next_song()
    
    async def play_next_track(self) -> bool:
        print("Playing next track...")
        if self.__queue.is_empty():
            await self.__display(text = "")
            await self.__vc.disconnect()
            print("Queue is empty.")
            return False

        return await self.__play()
    
    async def __join_voice_channel(self, user : Member) -> bool:
        if not getattr(user.voice, 'channel', None):
            return False
        
        new_channel = user.voice.channel
        if new_channel is None:
            return False
        
        voice_client = user.guild.voice_client

        if voice_client is None:
            self.__vc = await new_channel.connect()
        elif new_channel != self.__vc.channel:
            await self.__vc.move_to(new_channel)

        return True
    
    async def __play_next_song(self) -> bool:
        track = self.__queue.pop_first_track()
        
        #"""
        if track is None:
            await self.__display(text = "")
            await self.__vc.disconnect()
            return False
        #"""
        
        self.__history.add_track_end(track = track)
        
        url = track["url"]
        print(f"Playing {track['title']} : {track['url']}")

        source = discord.FFmpegOpusAudio(url, **FFMPEG_OPTIONS)
        def after_play(error):
            #if error:
            #    print(f"Error playing {track["title"]}: {error}")
            asyncio.run_coroutine_threadsafe(self.__play_next_song(), self.__bot.loop)

        self.__vc.play(source, after = after_play)
        await self.__display(text = f"www.youtube.com/watch?v={track['id']}") 
        return True

    @discord.ui.button(emoji = "⏮", row = 0, style = ButtonStyle.blurple)
    async def button_previous(self, interaction : Interaction, button : discord.ui.Button):
        await interaction.response.defer()

        for _ in range(2):
            if self.__history.is_empty():
                return
        
            joined = await self.__join_voice_channel(user = interaction.user)
            if not joined:
                return False
            
            track = self.__history.pop_last_track()
            self.__queue.add_track_start(track = track)
        
        if self.__vc.is_playing():
            self.__vc.stop()
        
        return await self.__play()


    @discord.ui.button(emoji = "⏸", row = 0, style = ButtonStyle.blurple)
    async def button_pause(self, interaction : Interaction, button : discord.ui.Button):
        if self.__vc is not None and self.__vc.is_playing():
            self.__vc.pause()
        await interaction.response.defer()
        
    @discord.ui.button(emoji = "▶", row = 0, style = ButtonStyle.blurple)
    async def button_resume(self, interaction : Interaction, button : discord.ui.Button):
        if self.__vc is not None and self.__vc.is_paused():
            self.__vc.resume()
        await interaction.response.defer()        

    @discord.ui.button(emoji = "⏭", row = 0, style = ButtonStyle.blurple)
    async def button_next(self, interaction : Interaction, button : discord.ui.Button):
        if self.__vc.is_playing:
            self.__vc.stop()
        await interaction.response.defer()

    @discord.ui.button(emoji = "⏹", row = 0, style = ButtonStyle.blurple)
    async def button_stop(self, interaction : Interaction, button : discord.ui.Button):
        if self.__vc is not None:
            self.__vc.stop()
            await self.__vc.disconnect()

        self.__queue : Queue = Queue()
        self.__vc : VoiceClient = None

        await self.__display(text = "")
        await interaction.response.defer()


    @discord.ui.button(emoji = "🔄", row = 1, style = ButtonStyle.blurple)
    async def button_replay(self, interaction : Interaction, button : discord.ui.Button):
        if self.__vc is not None and not self.__vc.is_playing or self.__history.is_empty():
            return

        track = self.__history.pop_last_track()
        self.__queue.add_track_start(track = track)
        self.__vc.stop()
        await interaction.response.defer()


    @discord.ui.button(emoji = "🔀", row = 1, style = ButtonStyle.blurple)
    async def button_shuffle(self, interaction : Interaction, button : discord.ui.Button):
        self.__queue.shuffle()
        await interaction.response.defer()