import discord
from discord.ext import commands
import lavalink
from discord import utils
from discord import VoiceState

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.lavalink = lavalink.Client(self.client.user.id)
        self.client.lavalink.add_node(
            host='127.0.0.1',
            port=2333,
            password='securepassfr',
            region='us'
        )
        self.client.add_listener(self.client.lavalink.voice_update_handler, 'on_socket_response')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: VoiceState, after: VoiceState):
        if member.id != self.client.user.id:
            return

        if before.channel is None and after.channel is not None:
            self.client.lavalink.player_manager.create(guild_id=after.channel.guild.id)
        elif after.channel is None and player := self.client.lavalink.player_manager.get(before.channel.guild.id):
            await player.disconnect()

    @commands.command()
    async def play(self, ctx, *, query: str):
        member = utils.find(lambda m: m.id == ctx.author.id, ctx.guild.members)
        if member is not None and member.voice is not None:
            player = self.client.lavalink.player_manager.create(ctx.guild.id)
            player.store('channel', ctx.channel.id)
            await ctx.guild.change_voice_state(channel=member.voice.channel)
            
            result = await player.node.get_tracks(f'ytsearch:{query}')
            if not result or not result.tracks:
                return await ctx.send('Nothing found!')

            track = result.tracks[0]
            await player.play(track)
            await ctx.send(f'Now playing: `{track.title}`')

    @commands.command()
    async def stop(self, ctx):
        player = self.client.lavalink.player_manager.get(ctx.guild.id)
        if not player:
            return await ctx.send('Not playing anything.')
        await player.stop()
        await ctx.send('Stopped playing.')

    @commands.command()
    async def pause(self, ctx):
        player = self.client.lavalink.player_manager.get(ctx.guild.id)
        if not player:
            return await ctx.send('Not playing anything.')
        await player.set_pause(True)
        await ctx.send('Paused.')

    @commands.command()
    async def resume(self, ctx):
        player = self.client.lavalink.player_manager.get(ctx.guild.id)
        if not player:
            return await ctx.send('Not playing anything.')
        await player.set_pause(False)
        await ctx.send('Resumed.')

    @commands.command()
    async def volume(self, ctx, volume: int):
        player = self.client.lavalink.player_manager.get(ctx.guild.id)
        if not player:
            return await ctx.send('Not playing anything.')
        
        await player.set_volume(volume)
        await ctx.send(f'Set volume to {volume}')

    @commands.command()
    async def skip(self, ctx):
        player = self.client.lavalink.player_manager.get(ctx.guild.id)
        if not player:
            return await ctx.send('Not playing anything.')
        await player.skip()
        await ctx.send('Skipped song.')

    @commands.command()
    async def disconnect(self, ctx):
        player = self.client.lavalink.player_manager.get(ctx.guild.id)
        if not player:
            return await ctx.send('Not connected.')
        await player.disconnect()
        await ctx.send('Disconnected.')

async def setup(client):
    await client.add_cog(Music(client))
