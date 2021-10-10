import datetime
import io
import random

import aiosqlite
import discord
from discord.ext import commands

class owner(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="공지")
    @commands.is_owner()
    async def broadcasting(self,ctx,*,value):
        em = discord.Embed(
            title="하린 봇 공지사항!",
            description=value,
            colour=discord.Colour.random()
        )
        em.set_thumbnail(url=self.bot.user.avatar_url)
        em.set_image(url="https://media.discordapp.net/attachments/889514827905630290/896359450544308244/37cae031dc5a6c40.png")
        em.set_footer(text="특정 채널에 받고싶다면 '하린아 설정'으로 설정하세요! 권한 확인 필수!")
        msg = await ctx.reply("발송중...")
        guilds = self.bot.guilds
        ok = []
        ok_guild = []
        success = 0
        failed = 0
        for guild in guilds:
            channels = guild.text_channels
            for channel in channels:
                if guild.id == 653083797763522580 or guild.id == 786470326732587008:
                    break
                if channel.topic is not None:
                    if str(channel.topic).find("-HOnNt") != -1:
                        ok.append(channel.id)
                        ok_guild.append(guild.id)
                        break

        for guild in guilds:
            channels = guild.text_channels
            for channel in channels:
                if guild.id in ok_guild:
                    break
                random_channel = random.choices(channels)
                ok.append(random_channel[0].id)
                break
        for i in ok:
            channel = self.bot.get_channel(i)
            try:
                await channel.send(embed=em)
                success += 1
            except discord.Forbidden:
                failed += 1
                pass
        await msg.edit("발송완료!\n성공: `{ok}`\n실패: `{no}`".format(ok=success,no=failed))

    @commands.command(name="메일작성")
    @commands.is_owner()
    async def mail(self, ctx, *, va_lue):
        database = await aiosqlite.connect("db/db.sqlite")
        cur = await database.execute(f"SELECT * FROM mail")
        mails = await cur.fetchall()
        print(mails)
        check = 1
        try:
            for j in mails:
                check += 1
        except:
            pass
        end = datetime.datetime.now()
        end = end.strftime('%Y-%m-%d %H:%M:%S')
        await database.execute(f"INSERT INTO mail(id,value) VALUES (?,?)", (check, va_lue))
        await database.commit()
        await ctx.send('성공적으로 메일을 발송하였습니다.')

def setup(bot):
    bot.add_cog(owner(bot))