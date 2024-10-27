import discord
import aiohttp

from discord.ext       import commands
from fulcrum_api       import FulcrumAPI
from discord.utils     import format_dt, get
from discord.ui        import Button, View
from datetime          import datetime, timedelta

from tools.context     import Context
from tools.config      import emoji, color

class Network(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.fulcrumapi = FulcrumAPI()

    @commands.command()
    async def tiktok(self, ctx, username: str):
        data = await self.fulcrumapi.tiktok_user(username)
        
        embed = discord.Embed(color=color.default, description=f"> {data.get('bio', 'n/a')}")
        embed.set_author(name=f"{data.get('nickname', 'unknown')} | {data.get('username', 'n/a')}")
        embed.set_thumbnail(url=data.get("avatar", ""))
        embed.add_field(name="Counts", value=f"> **Followers:** {data.get('followers', 'n/a')}\n> **Following:** {data.get('following', 'n/a')}\n> **Likes:** {data.get('hearts', 'n/a')}")
        embed.add_field(name="Extras", value=f"> **ID:** {data.get('id', 'n/a')}\n> **Verified:** {'Yes' if data.get('verified') else 'No'}\n> **Private:** {'Yes' if data.get('private') else 'No'}")
        embed.add_field(name="Videos", value=f"> **Amount:** {data.get('videos', 'n/a')}")
        
        view = View()
        profile = Button(style=discord.ButtonStyle.link, label="Profile", url=data.get("url", ""), emoji=emoji.link)
        view.add_item(profile)
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def twitter(self, ctx, username: str):
        data = await self.fulcrumapi.twitter_user(username)
        
        embed = discord.Embed(color=color.default, description=f"> {data.get('bio', 'n/a')}")
        embed.set_author(name=f"{data.get('display_name', 'unknown')} | {data.get('username', 'n/a')}")
        embed.set_thumbnail(url=data.get("avatar", ""))
        embed.add_field(name="Counts", value=f"> **Followers:** {data.get('followers', 'n/a')}\n> **Following:** {data.get('following', 'n/a')}\n> **Posts:** {data.get('posts', 'n/a')}")
        embed.add_field(name="Extras", value=f"> **ID:** {data.get('id', 'n/a')}\n> **Verified:** {'Yes' if data.get('verified') else 'No'}\n> **Location:** {data.get('location', 'n/a')}")
        
        created_at = data.get('created_at', None)
        try:
            created_at_formatted = format_dt(datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y'), 'R') if created_at else 'n/a'
        except ValueError:
            created_at_formatted = 'n/a'
        embed.add_field(name="Stats", value=f"> **Liked Posts:** {data.get('liked_posts', 'n/a')}\n> **Tweets:** {data.get('tweets', 'n/a')}\n> **Created:** {created_at_formatted}")
        
        view = View()
        profile = Button(style=discord.ButtonStyle.link, label="Profile", url=data.get("url", ""), emoji=emoji.link)
        view.add_item(profile)
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def roblox(self, ctx, username: str):
        data = await self.fulcrumapi.roblox(username)
        
        embed = discord.Embed(color=color.default, description=f"> {data.get('bio', 'n/a')}")
        embed.set_author(name=f"{data.get('display_name', 'unknown')} | {data.get('username', 'n/a')}")
        embed.set_thumbnail(url=data.get("avatar", ""))
        embed.add_field(name="Profile Info", value=f"> **ID:** {data.get('id', 'n/a')}\n> **Banned:** {'Yes' if data.get('banned') else 'No'}\n> **Verified:** {'Yes' if data.get('verified') else 'No'}")
        embed.add_field(name="Social", value=f"> **Friends:** {data.get('friends', 'n/a')}\n> **Followers:** {data.get('followers', 'n/a')}\n> **Following:** {data.get('followings', 'n/a')}")
        
        created_at = data.get('created_at', None)
        created_at_formatted = format_dt(datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S'), 'R') if created_at else 'n/a'
        embed.add_field(name="Created", value=f"> **At:** {created_at_formatted}")
        
        view = View()
        profile = Button(style=discord.ButtonStyle.link, label="Profile", url=data.get("url", ""), emoji=emoji.link)
        view.add_item(profile)
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def cashapp(self, ctx, username: str):
        data = await self.fulcrumapi.cashapp(username)
        
        embed = discord.Embed(color=color.default)
        embed.set_author(name=f"{data.get('display_name', 'unknown')} | {data.get('username', 'n/a')}")
        embed.set_thumbnail(url=data.get("avatar", ""))
        embed.add_field(name="Profile Info", value=f"> **Verified:** {'Yes' if data.get('verified') else 'No'}", inline=True)
        
        view = View()
        profile = Button(style=discord.ButtonStyle.link, label="Profile", url=data.get("url", ""), emoji=emoji.link)
        qr_code = Button(style=discord.ButtonStyle.link, label="QR Code", url=data.get("qr_url", ""), emoji=emoji.link)
        
        view.add_item(profile)
        view.add_item(qr_code)
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def weather(self, ctx, city: str):
        data = await self.fulcrumapi.weather(city)
        
        city_name = data.get('city', 'unknown')
        country = data.get('country', 'unknown')
        time = data.get('timestring', 'unavailable')
        last_updated = data.get('last_updated', 'unknown')
        celsius = data.get('celsius', 'n/a')
        fahrenheit = data.get('fahrenheit', 'n/a')
        feelslike_c = data.get('feelslike_c', 'n/a')
        feelslike_f = data.get('feelslike_f', 'n/a')
        wind_mph = data.get('wind_mph', 'n/a')
        wind_kph = data.get('wind_kph', 'n/a')
        condition_text = data.get('condition_text', 'no data')
        condition_icon = data.get('condition_icon', '')
        humidity = data.get('humidity', 'n/a')
        
        embed = discord.Embed(color=color.default, description=f"> {condition_text}")
        embed.set_author(name=f"{city_name}, {country} | {time}")
        embed.set_thumbnail(url=condition_icon)
        embed.add_field(name="Temp", value=f"> **C:** {celsius}°C\n> **F:** {fahrenheit}°F")
        embed.add_field(name="Feels", value=f"> **C:** {feelslike_c}°C\n> **F:** {feelslike_f}°F")
        embed.add_field(name="Wind", value=f"> **MPH:** {wind_mph} mph\n> **KPH:** {wind_kph} kph")
        embed.add_field(name="Extras", value=f"> **Humidity:** {humidity}%\n> **Last Updated:** {last_updated}")
        
        view = View()
        more_info = Button(style=discord.ButtonStyle.link, label="More Info", url=f"https://www.weather.com/weather/today/l/{city_name}", emoji="🔗")
        view.add_item(more_info)
        
        await ctx.send(embed=embed, view=view)

async def setup(client):
    await client.add_cog(Network(client))
