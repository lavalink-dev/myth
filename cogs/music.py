import discord
from discord.ext import commands
import lavalink
from discord import utils
from discord import VoiceState

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        
        if not hasattr(self.client, 'lavalink'):  
            self.client.lavalink = lavalink.Client(self.client.user.id)
            self.client.lavalink.add_node(
                host='127.0.0.1',
                port=2333,
                password='securepassfr',
                region='us',
                name='default-node',
                spotify_client_id='95e6ef4cb4e14e14bec705ea61b0cb1d',
                spotify_client_secret='f32c0b8bc3364dcea0f1ebaa15d45911'
            )
            self.client.add_listener(self.client.lavalink.voice_update_handler, 'on_socket_response')

    def cog_unload(self):
        """ Cog unload handler. This removes any event hooks that were registered. """
        self.client.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        """ Command before-invoke handler. """
        guild_check = ctx.guild is not None
        if guild_check:
            await self.ensure_voice(ctx)
        return guild_check

    async def ensure_voice(self, ctx):
        """ This check ensures that the bot and command author are in the same voice channel. """
        player = self.client.lavalink.player_manager.create(ctx.guild.id)
        
        should_connect = ctx.command.name in ('play',)

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandInvokeError('Join a voice channel first.')

        if not player.is_connected:
            if not should_connect:
                raise commands.CommandInvokeError('Not connected.')

            permissions = ctx.author.voice.channel.permissions_for(ctx.guild.me)

            if not permissions.connect or not permissions.speak:
                raise commands.CommandInvokeError('I need the `CONNECT` and `SPEAK` permissions.')

            player.store('channel', ctx.channel.id)
            await ctx.guild.change_voice_state(channel=ctx.author.voice.channel)
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError('You need to be in my voice channel.')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.id != self.client.user.id:
            return

        if before.channel is None and after.channel is not None:
            # Joined a channel - create a player
            self.client.lavalink.player_manager.create(after.channel.guild.id)
        elif after.channel is None:
            # Left a channel - remove the player
            player = self.client.lavalink.player_manager.get(before.channel.guild.id)
            if player:
                await player.disconnect()
                player.cleanup()

    @commands.command()
    async def play(self, ctx, *, query: str):
        """ Searches and plays a song from a given query. """
        player = self.client.lavalink.player_manager.get(ctx.guild.id)

        query = query.strip('<>')

        if not query.startswith('http'):
            query = f'ytsearch:{query}'

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('Nothing found!')

        embed = discord.Embed(color=discord.Color.blurple())

        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            embed.title = 'Playlist Enqueued!'
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
        else:
            track = results['tracks'][0]
            embed.title = 'Track Enqueued'
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'

            player.add(requester=ctx.author.id, track=track)

        await ctx.send(embed=embed)

        if not player.is_playing:
            await player.play()

    @commands.command()
    async def stop(self, ctx):
        """ Stops the player and clears its queue. """
        player = self.client.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Not playing.')

        player.queue.clear()
        await player.stop()
        await ctx.send('⏹ | Stopped.')

    @commands.command()
    async def skip(self, ctx):
        """ Skips the current track. """
        player = self.client.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Not playing.')

        await player.skip()
        await ctx.send('⏭ | Skipped.')

    @commands.command()
    async def volume(self, ctx, volume: int):
        """ Changes the player's volume (0-1000). """
        player = self.client.lavalink.player_manager.get(ctx.guild.id)

        await player.set_volume(volume)
        await ctx.send(f'🔈 | Set to {volume}%')

    @commands.command()
    async def pause(self, ctx):
        """ Pauses the current track. """
        player = self.client.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Not playing.')

        if player.paused:
            return await ctx.send('Already paused.')

        await player.set_pause(True)
        await ctx.send('⏸ | Paused.')

    @commands.command()
    async def resume(self, ctx):
        """ Resumes a currently paused track. """
        player = self.client.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Not playing.')

        if not player.paused:
            return await ctx.send('Not paused.')

        await player.set_pause(False)
        await ctx.send('▶ | Resumed.')

    @commands.command()
    async def disconnect(self, ctx):
        """ Disconnects the player from the voice channel and clears its queue. """
        player = self.client.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            return await ctx.send('Not connected.')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('You\'re not in my voice channel!')

        player.queue.clear()
        await player.stop()
        await ctx.guild.change_voice_state(channel=None)
        await ctx.send('*⃣ | Disconnected.')

async def setup(client):
    await client.add_cog(Music(client))
