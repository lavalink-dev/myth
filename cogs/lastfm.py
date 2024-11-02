import discord
from discord.ext import commands, tasks
import asyncpg
import aiohttp

class LastFm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = "4d2d1157ada4114d6cacd34fc0e58532"
        self.session = aiohttp.ClientSession()

    async def get_lastfm_username(self, user_id):
        query = "SELECT lastfm_username FROM users WHERE user_id = $1"
        return await self.bot.db.fetchval(query, user_id)

    async def set_lastfm_username(self, user_id, username):
        query = """
        INSERT INTO users (user_id, lastfm_username)
        VALUES ($1, $2)
        ON CONFLICT (user_id) DO UPDATE SET lastfm_username = $2
        """
        await self.bot.db.execute(query, user_id, username)

    async def remove_lastfm_username(self, user_id):
        query = "UPDATE users SET lastfm_username = NULL WHERE user_id = $1"
        await self.bot.db.execute(query, user_id)

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

    @commands.command()
    async def nowplaying(self, ctx):
        username = await self.get_lastfm_username(ctx.author.id)
        if not username:
            await ctx.send("You haven't set a Last.fm username. Use `!lastfm set <username>` to set one.")
        else:
            now_playing = await self.fetch_now_playing(username)
            await ctx.send(f"Now playing: {now_playing}")

    @commands.command()
    async def lfset(self, ctx, username: str):
        await self.set_lastfm_username(ctx.author.id, username)
        await ctx.send(f"Your Last.fm username has been set to {username}.")

    @commands.command()
    async def lfremove(self, ctx):
        await self.remove_lastfm_username(ctx.author.id)
        await ctx.send("Your Last.fm username has been removed.")

async def setup(bot):
    await bot.add_cog(LastFm(bot))
