import discord
import asyncpg

from discord.ext       import commands

from tools.context     import Context
from tools.config      import emoji, color

class Reactionroles(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(
        description="Configure reaction roles for messages", 
        aliases=["rr"]
    )
    @commands.has_permissions(manage_channels=True)
    async def reactionroles(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command.qualified_name)
      
    @reactionroles.command(
      name="add",
      description="Add a reaction role to a message"
    )
    @commands.has_permissions(manage_roles=True)
    async def reactionroles_add(self, ctx, role: discord.Role, message: discord.Message, emoji: str):
        await self.client.pool.execute("INSERT INTO reactionroles_settings (guild_id, message_id, emoji, role_id) VALUES ($1, $2, $3, $4) ON CONFLICT DO NOTHING", ctx.guild.id, message.id, emoji, role.id)
      
        try:
            await message.add_reaction(emoji)
            await ctx.agree(f"**Added** {role.mention} with the emoji {emoji} on the message {message.id}")
        except discord.HTTPException:
            await ctx.send(f"Could not add reaction {emoji} to the message.")

    @reactionroles.command(
      name="remove",
      description="Remove a reaction role from a message"
    )
    @commands.has_permissions(manage_roles=True)
    async def reactionroles_remove(self, ctx, role: discord.Role, message: discord.Message, emoji: str):
        await self.client.pool.execute("DELETE FROM reactionroles_settings WHERE guild_id = $1 AND message_id = $2 AND emoji = $3 AND role_id = $4", ctx.guild.id, message.id, emoji, role.id)

        try:
            await message.clear_reaction(emoji)
            await ctx.agree(f"**Removed** {role.mention} with the emoji {emoji} from the message {message.id}")
        except discord.HTTPException:
            await ctx.send(f"Could not remove reaction {emoji} from the message.")

    @reactionroles.command(
      name="clear",
      description="Clear all reactionrole settings"
    )
    @commands.has_permissions(manage_roles=True)
    async def reactionroles_clear(self, ctx):
        await self.db.execute("DELETE FROM reactionroles_settings WHERE guild_id = $1", ctx.guild.id)
        await ctx.agree("**Cleared** all reactionroles settings")

    @reactionroles.command(
      name="list",
      description="Check out the reactionrole list"
    )
    @commands.has_permissions(administrator=True)
    async def reactionroles_list(self, ctx):
        records = await self.client.pool.fetch("SELECT * FROM reactionroles_settings WHERE guild_id = $1", ctx.guild.id)

        if not records:
            await ctx.deny("**No** reactionroles are currently added")
            return

        roles_list = '\n> '.join([ctx.guild.get_role(role['role_id']).mention for role in roles])
        user_pfp = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url

        embed = discord.Embed(color=color.default)
        embed.set_author(name=f"{ctx.author.name} | Reactionroles list", icon_url=user_pfp)
        for record in records:
            role = ctx.guild.get_role(record["role_id"])
            if role:
                embed.add_field(name=f"Message ID: {record['message_id']}", value=f"> Emoji: {record['emoji']} | Role: {role.name}", inline=False)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.guild_id is None:
            return  
        
        guild = self.client.get_guild(payload.guild_id)
        role_data = await self.client.pool.fetchrow("SELECT role_id FROM reactionroles_settings WHERE guild_id = $1 AND message_id = $2 AND emoji = $3", payload.guild_id, payload.message_id, str(payload.emoji))
        
        if role_data:
            role = guild.get_role(role_data["role_id"])
            if role:
                member = guild.get_member(payload.user_id)
                if member:
                    await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.guild_id is None:
            return
        
        guild = self.client.get_guild(payload.guild_id)
        role_data = await self.client.pool.fetchrow("SELECT role_id FROM reactionroles_settings WHERE guild_id = $1 AND message_id = $2 AND emoji = $3", payload.guild_id, payload.message_id, str(payload.emoji))
        
        if role_data:
            role = guild.get_role(role_data["role_id"])
            if role:
                member = guild.get_member(payload.user_id)
                if member:
                    await member.remove_roles(role)

async def setup(client):
    await client.add_cog(Reactionroles(client))
