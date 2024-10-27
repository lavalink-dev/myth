import discord
from discord.ext import commands
import wavelink
from typing import Optional

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.setup_hook())

    async def setup_hook(self):
        """Connect to our Lavalink nodes."""
        await self.bot.wait_until_ready()
        
        node: wavelink.Node = wavelink.Node(
            uri='http://localhost:2333', # Your lavalink server
            password='securepassfr'   # From your application.yml
        )
        await wavelink.NodePool.connect(client=self.bot, nodes=[node])

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        """Event fired when a node has finished connecting."""
        print(f'Node {node.identifier} is ready!')

    @commands.command()
    async def play(self, ctx: commands.Context, *, search: str):
        """Play a song with the given search query."""
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        # Search for the track
        track = await wavelink.YouTubeTrack.search(search, return_first=True)
        
        if not track:
            return await ctx.send('No song found.')
            
        await vc.play(track)
        await ctx.send(f'Now playing: `{track.title}`')

    @commands.command()
    async def stop(self, ctx: commands.Context):
        """Stop the currently playing song."""
        if not ctx.voice_client:
            return await ctx.send("Not connected to a voice channel.")
            
        node = ctx.voice_client
        await node.stop()
        await ctx.send("Stopped playing.")

    @commands.command()
    async def pause(self, ctx: commands.Context):
        """Pause the currently playing song."""
        if not ctx.voice_client:
            return await ctx.send("Not connected to a voice channel.")
            
        node = ctx.voice_client
        
        if not node.is_playing():
            return await ctx.send("Nothing is playing.")
            
        await node.pause()
        await ctx.send("Paused the player.")

    @commands.command()
    async def resume(self, ctx: commands.Context):
        """Resume the currently paused song."""
        if not ctx.voice_client:
            return await ctx.send("Not connected to a voice channel.")
            
        node = ctx.voice_client
        
        if not node.is_paused():
            return await ctx.send("Player is not paused.")
            
        await node.resume()
        await ctx.send("Resumed the player.")

    @commands.command()
    async def volume(self, ctx: commands.Context, vol: int):
        """Change the player's volume."""
        if not ctx.voice_client:
            return await ctx.send("Not connected to a voice channel.")
            
        if not 0 <= vol <= 100:
            return await ctx.send("Volume must be between 0 and 100.")
            
        node = ctx.voice_client
        await node.set_volume(vol)
        await ctx.send(f"Set volume to {vol}%")

    @commands.command()
    async def skip(self, ctx: commands.Context):
        """Skip the currently playing song."""
        if not ctx.voice_client:
            return await ctx.send("Not connected to a voice channel.")
            
        node = ctx.voice_client
        
        if not node.is_playing():
            return await ctx.send("Nothing is playing.")
            
        await node.stop()
        await ctx.send("Skipped the current track.")

    @commands.command()
    async def disconnect(self, ctx: commands.Context):
        """Disconnect the bot from the voice channel."""
        if not ctx.voice_client:
            return await ctx.send("Not connected to a voice channel.")
            
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from voice channel.")

    @play.before_invoke
    async def ensure_voice(self, ctx: commands.Context):
        """Ensure the bot and user are in a voice channel."""
        if not ctx.author.voice:
            raise commands.CommandError("You are not connected to a voice channel.")
        
        if ctx.voice_client and ctx.voice_client.channel != ctx.author.voice.channel:
            raise commands.CommandError("Bot is already in a voice channel.")

async def setup(bot):
    await bot.add_cog(Music(bot))
