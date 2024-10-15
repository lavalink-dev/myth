import discord
import asyncpg
import aiohttp
import requests
import

from discord.ext       import commands

from tools.context     import Context
from tools.config      import emoji, color

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def dog(self, ctx):
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        data = response.json()
        img = data["message"]
        embed = discord.Embed(color=color.default)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.command()
    async def cat(self, ctx):
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        data = response.json()
        img = data[0]["url"]
        embed = discord.Embed(color=color.default)
        embed.set_image(url=img)
        await ctx.send(embed=embed)
        
    @commands.command(aliases = ["gayrate"])
    async def gay(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        num1 = 1
        num2 = 100
        value = random.randint(min(num1, num2), max(num1, num2))
        embed = discord.Embed(title=f"🏳️‍🌈 Gay rating", description=f"**Gayrating** {user.mention} \n> You're **{value}%** gay", color=color.default)
        user_pfp = user.avatar.url if user.avatar else user.default_avatar.url
        embed.set_thumbnail(url=user_pfp)
        await ctx.send(embed=embed)
        
    @commands.command(aliases = ["lesbianrate"])
    async def lesbian(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        num1 = 1
        num2 = 100
        value = random.randint(min(num1, num2), max(num1, num2))
        embed = discord.Embed(title=f"🏳️‍🌈 Lesbian rating", description=f"**Lesbianrating** {user.mention} \n> You're **{value}%** lesbian", color=color.default)
        user_pfp = user.avatar.url if user.avatar else user.default_avatar.url
        embed.set_thumbnail(url=user_pfp)
        await ctx.send(embed=embed)
        
    @commands.command(aliases = ["rizzrate"])
    async def rizz(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        num1 = 1
        num2 = 10
        value = random.randint(min(num1, num2), max(num1, num2))
        embed = discord.Embed(title=f":heart_eyes: Rizz rating", description=f"**Rizzrating** {user.mention} \n> You have **{value}/10** rizz", color=color.default)
        user_pfp = user.avatar.url if user.avatar else user.default_avatar.url
        embed.set_thumbnail(url=user_pfp)
        await ctx.send(embed=embed)
        
    @commands.command(aliases = ["simprate"])
    async def simp(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        num1 = 1
        num2 = 100
        value = random.randint(min(num1, num2), max(num1, num2))
        embed = discord.Embed(title=f":pleading_face: Simp rating", description=f"**Simprating** {user.mention} \n> You're **{value}%** a simp", color=color.default)
        user_pfp = user.avatar.url if user.avatar else user.default_avatar.url
        embed.set_thumbnail(url=user_pfp)
        await ctx.send(embed=embed)
        
    @commands.command(aliases = ["hotrate"])
    async def hot(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        num1 = 1
        num2 = 100
        value = random.randint(min(num1, num2), max(num1, num2))
        embed = discord.Embed(title=f":hot_face: Hot rating", description=f"**Hotrating** {user.mention} \n> You're **{value}%** hot", color=color.default)
        user_pfp = user.avatar.url if user.avatar else user.default_avatar.url
        embed.set_thumbnail(url=user_pfp)
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Fun(client))
