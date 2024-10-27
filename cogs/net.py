import discord
from discord.ext import commands
from fulcrum_api import FulcrumAPI

class Network(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.fulcrumapi = FulcrumAPI()

    @commands.command()
    async def tiktok(self, ctx, username: str):
        data = await self.fulcrumapi.tiktok_user(username)
        embed = discord.Embed(color=color.default, title=data["nickname"])
        embed.add_field(name="followers", value=data["followers"])
        embed.add_field(name="following", value=data["following"])
        embed.add_field(name="videos", value=data["videos"])
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Network(client))
