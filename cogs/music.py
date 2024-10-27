import discord
from discord.ext import commands
import wavelink

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.loop.create_task(self.setup_hook())

    async def setup_hook(self):
        node = wavelink.Node(
            uri='http://127.0.0.1:2333',
            password='securepassfr'
        )
        try:
            await wavelink.Pool.connect(nodes=[node], client=self.client)
        except Exception as e:
            print(f"Failed to connect to Lavalink node: {e}")

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f'Node {node.identifier} is ready!')

    @commands.command()
    async def play(self, ctx: commands.Context, *, search: str):
        if not ctx.voice_client:
            try:
                vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            except Exception as e:
                return await ctx.send(f"Could not connect to voice channel: {e}")
        else:
            vc: wavelink.Player = ctx.voice_client

        try:
            track = await wavelink.YouTubeTrack.search(search, return_first=True)
            if not track:
                return await ctx.send('No song found.')
            await vc.play(track)
            await ctx.send(f'Now playing: `{track.title}`')
        except Exception as e:
            await ctx.send(f"Error playing track: {e}")

    @commands.command()
    async def stop(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("Not connected to a voice channel.")
        node = ctx.voice_client
        await node.stop()
        await ctx.send("Stopped playing.")

    @commands.command()
    async def pause(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("Not connected to a voice channel.")
        node = ctx.voice_client
        if not node.is_playing():
            return await ctx.send("Nothing is playing.")
        await node.pause()
        await ctx.send("Paused the player.")

    @commands.command()
    async def resume(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("Not connected to a voice channel.")
        node = ctx.voice_client
        if not node.is_paused():
            return await ctx.send("Player is not paused.")
        await node.resume()
        await ctx.send("Resumed the player.")

    @commands.command()
    async def volume(self, ctx: commands.Context, vol: int):
        if not ctx.voice_client:
            return await ctx.send("Not connected to a voice channel.")
        if not 0 <= vol <= 100:
            return await ctx.send("Volume must be between 0 and 100.")
        node = ctx.voice_client
        await node.set_volume(vol)
        await ctx.send(f"Set volume to {vol}%")

    @commands.command()
    async def skip(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("Not connected to a voice channel.")
        node = ctx.voice_client
        if not node.is_playing():
            return await ctx.send("Nothing is playing.")
        await node.stop()
        await ctx.send("Skipped the current track.")

    @commands.command()
    async def disconnect(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("Not connected to a voice channel.")
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from voice channel.")

    @play.before_invoke
    async def ensure_voice(self, ctx: commands.Context):
        if not ctx.author.voice:
            raise commands.CommandError("You are not connected to a voice channel.")
        if ctx.voice_client and ctx.voice_client.channel != ctx.author.voice.channel:
            raise commands.CommandError("Bot is already in a voice channel.")

async def setup(client):
    await client.add_cog(Music(client))
