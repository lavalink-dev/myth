from __future__        import annotations

import discord
import uuid

from discord.ext       import commands

from tools.config      import emoji, color


class Simple(discord.ui.View):
    def __init__(self, *,
                 timeout: int = None,
                 PreviousButton: discord.ui.Button = discord.ui.Button(emoji='<:left:1284955832911663225>', style=discord.ButtonStyle.primary),
                 NextButton: discord.ui.Button = discord.ui.Button(emoji='<:right:1284955811084505220>', style=discord.ButtonStyle.primary),
                 ExitButton: discord.ui.Button = discord.ui.Button(emoji='<:exit:1284955853778190398>', style=discord.ButtonStyle.grey),
                 InitialPage: int = 0,
                 AllowExtInput: bool = True,
                 ephemeral: bool = False) -> None:
        super().__init__(timeout=timeout)

        self.PreviousButton = PreviousButton
        self.NextButton = NextButton
        self.ExitButton = ExitButton
        self.InitialPage = InitialPage
        self.AllowExtInput = AllowExtInput
        self.ephemeral = ephemeral

        self.pages = None
        self.ctx = None
        self.message = None
        self.current_page = None
        self.total_page_count = None

        self.paginator_id = str(uuid.uuid4())

        self.PreviousButton.custom_id = f"previous:{self.paginator_id}"
        self.NextButton.custom_id = f"next:{self.paginator_id}"
        self.ExitButton.custom_id = f"exit:{self.paginator_id}"

        self.PreviousButton.callback = self.previous_button_callback
        self.NextButton.callback = self.next_button_callback
        self.ExitButton.callback = self.exit_button_callback

        self.add_item(self.PreviousButton)
        self.add_item(self.NextButton)
        self.add_item(self.ExitButton)

    async def start(self, ctx: discord.Interaction | commands.Context, pages: list[discord.Embed]):
        if isinstance(ctx, discord.Interaction):
            ctx = await commands.Context.from_interaction(ctx)

        self.pages = pages
        self.total_page_count = len(pages)
        self.ctx = ctx
        self.current_page = self.InitialPage

        self.message = await ctx.send(embed=self.pages[self.InitialPage], view=self, ephemeral=self.ephemeral)

    async def previous(self):
        if self.current_page == 0:
            self.current_page = self.total_page_count - 1
        else:
            self.current_page -= 1

        await self.message.edit(embed=self.pages[self.current_page], view=self)

    async def exit(self):
        await self.message.delete()

    async def next(self):
        if self.current_page == self.total_page_count - 1:
            self.current_page = 0
        else:
            self.current_page += 1

        await self.message.edit(embed=self.pages[self.current_page], view=self)

    async def next_button_callback(self, interaction: discord.Interaction):
        if interaction.data['custom_id'] != f"next:{self.paginator_id}":
            return

        if interaction.user != self.ctx.author and not self.AllowExtInput:
            embed = discord.Embed(description=f"{emoji.deny} {interaction.user.mention}: You **cannot** intract with this", color=color.deny)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.next()
        await interaction.response.defer()

    async def exit_button_callback(self, interaction: discord.Interaction):
        if interaction.data['custom_id'] != f"exit:{self.paginator_id}":
            return

        if interaction.user != self.ctx.author and not self.AllowExtInput:
            embed = discord.Embed(description=f"{emoji.deny} {interaction.user.mention}: You **cannot** intract with this", color=color.default)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.exit()
        await interaction.response.defer()

    async def previous_button_callback(self, interaction: discord.Interaction):
        if interaction.data['custom_id'] != f"previous:{self.paginator_id}":
            return

        if interaction.user != self.ctx.author and not self.AllowExtInput:
            embed = discord.Embed(description=f"{emoji.deny} {interaction.user.mention}: You **cannot** intract with this", color=color.deny)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.previous()
        await interaction.response.defer()
