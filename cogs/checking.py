import datetime
import io
import asyncio
import time
import urllib.request

import aiosqlite
import discord
from PIL import Image
from discord.ext import commands
import discordSuperUtils
from pycord_components import (
    Button,
    ButtonStyle,
    Select,
    SelectOption,
    Interaction
)
class invitetracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ImageManager = discordSuperUtils.ImageManager()
        self.InviteTracker = discordSuperUtils.InviteTracker(self.bot)

    async def cog_before_invoke(self, ctx: commands.Context):
        print(ctx.command)
        if ctx.command.name != '메일':
            database = await aiosqlite.connect("db/db.sqlite")
            cur = await database.execute(f"SELECT * FROM uncheck WHERE user_id = ?", (ctx.author.id,))
            if await cur.fetchone() == None:
                cur = await database.execute(f"SELECT * FROM mail")
                mails = await cur.fetchall()
                check = 0
                for j in mails:
                    check += 1
                mal = discord.Embed(title=f"📫하린봇 메일함 | {str(check)}개 수신됨",
                                    description="아직 읽지 않은 메일이 있어요.'`하린아 메일`'로 확인하세요.\n주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                                    colour=ctx.author.colour)
                return await ctx.send(embed=mal)
            cur = await database.execute(f"SELECT * FROM mail")
            mails = await cur.fetchall()
            check = 0
            for j in mails:
                check += 1
            cur = await database.execute(f"SELECT * FROM uncheck WHERE user_id = ?", (ctx.author.id,))
            CHECK = await cur.fetchone()
            if str(check) == str(CHECK[1]):
                pass
            else:
                mal = discord.Embed(title=f"📫하린봇 메일함 | {str(int(check) - int(CHECK[1]))}개 수신됨",
                                    description="아직 읽지 않은 메일이 있어요.'`하린아 메일`'로 확인하세요.\n주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                                    colour=ctx.author.colour)
                await ctx.send(embed=mal)

    @commands.group(name="출석체크",aliases=["출쳌","출첵"],invoke_without_command=True)
    async def chulcheck(self,ctx):
        now = datetime.datetime.now()
        dates = f"{now.year}-{now.month}-{now.day}"
        db = await aiosqlite.connect("db/db.sqlite")
        cur = await db.execute("SELECT * FROM chulcheck WHERE user = ? AND stand = ?",(ctx.author.id,dates))
        res = await cur.fetchone()
        if res != None:
            times = res[1]
            timestamp = time.mktime(datetime.datetime.strptime(times, '%Y-%m-%d %H:%M:%S').timetuple())
            return await ctx.reply(f"이미 출석체크를 하셨어요!\n출석체크일시 - <t:{str(timestamp)[:-2]}:R>")
        await db.execute("INSERT INTO chulcheck(user) VALUES (?)",(ctx.author.id,))
        await db.commit()
        dates = f"{now.year}-{now.month}-{now.day}"
        await ctx.reply(f"출석체크를 완료했어요!\n출석체크일시 - {now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}")
        cur = await db.execute("SELECT * FROM chulcheck WHERE stand = ? ORDER BY dates", (dates,))
        res = await cur.fetchall()
        check_list = []
        num = 0
        for i in res:
            num += 1
            check_list.append(f"{num}. {self.bot.get_user(i[0])} | {i[1]}")
        leaderboard = "\n".join(check_list)
        em = discord.Embed(
            title="오늘의 출석체크 리더보드",
            description=f"누가 가장먼저 출석체크를 했을까요?```fix\n{leaderboard}```"
        )
        await ctx.send(embed=em)

    @chulcheck.command(name="리더보드")
    async def chulcheck_leaderboard(self,ctx):
        async def btn_callback(interaction: Interaction):
            if interaction.custom_id == "close":
                await interaction.message.delete()
        async def callback(interaction: Interaction):
            values = interaction.values[0]
            if interaction.user.id == ctx.author.id:
                cur = await db.execute("SELECT * FROM chulcheck WHERE stand = ? ORDER BY dates", (values,))
                res = await cur.fetchall()
                check_list = []
                num = 0
                for i in res:
                    num += 1
                    check_list.append(f"{num}. {self.bot.get_user(i[0])} | {i[1]}")
                leaderboard = "\n".join(check_list)
                #cur = await db.execute("SELECT * FROM chulcheck", (dates,))
                #res = await cur.fetchall()
                em = discord.Embed(
                    title=f"{values} | 출석체크 리더보드",
                    description=f"누가 가장먼저 출석체크를 했을까요?```fix\n{leaderboard}```"
                )
                dates = [i[2] for i in res]
                new_dates = []
                for i in dates:
                    if i not in new_dates:
                        new_dates.append(i)
                await interaction.edit_origin(embed=em,
            components=[
                self.bot.components_manager.add_callback(
                    Select(
                        options=[
                            SelectOption(label=i, value=i) for i in new_dates
                        ],
                    ),
                    callback,
                ),
                self.bot.components_manager.add_callback(
                    Button(label="메세지 닫기", style=4, custom_id="close", emoji="❎"
                           ),
                    btn_callback,
                )
            ])
        db = await aiosqlite.connect("db/db.sqlite")
        cur = await db.execute("SELECT * FROM chulcheck")
        res = await cur.fetchall()
        dates = [i[2] for i in res]
        new_dates = []
        for i in dates:
            if i not in new_dates:
                new_dates.append(i)
        print(new_dates)
        await ctx.reply(
            "조회할 리더보드 일정을 선택해주세요.",
            components=[
                self.bot.components_manager.add_callback(
                    Select(
                        options=[
                            SelectOption(label=i, value=i) for i in new_dates
                        ],
                    ),
                    callback,
                ),
                self.bot.components_manager.add_callback(
                    Button(label="메세지 닫기",style=4,custom_id="close",emoji="❎"
                    ),
                    btn_callback,
                )
            ]
        )


def setup(bot):
    bot.add_cog(invitetracker(bot))