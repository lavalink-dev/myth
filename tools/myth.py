import discord
import asyncpg
import jishaku
import discord_ios
import os
import time

from discord.ext import commands
from asyncpg import Pool

from tools.context import Context

intents = discord.Intents().default()
intents.members = True
intents.message_content = True
intents.messages = True
intents.dm_messages = True

class Myth(commands.AutoShardedBot):
    def __init__(self, token):
        super().__init__(
            command_prefix=self.get_prefix,
            help_command=None,
            intents=intents,
            owner_ids=[394152799799345152, 255841984470712330],
            activity=discord.CustomActivity(name=f"🔗 discord.gg/strict"),  
        )
        self.pool = None 
        self.start_time = time.time()
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

    async def setup_hook(self):
        await self.load_extension('jishaku')
        await self.load("cogs")
        self.pool = await self._load_database()
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
                    print('Database schema loaded')
                else:
                    print('Database schema file is empty')
                file.close()

            return pool
        except Exception as e:
            print(f'Error loading database: {e}')
            raise e
