import discord; from discord.ext import commands
import asyncpg; import asyncio; import time
from tools.config import color, emoji; from tools.context import Context

class Antinuke(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def is_admin(self, ctx):
        if ctx.author.id == ctx.guild.owner_id:
            return True
        result = await self.client.pool.fetchrow('SELECT 1 FROM antinuke_admins WHERE guild_id = $1 AND user_id = $2', ctx.guild.id, ctx.author.id)
        return result is not None

    @commands.group(description="HOLD UP! The features do NOT work, please use a diffrent antinuke.", aliases=["an"])
    @commands.has_permissions(administrator=True)
    async def antinuke(self, ctx):
        if not await self.is_admin(ctx):
            await ctx.deny("You're **not** an antinuke admin or an owner")
            return
          
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command.qualified_name)

    @antinuke.command(name="createchannels")
    async def createchannels(self, ctx, on_off: str, punishment: str):
        if not await self.is_admin(ctx):
            await ctx.deny("You're **not** an antinuke admin or an owner")
            return
        
        guild_id = ctx.guild.id
        threshold = 3
        await self.client.pool.execute(f'''
            INSERT INTO antinuke_settings (guild_id, createchannels, punishment, antinuke_enabled)
            VALUES ($1, $2, $3, TRUE)
            ON CONFLICT (guild_id) DO UPDATE SET createchannels = $2, punishment = $3;
        ''', guild_id, on_off.lower() == 'on', punishment.lower())
        
        if on_off.lower() == 'on':
            await ctx.agree(f"**Enabled** createchannels with punishment: {punishment.upper()} \nThreshold: {threshold}")
        else:
            await ctx.agree("**Disabled** createchannels")

    @antinuke.command(name="deletechannels")
    async def deletechannels(self, ctx, on_off: str, punishment: str):
        if not await self.is_admin(ctx):
            await ctx.deny("You're **not** an antinuke admin or an owner")
            return
        
        guild_id = ctx.guild.id
        threshold = 3
        await self.client.pool.execute(f'''
            INSERT INTO antinuke_settings (guild_id, deletechannels, punishment, antinuke_enabled)
            VALUES ($1, $2, $3, TRUE)
            ON CONFLICT (guild_id) DO UPDATE SET deletechannels = $2, punishment = $3;
        ''', guild_id, on_off.lower() == 'on', punishment.lower())
        
        if on_off.lower() == 'on':
            await ctx.agree(f"**Enabled** deletechannels with punishment: {punishment.upper()} \nThreshold: {threshold}")
        else:
            await ctx.agree("**Disabled** deletechannels")

    @antinuke.command(name="roleedit")
    async def roleedit(self, ctx, on_off: str, punishment: str):
        if not await self.is_admin(ctx):
            await ctx.deny("You're **not** an antinuke admin or an owner")
            return
        
        guild_id = ctx.guild.id
        threshold = 5
        await self.client.pool.execute(f'''
            INSERT INTO antinuke_settings (guild_id, roleedit, punishment, antinuke_enabled)
            VALUES ($1, $2, $3, TRUE)
            ON CONFLICT (guild_id) DO UPDATE SET roleedit = $2, punishment = $3;
        ''', guild_id, on_off.lower() == 'on', punishment.lower())
        
        if on_off.lower() == 'on':
            await ctx.agree(f"**Enabled** roleedit with punishment: {punishment.upper()} \nThreshold: {threshold}")
        else:
            await ctx.agree("**Disabled** roleedit")

    @antinuke.command(name="roledelete")
    async def roledelete(self, ctx, on_off: str, punishment: str):
        if not await self.is_admin(ctx):
            await ctx.deny("You're **not** an antinuke admin or an owner")
            return
        
        guild_id = ctx.guild.id
        threshold = 5
        await self.client.pool.execute(f'''
            INSERT INTO antinuke_settings (guild_id, roledelete, punishment, antinuke_enabled)
            VALUES ($1, $2, $3, TRUE)
            ON CONFLICT (guild_id) DO UPDATE SET roledelete = $2, punishment = $3;
        ''', guild_id, on_off.lower() == 'on', punishment.lower())
        
        if on_off.lower() == 'on':
            await ctx.send(f"**Enabled** roledelete with punishment: {punishment.upper()} \nThreshold: {threshold}")
        else:
            await ctx.send("**Disabled** roledelete")

    @antinuke.command(name="rolecreate")
    async def rolecreate(self, ctx, on_off: str, punishment: str):
        if not await self.is_admin(ctx):
            await ctx.deny("You're **not** an antinuke admin or an owner")
            return
        
        guild_id = ctx.guild.id
        threshold = 5
        await self.client.pool.execute(f'''
            INSERT INTO antinuke_settings (guild_id, rolecreate, punishment, antinuke_enabled)
            VALUES ($1, $2, $3, TRUE)
            ON CONFLICT (guild_id) DO UPDATE SET rolecreate = $2, punishment = $3;
        ''', guild_id, on_off.lower() == 'on', punishment.lower())
        
        if on_off.lower() == 'on':
            await ctx.agree(f"**Enabled** rolecreate with punishment: {punishment.upper()} \nThreshold: {threshold}")
        else:
            await ctx.agree("**Disabled** rolecreate")

    @antinuke.command(name="roleadd")
    async def roleadd(self, ctx, on_off: str, punishment: str):
        if not await self.is_admin(ctx):
            await ctx.deny("You're **not** an antinuke admin or an owner")
            return
        
        guild_id = ctx.guild.id
        threshold = 2
        await self.client.pool.execute(f'''
            INSERT INTO antinuke_settings (guild_id, roleadd, punishment, antinuke_enabled)
            VALUES ($1, $2, $3, TRUE)
            ON CONFLICT (guild_id) DO UPDATE SET roleadd = $2, punishment = $3;
        ''', guild_id, on_off.lower() == 'on', punishment.lower())
        
        if on_off.lower() == 'on':
            await ctx.agree(f"**Enabled** roleadd with punishment: {punishment.upper()} \nThreshold: {threshold}")
        else:
            await ctx.agree("**Disabled** roleadd")

    @antinuke.command(name="roleremove")
    async def roleremove(self, ctx, on_off: str, punishment: str):
        if not await self.is_admin(ctx):
            await ctx.deny("You're **not** an antinuke admin or an owner")
            return
        
        guild_id = ctx.guild.id
        threshold = 2
        await self.client.pool.execute(f'''
            INSERT INTO antinuke_settings (guild_id, roleremove, punishment, antinuke_enabled)
            VALUES ($1, $2, $3, TRUE)
            ON CONFLICT (guild_id) DO UPDATE SET roleremove = $2, punishment = $3;
        ''', guild_id, on_off.lower() == 'on', punishment.lower())
        
        if on_off.lower() == 'on':
            await ctx.agree(f"**Enabled** roleremove with punishment: {punishment.upper()} \nThreshold: {threshold}")
        else:
            await ctx.agree("**Disabled** roleremove")

    @antinuke.command(name="botadd")
    async def botadd(self, ctx, punishment: str):
        if not await self.is_admin(ctx):
            await ctx.deny("You're **not** an antinuke admin or an owner")
            return
        
        guild_id = ctx.guild.id
        await self.client.pool.execute(f'''
            INSERT INTO antinuke_settings (guild_id, botadd, punishment, antinuke_enabled)
            VALUES ($1, TRUE, $2, TRUE)
            ON CONFLICT (guild_id) DO UPDATE SET botadd = TRUE, punishment = $2;
        ''', guild_id, punishment.lower())
        
        await ctx.agree(f"**Enabled** botadd with punishment: {punishment.upper()}")

    @antinuke.command(name="admin")
    async def admin(self, ctx, action: str, user: discord.Member):
        if not await self.is_admin(ctx):
            await ctx.deny("You're **not** an antinuke owner")
            return
        
        guild_id = ctx.guild.id
        if action == "add":
            await self.client.pool.execute(f'''
                INSERT INTO antinuke_admins (guild_id, user_id) 
                VALUES ($1, $2)
                ON CONFLICT (guild_id, user_id) DO NOTHING;
            ''', guild_id, user.id)
            await ctx.agree(f"**Added** {user.mention} as an antinuke admin")
        elif action == "remove":
            await self.client.pool.execute(f'''
                DELETE FROM antinuke_admins WHERE guild_id = $1 AND user_id = $2;
            ''', guild_id, user.id)
            await ctx.agree(f"**Removed** {user.mention} from an antinuke admin")

    @antinuke.command(name="setup")
    async def setup(self, ctx):
        if not await self.is_admin(ctx):
            await ctx.deny("You're **not** an antinuke owner")
            return
        
        guild_id = ctx.guild.id
        await self.client.pool.execute(f'''
            INSERT INTO antinuke_settings (guild_id, antinuke_enabled)
            VALUES ($1, TRUE)
            ON CONFLICT (guild_id) DO UPDATE SET antinuke_enabled = TRUE;
        ''', guild_id)
        await ctx.agree("**Enabled** antinuke")

    @antinuke.command(name="clear")
    async def clear(self, ctx):
        if not await self.is_admin(ctx):
            await ctx.deny("You're **not** an antinuke owner")
            return
        
        guild_id = ctx.guild.id
        await self.client.pool.execute(f'''
            DELETE FROM antinuke_settings WHERE guild_id = $1;
            DELETE FROM antinuke_logs WHERE guild_id = $1;
            DELETE FROM antinuke_admins WHERE guild_id = $1;
        ''', guild_id)
        await ctx.agree("**Cleared** all antinuke settings")

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild_id = channel.guild.id
        user = await self.detect_last_audit_log_entry(channel.guild, discord.AuditLogAction.channel_create)
        if user:
            record = await self.client.pool.fetchrow('SELECT * FROM antinuke_settings WHERE guild_id = $1', guild_id)
            if record and record['createchannels']:
                threshold = 3
                await self.check_threshold(guild_id, user, 'createchannels', threshold)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        guild_id = channel.guild.id
        user = await self.detect_last_audit_log_entry(channel.guild, discord.AuditLogAction.channel_delete)
        if user:
            record = await self.client.pool.fetchrow('SELECT * FROM antinuke_settings WHERE guild_id = $1', guild_id)
            if record and record['deletechannels']:
                threshold = 3
                await self.check_threshold(guild_id, user, 'deletechannels', threshold)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        guild_id = before.guild.id
        user = await self.detect_last_audit_log_entry(before.guild, discord.AuditLogAction.role_update)
        if user:
            record = await self.client.pool.fetchrow('SELECT * FROM antinuke_settings WHERE guild_id = $1', guild_id)
            if record and record['roleedit']:
                threshold = 5
                await self.check_threshold(guild_id, user, 'roleedit', threshold)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        guild_id = role.guild.id
        user = await self.detect_last_audit_log_entry(role.guild, discord.AuditLogAction.role_create)
        if user:
            record = await self.client.pool.fetchrow('SELECT * FROM antinuke_settings WHERE guild_id = $1', guild_id)
            if record and record['rolecreate']:
                threshold = 5
                await self.check_threshold(guild_id, user, 'rolecreate', threshold)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        guild_id = role.guild.id
        user = await self.detect_last_audit_log_entry(role.guild, discord.AuditLogAction.role_delete)
        if user:
            record = await self.client.pool.fetchrow('SELECT * FROM antinuke_settings WHERE guild_id = $1', guild_id)
            if record and record['roledelete']:
                threshold = 5
                await self.check_threshold(guild_id, user, 'roledelete', threshold)

    @commands.Cog.listener()
    async def on_guild_member_add(self, member):
        guild_id = member.guild.id
        if member.bot:
            user = await self.detect_last_audit_log_entry(member.guild, discord.AuditLogAction.bot_add)
            if user:
                await member.kick(reason="Antinuke: Bot auto-kick")
                record = await self.client.pool.fetchrow('SELECT * FROM antinuke_settings WHERE guild_id = $1', guild_id)
                if record and record['botadd']:
                    await self.punishments(member.guild, user, record['punishment'])

    async def threshold(self, guild_id, user, action, threshold, time_limit):
        async with self.client.pool.acquire() as conn:
            record = await self.client.pool.fetchrow('SELECT action_count, last_action_time FROM antinuke_logs WHERE guild_id = $1 AND user_id = $2 AND action = $3', guild_id, user.id, action)

            current_time = int(time.time())
            if record:
                count = record['action_count'] + 1
                last_time = record['last_action_time']
                if current_time - last_time > time_limit:
                    count = 1
            else:
                count = 1

            if count >= threshold:
                punishment_record = await self.client.pool.fetchrow('SELECT punishment FROM antinuke_settings WHERE guild_id = $1', guild_id)
                if punishment_record:
                    punishment = punishment_record['punishment']
                    await self.punishments(user.guild, user, punishment)

            await self.client.pool.execute(
                '''INSERT INTO antinuke_logs (guild_id, user_id, action, action_count, last_action_time)
                   VALUES ($1, $2, $3, $4, $5)
                   ON CONFLICT (guild_id, user_id, action)
                   DO UPDATE SET action_count = $4, last_action_time = $5''',
                guild_id, user.id, action, count, current_time
            )

    async def punishments(self, guild, user, punishment):
        if punishment == "ban":
            await guild.ban(user, reason="Antinuke violation")
        elif punishment == "kick":
            await guild.kick(user, reason="Antinuke violation")

    async def audit(self, guild, action):
        async for entry in guild.audit_logs(limit=1, action=action):
            return entry.user
        return None

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        action_type = discord.AuditLogAction.ban
        actor = await self.audit(guild, action_type)
        
        if actor:
            guild_id = guild.id
            threshold = 5
            time_limit = 5
            await self.threshold(guild_id, actor, "ban", threshold, time_limit)

    @commands.Cog.listener()
    async def on_member_kick(self, guild, user):
        action_type = discord.AuditLogAction.kick
        actor = await self.audit(guild, action_type)
        
        if actor:
            guild_id = guild.id
            threshold = 3
            time_limit = 3
            await self.threshold(guild_id, actor, "kick", threshold, time_limit)

async def setup(client):
    await client.add_cog(Antinuke(client))
