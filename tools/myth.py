import discord
import asyncpg
import jishaku
import aiohttp
import discord_ios
import os
import time

from discord.ext       import commands
from asyncpg           import Pool
from datetime          import datetime, timedelta

from tools.context     import Context
from tools.config      import color, emoji

intents = discord.Intents().default()
intents.members = True
intents.message_content = True
intents.messages = True
intents.dm_messages = True
intents.presences = True

class Myth(commands.AutoShardedBot):
    def __init__(self, token):
        self.message_cache = {}
        self.cache_expiry_seconds = 15
        self.session = None
        self.pool = None
        self.start_time = time.time()
        
        super().__init__(
            command_prefix=self.get_prefix,
            help_command=None,
            intents=intents,
            owner_ids=[
                394152799799345152, # main
                255841984470712330, # solix
                1168186952772747364, # alt
                1282499485536092181 # leon
            ],
            activity=discord.CustomActivity(name=f"🔗 discord.gg/uid"),  
        )
        self.run(token)

    def uptime(self):
        current_time = time.time()
        uptime_seconds = int(current_time - self.start_time)
        uptime_datetime = datetime.utcfromtimestamp(self.start_time)
        return uptime_datetime

    def lines(self):
        total_lines = 0
        for root, _, files in os.walk("."):
            for filename in files:
                if filename.endswith(".py"): 
                    with open(os.path.join(root, filename), "r", encoding="utf-8") as file:
                        lines = file.readlines()
                        total_lines += len(lines)
        return total_lines

    async def get_prefix(self, message):
        if not self.pool: 
            return ';'
        user_id = str(message.author.id)
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow("SELECT prefix FROM prefixes WHERE user_id = $1", user_id)
        return result['prefix'] if result else ';'

    async def load(self, directory):
        for filename in os.listdir(directory):
            if filename.endswith('.py'):
                await self.load_extension(f'{directory}.{filename[:-3]}')

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        author_id_str = str(message.author.id)

        check = await self.pool.fetchrow("SELECT * FROM blacklist WHERE user_id = $1", author_id_str)
        if check:
            return

        prefix = await self.get_prefix(message)
        if not message.content.startswith(tuple(prefix)):
            return

        now = time.time()
        author_id = message.author.id

        if author_id not in self.message_cache:
            self.message_cache[author_id] = []

        self.message_cache[author_id] = [
            timestamp for timestamp in self.message_cache[author_id]
            if now - timestamp < self.cache_expiry_seconds
        ]

        if len(self.message_cache[author_id]) >= 10:
            await self.pool.execute("INSERT INTO blacklist (user_id) VALUES ($1)", author_id_str)
            embed = discord.Embed(description=f"> {emoji.deny} {message.author.mention}: **You got blacklisted,** if you think is by accident join the [support server](https://discord.gg/uid)", color=color.deny)
            await message.channel.send(embed=embed)
        else:
            self.message_cache[author_id].append(now)
            await self.process_commands(message)

    async def uid(self, user_id):
        existing_uid = await self.pool.fetchrow("SELECT uid FROM uids WHERE user_id = $1", user_id)
        if existing_uid:
            return existing_uid['uid']

        new_uid = await self.pool.execute("INSERT INTO uids (user_id) VALUES ($1) RETURNING uid", user_id)
        return new_uid

    async def on_command(self, ctx):
        user_id = ctx.author.id
        uid = await self.uid(user_id)

    async def setup_hook(self):
        await self.load_extension('jishaku')
        await self.load("cogs")
        self.pool = await self._load_database()
        self.session = aiohttp.ClientSession()
        print(f"[ + ] {self.user} is ready")
 
    async def get_context(self, origin, cls=Context):
        return await super().get_context(origin, cls=cls)

    async def _load_database(self) -> Pool:
        try:
            pool = await asyncpg.create_pool(
                **{var: os.environ[f'DATABASE_{var.upper()}' if var != 'database' else 'DATABASE'] for var in ['database', 'user', 'password', 'host']},
                max_size=30,
                min_size=10,
            )
            print('Database connection established')

            with open('tools/schema/schema.sql', 'r') as file:
                schema = file.read()
                if schema.strip():
                    await pool.execute(schema)
                    print("[ + ] Loaded the database schema")
                else:
                    print("[ . ] Database schema file is empty")
                file.close()

            return pool
        except Exception as e:
            print(f"[ ! ] Error loading database: {e}")
            raise e
