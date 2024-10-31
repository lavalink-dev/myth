from config import Emojis, Color
from system.types import CogMeta
from system.base import Context

from datetime import datetime, timezone

from discord import Message, Embed, ButtonStyle, __version__
from discord.ui import Button, View
from discord.utils import format_dt
from discord.ext.commands import command
from discord.ext.commands.parameters import Author

from platform import python_version
from psutil import cpu_percent, virtual_memory

class Information(CogMeta):
    """
    Display information about other users, or yourself.
    """

    @command(aliases=("p", "latency"))
    async def ping(self, ctx: Context) -> Message:
        """ View the bot's websocket and rest latency """

        return await (
            await ctx.reply("pinging...")
        ).edit(
            content=f"... `WS: {round(self.bot.latency * 1000)}ms` | `REST: {round((datetime.now(timezone.utc) - ctx.message.created_at).total_seconds() * 1000)}ms`"
        )
    
    @command(aliases=("inv", "links"))
    async def invite(self, ctx: Context) -> Message:
        """ Get the invite link for the bot """

        return await ctx.send(
            view=View(
                timeout=None
            ).add_item(
                Button(
                    style=ButtonStyle.link,
                    label="support",
                    url="https://discord.gg/uid"
                )
            ).add_item(
                Button(
                    style=ButtonStyle.link,
                    label="invite me",
                    url=f"https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot+applications.commands&permissions=8" # type: ignore
                )
            )
        )
    
    @command(aliases=("bi", "bot"))
    async def botinfo(self, ctx: Context) -> Message:
        """ Display information about the bot """

        guilds = [guild async for guild in self.bot.fetch_guilds(limit=None)]
        guild_count = len(guilds)

        latency = round(self.bot.latency * 1000)

        return await ctx.send(
            embed=Embed(
                title="Information",
                description=f"Developed by [lavalink](https://github.com/lavalink-dev) & [misimpression]\nPython version: {python_version()}",
                color=Color.default
            ).add_field(
                name="Statistics",
                value=(
                    f"Latency: `{latency}ms`\n"
                    f"Commands: `{len(self.bot.public_commands)}`\n" # type: ignore
                    f"Guilds: `{guild_count}`\n"
                    f"Users: `{len(self.bot.members):,}`"
                )
            ).add_field(
                name="Other Information",
                value=(
                    f"GPU Usage: `{cpu_percent()}%`\n"
                    f"CPU Usage: `{virtual_memory().percent}%`\n"
                    f"Support: [click here](https://discord.gg/uid)\n"
                    f"Discord.py: {__version__}"
                )
            ).set_footer(
                text="Myth v1.2"
            ).set_thumbnail(
                url=self.bot.user.display_avatar.url # type: ignore
            ).set_author(
                name=ctx.author.name,
                icon_url=ctx.author.display_avatar.url # type: ignore
            )
        )