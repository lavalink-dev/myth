import discord
from discord.ext import commands
import aiohttp

class LastFm(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.api_key = "4d2d1157ada4114d6cacd34fc0e58532"
        self.session = aiohttp.ClientSession()

    async def fetch_now_playing(self, username):
        url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={self.api_key}&format=json&limit=1"
        async with self.session.get(url) as response:
            data = await response.json()
            track = data["recenttracks"]["track"]
            if track:
                now_playing = track[0]
                artist = now_playing["artist"]["#text"]
                track_name = now_playing["name"]
                album = now_playing.get("album", {}).get("#text", "Unknown Album")
                url = now_playing.get("url", "No URL")
                return f"**{artist} - {track_name}**\nAlbum: {album}\n[Link to track]({url})"
            return "No currently playing track found."

    async def fetch_top_week(self, username):
        url = f"http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user={username}&api_key={self.api_key}&format=json&period=7day&limit=10"
        async with self.session.get(url) as response:
            data = await response.json()
            top_tracks = data["toptracks"]["track"]
            if top_tracks:
                result = []
                for track in top_tracks:
                    artist = track["artist"]["name"]
                    track_name = track["name"]
                    play_count = track["playcount"]
                    result.append(f"**{artist} - {track_name}** ({play_count} plays)")
                return "\n".join(result)
            return "No top tracks found for the past week."

    @commands.group(
        description="Filter out bad words", 
        aliases=["lf", "fm"]
    )
    async def lastfm(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command.qualified_name)

    @lastfm.command(
        name="nowplaying",
        description="Check what's playing currently",
        aliases=["np"]
    )
    async def lastfm_nowplaying(self, ctx):
        username = await self.client.pool.fetchval("SELECT username FROM lastfm WHERE user_id = $1", ctx.author.id)
        if not username:
            await ctx.send("You haven't set a Last.fm username. Use `!lastfm set <username>` to set one.")
        else:
            np = await self.fetch_now_playing(username)
            await ctx.send(f"Now playing:\n{np}")

    @lastfm.command(
        name="topweek",
        description="Check the top tracks played this week",
        aliases=["tw"]
    )
    async def lastfm_topweek(self, ctx):
        username = await self.client.pool.fetchval("SELECT username FROM lastfm WHERE user_id = $1", ctx.author.id)
        if not username:
            await ctx.send("You haven't set a Last.fm username. Use `!lastfm set <username>` to set one.")
        else:
            top_week = await self.fetch_top_week(username)
            await ctx.send(f"Top tracks this week:\n{top_week}")

    @lastfm.command(
        name="set",
        description="Set your LastFm username",
        aliases=["add"]
    )
    async def lastfm_set(self, ctx, username: str):
        await self.client.pool.execute(
            """
            INSERT INTO lastfm (user_id, username)
            VALUES ($1, $2)
            ON CONFLICT (user_id) DO UPDATE SET username = $2
            """,
            ctx.author.id, username
        )
        await ctx.send(f"**Set** your LastFm user to: `{username}`")

    @lastfm.command(
        name="remove",
        description="Remove your LastFm username",
        aliases=["delete"]
    )
    async def lastfm_remove(self, ctx):
        await self.client.pool.execute("UPDATE lastfm SET username = NULL WHERE user_id = $1", ctx.author.id)
        await ctx.send("**Removed** your LastFm username")

async def setup(client):
    await client.add_cog(LastFm(client))
