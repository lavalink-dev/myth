import discord
from discord.ext import commands

class Leveling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(name="level", invoke_without_command=True)
    async def level(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        user = await self.client.pool.fetchrow("SELECT xp, level FROM users WHERE user_id = $1 AND guild_id = $2", member.id, ctx.guild.id)
        if not user:
            return await ctx.send("User has no level data.")
        await ctx.send(f"{member.mention} is at level {user['level']} with {user['xp']} XP.")

    @level.command(name="set")
    async def level_set(self, ctx, status: str):
        if status.lower() not in ("on", "off"):
            return await ctx.send("Specify 'on' or 'off'.")
        await self.client.pool.execute("INSERT INTO level_settings (guild_id, leveling_enabled) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET leveling_enabled = EXCLUDED.leveling_enabled", ctx.guild.id, status.lower() == "on")
        await ctx.send(f"Leveling has been {'enabled' if status.lower() == 'on' else 'disabled'}.")

    @level.group(name="reward")
    async def level_reward(self, ctx):
        pass

    @level_reward.command(name="add")
    async def level_reward_add(self, ctx, role: discord.Role):
        settings = await self.client.pool.fetchrow("SELECT reward_roles FROM level_settings WHERE guild_id = $1", ctx.guild.id)
        reward_roles = settings["reward_roles"] if settings else []
        if role.id in reward_roles:
            return await ctx.send("Role already a reward role.")
        reward_roles.append(role.id)
        await self.client.pool.execute("UPDATE level_settings SET reward_roles = $1 WHERE guild_id = $2", reward_roles, ctx.guild.id)
        await ctx.send(f"{role.name} added as a reward role.")

    @level_reward.command(name="remove")
    async def level_reward_remove(self, ctx, role: discord.Role):
        settings = await self.client.pool.fetchrow("SELECT reward_roles FROM level_settings WHERE guild_id = $1", ctx.guild.id)
        reward_roles = settings["reward_roles"] if settings else []
        if role.id not in reward_roles:
            return await ctx.send("Role is not a reward role.")
        reward_roles.remove(role.id)
        await self.client.pool.execute("UPDATE level_settings SET reward_roles = $1 WHERE guild_id = $2", reward_roles, ctx.guild.id)
        await ctx.send(f"{role.name} removed from reward roles.")

    @level.group(name="notifications")
    async def level_notifications(self, ctx):
        pass

    @level_notifications.command(name="channel")
    async def level_notifications_channel(self, ctx, channel: discord.TextChannel):
        await self.client.pool.execute("UPDATE level_settings SET notification_channel = $1 WHERE guild_id = $2", channel.id, ctx.guild.id)
        await ctx.send(f"Notifications will be sent in {channel.mention}.")

    @level_notifications.command(name="set")
    async def level_notifications_set(self, ctx, status: str):
        if status.lower() not in ("on", "off"):
            return await ctx.send("Specify 'on' or 'off'.")
        await self.client.pool.execute("UPDATE level_settings SET notification_enabled = $1 WHERE guild_id = $2", status.lower() == "on", ctx.guild.id)
        await ctx.send(f"Notifications {'enabled' if status.lower() == 'on' else 'disabled'}.")

    @level_notifications.command(name="message")
    async def level_notifications_message(self, ctx, *, message: str):
        await self.client.pool.execute("UPDATE level_settings SET notification_message = $1 WHERE guild_id = $2", message, ctx.guild.id)
        await ctx.send("Level-up notification message updated.")

    @commands.command(name="leaderboard")
    async def level_leaderboard(self, ctx):
        leaderboard = await self.client.pool.fetch("SELECT user_id, level, xp FROM users WHERE guild_id = $1 ORDER BY xp DESC LIMIT 10", ctx.guild.id)
        if not leaderboard:
            return await ctx.send("No users found on the leaderboard.")
        leaderboard_message = "\n".join([f"{i+1}. <@{row['user_id']}> - Level {row['level']} ({row['xp']} XP)" for i, row in enumerate(leaderboard)])
        await ctx.send(f"**Server Leaderboard**:\n{leaderboard_message}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        settings = await self.client.pool.fetchrow("SELECT leveling_enabled FROM level_settings WHERE guild_id = $1", message.guild.id)
        if not settings or not settings["leveling_enabled"]:
            return

        xp_gained = 5
        user = await self.client.pool.fetchrow("SELECT xp, level FROM users WHERE user_id = $1 AND guild_id = $2", message.author.id, message.guild.id)
        new_xp = (user["xp"] if user else 0) + xp_gained
        new_level = (user["level"] if user else 0)
        level_up_xp = 100 + (new_level * 50)

        if new_xp >= level_up_xp:
            new_level += 1
            new_xp -= level_up_xp
            notification_settings = await self.client.pool.fetchrow("SELECT notification_channel, notification_enabled, notification_message, reward_roles FROM level_settings WHERE guild_id = $1", message.guild.id)

            if notification_settings["notification_enabled"]:
                channel = message.guild.get_channel(notification_settings["notification_channel"])
                if channel:
                    await channel.send(notification_settings["notification_message"].format(user=message.author.mention, level=new_level))

            reward_roles = notification_settings["reward_roles"]
            for role_id in reward_roles:
                role = message.guild.get_role(role_id)
                if role and role not in message.author.roles:
                    await message.author.add_roles(role)

        await self.client.pool.execute("INSERT INTO users (user_id, guild_id, xp, level) VALUES ($1, $2, $3, $4) ON CONFLICT (user_id, guild_id) DO UPDATE SET xp = $3, level = $4", message.author.id, message.guild.id, new_xp, new_level)

async def setup(client):
    await client.add_cog(Leveling(client))
