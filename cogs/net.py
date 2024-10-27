import discord
import aiohttp

from discord.ext       import commands
from fulcrum_api       import FulcrumAPI
from discord.ui        import Button, View

from tools.context     import Context
from tools.config      import emoji, color

class Network(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.fulcrumapi = FulcrumAPI()

    @commands.command()
    async def tiktok(self, ctx, username: str):
        data = await self.fulcrumapi.tiktok_user(username)
        embed = discord.Embed(color=color.default, description=f"> {data["bio"] if data["bio"] else "n/a"}")
        embed.set_author(name=f"{data['nickname']} | {data['username']}")
        embed.set_thumbnail(url=data["avatar"])
        embed.add_field(name="Counts", value=f"> **Followers:** {data["followers"]} \n> **Following:** {data["following"]} \n> **Likes:** {data["hearts"]}")
        embed.add_field(name="Extras", value=f"> **ID:** {data['id']} \n> **Verified:** {'Yes' if data['verified'] else 'No'} \n> **Private:** {'Yes' if data['private'] else 'No'} ")
        embed.add_field(name="Videos", value=f"> **Amount:** {data["videos"]}")
        view = View()
        profile = Button(style=discord.ButtonStyle.link, label="Profile", url=data["url"], emoji=f"{emoji.link}")
        
        view.add_item(profile)
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def twitter(self, ctx, username: str):
        data = await self.fulcrumapi.twitter_user(username)
        embed = discord.Embed(color=color.defualt, title=f"{data['display_name']} {data['username']}")
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
        data = await self.fulcrumapi.roblox(username)
        embed = discord.Embed(color=0xffffff, title=data["display_name"])
        embed.set_thumbnail(url=data["avatar"])
        embed.add_field(name="Username", value=data["username"], inline=True)
        embed.add_field(name="ID", value=data["id"], inline=True)
        embed.add_field(name="Bio", value=data["bio"] or "No bio", inline=False)
        embed.add_field(name="Banned", value="Yes" if data["banned"] else "No", inline=True)
        embed.add_field(name="Verified", value="Yes" if data["verified"] else "No", inline=True)
        embed.add_field(name="Friends", value=data["friends"], inline=True)
        embed.add_field(name="Followers", value=data["followers"], inline=True)
        embed.add_field(name="Following", value=data["followings"], inline=True)
        embed.add_field(name="Created At", value=data["created_at"], inline=False)
        embed.add_field(name="Profile URL", value=f"[Link]({data['url']})", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def cashapp(self, ctx, username: str):
        data = await self.fulcrumapi.cashapp(username)
        embed = discord.Embed(color=color.default, title=data["display_name"])
        embed.set_thumbnail(url=data["avatar"])
        embed.add_field(name="Username", value=data["username"], inline=True)
        embed.add_field(name="Verified", value="Yes" if data["verified"] else "No", inline=True)
        embed.add_field(name="Profile URL", value=f"[Link]({data['url']})", inline=False)
        embed.set_image(url=data["qr_url"]) 
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Network(client))
