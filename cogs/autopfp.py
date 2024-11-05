import discord
from discord.ext import commands, tasks
import json
import string
import random
import asyncio
from aiohttp import ClientSession
from config import Emojis, Colors

class autopfp(commands.Cog):
    header = {'Authorization': 'Bearer 59f4c035-cd6c-4a38-8f10-933a519f0a74'}

    def __init__(self, client):
        self.client = client
        self.pfp.start()

    @commands.command(aliases=["ap"])
    async def autopfp(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            avatar_url = self.client.user.avatar.url if self.client.user.avatar else self.client.user.default_avatar.url
            embed = discord.Embed(title=f"{Emojis.minus} Autopfp", 
                                  description=f"{Emojis.rp} Send automatically profile pictures to a channel", 
                                  color=Colors.default)
            embed.add_field(name=f"{Emojis.cmd} Usage:", 
                            value=f"{Emojis.rp2} Autopfp [#channel] \n {Emojis.rp} Clearautopfp", inline=False)
            embed.add_field(name=f"{Emojis.channel} Aliases:", value=f"{Emojis.rp} ap", inline=False)
            embed.set_thumbnail(url=avatar_url)
            await ctx.send(embed=embed)
        else:
            await self.client.pool.execute(
                'INSERT INTO autopfp (guild_id, channel_id) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET channel_id = $2', 
                ctx.guild.id, channel.id
            )
            embed = discord.Embed(description=f'> {Emojis.agree} {ctx.author.mention}: **Set** the channel to: `{channel.mention}`', color=Colors.default)
            await ctx.send(embed=embed)

    @commands.command()
    async def clearautopfp(self, ctx):
        await self.client.pool.execute('DELETE FROM autopfp WHERE guild_id = $1', ctx.guild.id)
        embed = discord.Embed(description=f'> {Emojis.agree} {ctx.author.mention}: **Removed** autopfp', color=Colors.default)
        await ctx.send(embed=embed)

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
                    async with session.post("https://undefined.rip/api", headers=self.header, json={'option': random.choice(category)}) as response:
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

                        embed = discord.Embed(color=Colors.default)
                        embed.set_author(name="powered by pill", icon_url=avatar_url)
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

async def setup(client):
    await client.add_cog(autopfp(client))
