import discord
import asyncpg

from discord.ext       import commands
from uwuipy            import Uwuipy

from tools.context     import Context
from tools.config      import emoji, color

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.uwu = Uwuipy()

# OTHERS

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
            
        result = await self.client.pool.fetchrow("SELECT user_id FROM uwulock WHERE user_id = $1 AND guild_id = $2", message.author.id, message.guild.id)

        if result:
            await message.delete()
            uwu_message = self.uwu.uwuify(message.content)

            name = message.author.display_name
            avatar_url = str(message.author.avatar.url) if message.author.avatar else None

            webhook = await message.channel.create_webhook(name=name, avatar=avatar_url)
            await webhook.send(uwu_message, username=name, avatar_url=av)
            await webhook.delete()

  # COMMANDS

    @commands.command(
      description="Make people sound funny"
    )
    @commands.has_permissions(administrator=True)
    async def uwulock(self, ctx, user: discord.Member):
        result = await self.client.pool.fetchrow("SELECT user_id FROM uwulock WHERE user_id = $1 AND guild_id = $2", user.id, ctx.guild.id)
        
        if result:
            await self.client.pool.execute("DELETE FROM uwulock WHERE user_id = $1 AND guild_id = $2", user.id, ctx.guild.id)
            await ctx.message.add_reaction(f"{emoji.agree}")
        else:
            await self.client.pool.execute("INSERT INTO uwulock (user_id, guild_id) VALUES ($1, $2)", user.id, ctx.guild.id)
            await ctx.message.add_reaction(f"{emoji.agree}")

async def setup(client):
    await client.add_cog(Fun(client))
