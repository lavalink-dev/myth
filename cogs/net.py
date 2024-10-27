import discord

from discord.ext       import commands
from fulcrum_api       import FulcrumAPI

from tools.context     import Context
from tools.config      import emoji, color

class Network(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.fulcrumapi = FulcrumAPI()

    @commands.command()
    async def tiktok(self, ctx, username: str):
        data = await self.fulcrumapi.tiktok_user(username)
        embed = discord.Embed(color=color.default, title=f"{data['nickname']} {data['username']}")
        embed.set_thumbnail(url=data["avatar"])
        embed.add_field(name="ID", value=data["id"])
        embed.add_field(name="ID", value=data["id"])
        embed.add_field(name="Bio", value=data["bio"], inline=False)
        embed.add_field(name="Verified", value="Yes" if data["verified"] else "No")
        embed.add_field(name="Private", value="Yes" if data["private"] else "No")
        embed.add_field(name="Following", value=data["following"])
        embed.add_field(name="Followers", value=data["followers"])
        embed.add_field(name="Hearts", value=data["hearts"])
        embed.add_field(name="Videos", value=data["videos"])
        embed.add_field(name="Profile URL", value=data["url"], inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def cashapp(self, ctx, username: str):
        data = await self.fulcrumapi.cashapp_user(username)
        embed = discord.Embed(color=int(data["accent_color"].lstrip("#"), 16), title=f"{data['display_name']} {data['username']}")
        embed.set_thumbnail(url=data["avatar"])
        embed.add_field(name="Verified", value="Yes" if data["verified"] else "No")
        embed.add_field(name="Profile URL", value=data["url"], inline=False)
        embed.set_image(url=data["qr_url"])
        await ctx.send(embed=embed)

    @commands.command()
    async def twitter(self, ctx, username: str):
        data = await self.fulcrumapi.twitter_user(username)
        embed = discord.Embed(color=0xffffff, title=f"{data['display_name']} {data['username']}")
        embed.set_thumbnail(url=data["avatar"])
        embed.add_field(name="Bio", value=data["bio"], inline=False)
        embed.add_field(name="Location", value=data["location"], inline=False)
        embed.add_field(name="Verified", value="Yes" if data["verified"] else "No")
        embed.add_field(name="Created At", value=data["created_at"], inline=False)
        embed.add_field(name="Followers", value=data["followers"])
        embed.add_field(name="Following", value=data["following"])
        embed.add_field(name="Posts", value=data["posts"])
        embed.add_field(name="Liked Posts", value=data["liked_posts"])
        embed.add_field(name="Tweets", value=data["tweets"])
        embed.add_field(name="Profile URL", value=data["url"], inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def roblox(self, ctx, username: str):
        data = await self.fulcrumapi.roblox_user(username)
        embed = discord.Embed(color=0xffffff, title=f"{data['display_name']} {data['username']}")
        embed.set_thumbnail(url=data["avatar"])
        embed.add_field(name="ID", value=data["id"])
        embed.add_field(name="Bio", value=data["bio"], inline=False)
        embed.add_field(name="Banned", value="Yes" if data["banned"] else "No")
        embed.add_field(name="Verified", value="Yes" if data["verified"] else "No")
        embed.add_field(name="Created At", value=data["created_at"], inline=False)
        embed.add_field(name="Friends", value=data["friends"])
        embed.add_field(name="Followers", value=data["followers"])
        embed.add_field(name="Following", value=data["followings"])
        embed.add_field(name="Profile URL", value=data["url"], inline=False)
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Network(client))
