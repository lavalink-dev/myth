import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
from discord.utils import format_dt
import random
from datetime import datetime, timedelta

class Giveaway(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.check_giveaway.start()

    @commands.command()
    async def start_giveaway(self, ctx, duration: int, prize: str):
        # Calculate end time and format it
        end_time = datetime.utcnow() + timedelta(seconds=duration)
        formatted_time = format_dt(end_time, style="R")

        # Embed setup
        embed = discord.Embed(
            title="🎉 Giveaway!",
            description=f"Prize: **{prize}**\nEnds {formatted_time}",
            color=discord.Color.blurple()
        )

        # Message and button setup
        message = await ctx.send(embed=embed)
        button = Button(label="Enter Giveaway", style=discord.ButtonStyle.primary)
        
        async def button_callback(interaction: discord.Interaction):
            # Call the enter_giveaway function to handle the entry
            await self.enter_giveaway(interaction, message.id)
        
        button.callback = button_callback
        view = View()
        view.add_item(button)
        await message.edit(view=view)

        # Store the giveaway in the database
        await self.client.pool.execute(
            "INSERT INTO giveaways (guild_id, message_id, end_time, prize) VALUES ($1, $2, $3, $4)",
            ctx.guild.id, message.id, end_time, prize
        )

    async def enter_giveaway(self, interaction: discord.Interaction, message_id: int):
        # Fetch the giveaway by message_id
        giveaway = await self.client.pool.fetchrow(
            "SELECT * FROM giveaways WHERE message_id = $1", message_id
        )
        
        if not giveaway:
            await interaction.response.send_message("This giveaway has ended or doesn't exist.", ephemeral=True)
            return

        user_id = interaction.user.id
        participants = await self.client.pool.fetch(
            "SELECT user_id FROM giveaway_entries WHERE giveaway_id = $1", giveaway['giveaway_id']
        )

        if any(user['user_id'] == user_id for user in participants):
            await interaction.response.send_message("You've already entered this giveaway!", ephemeral=True)
        else:
            await self.client.pool.execute(
                "INSERT INTO giveaway_entries (giveaway_id, user_id) VALUES ($1, $2)",
                giveaway['giveaway_id'], user_id
            )
            await interaction.response.send_message("You have entered the giveaway!", ephemeral=True)

    @tasks.loop(seconds=10)
    async def check_giveaway(self):
        now = datetime.utcnow()
        giveaways = await self.client.pool.fetch(
            "SELECT * FROM giveaways WHERE end_time <= $1", now
        )

        for giveaway in giveaways:
            guild = self.client.get_guild(giveaway['guild_id'])
            if not guild:
                continue

            try:
                # Fetch the message to locate the channel
                message = await guild.fetch_message(giveaway['message_id'])
                channel = message.channel
                participants = await self.client.pool.fetch(
                    "SELECT user_id FROM giveaway_entries WHERE giveaway_id = $1", giveaway['giveaway_id']
                )

                if participants:
                    winner = random.choice(participants)['user_id']
                    await channel.send(f"🎉 Congratulations <@{winner}>! You won **{giveaway['prize']}**!")
                else:
                    await channel.send(f"No one entered the giveaway for **{giveaway['prize']}**.")
                
                # Clean up database
                await self.client.pool.execute(
                    "DELETE FROM giveaways WHERE giveaway_id = $1", giveaway['giveaway_id']
                )

            except discord.NotFound:
                print(f"Message {giveaway['message_id']} not found in guild {guild.id}. Cleaning up giveaway.")
                await self.client.pool.execute(
                    "DELETE FROM giveaways WHERE giveaway_id = $1", giveaway['giveaway_id']
                )

    @check_giveaway.before_loop
    async def before_check_giveaway(self):
        await self.client.wait_until_ready()

async def setup(client):
    await client.add_cog(Giveaway(client))
