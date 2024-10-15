import discord
from discord.ext import commands
import random
from datetime import datetime, timedelta

class CooldownManager:
    def __init__(self):
        self.cooldowns = {}

    def is_on_cooldown(self, user_id, command_name, cooldown_time):
        now = datetime.utcnow()
        if (user_id, command_name) not in self.cooldowns:
            return False
        last_used = self.cooldowns[(user_id, command_name)]
        if (now - last_used).total_seconds() < cooldown_time:
            return True
        return False

    def update_cooldown(self, user_id, command_name):
        self.cooldowns[(user_id, command_name)] = datetime.utcnow()

class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cooldown_manager = CooldownManager()

    async def bal(self, user_id):
        result = await self.client.pool.fetchrow("SELECT balance FROM economy WHERE user_id = $1;", user_id)
        if result is None:
            await self.client.pool.execute("INSERT INTO economy (user_id, balance) VALUES ($1, 0);", user_id)
            return 0
        return result['balance']

    async def upd_bal(self, user_id, amount):
        await self.client.pool.execute("UPDATE economy SET balance = balance + $1 WHERE user_id = $2;", amount, user_id)

    @commands.command(aliases=["bal"])
    async def balance(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        balance = await self.bal(ctx.author.id)

        user_pfp = member.avatar.url if member.avatar else member.default_avatar.url
        
        if member == ctx.author:
            embed = discord.Embed(description=f"> You **have** {balance} 💵", color=color.default)
            embed.set_author(name=ctx.author.name, icon_url=user_pfp)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f">  {member.mention} **Has** {balance} 💵", color=color.default)
            embed.set_author(name=ctx.author.name, icon_url=user_pfp)
            await ctx.send(embed=embed)

    @commands.command()
    async def work(self, ctx):
        amount = random.randint(350, 1250)
        await self.upd_bal(ctx.author.id, amount)
        await ctx.send(f"{ctx.author.mention}, you worked and earned ${amount}!")

    @commands.command()
    async def slut(self, ctx):
        amount = random.randint(500, 1500)
        await self.upd_bal(ctx.author.id, amount)
        await ctx.send(f"{ctx.author.mention}, you earned ${amount}!")

    @commands.command()
    async def daily(self, ctx):
        await self.streaks(ctx, 'daily', 1500, "daily reward")

    @commands.command()
    async def weekly(self, ctx):
        await self.streaks(ctx, 'weekly', 3000, "weekly reward")

    async def streaks(self, ctx, streak_type, base_amount, message):
        user_id = ctx.author.id
        now = datetime.utcnow()

        row = await self.client.pool.fetchrow("SELECT last_claimed, streak FROM streaks WHERE user_id = $1 AND type = $2;", user_id, streak_type)

        if row:
            last_claimed, streak = row['last_claimed'], row['streak']
            time_diff = now - last_claimed

            if (streak_type == 'daily' and time_diff < timedelta(days=1)) or (streak_type == 'weekly' and time_diff < timedelta(weeks=1)):
                await ctx.send(f"{ctx.author.mention}, you've already claimed your {message}!")
                return
            if (streak_type == 'daily' and time_diff > timedelta(days=2)) or (streak_type == 'weekly' and time_diff > timedelta(weeks=2)):
                streak = 0
        else:
            streak = 0

        streak += 1
        reward = base_amount * streak

        await self.client.pool.execute(
            """INSERT INTO streaks (user_id, type, last_claimed, streak) VALUES ($1, $2, $3, $4)
               ON CONFLICT (user_id, type) DO UPDATE SET last_claimed = $3, streak = $4;""",
            user_id, streak_type, now, streak
        )
        await self.upd_bal(user_id, reward)
        await ctx.send(f"{ctx.author.mention}, you claimed your {message} and received ${reward}! Your streak is now {streak}.")

    @commands.command()
    async def coinflip(self, ctx, choice: str, amount: int):
        if choice.lower() not in ["heads", "tails"]:
            await ctx.send("Please choose either heads or tails!")
            return

        balance = await self.bal(ctx.author.id)
        if amount > balance:
            await ctx.send(f"{ctx.author.mention}, you don't have enough money to gamble that much!")
            return

        result = random.choice(["heads", "tails"])
        if choice.lower() == result:
            winnings = amount * 2
            await self.upd_bal(ctx.author.id, winnings)
            await ctx.send(f"Congratulations {ctx.author.mention}, you won! It was {result}. You earned ${winnings}.")
        else:
            await self.upd_bal(ctx.author.id, -amount)
            await ctx.send(f"Sorry {ctx.author.mention}, you lost! It was {result}.")

    @commands.command()
    async def gamble(self, ctx, amount: int):
        if amount <= 0:
            await ctx.send(f"{ctx.author.mention}, you must gamble a positive amount!")
            return
        
        balance = await self.bal(ctx.author.id)
        if amount > balance:
            await ctx.send(f"{ctx.author.mention}, you don't have enough money to gamble that much!")
            return

        if random.random() < 0.5:
            winnings = amount * 2
            await self.upd_bal(ctx.author.id, winnings)
            await ctx.send(f"Congratulations {ctx.author.mention}, you won and doubled your money!")
        else:
            await self.upd_bal(ctx.author.id, -amount)
            await ctx.send(f"Sorry {ctx.author.mention}, you lost ${amount}.")

    @commands.command()
    async def pay(self, ctx, member: discord.Member, amount: int):
        if amount <= 0:
            await ctx.send(f"{ctx.author.mention}, you must send a positive amount!")
            return

        balance = await self.bal(ctx.author.id)
        if amount > balance:
            await ctx.send(f"{ctx.author.mention}, you don't have enough money to send that much!")
            return

        await self.upd_bal(ctx.author.id, -amount)
        await self.upd_bal(member.id, amount)
        await ctx.send(f"{ctx.author.mention} has sent ${amount} to {member.mention}.")

    @commands.command()
    async def rob(self, ctx, member: discord.Member):
        balance = await self.bal(member.id)
        if balance < 500:
            await ctx.send(f"{member.mention} doesn't have enough money to be worth robbing!")
            return

        if random.random() < 0.5:
            stolen_amount = random.randint(100, min(1000, balance))
            await self.upd_bal(ctx.author.id, stolen_amount)
            await self.upd_bal(member.id, -stolen_amount)
            await ctx.send(f"{ctx.author.mention} successfully robbed {member.mention} and stole ${stolen_amount}!")
        else:
            await ctx.send(f"{ctx.author.mention}, your robbery attempt failed!")

    @commands.command()
    async def economylb(self, ctx):
        leaderboard = await self.client.pool.fetch("SELECT user_id, balance FROM economy ORDER BY balance DESC LIMIT 10;")
        if not leaderboard:
            await ctx.send("No data available.")
            return

        embed = discord.Embed(title="Economy Leaderboard", color=discord.Color.gold())
        for rank, entry in enumerate(leaderboard, start=1):
            user = self.client.get_user(entry['user_id'])
            embed.add_field(name=f"#{rank} {user.mention} **{entry['balance']} 💵**", value="\u200b", inline=False)

        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Economy(client))
