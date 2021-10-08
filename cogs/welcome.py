import io
import asyncio
import urllib.request

import discord
from PIL import Image
from discord.ext import commands
import discordSuperUtils
class welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ImageManager = discordSuperUtils.ImageManager()

    @commands.Cog.listener("on_member_join")
    async def member_welcome(self,ctx):
        member = ctx.author
        urllib.request.urlretrieve(
            'https://media.discordapp.net/attachments/889514827905630290/894411039326748742/bgimg.jpg',
            "bg.png")

        img = Image.open("bg.png")
        img = await self.ImageManager.create_welcome_card(
                member,
                img,#discordSuperUtils.Backgrounds.DISCORD,#discordSuperUtils.ImageManager.load_asset("bgimg.png")
                f"Welcome!, {member}",
                "plz read this channel #rules",
                title_color=(127, 255, 0),
                description_color=(127, 255, 0),
                font_path="user.ttf",
                transparency=127
            )
        await ctx.send(
            file=img
        )

def setup(bot):
    bot.add_cog(welcome(bot))
