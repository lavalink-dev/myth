import discord
from discord.ext import commands
import aiohttp

class LastFm(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.api_key = "4d2d1157ada4114d6cacd34fc0e58532"

    async def fetch_now_playing(self, username):
        url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={self.api_key}&format=json&limit=1"
        async with self.session.get(url) as response:
            data = await response.json()
            track = data["recenttracks"]["track"]
            if track:
                now_playing = track[0]
                artist = now_playing["artist"]["#text"]
                track_name = now_playing["name"]
                return f"{artist} - {track_name}"
            return "No currently playing track found."

    @commands.group(invoke_without_command=True)
    async def lastfm(self, ctx):
        await ctx.send("Available subcommands: `nowplaying`, `set <username>`, `remove`.")

    @lastfm.command()
    async def nowplaying(self, ctx):
        username = await self.client.pool.fetchval("SELECT username FROM lastfm WHERE user_id = $1", ctx.author.id)
        if not username:
            await ctx.send("You haven't set a Last.fm username. Use `!lastfm set <username>` to set one.")
        else:
            now_playing = await self.fetch_now_playing(username)
            await ctx.send(f"Now playing: {now_playing}")

    @lastfm.command()
    async def set(self, ctx, username: str):
        await self.client.pool.execute(
            """
            INSERT INTO lastfm (user_id, username)
            VALUES ($1, $2)
            ON CONFLICT (user_id) DO UPDATE SET username = $2
            """,
            ctx.author.id, username
        )
        await ctx.send(f"Your Last.fm username has been set to {username}.")

    @lastfm.command()
    async def remove(self, ctx):
        await self.client.pool.execute("UPDATE lastfm SET username = NULL WHERE user_id = $1", ctx.author.id)
        await ctx.send("Your Last.fm username has been removed.")

async def setup(client):
    await client.add_cog(LastFm(client))
