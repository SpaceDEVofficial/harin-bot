import io
import asyncio
import discord
from discord.ext import commands
import discordSuperUtils
class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ImageManager = discordSuperUtils.ImageManager()

    @commands.command(name="ping")
    async def test_welcome(self,ctx):
        member = ctx.author

        await ctx.send(
            file=await self.ImageManager.create_welcome_card(
                member,
                discordSuperUtils.Backgrounds.GALAXY,
                f"어서오세요, {member}님!",
                "#rules 채널을 읽어주세요.",
                title_color=(127, 255, 0),
                description_color=(127, 255, 0),
                font_path="user.ttf"
            )
        )

def setup(bot):
    bot.add_cog(general(bot))
