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

    @commands.group(description="Get e-cancer by vaping digitally", aliases=["v"], invoke_without_command=True)
    async def vape(self, ctx):
        await ctx.send_help(ctx.command.qualified_name)

    @vape.command(
        description="Be closer to getting cancer"
    )
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

    @vape.command(
        description="Check the vape flavors"
    )
    async def flavors(self, ctx):
        embeds = []
        page_size = 10
        pages = [self.flavors[i:i + page_size] for i in range(0, len(self.flavors), page_size)]
        
        for page in pages:
            flavors = "\n".join([f"> {flavor}" for flavor in page])
            embed = discord.Embed(description=flavors, color=color.default)
            embed.set_author(name=f"{ctx.author.name} | Flavors", icon_url=ctx.author.avatar.url or ctx.author.default_avatar.url)
            embeds.append(embed)

        paginator = Paginator(ctx, embeds, current=0)
        message = await ctx.send(embed=embeds[0], view=paginator)

    @vape.command(
        description="Set your vape flavor"
    )
    async def flavor(self, ctx, *, flavor: str):
        if flavor not in self.flavors:
            await ctx.deny(f"**Invalid flavor,** use a flavor from `{ctx.prefix}vape flavors`")
            return

        await self.client.pool.execute("INSERT INTO vape (user_id, flavor, hits) VALUES ($1, $2, 0) ON CONFLICT (user_id) DO UPDATE SET flavor = $2", ctx.author.id, flavor)
        await ctx.agree(f"**Set** your vape flavor to: `{flavor}`")
        
    @vape.command(
        description="Check who has the biggest e-cancer",
        aliases=["lb"]
    )
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
            leaderboard += f"> `{index}.` **{username}** - {hits} hits\n"

        embed = discord.Embed(description=leaderboard, color=color.default)
        embed.set_author(name=f"{ctx.author.name} | Vape leaderboard", icon_url=ctx.author.avatar.url or ctx.author.default_avatar.url)
        await ctx.send(embed=embed)
        
    @commands.command(
        description="make a sad cat meme"
    )
    async def sadcat(self, ctx, *, text):
        text = text.replace(" ", "+")
        image = f"https://api.popcat.xyz/sadcat?text={text}"
        await ctx.send(f"{image}")
        
    @commands.command(
        description="make a oogway meme"
    )
    async def oogway(self, ctx, *, text):
        text = text.replace(" ", "+")
        image = f"https://api.popcat.xyz/oogway?text={text}"
        await ctx.send(f"{image}")

    @commands.command(
        description="make a pikachu meme"
    )
    async def pikachu(self, ctx, *, text):
        text = text.replace(" ", "+")
        image = f"https://api.popcat.xyz/pikachu?text={text}"
        await ctx.send(f"{image}")

    @commands.command(
        description="let joe biden tweet something"
    )
    async def biden(self, ctx, *, text):
        text = text.replace(" ", "+")
        image = f"https://api.popcat.xyz/biden?text={text}"
        await ctx.send(f"{image}")

    @commands.command(
        description="create a wanted poster"
    )
    async def wanted(self, ctx, *, user: discord.Member=None):
        if user == None:
            avatar = ctx.author.display_avatar
        else:
            avatar = user.display_avatar

            image = f"https://api.popcat.xyz/wanted?image={avatar}"
            image = image.replace("webp", "png")

            await ctx.send(f"{image}")

    @commands.command(
        description="make someones avatar inverted"
    )
    async def invert(self, ctx, *, user: discord.Member=None):
        if user == None:
            avatar = ctx.author.display_avatar
        else:
            avatar = user.display_avatar

            image = f"https://api.popcat.xyz/invert?image={avatar}"
            image = image.replace("webp", "png")

            await ctx.send(f"{image}")

    @commands.command(
        description="create a gun image"
    )
    async def gun(self, ctx, *, user: discord.Member=None):
        if user == None:
            avatar = ctx.author.display_avatar
        else:
            avatar = user.display_avatar

            image = f"https://api.popcat.xyz/gun?image={avatar}"
            image = image.replace("webp", "png")

            await ctx.send(f"{image}")

    @commands.command(
        description="make a drip image"
    )
    async def drip(self, ctx, *, user: discord.Member=None):
        if user == None:
            avatar = ctx.author.display_avatar
        else:
            avatar = user.display_avatar

            image = f"https://api.popcat.xyz/drip?image={avatar}"
            image = image.replace("webp", "png")

            await ctx.send(f"{image}")

    @commands.command(
        description="make a clown image"
    )
    async def clown(self, ctx, *, user: discord.Member=None):
        if user == None:
            avatar = ctx.author.display_avatar
        else:
            avatar = user.display_avatar

            image = f"https://api.popcat.xyz/clown?image={avatar}"
            image = image.replace("webp", "png")

            await ctx.send(f"{image}")

    @commands.command(
        description="blur an image"
    )
    async def blur(self, ctx, *, user: discord.Member=None):
        if user == None:
            avatar = ctx.author.display_avatar
        else:
            avatar = user.display_avatar

            image = f"https://api.popcat.xyz/blur?image={avatar}"
            image = image.replace("webp", "png")

            await ctx.send(f"{image}")

    @commands.command(
        description="uncover an image"
    )
    async def uncover(self, ctx, *, user: discord.Member=None):
        if user == None:
            avatar = ctx.author.display_avatar
        else:
            avatar = user.display_avatar

            image = f"https://api.popcat.xyz/uncover?image={avatar}"
            image = image.replace("webp", "png")

            await ctx.send(f"{image}")

    @commands.command(
        description="remove a bg from an image", 
        aliases=["tp", "transparent"]
    )
    async def removebg(self, ctx, image=None):
        key = ['Q5BmkrUQWY7tTMi49QPJ7ooF', '57ZKaBsCHtoV6hq2HaGYQUz9', 'yA9sgXedXts6asYUa5TaQkV2', 'Tn7dfYzYxM1U54KqrYiFziRu', 'eKJ6cVmVDzVGY6jhfz5E56Pn', '2ZQnoDeXL4h9P7hHp5esjvWa']

        if image == None:
            if len(ctx.message.attachments) > 0:
                for file in ctx.message.attachments:
                    url = ctx.message.attachments[0].url
                    async with aiohttp.ClientSession() as ses:
                        async with ses.get(url) as r:
                            img = BytesIO(await r.read())
                            bytes = img.getvalue()

                            response = requests.post(
                            "https://api.remove.bg/v1.0/removebg",
                            data={
                                'image_url': ctx.message.attachments[0].url,
                                'size': 'auto'},
                            headers={'X-Api-Key': random.choice(key)},
                            )
                            if response.status_code == requests.codes.ok:
                                with open('no-bg.png', 'wb') as out:
                                    out.write(response.content)
                                    await ctx.send(file=discord.File('no-bg.png'))
                            else:
                                print("Error:", response.status_code, response.text)

        else:
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                data={
                    'image_url': image,
                    'size': 'auto'},
                headers={'X-Api-Key': random.choice(key)},
            )
            if response.status_code == requests.codes.ok:
                with open('no-bg.png', 'wb') as out:
                    out.write(response.content)
                    await ctx.send(file=discord.File('no-bg.png'))
            else:
                print("Error:", response.status_code, response.text)

async def setup(client):
    await client.add_cog(Fun(client))
