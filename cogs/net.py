import discord
import aiohttp

from discord.ext       import commands
from fulcrum_api       import FulcrumAPI
from discord.ui        import Button, View

from tools.context     import Context
from tools.config      import emoji, color

class Network(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.fulcrumapi = FulcrumAPI()

    @commands.command()
    async def tiktok(self, ctx, username: str):
        data = await self.fulcrumapi.tiktok_user(username)
        embed = discord.Embed(color=color.default, description=f"> {data["bio"] if data["bio"] else "n/a"}")
        embed.set_author(name=f"{data['nickname']} | {data['username']}")
        embed.set_thumbnail(url=data["avatar"])
        embed.add_field(name="Counts", value=f"> **Followers:** {data["followers"]} \n> **Following:** {data["following"]} \n> **Likes:** {data["hearts"]}")
        embed.add_field(name="Extras", value=f"> **ID:** {data['id']} \n> **Verified:** {'Yes' if data['verified'] else 'No'} \n> **Private:** {'Yes' if data['private'] else 'No'} ")
        embed.add_field(name="Videos", value=f"> **Amount:** {data["videos"]}")
        
        view = View()
        profile = Button(style=discord.ButtonStyle.link, label="Profile", url=data["url"], emoji={emoji.link})
        
        view.add_item(profile)
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def twitter(self, ctx, username: str):
        data = await self.fulcrumapi.twitter_user(username)
        embed = discord.Embed(color=color.default, description=f"> {data['bio'] if data['bio'] else 'n/a'}")
        embed.set_author(name=f"{data['display_name']} | {data['username']}")
        embed.set_thumbnail(url=data["avatar"])
        embed.add_field(name="Counts", value=f"> **Followers:** {data['followers']} \n> **Following:** {data['following']} \n> **Posts:** {data['posts']}")
        embed.add_field(name="Extras", value=f"> **ID:** {data['id']} \n> **Verified:** {'Yes' if data['verified'] else 'No'} \n> **Location:** {data['location'] if data['location'] else 'n/a'}")
        embed.add_field(name="Stats", value=f"> **Liked Posts:** {data['liked_posts']} \n> **Tweets:** {data['tweets']} \n> **Created At:** {data['created_at']}")
        
        view = View()
        profile = Button(style=discord.ButtonStyle.link, label="Profile", url=data["url"], emoji=emoji.link)
        
        view.add_item(profile)
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def roblox(self, ctx, username: str):
        data = await self.fulcrumapi.roblox(username)
        embed = discord.Embed(color=color.default, description=f"> {data['bio'] if data['bio'] else 'n/a'}")
        embed.set_author(name=f"{data['display_name']} | {data['username']}")
        embed.set_thumbnail(url=data["avatar"])
        embed.add_field(name="Profile Info", value=f"> **ID:** {data['id']} \n> **Banned:** {'Yes' if data['banned'] else 'No'} \n> **Verified:** {'Yes' if data['verified'] else 'No'}")
        embed.add_field(name="Social", value=f"> **Friends:** {data['friends']} \n> **Followers:** {data['followers']} \n> **Following:** {data['followings']}")
        embed.add_field(name="Account Created", value=f"> **Created At:** {data['created_at']}")

        view = View()
        profile = Button(style=discord.ButtonStyle.link, label="Profile", url=data["url"], emoji=emoji.link)
        
        view.add_item(profile)
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def cashapp(self, ctx, username: str):
        data = await self.fulcrumapi.cashapp(username)
        embed = discord.Embed(color=color.default)
        embed.set_author(name=f"{data['display_name']} | {data['username']}")
        embed.set_thumbnail(url=data["avatar"])
        embed.add_field(name="Profile Info", value=f"> **Verified:** {'Yes' if data['verified'] else 'No'}", inline=True)
        
        view = View()
        profile = Button(style=discord.ButtonStyle.link, label="Profile", url=data["url"], emoji=emoji.link)
        qr_code = Button(style=discord.ButtonStyle.link, label="QR Code", url=data["qr_url"], emoji=emoji.link)
        
        view.add_item(profile)
        view.add_item(qr_code)
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def weather(self, ctx, city: str):
        data = await self.fulcrumapi.weather(city)

        city_name = data.get('city', 'Unknown City')
        country = data.get('country', 'Unknown Country')
        timestring = data.get('timestring', 'Time Unavailable')
        last_updated = data.get('last_updated', 'Unknown')
        celsius = data.get('celsius', 'N/A')
        fahrenheit = data.get('fahrenheit', 'N/A')
        feelslike_c = data.get('feelslike_c', 'N/A')
        feelslike_f = data.get('feelslike_f', 'N/A')
        wind_mph = data.get('wind_mph', 'N/A')
        wind_kph = data.get('wind_kph', 'N/A')
        condition_text = data.get('condition_text', 'No data')
        condition_icon = data.get('condition_icon', '')
        humidity = data.get('humidity', 'N/A')
        
        embed = Embed(color=color.default, description=f"> {condition_text}")
        embed.set_author(name=f"{city_name}, {country} | {timestring}")
        embed.set_thumbnail(url=condition_icon)
        embed.add_field(name="Temperature", value=f"> **Celsius:** {celsius}°C\n> **Fahrenheit:** {fahrenheit}°F")
        embed.add_field(name="Feels Like", value=f"> **Celsius:** {feelslike_c}°C\n> **Fahrenheit:** {feelslike_f}°F")
        embed.add_field(name="Wind", value=f"> **MPH:** {wind_mph} mph\n> **KPH:** {wind_kph} kph")
        embed.add_field(name="Extras", value=f"> **Humidity:** {humidity}% \n> **Last Updated:** {last_updated}")

        view = View()
        more_info = Button(style=discord.ButtonStyle.link, label="More Info", url=f"https://www.weather.com/weather/today/l/{city_name}", emoji="🔗")
        view.add_item(more_info)

        await ctx.send(embed=embed, view=view)

async def setup(client):
    await client.add_cog(Network(client))
