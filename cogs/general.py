import io
import asyncio
import os
import urllib.request

import discord
from PIL import Image
from discord.ext import commands
import discordSuperUtils
class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ImageManager = discordSuperUtils.ImageManager()

    @commands.command(name="ping")
    async def test_welcome(self,ctx):
        member = ctx.author
        img = await self.ImageManager.create_welcome_card(
            member,
            "https://media.discordapp.net/attachments/889514827905630290/896007967915261982/ada.png",  # discordSuperUtils.Backgrounds.DISCORD,#discordSuperUtils.ImageManager.load_asset("bgimg.png")
            f"Welcome!, {member}",
            "plz read this channel #rules",
            title_color=(127, 255, 0),
            description_color=(127, 255, 0),
            font_path="user.ttf",
        )
        await ctx.send(
            file=img
        )

def setup(bot):
    bot.add_cog(general(bot))
