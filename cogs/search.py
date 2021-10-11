import datetime
import io
import asyncio
import os
import urllib.request

import neispy.error
from neispy import Neispy
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
class search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

    @commands.group(name="학교검색",invoke_without_command=True)
    async def main_school(self,ctx,school=None):
        if school == None:
            return await ctx.reply("학교명을 입력해주세요!")
        msg = await ctx.reply("검색중이니 조금만 기다려주세요! <a:loading:888625946565935167>")
        async with Neispy(KEY=os.getenv("NEIS_TOKEN")) as neis:
            scinfo = await neis.schoolInfo(SCHUL_NM=school)
            if len(scinfo) >= 2:
                await msg.delete()
                many_msg = await ctx.reply(
                    f"학교명이 같은 학교가 `{len(scinfo[:25])}`개 있어요.\n아래에서 검색하시려는 학교를 선택해주세요.",
                    components=[
                        Select(
                            placeholder="학교를 선택해주세요.",
                            options=[
                                SelectOption(label=i.SCHUL_NM, value=f"{i.SD_SCHUL_CODE}",
                                             description="지역 - {}".format(i.LCTN_SC_NM),emoji="🏫") for i in scinfo[:25]
                            ],
                        ),
                    ],
                )
                try:
                    interaction = await self.bot.wait_for("select_option", check=lambda
                        i: i.user.id == ctx.author.id and i.message.id ==many_msg.id, timeout=30)
                    value = interaction.values[0]
                    # stamp = str(time.mktime(datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S').timetuple()))[:-2]
                except asyncio.TimeoutError:
                    await many_msg.delete()
                    return

                for i in scinfo:
                    if i.SD_SCHUL_CODE == value:
                        em = discord.Embed(
                            title=f"{i.SCHUL_NM}| {i.ENG_SCHUL_NM}( {i.LCTN_SC_NM} )",
                            description=f"주소: {i.ORG_RDNMA}\n대표번호: {i.ORG_TELNO}\nFax: {i.ORG_FAXNO}\n홈페이지: {i.HMPG_ADRES}",
                            colour=discord.Colour.random()
                        )
                        em.add_field(name="소속교육청",value=f"```{i.ATPT_OFCDC_SC_NM}```")
                        em.add_field(name="타입",value=f"```{i.COEDU_SC_NM} | {i.HS_SC_NM}```")
                        await many_msg.edit(embed=em,components=[])
            else:
                em = discord.Embed(
                    title=f"{scinfo[0].SCHUL_NM}| {scinfo[0].ENG_SCHUL_NM}( {scinfo[0].LCTN_SC_NM} )",
                    description=f"주소: {scinfo[0].ORG_RDNMA}\n대표번호: {scinfo[0].ORG_TELNO}\nFax: {scinfo[0].ORG_FAXNO}\n홈페이지: {scinfo[0].HMPG_ADRES}",
                    colour=discord.Colour.random()
                )
                em.add_field(name="소속교육청", value=f"```{scinfo[0].ATPT_OFCDC_SC_NM}```")
                em.add_field(name="타입", value=f"```{scinfo[0].COEDU_SC_NM} | {scinfo[0].HS_SC_NM}```")
                await msg.delete()
                await ctx.reply(embed=em)

    @main_school.command(name="급식")
    async def school_meal(self,ctx,school=None,dates = None):
        if school == None:
            return await ctx.reply("학교명을 입력해주세요!")
        if dates == None:
            now = datetime.datetime.now()
            dates = f"{now.year}{now.month}{now.day}"
        msg = await ctx.reply("검색중이니 조금만 기다려주세요! <a:loading:888625946565935167>")
        neis = Neispy(KEY=os.getenv("NEIS_TOKEN"))
        scinfo = await neis.schoolInfo(SCHUL_NM=school)
        if len(scinfo) >= 2:
            await msg.delete()
            many_msg = await ctx.reply(
                f"학교명이 같은 학교가 `{len(scinfo[:25])}`개 있어요.\n아래에서 검색하시려는 학교를 선택해주세요.",
                components=[
                    Select(
                        placeholder="학교를 선택해주세요.",
                        options=[
                            SelectOption(label=i.SCHUL_NM, value=i.SD_SCHUL_CODE,
                                         description="지역 - {}".format(i.LCTN_SC_NM),emoji="🏫") for i in scinfo[:25]
                        ],
                    ),
                ],
            )
            print(many_msg.id)
            try:
                interaction = await self.bot.wait_for("select_option", check=lambda
                    i: i.user.id == ctx.author.id and i.message.id == many_msg.id, timeout=30)
                value = interaction.values[0]
                # stamp = str(time.mktime(datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S').timetuple()))[:-2]
            except asyncio.TimeoutError:
                await many_msg.delete()
                return
            print(value)
            for i in scinfo:
                if i.SD_SCHUL_CODE == value:
                    AE = i.ATPT_OFCDC_SC_CODE  # 교육청코드
                    SE = i.SD_SCHUL_CODE  # 학교코드
                    diet_dict = {
                        "1":"조식",
                        "2":"중식",
                        "3":"석식"
                    }
                    async def callback(interaction:Interaction):
                        values = interaction.values[0]
                        print(values)
                        if interaction.user.id == ctx.author.id:
                            try:
                                scmeal = await neis.mealServiceDietInfo(AE, SE, MLSV_YMD=dates, MMEAL_SC_CODE=values)
                            except neispy.error.DataNotFound:
                                await interaction.send(f"선택하신 `{diet_dict[values]}`의 메뉴를 찾을 수 없어요..")
                                return
                            meal = scmeal[0].DDISH_NM.replace("<br/>", "\n")
                            em = discord.Embed(
                                title=f"{i.SCHUL_NM} | {diet_dict[values]}",
                                description=f"```fix\n{meal}```"
                            )
                            await interaction.edit_origin(embed=em,components=[
                            self.bot.components_manager.add_callback(
                                Select(
                                    options=[
                                        SelectOption(label="조식", value="1",emoji="🌅"),
                                        SelectOption(label="중식", value="2",emoji="☀"),
                                        SelectOption(label="석식", value="3",emoji="🌙")
                                    ],
                                ),
                                callback,
                            )
                        ])
                    await many_msg.delete()
                    await ctx.reply(
                        "조회할 급식을 선택해주세요.",
                        components=[
                            self.bot.components_manager.add_callback(
                                Select(
                                    options=[
                                        SelectOption(label="조식", value="1",emoji="🌅"),
                                        SelectOption(label="중식", value="2",emoji="☀"),
                                        SelectOption(label="석식", value="3",emoji="🌙")
                                    ],
                                ),
                                callback,
                            )
                        ]
                    )
        else:
            AE = scinfo[0].ATPT_OFCDC_SC_CODE  # 교육청코드
            SE = scinfo[0].SD_SCHUL_CODE  # 학교코드
            diet_dict = {
                "1": "조식",
                "2": "중식",
                "3": "석식"
            }

            async def callback(interaction: Interaction):
                values = interaction.values[0]
                print(values)
                if interaction.user.id == ctx.author.id:
                    try:
                        scmeal = await neis.mealServiceDietInfo(AE, SE, MLSV_YMD=dates, MMEAL_SC_CODE=values)
                    except neispy.error.DataNotFound:
                        await interaction.send(f"선택하신 `{diet_dict[values]}`의 메뉴를 찾을 수 없어요..")
                        return
                    meal = scmeal[0].DDISH_NM.replace("<br/>", "\n")
                    em = discord.Embed(
                        title=f"{scinfo[0].SCHUL_NM} | {diet_dict[values]}",
                        description=f"```fix\n{meal}```"
                    )
                    await interaction.edit_origin(embed=em,components=[
                            self.bot.components_manager.add_callback(
                                Select(
                                    options=[
                                        SelectOption(label="조식", value="1",emoji="🌅"),
                                        SelectOption(label="중식", value="2",emoji="☀"),
                                        SelectOption(label="석식", value="3",emoji="🌙")
                                    ],
                                ),
                                callback,
                            )
                        ])

            await msg.delete()
            await ctx.reply(
                "조회할 급식을 선택해주세요.",
                components=[
                    self.bot.components_manager.add_callback(
                        Select(
                            options=[
                                SelectOption(label="조식", value="1", emoji="🌅"),
                                SelectOption(label="중식", value="2", emoji="☀"),
                                SelectOption(label="석식", value="3", emoji="🌙")
                            ],
                        ),
                        callback,
                    )
                ]
            )




def setup(bot):
    bot.add_cog(search(bot))