import discord; from discord.ext import commands
import asyncpg
from tools.context import Context; from tools.config import emoji, color

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            command_name = ctx.command.name
            cooldown_time = error.retry_after
            await ctx.deny(f"**{command_name}** is on cooldown, try again in `{cooldown_time:.2f}s`")

        elif isinstance(error, commands.MissingPermissions):
            missing_perms = format(error.missing_permissions).replace('[', '').replace("'", '').replace(']', '').replace('_', ' ')
            await ctx.deny(f"You're **missing** `{missing_perms}` permission(s)")

        elif isinstance(error, commands.UserInputError):
            await ctx.warn("**Invalid** input")

        elif isinstance(error, commands.BadArgument):
            await ctx.deny(f"**Invalid** argument \n ```{error}```")

        elif isinstance(error, commands.BadUnionArgument):
            await ctx.deny(f"**Invalid** argument {error}\n ```{error}```")

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.deny(f"**Missing required argument** \n ```{error.param.name}```")

        elif isinstance(error, commands.TooManyArguments):
            await ctx.deny("**Too many arguments provided**")

        elif isinstance(error, commands.ChannelNotFound):
            await ctx.deny("**Could not** find the channel")

        elif isinstance(error, commands.UserNotFound):
            await ctx.deny("**Could not** find the user")

        elif isinstance(error, commands.RoleNotFound):
            await ctx.deny("**Could not** find the role")

        elif isinstance(error, commands.EmojiNotFound):
            await ctx.deny("**Could not** find the emoji")

        elif isinstance(error, commands.MemberNotFound):
            await ctx.deny("**Could not** find the user")

        else:
            print(str(error))

    @commands.Cog.listener()
    async def on_message(self, message):
        ctx = await self.client.get_context(message)
        
        if message.author == self.client.user or not ctx:
            return
        
        if self.client.user.mentioned_in(message) and message.content.strip() in [f"<@{self.client.user.id}>", f"<@!{self.client.user.id}>"]:
            if message.mention_everyone:
                return
            if isinstance(message.channel, discord.DMChannel):
                return

            user_id = str(message.author.id)
            result = await self.client.pool.fetchrow('SELECT prefix FROM prefixes WHERE user_id = $1', user_id)
            prefix = result['prefix'] if result else ';'
            
            embed = discord.Embed(description=f"> <:top:1284792567073996921> {message.author.mention}: **Selfprefix:** `{prefix}`", color=color.default)
            await message.channel.send(embed=embed)

async def setup(client):
    await client.add_cog(Events(client))
