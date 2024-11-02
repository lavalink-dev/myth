from system.myth import Myth

async def setup(bot: Myth) -> None:
    from .information import Information
    await bot.add_cog(Information(bot))
