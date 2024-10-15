import discord
import random
import asyncpg

from discord.ext       import commands
from datetime          import datetime, timedelta
from discord.utils     import format_dt

from tools.config      import emoji, color
from tools.context     import Context

class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cooldowns = {}

    async def bal(self, user_id):
        result = await self.client.pool.fetchrow("SELECT balance FROM economy WHERE user_id = $1;", user_id)
        if result is None:
            await self.client.pool.execute("INSERT INTO economy (user_id, balance) VALUES ($1, 0);", user_id)
            return 0
        return result['balance']

    async def upd_bal(self, user_id, amount):
        await self.client.pool.execute("UPDATE economy SET balance = balance + $1 WHERE user_id = $2;", amount, user_id)

    def format_duration(self, duration):
        total_seconds = int(duration.total_seconds())
        minutes, seconds = divmod(total_seconds, 60)
        return f"{minutes}m {seconds}s"

    async def cooldown(self, ctx, cmd, cooldown):
        now = datetime.utcnow()
        if (ctx.author.id, cmd) in self.cooldowns:
            last_used = self.cooldowns[(ctx.author.id, cmd)]
            if (now - last_used).total_seconds() < cooldown:
                remaining_time = timedelta(seconds=cooldown) - (now - last_used)
                await ctx.deny(f"You need to wait {format_dt(now + remaining_time, 'R')} before using {cmd} again")
                return False
        self.cooldowns[(ctx.author.id, cmd)] = now
        return True

    async def streaks(self, ctx, streak_type, base_amount, message):
        user_id = ctx.author.id
        now = datetime.utcnow()

        row = await self.client.pool.fetchrow("SELECT last_claimed, streak FROM streaks WHERE user_id = $1 AND type = $2;", user_id, streak_type)

        if row:
            last_claimed, streak = row['last_claimed'], row['streak']
            time_diff = now - last_claimed

            if (streak_type == 'daily' and time_diff < timedelta(days=1)) or (streak_type == 'weekly' and time_diff < timedelta(weeks=1)):
                remaining_time = timedelta(days=1) - time_diff if streak_type == 'daily' else timedelta(weeks=1) - time_diff
                await ctx.deny(f"You need to wait {format_dt(now + remaining_time, 'R')} before claiming your {message}")
                return

            if (streak_type == 'daily' and time_diff > timedelta(days=3)) or (streak_type == 'weekly' and time_diff > timedelta(days=10)):
                streak = 0
        else:
            streak = 0

        streak += 1
        reward = (base_amount * 2) * streak 

        await self.client.pool.execute(
            """INSERT INTO streaks (user_id, type, last_claimed, streak) VALUES ($1, $2, $3, $4)
               ON CONFLICT (user_id, type) DO UPDATE SET last_claimed = $3, streak = $4;""",
            user_id, streak_type, now, streak
        )
        await self.upd_bal(user_id, reward)
        await ctx.agree(f"You claimed your **{message}** and received {reward}💵, your streak is now {streak}")

    @commands.command(aliases=["bal"])
    async def balance(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        balance = await self.bal(user.id)

        user_pfp = user.avatar.url if user.avatar else user.default_avatar.url
        if user == ctx.author:
            embed = discord.Embed(description=f"> You **have** {balance} 💵", color=color.default)
        else:
            embed = discord.Embed(description=f"> {user.mention} **has** {balance} 💵", color=color.default)

        embed.set_author(name=ctx.author.name, icon_url=user_pfp)
        await ctx.send(embed=embed)

    @commands.command()
    async def work(self, ctx):
        if not await self.cooldown(ctx, 'work', 60):
            return
            
        messages = ["at McDonald's", "at the homeless shelter"]
        amount = random.randint(350, 1250)
        
        await self.upd_bal(ctx.author.id, amount)
        await ctx.agree(f"You **worked** {random.choice(messages)} and earned {amount}💵")

    @commands.command()
    async def slut(self, ctx):
        if not await self.cooldown(ctx, 'slut', 300):
            return
        amount = random.randint(500, 1500)
        await self.upd_bal(ctx.author.id, amount)
        await ctx.agree(f"You **worked** as a prostitute and earned {amount}💵")

    @commands.command()
    async def daily(self, ctx):
        await self.streaks(ctx, 'daily', 750, "daily reward")

    @commands.command()
    async def weekly(self, ctx):
        await self.streaks(ctx, 'weekly', 1500, "weekly reward")

# UNFINISHED

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

        embed = discord.Embed(title="Economy Leaderboard", color=color.default)
        for i, row in enumerate(leaderboard, 1):
            user = self.client.get_user(row['user_id']) or await self.client.fetch_user(row['user_id'])
            embed.add_field(name=f"#{i} {user.name}", value=f"**{row['balance']} 💵**", inline=False)

        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Economy(client))
