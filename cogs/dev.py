import discord
import aiohttp
import asyncio

from discord.ext       import commands
from discord.utils     import oauth_url

from tools.config      import emoji, color
from tools.context     import Context

class Developer(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(
        desription="Change the bots pfp"
    )
    @commands.is_owner()
    async def botpfp(self, ctx, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        print(f"Failed failed: {resp.status}")
                        return await ctx.deny('coulnt fetch the img')

                    data = await resp.read()

                    await self.client.user.edit(avatar=data)
                    await ctx.message.add_reaction(f"{emoji.agree}")
        except Exception as e:
            await ctx.warn(f'```{e}```')

    @commands.command(
        desription="Change the bots banner"
    )
    @commands.is_owner()
    async def botbanner(self, ctx, url: str):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        return await ctx.deny('coulnt fetch the img')

                    data = await resp.read()

                    await self.client.user.edit(banner=data)
                    await ctx.message.add_reaction(f"{emoji.agree}")
        except discord.HTTPException as e:
            await ctx.warn(f'```{e}```')
        except Exception as e:
            await ctx.warn(f'```{e}```')

    @commands.command(
        description="Check out the lastest guilds",
        aliases=["lastestgd", "lgd"]
    )
    @commands.is_owner()
    async def latestguilds(self, ctx):
        guilds = sorted(self.client.guilds, key=lambda g: g.me.joined_at, reverse=True)[:5]
        
        if not guilds:
            await ctx.send("aint in any guilds")
            return

        description = []
        for guild in guilds:
            invite = None
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).create_instant_invite:
                    invite = await channel.create_invite(max_age=0, max_uses=1)
                    break

            invite_link = invite.url if invite else "cant get inv"
            description.append(f"**{guild.name}** ({guild.member_count} members)\nInvite: {invite_link}")

        await ctx.send("\n\n".join(description))

    @commands.command(
        description="Make the bot leave a guild"
    )
    @commands.is_owner()
    async def botleave(self, ctx, guild_id: int = None):
        guild = None

        if guild_id:
            guild = self.client.get_guild(guild_id)
            if guild is None:
                await ctx.send(f"cant find the id: {guild_id}")
                return
        else:
            guild = ctx.guild

        await ctx.agree(f"left: {guild.name} ({guild.id})")
        await guild.leave()

    @commands.command(
        description="Leave servers under 10 humans"
    )
    @commands.is_owner()
    async def massleave(self, ctx):
        left_guilds = []
        for guild in self.client.guilds:
            human_members = sum(1 for member in guild.members if not member.bot)  
            if human_members < 10:
                await guild.leave()  
                left_guilds.append(guild.name)
                
        if left_guilds:
            await ctx.agree(f"left: {', '.join(left_guilds)}")
        else:
            await ctx.deny("cant find shit")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        invite_link = f"https://discord.gg/{guild.vanity_url_code}" if guild.vanity_url_code else None

        if not invite_link:
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).create_instant_invite:
                    invite = await channel.create_invite(max_age=0, max_uses=0)
                    invite_link = invite.url
                    break

        embed = discord.Embed(title=f"Joined: {guild.name}", description=f"> {invite_link}\n> **Members**: {guild.member_count}\n> **Owner**: {guild.owner}", color=color.default)
        embed.set_footer(text=f"ID: {guild.id}")
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

        channel = self.client.get_channel(1293657243379695627)
        if channel:
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        embed = discord.Embed(title=f"Left: {guild.name}", description=f"> **Members**: {guild.member_count}\n> **Owner**: {guild.owner}", color=color.default)
        embed.set_footer(text=f"ID: {guild.id}")
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

        channel = self.client.get_channel(1293657357137743933)
        if channel:
            await channel.send(embed=embed)

async def setup(client):
    await client.add_cog(Developer(client))
