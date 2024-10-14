import discord
import asyncpg

from discord.ext       import commands

from tools.context     import Context
from tools.config      import emoji, color

class Reactionroles(commands.Cog):
    def __init__(self, client):
        self.client = client




async def setup(client):
    await client.add_cog(Reactionroles(client))
