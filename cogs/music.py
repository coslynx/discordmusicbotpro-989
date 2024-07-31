import discord
from discord.ext import commands

import youtube_dl
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import soundcloud
import requests
import asyncio

from cogs.utils import format_message

# Suppress noisy youtube_dl logging
youtube_dl.utils.bug_reports_message = lambda: ''

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None
        self.queue = []
        self.current = None

    @commands.command(name='join', help='Connects the bot to the voice channel you are in.')
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You are not in a voice channel.")
            return
        
        if self.voice_client is None:
            self.voice_client = await ctx.author.voice.channel.connect()
        else:
            await self.voice_client.move_to(ctx.author.voice.channel)
        await ctx.send(f"Joined {ctx.author.voice.channel}")

    @commands.command(name='leave', help='Disconnects the bot from the voice channel.')
    async def leave(self, ctx):
        if self.voice_client is None:
            await ctx.send("I'm not in a voice channel.")
            return

        await self.voice_client.disconnect()
        self.voice_client = None
        await ctx.send("Disconnected.")

    @commands.command(name='play', help='Plays a song or playlist from YouTube, Spotify, or SoundCloud.')
    async def play(self, ctx, *, query):
        if self.voice_client is None:
            await ctx.send("I'm not in a voice channel.")
            return
        
        # Check if the query is a URL
        if "https://" in query or "http://" in query:
            await self.play_url(ctx, query)
        else:
            await self.play_search(ctx, query)

    @commands.command(name='pause', help='Pauses the music playback.')
    async def pause(self, ctx):
        if self.voice_client is None:
            await ctx.send("I'm not in a voice channel.")
            return

        if self.voice_client.is_playing():
            self.voice_client.pause()
            await ctx.send("Paused.")
        else:
            await ctx.send("Music is not playing.")

    @commands.command(name='resume', help='Resumes music playback.')
    async def resume(self, ctx):
        if self.voice_client is None:
            await ctx.send("I'm not in a voice channel.")
            return

        if self.voice_client.is_paused():
            self.voice_client.resume()
            await ctx.send("Resumed.")
        else:
            await ctx.send("Music is not paused.")

    @commands.command(name='skip', help='Skips to the next song in the queue.')
    async def skip(self, ctx):
        if self.voice_client is None:
            await ctx.send("I'm not in a voice channel.")
            return

        if self.voice_client.is_playing():
            self.voice_client.stop()
            await ctx.send("Skipped.")
        else:
            await ctx.send("Music is not playing.")

    @commands.command(name='stop', help='Stops music playback and clears the queue.')
    async def stop(self, ctx):
        if self.voice_client is None:
            await ctx.send("I'm not in a voice channel.")
            return

        if self.voice_client.is_playing():
            self.voice_client.stop()
            self.queue.clear()
            self.current = None
            await ctx.send("Stopped.")
        else:
            await ctx.send("Music is not playing.")

    @commands.command(name='queue', help='Displays the current song queue.')
    async def queue(self, ctx):
        if len(self.queue) == 0:
            await ctx.send("Queue is empty.")
            return

        queue_str = ""
        for i, song in enumerate(self.queue):
            queue_str += f"{i+1}. {song['title']}\n"

        await ctx.send(format_message(queue_str, title="Song Queue"))

    @commands.command(name='search', help='Searches for a song and adds it to the queue.')
    async def search(self, ctx, *, query):
        if self.voice_client is None:
            await ctx.send("I'm not in a voice channel.")
            return

        async with ctx.typing():
            # Search YouTube
            try:
                info = await self.get_youtube_info(query)
                self.queue.append({
                    "source": "youtube",
                    "url": info['url'],
                    "title": info['title']
                })
                await ctx.send(f"Added {info['title']} to queue.")
            except Exception as e:
                print(f"Error searching YouTube: {e}")
                await ctx.send("Error searching YouTube.")

            # Search Spotify
            # ... (implement Spotify search)

            # Search SoundCloud
            # ... (implement SoundCloud search)

    async def play_url(self, ctx, url):
        async with ctx.typing():
            # Check the URL type
            if "youtube.com" in url:
                try:
                    info = await self.get_youtube_info(url)
                    self.current = info
                    source = discord.FFmpegPCMAudio(info['url'], before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5')
                    self.voice_client.play(source)
                    await ctx.send(f"Now playing: {info['title']}")
                except Exception as e:
                    print(f"Error playing YouTube URL: {e}")
                    await ctx.send("Error playing YouTube URL.")
            elif "spotify.com" in url:
                try:
                    info = await self.get_spotify_info(url)
                    self.current = info
                    source = discord.FFmpegPCMAudio(info['url'], before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5')
                    self.voice_client.play(source)
                    await ctx.send(f"Now playing: {info['title']}")
                except Exception as e:
                    print(f"Error playing Spotify URL: {e}")
                    await ctx.send("Error playing Spotify URL.")
            elif "soundcloud.com" in url:
                try:
                    info = await self.get_soundcloud_info(url)
                    self.current = info
                    source = discord.FFmpegPCMAudio(info['url'], before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5')
                    self.voice_client.play(source)
                    await ctx.send(f"Now playing: {info['title']}")
                except Exception as e:
                    print(f"Error playing SoundCloud URL: {e}")
                    await ctx.send("Error playing SoundCloud URL.")
            else:
                await ctx.send("Unsupported URL.")

    async def play_search(self, ctx, query):
        async with ctx.typing():
            # Search YouTube
            try:
                info = await self.get_youtube_info(query)
                self.current = info
                source = discord.FFmpegPCMAudio(info['url'], before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5')
                self.voice_client.play(source)
                await ctx.send(f"Now playing: {info['title']}")
            except Exception as e:
                print(f"Error playing YouTube search: {e}")
                await ctx.send("Error playing YouTube search.")

            # Search Spotify
            # ... (implement Spotify search and playback)

            # Search SoundCloud
            # ... (implement SoundCloud search and playback)

    async def get_youtube_info(self, query):
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(query, download=False)
            except Exception as e:
                raise e

        if 'entries' in info:
            # It's a playlist
            return info['entries'][0]
        else:
            # It's a single song
            return info

    async def get_spotify_info(self, url):
        # Implement Spotify API integration
        # Use spotipy to fetch the track or playlist info
        # ...

        # Example:
        # sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='your_spotify_client_id', client_secret='your_spotify_client_secret'))
        # track_info = sp.track(track_id)

        # Convert track_info to a format suitable for playback
        # ...

        # Return the track info
        return track_info

    async def get_soundcloud_info(self, url):
        # Implement SoundCloud API integration
        # Use the soundcloud library to fetch the track info
        # ...

        # Example:
        # client = soundcloud.Client(client_id='your_soundcloud_client_id')
        # track_info = client.get('/tracks/' + track_id)

        # Convert track_info to a format suitable for playback
        # ...

        # Return the track info
        return track_info

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member == self.bot.user and after.channel is None:
            self.voice_client = None

def setup(bot):
    bot.add_cog(MusicCog(bot))