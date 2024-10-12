import discord
from discord.ext import commands
import asyncpg

class VanityRoles(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def vanityroles(self, ctx):
        await ctx.send("Available subcommands: set, string, add, remove, clear, show")

    @vanityroles.command()
    async def set(self, ctx, status: str):
        if status.lower() == "on":
            await self.client.pool.execute("INSERT INTO vanityroles (guild_id, enabled) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET enabled = TRUE", ctx.guild.id, True)
            await ctx.send("Vanity roles system is now **enabled**.")
        elif status.lower() == "off":
            await self.client.pool.execute(
                "UPDATE vanityroles SET enabled = FALSE WHERE guild_id = $1", 
                ctx.guild.id
            )
            await ctx.send("Vanity roles system is now **disabled**.")
        else:
            await ctx.send("Please specify either `on` or `off`.")

    @vanityroles.command()
    async def string(self, ctx, *, vanity_string: str):
        if not vanity_string.startswith(".gg/") and not vanity_string.startswith("/"):
            return await ctx.send("Vanity string must start with `.gg/` or `/`.")
        await self.client.pool.execute(
            "UPDATE vanityroles SET text = $1 WHERE guild_id = $2", 
            vanity_string, ctx.guild.id
        )
        await ctx.send(f"Vanity string set to `{vanity_string}`.")

    @vanityroles.command()
    async def add(self, ctx, *, role: discord.Role):
        await self.client.pool.execute(
            "INSERT INTO vanityroles_roles (guild_id, role_id) VALUES ($1, $2) ON CONFLICT (guild_id, role_id) DO NOTHING", 
            ctx.guild.id, role.id
        )
        await ctx.send(f"Role {role.name} added for vanity role system.")

    @vanityroles.command()
    async def remove(self, ctx, *, role: discord.Role):
        await self.client.pool.execute(
            "DELETE FROM vanityroles_roles WHERE guild_id = $1 AND role_id = $2", 
            ctx.guild.id, role.id
        )
        await ctx.send(f"Role {role.name} removed from vanity role system.")

    @vanityroles.command()
    async def clear(self, ctx):
        await self.client.pool.execute(
            "DELETE FROM vanityroles WHERE guild_id = $1", 
            ctx.guild.id
        )
        await self.client.pool.execute(
            "DELETE FROM vanityroles_roles WHERE guild_id = $1", 
            ctx.guild.id
        )
        await ctx.send("Vanity role settings cleared for this server.")

    @vanityroles.command()
    async def show(self, ctx):
        data = await self.client.pool.fetchrow(
            "SELECT enabled, text FROM vanityroles WHERE guild_id = $1", 
            ctx.guild.id
        )
        roles = await self.client.pool.fetch(
            "SELECT role_id FROM vanityroles_roles WHERE guild_id = $1", 
            ctx.guild.id
        )

        if data:
            status = "Enabled" if data['enabled'] else "Disabled"
            vanity_string = data['text'] or "None"
            role_names = [ctx.guild.get_role(role['role_id']).name for role in roles if ctx.guild.get_role(role['role_id'])]

            await ctx.send(
                f"**Vanity Roles Status:** {status}\n"
                f"**Vanity String:** {vanity_string}\n"
                f"**Assigned Roles:** {', '.join(role_names) if role_names else 'None'}"
            )
        else:
            await ctx.send("No vanity roles settings found for this server.")

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        if not after.guild:
            return

        data = await self.client.pool.fetchrow(
            "SELECT * FROM vanityroles WHERE guild_id = $1 AND enabled = TRUE", 
            after.guild.id
        )

        if not data:
            return

        vanity_string = data['text']
        roles = await self.client.pool.fetch(
            "SELECT role_id FROM vanityroles_roles WHERE guild_id = $1", 
            after.guild.id
        )

        if not roles or not vanity_string:
            return

        activity = after.activity.name if after.activity else ''
        for role_data in roles:
            role = after.guild.get_role(role_data['role_id'])
            if role:
                if vanity_string in activity:
                    if role not in after.roles:
                        await after.add_roles(role)
                else:
                    if role in after.roles:
                        await after.remove_roles(role)

async def setup(client):
    await client.add_cog(VanityRoles(client))
