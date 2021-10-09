import io
import asyncio
import urllib.request

<<<<<<< HEAD
import aiosqlite
=======
>>>>>>> origin/main
import discord
from PIL import Image
from discord.ext import commands
import discordSuperUtils
class welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ImageManager = discordSuperUtils.ImageManager()

    @commands.Cog.listener("on_member_join")
<<<<<<< HEAD
    async def member_welcome(self,member):
        database = await aiosqlite.connect("db/db.sqlite")
        cur = await database.execute("SELECT * FROM welcome WHERE guild = ?",(member.guild.id,))
        data = await cur.fetchone()
        if data != None:
            img = await self.ImageManager.create_welcome_card(
                    member,
                    "https://media.discordapp.net/attachments/889514827905630290/896007967915261982/ada.png?width=1056&height=631",#discordSuperUtils.Backgrounds.DISCORD,#discordSuperUtils.ImageManager.load_asset("bgimg.png")
                    f"어서오세요!, {member}님!",
                    "서버 규칙을 확인해주시고 많은 이용부탁드립니다!",
                    title_color=(127, 255, 0),
                    description_color=(127, 255, 0),
                    font_path="user.ttf"
                )
            channel = self.bot.get_channel(data[1])
            await channel.send(
                file=img
            )

def setup(bot):
    bot.add_cog(welcome(bot))
=======
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
>>>>>>> origin/main