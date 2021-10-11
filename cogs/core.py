import io
import asyncio
import urllib.request
import aiosqlite
import discord
from PIL import Image
from discord.ext import commands
import discordSuperUtils
import random
from typing import List


class core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(name="하린아 도움 | 서버: {}".format(len(self.bot.guilds)),
                                                                                               type=discord.ActivityType.playing))
        if guild.id == 653083797763522580 or guild.id == 786470326732587008:
            return
        em = discord.Embed(
            title="초대해줘서 고마워요!",
            description="""
하린봇을 초대주셔서 감사드립니다.
하린봇은 유저 친화적이며 다기능봇입니다.

도움말은 `하린아 도움`,
프리픽스는 `하린아 `,`하린아`,`ㅎ `,`ㅎ` 입니다.            
"""
        )
        em.set_thumbnail(url=self.bot.user.avatar_url)
        em.set_image(
            url="https://media.discordapp.net/attachments/889514827905630290/896359450544308244/37cae031dc5a6c40.png")
        try:
            await guild.owner.send(embed=em)
        except:
            ch = self.bot.get_channel((random.choice(guild.channels)).id)
            await ch.send(embed=em)
        em = discord.Embed(
            description=f"{guild.name}({guild.id})에 접속함\n서버수 : {len(self.bot.guilds)}"
        )
        await self.bot.get_channel(896635424867495936).send(embed=em)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Activity(name="하린아 도움 | 서버: {}".format(len(self.bot.guilds)),
                                                                 type=discord.ActivityType.playing))
        em = discord.Embed(
            description=f"{guild.name}({guild.id})에 접속함\n서버수 : {len(self.bot.guilds)}"
        )
        await self.bot.get_channel(896635424867495936).send(embed=em)


def setup(bot):
    bot.add_cog(core(bot))