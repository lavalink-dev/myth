import discord
import asyncpg
import aiohttp
import requests
import random

from discord.ext       import commands

from system.base.context     import Context
from config                  import emoji, color
from system.base.paginator   import Paginator

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.flavors = [
            "Vanilla", "Mint", "Berry", "Citrus", 
            "Lavender", "Dragonfruit", "Cherry", "Orange", 
            "Blueberry", "Tropical", "Cranberry", "Mango", 
            "Ginger", "Pineapple", "Raspberry"
        ]
        
    @commands.command(
        description="Get an image of a dog"
    )
    async def dog(self, ctx):
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        data = response.json()
        img = data["message"]
        embed = discord.Embed(color=color.default)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.command(
        description="Get an image of a cat"
    )
    async def cat(self, ctx):
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        data = response.json()
        img = data[0]["url"]
        embed = discord.Embed(color=color.default)
        embed.set_image(url=img)
        await ctx.send(embed=embed)
        
    @commands.command(
        description="Check how gay you are",
        aliases=["gayrate"]
    )
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
        
    @commands.command(
        description="Check how lesbian you are",
        aliases=["lesbianrate"]
    )
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
        
    @commands.command(
        description="Check how of a big simp you are",
        aliases=["simprate"]
    )
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
        
    @commands.command(
        description="Check how hot you are",
        aliases=["hotrate"]
    )
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

    @commands.command(
        description="Make a fun poll",
        aliases=["quickpoll", "qp"]
    )
    async def poll(self, ctx, *, question=None):
        if question is None:
             await ctx.send_help(ctx.command.qualified_name)
        else:
            user_pfp = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
            embed = discord.Embed(description=f"> {question}", color=color.default)
            embed.set_author(name=ctx.author.name, icon_url=user_pfp)
            message = await ctx.send(embed=embed)

            await message.add_reaction("👍")
            await message.add_reaction("👎")

            await ctx.message.delete()

    @commands.group(
        description="Configure ur userinfo", 
        aliases=["userinfoconfig", "userinfoedit", "uiedit"]
    )
    async def uiconfig(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command.qualified_name)

    @uiconfig.command(
        name="name",
        description="Edit your userinfo name"
    )
    async def uiconfig_name(self, ctx, *, name: str):
        await self.client.pool.execute("INSERT INTO userinfo (user_id, name) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET name = $2", ctx.author.id, name)
        await ctx.agree(f"**Set** your userinfo name to: `{name}`")

    @uiconfig.command(
        name="footer",
        description="Edit your userinfo footer"
    )
    async def uiconfig_footer(self, ctx, *, footer: str):
        await self.client.pool.execute("INSERT INTO userinfo (user_id, footer) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET footer = $2", ctx.author.id, footer)
        await ctx.agree(f"**Set** your userinfo footer to: `{footer}`")

    @uiconfig.command(
        name="bio",
        description="Edit your userinfo bio"
    )
    async def uiconfig_bio(self, ctx, *, bio: str):
        await self.client.pool.execute("INSERT INTO userinfo (user_id, bio) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET bio = $2", ctx.author.id, bio)
        await ctx.agree("**Set** your userinfo bio")

    @commands.group(description="Get 'e-cancer' by 'e-vaping' :sob:", aliases=["v"], invoke_without_command=True)
    async def vape(self, ctx):
        await ctx.send_help(ctx.command.qualified_name)

    @vape.command()
    async def hit(self, ctx):
        result = await self.client.pool.fetchrow("SELECT flavor, hits FROM vape WHERE user_id = $1", ctx.author.id)
        
        if not result or not result["flavor"]:
            await ctx.deny(f"You **have not** set a flavor, use `{ctx.prefix}vape flavor [flavor]` to set one")
            return

        flavor = result["flavor"]
        hits = result["hits"] + 1 if result["hits"] else 1

        await self.client.pool.execute("UPDATE vape SET hits = $1 WHERE user_id = $2 AND flavor = $3", hits, ctx.author.id, flavor)

        embed = discord.Embed(description=f"> <:vape:1296191531241312326> {ctx.author.mention}: You **hit** the flavor `{flavor}`", color=color.default)
        await ctx.send(embed=embed)

    @vape.command()
    async def flavors(self, ctx):
        embeds = []
        page_size = 10
        pages = [self.flavors[i:i + page_size] for i in range(0, len(self.flavors), page_size)]
        
        for page in pages:
            flavors = "\n".join([f"> {flavor}" for flavor in page])
            embed = discord.Embed(description=flavors, color=color.default)
            embed.set_author(name=f"{ctx.author.name} | Flavors", icon_url=user.avatar.url or user.default_avatar.url)
            embeds.append(embed)

        paginator = Paginator(ctx, embeds, current=0)
        message = await ctx.send(embed=embeds[0], view=paginator)

    @vape.command()
    async def flavor(self, ctx, *, flavor: str):
        if flavor not in self.flavors:
            await ctx.deny(f"**Invalid flavor,** use a flavor from `{ctx.prefix}vape flavors`")
            return

        await self.client.pool.execute("INSERT INTO vape (user_id, flavor, hits) VALUES ($1, $2, 0) ON CONFLICT (user_id) DO UPDATE SET flavor = $2", ctx.author.id, flavor)
        await ctx.agree(f"**Set** your vape flavor to: `{flavor}`")
        
    @vape.command()
    async def leaderboard(self, ctx):
        rows = await self.client.pool.fetch("SELECT user_id, hits FROM vape ORDER BY hits DESC LIMIT 10")

        if not rows:
            await ctx.send("No one has vaped yet.")
            return

        leaderboard = ""
        for index, row in enumerate(rows, start=1):
            user = self.client.get_user(row["user_id"])
            username = user.mention if user else "Unknown User"
            hits = row["hits"]
            leaderboard += f"`{index}.` **{username}** - {hits} hits\n"

        embed = discord.Embed(description=leaderboard, color=color.default)
        embed.set_author(name=f"{ctx.author.name} | Vape leaderboard", icon_url=user.avatar.url or user.default_avatar.url)
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Fun(client))
