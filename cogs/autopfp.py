import discord
from discord.ext import commands, tasks
import json
import string
import random
import asyncio
from aiohttp import ClientSession
from config import emoji, color

class autopfp(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.pfp.start()
        self.header = {'Authorization': 'Bearer 59f4c035-cd6c-4a38-8f10-933a519f0a74'}

    @commands.command()
    async def autopfp(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            await ctx.send("1")
        else:
            await self.client.pool.execute(
                'INSERT INTO autopfp (guild_id, channel_id) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET channel_id = $2', 
                ctx.guild.id, channel.id
            )
            await ctx.agree("sending")

    @commands.command()
    async def clearautopfp(self, ctx):
        await self.client.pool.execute('DELETE FROM autopfp WHERE guild_id = $1', ctx.guild.id)
        await ctx.agree("cleared")

    @tasks.loop(seconds=25)
    async def pfp(self):
        avatar_url = self.client.user.avatar.url if self.client.user.avatar else self.client.user.default_avatar.url
        category = ["match", "random pfp", "shoes", "nike", "jewellry", "aesthetic", "cartoon", "drill", 
                    "hello kitty", "money", "smoke", "anime", "cars", "faceless", "female gif", "guns", 
                    "female", "male gif", "male", "animals", "soft", "couple gif", "besties", "kpop", 
                    "edgy", "core"]
        
        rows = await self.client.pool.fetch('SELECT * FROM autopfp')
        
        async with ClientSession() as session:
            for row in rows:
                guild_id, channel_id = row['guild_id'], row['channel_id']
                try:
                    async with session.get("https://signed.bio/api", headers=self.header, params={'option': random.choice(category)}) as response:
                        if response.status != 200:
                            print(f"[!] Error: API returned status code {response.status}")
                            continue
                        data = await response.json()

                        image = data.get("url")
                        if image is None:
                            print("[!] Error: 'url' key is missing in the API response")
                            continue

                        channel = self.client.get_channel(channel_id)
                        if channel is None:
                            print(f"[!] Error: Channel with ID {channel_id} not found")
                            continue

                        embed = discord.Embed(color=color.default)
                        embed.set_author(name="powered by myth", icon_url=avatar_url)
                        embed.set_image(url=image)
                        await channel.send(embed=embed)
                except Exception as e:
                    print(f"[!] An unexpected error occurred: {e}")
                await asyncio.sleep(5)

    @commands.command()
    @commands.is_owner()
    async def apstart(self, ctx):
        self.pfp.start()
        await ctx.send("started")

    @commands.command()
    @commands.is_owner()
    async def apstop(self, ctx):
        self.pfp.stop()
        await ctx.send("stopped")

    @commands.command()
    @commands.is_owner()
    async def testpfp(self, ctx, *, option: str):
        embed = discord.Embed(color=0x2b2d31).set_footer(text="powered by signed.bio")
        async with ClientSession() as session:
            async with session.get("https://signed.bio/api", headers=self.header, params={"option": option}) as response:
                if response.status != 200:
                    await ctx.send("Failed to fetch image.")
                    return
                data = await response.json()
                embed.set_thumbnail(url=data["url"])
                msg = await ctx.send(embed=embed)
                await msg.add_reaction(f"{emoji.agree}")

async def setup(client):
    await client.add_cog(autopfp(client))
