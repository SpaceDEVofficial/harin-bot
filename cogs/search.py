import asyncio
import datetime
import os
import aiosqlite
import discord
import neispy.error
from discord.ext import commands
from neispy import Neispy
from pycord_components import (
    Select,
    SelectOption,
    Interaction
)
from Naver_Api.Api import Naver
from dotenv import load_dotenv
load_dotenv(verbose=True)
N = Naver(os.getenv("NAVER_CLIENT"),os.getenv("NAVER_SECRET"))
class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_before_invoke(self, ctx: commands.Context):
        print(ctx.command)
        if ctx.command.name != 'λ©μΌ':
            database = await aiosqlite.connect("db/db.sqlite")
            cur = await database.execute(
                'SELECT * FROM uncheck WHERE user_id = ?', (ctx.author.id,)
            )

            if await cur.fetchone() is None:
                cur = await database.execute('SELECT * FROM mail')
                mails = await cur.fetchall()
                check = sum(1 for _ in mails)
                mal = discord.Embed(
                    title=f'π«νλ¦°λ΄ λ©μΌν¨ | {check}κ° μμ λ¨',
                    description="μμ§ μ½μ§ μμ λ©μΌμ΄ μμ΄μ.'`νλ¦°μ λ©μΌ`'λ‘ νμΈνμΈμ.\nμ£ΌκΈ°μ μΌλ‘ λ©μΌν¨μ νμΈν΄μ£ΌμΈμ! μμν μλ°μ΄νΈ λ° μ΄λ²€νΈκ°μ΅λ± μ¬λ¬μμμ νμΈν΄λ³΄μΈμ.",
                    colour=ctx.author.colour,
                )

                return await ctx.send(embed=mal)
            cur = await database.execute("SELECT * FROM mail")
            mails = await cur.fetchall()
            check = sum(1 for _ in mails)
            cur = await database.execute("SELECT * FROM uncheck WHERE user_id = ?", (ctx.author.id,))
            check2 = await cur.fetchone()
            if str(check) != str(check2[1]):
                mal = discord.Embed(
                    title=f'π«νλ¦°λ΄ λ©μΌν¨ | {int(check) - int(check2[1])}κ° μμ λ¨',
                    description="μμ§ μ½μ§ μμ λ©μΌμ΄ μμ΄μ.'`νλ¦°μ λ©μΌ`'λ‘ νμΈνμΈμ.\nμ£ΌκΈ°μ μΌλ‘ λ©μΌν¨μ νμΈν΄μ£ΌμΈμ! μμν μλ°μ΄νΈ λ° μ΄λ²€νΈκ°μ΅λ± μ¬λ¬μμμ νμΈν΄λ³΄μΈμ.",
                    colour=ctx.author.colour,
                )

                await ctx.send(embed=mal)

    @commands.group(name="νκ΅κ²μ", invoke_without_command=True)
    async def main_school(self, ctx, school=None):
        if school is None:
            return await ctx.reply("νκ΅λͺμ μλ ₯ν΄μ£ΌμΈμ!")
        msg = await ctx.reply("κ²μμ€μ΄λ μ‘°κΈλ§ κΈ°λ€λ €μ£ΌμΈμ! <a:loading:888625946565935167>")
        async with Neispy(KEY=os.getenv("NEIS_TOKEN")) as neis:
            scinfo = await neis.schoolInfo(SCHUL_NM=school)
            if len(scinfo) >= 2:
                await msg.delete()
                many_msg = await ctx.reply(
                    f"νκ΅λͺμ΄ κ°μ νκ΅κ° `{len(scinfo[:25])}`κ° μμ΄μ.\nμλμμ κ²μνμλ €λ νκ΅λ₯Ό μ νν΄μ£ΌμΈμ.",
                    components=[
                        Select(
                            placeholder="νκ΅λ₯Ό μ νν΄μ£ΌμΈμ.",
                            options=[
                                SelectOption(label=i.SCHUL_NM, value=f"{i.SD_SCHUL_CODE}",
                                             description="μ§μ­ - {}".format(i.LCTN_SC_NM), emoji="π«") for i in
                                scinfo[:25]
                            ],
                        ),
                    ],
                )
                try:
                    interaction = await self.bot.wait_for("select_option", check=lambda i: i.user.id == ctx.author.id and i.message.id == many_msg.id, timeout=30)
                    value = interaction.values[0]
                    # stamp = str(time.mktime(datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S').timetuple()))[:-2]
                except asyncio.TimeoutError:
                    await many_msg.delete()
                    return

                for i in scinfo:
                    if i.SD_SCHUL_CODE == value:
                        em = discord.Embed(
                            title=f"{i.SCHUL_NM}| {i.ENG_SCHUL_NM}( {i.LCTN_SC_NM} )",
                            description=f"μ£Όμ: {i.ORG_RDNMA}\nλνλ²νΈ: {i.ORG_TELNO}\nFax: {i.ORG_FAXNO}\nννμ΄μ§: {i.HMPG_ADRES}",
                            colour=discord.Colour.random()
                        )
                        em.add_field(name="μμκ΅μ‘μ²­", value=f"```{i.ATPT_OFCDC_SC_NM}```")
                        em.add_field(name="νμ", value=f"```{i.COEDU_SC_NM} | {i.HS_SC_NM}```")
                        await many_msg.edit(embed=em, components=[])
            else:
                em = discord.Embed(
                    title=f"{scinfo[0].SCHUL_NM}| {scinfo[0].ENG_SCHUL_NM}( {scinfo[0].LCTN_SC_NM} )",
                    description=f"μ£Όμ: {scinfo[0].ORG_RDNMA}\nλνλ²νΈ: {scinfo[0].ORG_TELNO}\nFax: {scinfo[0].ORG_FAXNO}\nννμ΄μ§: {scinfo[0].HMPG_ADRES}",
                    colour=discord.Colour.random()
                )
                em.add_field(name="μμκ΅μ‘μ²­", value=f"```{scinfo[0].ATPT_OFCDC_SC_NM}```")
                em.add_field(name="νμ", value=f"```{scinfo[0].COEDU_SC_NM} | {scinfo[0].HS_SC_NM}```")
                await msg.delete()
                await ctx.reply(embed=em)

    @main_school.command(name="κΈμ")
    async def school_meal(self, ctx, school=None, dates=None):
        if school is None:
            return await ctx.reply("νκ΅λͺμ μλ ₯ν΄μ£ΌμΈμ!")
        if dates is None:
            now = datetime.datetime.now()
            dates = f"{now.year}{now.month}{now.day}"
        msg = await ctx.reply("κ²μμ€μ΄λ μ‘°κΈλ§ κΈ°λ€λ €μ£ΌμΈμ! <a:loading:888625946565935167>")
        neis = Neispy(KEY=os.getenv("NEIS_TOKEN"))
        scinfo = await neis.schoolInfo(SCHUL_NM=school)
        if len(scinfo) >= 2:
            await msg.delete()
            many_msg = await ctx.reply(
                f"νκ΅λͺμ΄ κ°μ νκ΅κ° `{len(scinfo[:25])}`κ° μμ΄μ.\nμλμμ κ²μνμλ €λ νκ΅λ₯Ό μ νν΄μ£ΌμΈμ.",
                components=[
                    Select(
                        placeholder="νκ΅λ₯Ό μ νν΄μ£ΌμΈμ.",
                        options=[
                            SelectOption(label=i.SCHUL_NM, value=i.SD_SCHUL_CODE,
                                         description="μ§μ­ - {}".format(i.LCTN_SC_NM), emoji="π«") for i in scinfo[:25]
                        ],
                    ),
                ],
            )
            try:
                interaction = await self.bot.wait_for("select_option", check=lambda i: i.user.id == ctx.author.id and i.message.id == many_msg.id, timeout=30)
                value = interaction.values[0]
                # stamp = str(time.mktime(datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S').timetuple()))[:-2]
            except asyncio.TimeoutError:
                await many_msg.delete()
                return
            for i in scinfo:
                if i.SD_SCHUL_CODE == value:
                    ae = i.ATPT_OFCDC_SC_CODE  # κ΅μ‘μ²­μ½λ
                    se = i.SD_SCHUL_CODE  # νκ΅μ½λ
                    diet_dict = {
                        "1": "μ‘°μ",
                        "2": "μ€μ",
                        "3": "μμ"
                    }

                    async def callback(interaction: Interaction):
                        values = interaction.values[0]
                        print(values)
                        if interaction.user.id == ctx.author.id:
                            try:
                                scmeal = await neis.mealServiceDietInfo(ae, se, MLSV_YMD=dates, MMEAL_SC_CODE=values)
                            except neispy.error.DataNotFound:
                                await interaction.send(f"μ ννμ  `{diet_dict[values]}`μ λ©λ΄λ₯Ό μ°Ύμ μ μμ΄μ..")
                                return
                            meal = scmeal[0].DDISH_NM.replace("<br/>", "\n")
                            em = discord.Embed(
                                title=f"{i.SCHUL_NM} | {diet_dict[values]}",
                                description=f"```fix\n{meal}```"
                            )
                            await interaction.edit_origin(embed=em, components=[
                                self.bot.components_manager.add_callback(
                                    Select(
                                        options=[
                                            SelectOption(label="μ‘°μ", value="1", emoji="π"),
                                            SelectOption(label="μ€μ", value="2", emoji="β"),
                                            SelectOption(label="μμ", value="3", emoji="π")
                                        ],
                                    ),
                                    callback,
                                )
                            ])

                    await many_msg.delete()
                    await ctx.reply(
                        "μ‘°νν  κΈμμ μ νν΄μ£ΌμΈμ.",
                        components=[
                            self.bot.components_manager.add_callback(
                                Select(
                                    options=[
                                        SelectOption(label="μ‘°μ", value="1", emoji="π"),
                                        SelectOption(label="μ€μ", value="2", emoji="β"),
                                        SelectOption(label="μμ", value="3", emoji="π")
                                    ],
                                ),
                                callback,
                            )
                        ]
                    )
        else:
            ae = scinfo[0].ATPT_OFCDC_SC_CODE  # κ΅μ‘μ²­μ½λ
            se = scinfo[0].SD_SCHUL_CODE  # νκ΅μ½λ
            diet_dict = {
                "1": "μ‘°μ",
                "2": "μ€μ",
                "3": "μμ"
            }

            async def callback(interaction: Interaction):
                values = interaction.values[0]
                print(values)
                if interaction.user.id == ctx.author.id:
                    try:
                        scmeal = await neis.mealServiceDietInfo(ae, se, MLSV_YMD=dates, MMEAL_SC_CODE=values)
                    except neispy.error.DataNotFound:
                        await interaction.send(f"μ ννμ  `{diet_dict[values]}`μ λ©λ΄λ₯Ό μ°Ύμ μ μμ΄μ..")
                        return
                    meal = scmeal[0].DDISH_NM.replace("<br/>", "\n")
                    em = discord.Embed(
                        title=f"{scinfo[0].SCHUL_NM} | {diet_dict[values]}",
                        description=f"```fix\n{meal}```"
                    )
                    await interaction.edit_origin(embed=em, components=[
                        self.bot.components_manager.add_callback(
                            Select(
                                options=[
                                    SelectOption(label="μ‘°μ", value="1", emoji="π"),
                                    SelectOption(label="μ€μ", value="2", emoji="β"),
                                    SelectOption(label="μμ", value="3", emoji="π")
                                ],
                            ),
                            callback,
                        )
                    ])

            await msg.delete()
            await ctx.reply(
                "μ‘°νν  κΈμμ μ νν΄μ£ΌμΈμ.",
                components=[
                    self.bot.components_manager.add_callback(
                        Select(
                            options=[
                                SelectOption(label="μ‘°μ", value="1", emoji="π"),
                                SelectOption(label="μ€μ", value="2", emoji="β"),
                                SelectOption(label="μμ", value="3", emoji="π")
                            ],
                        ),
                        callback,
                    )
                ]
            )

    @main_school.command(name="μκ°ν")
    async def school_schedule(self, ctx, school=None, dates=None):
        if school is None:
            return await ctx.reply("νκ΅λͺμ μλ ₯ν΄μ£ΌμΈμ!")
        if dates is None:
            now = datetime.datetime.now()
            dates = f"{now.year}{now.month}{now.day}"
        msg = await ctx.reply("κ²μμ€μ΄λ μ‘°κΈλ§ κΈ°λ€λ €μ£ΌμΈμ! <a:loading:888625946565935167>")
        neis = Neispy(KEY=os.getenv("NEIS_TOKEN"))
        scinfo = await neis.schoolInfo(SCHUL_NM=school)
        if len(scinfo) >= 2:
            await msg.delete()
            many_msg = await ctx.reply(
                f"νκ΅λͺμ΄ κ°μ νκ΅κ° `{len(scinfo[:25])}`κ° μμ΄μ.\nμλμμ κ²μνμλ €λ νκ΅λ₯Ό μ νν΄μ£ΌμΈμ.",
                components=[
                    Select(
                        placeholder="νκ΅λ₯Ό μ νν΄μ£ΌμΈμ.",
                        options=[
                            SelectOption(label=i.SCHUL_NM, value=i.SD_SCHUL_CODE,
                                         description="μ§μ­ - {}".format(i.LCTN_SC_NM), emoji="π«") for i in scinfo[:25]
                        ],
                    ),
                ],
            )
            try:
                interaction = await self.bot.wait_for("select_option", check=lambda
                    i: i.user.id == ctx.author.id and i.message.id == many_msg.id, timeout=30)
                value = interaction.values[0]
                # stamp = str(time.mktime(datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S').timetuple()))[:-2]
            except asyncio.TimeoutError:
                await many_msg.delete()
                return
            for i in scinfo:
                if i.SD_SCHUL_CODE == value:
                    ae = i.ATPT_OFCDC_SC_CODE  # κ΅μ‘μ²­μ½λ
                    se = i.SD_SCHUL_CODE  # νκ΅μ½λ
                    diet_dict = {
                        "1": "μ‘°μ",
                        "2": "μ€μ",
                        "3": "μμ"
                    }

                    async def callback(interaction: Interaction):
                        values = interaction.values[0]
                        print(values)
                        if interaction.user.id == ctx.author.id:
                            try:
                                scmeal = await neis.mealServiceDietInfo(ae, se, MLSV_YMD=dates, MMEAL_SC_CODE=values)
                            except neispy.error.DataNotFound:
                                await interaction.send(f"μ ννμ  `{diet_dict[values]}`μ λ©λ΄λ₯Ό μ°Ύμ μ μμ΄μ..")
                                return
                            meal = scmeal[0].DDISH_NM.replace("<br/>", "\n")
                            em = discord.Embed(
                                title=f"{i.SCHUL_NM} | {diet_dict[values]}",
                                description=f"```fix\n{meal}```"
                            )
                            await interaction.edit_origin(embed=em, components=[
                                self.bot.components_manager.add_callback(
                                    Select(
                                        options=[
                                            SelectOption(label="μ‘°μ", value="1", emoji="π"),
                                            SelectOption(label="μ€μ", value="2", emoji="β"),
                                            SelectOption(label="μμ", value="3", emoji="π")
                                        ],
                                    ),
                                    callback,
                                )
                            ])

                    await many_msg.delete()
                    await ctx.reply(
                        "μ‘°νν  κΈμμ μ νν΄μ£ΌμΈμ.",
                        components=[
                            self.bot.components_manager.add_callback(
                                Select(
                                    options=[
                                        SelectOption(label="μ‘°μ", value="1", emoji="π"),
                                        SelectOption(label="μ€μ", value="2", emoji="β"),
                                        SelectOption(label="μμ", value="3", emoji="π")
                                    ],
                                ),
                                callback,
                            )
                        ]
                    )
        else:
            ae = scinfo[0].ATPT_OFCDC_SC_CODE  # κ΅μ‘μ²­μ½λ
            se = scinfo[0].SD_SCHUL_CODE  # νκ΅μ½λ
            diet_dict = {
                "1": "μ‘°μ",
                "2": "μ€μ",
                "3": "μμ"
            }

            async def callback(interaction: Interaction):
                values = interaction.values[0]
                print(values)
                if interaction.user.id == ctx.author.id:
                    try:
                        scmeal = await neis.mealServiceDietInfo(ae, se, MLSV_YMD=dates, MMEAL_SC_CODE=values)
                    except neispy.error.DataNotFound:
                        await interaction.send(f"μ ννμ  `{diet_dict[values]}`μ λ©λ΄λ₯Ό μ°Ύμ μ μμ΄μ..")
                        return
                    meal = scmeal[0].DDISH_NM.replace("<br/>", "\n")
                    em = discord.Embed(
                        title=f"{scinfo[0].SCHUL_NM} | {diet_dict[values]}",
                        description=f"```fix\n{meal}```"
                    )
                    await interaction.edit_origin(embed=em, components=[
                        self.bot.components_manager.add_callback(
                            Select(
                                options=[
                                    SelectOption(label="μ‘°μ", value="1", emoji="π"),
                                    SelectOption(label="μ€μ", value="2", emoji="β"),
                                    SelectOption(label="μμ", value="3", emoji="π")
                                ],
                            ),
                            callback,
                        )
                    ])

            await msg.delete()
            await ctx.reply(
                "μ‘°νν  κΈμμ μ νν΄μ£ΌμΈμ.",
                components=[
                    self.bot.components_manager.add_callback(
                        Select(
                            options=[
                                SelectOption(label="μ‘°μ", value="1", emoji="π"),
                                SelectOption(label="μ€μ", value="2", emoji="β"),
                                SelectOption(label="μμ", value="3", emoji="π")
                            ],
                        ),
                        callback,
                    )
                ]
            )

    @commands.command(name="λ¨μΆ")
    async def shorturl(self, ctx, *, orgurl):
        res = await N.ShortUrl(url=orgurl)
        print(res)
        if res["code"] == '200':
            embed = discord.Embed(title="λ¨μΆμ±κ³΅! β")
            if len(orgurl) > 100:
                call_url = f'{orgurl[:100]}...'
            else:
                call_url = orgurl
            embed.add_field(name=f"μμ²­ν μλ³Έλ§ν¬: {call_url}", value="** **", inline=False)
            embed.add_field(name=f"λ¨μΆλ λ§ν¬: {res['result']['url']}", value="\n** **", inline=False)
            embed.add_field(name="λ¨μΆλ λ§ν¬QRμ΄λ―Έμ§", value="** **", inline=False)
            embed.set_image(url=f"{res['result']['url']}.qr")
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title=f"ERROR..λ¨μΆμ€ν¨ β\nμλ¬μ½λ: {res['code']}",description="μλ¬λ©μμ§: " + res["message"])
            if len(orgurl) > 100:
                call_url = f'{orgurl[:100]}...'
            else:
                call_url = orgurl
            embed.add_field(name=f"μμ²­ν μλ³Έλ§ν¬: {call_url}", value="** **", inline=False)
            await ctx.reply(embed=embed)

    @commands.command(name="μνκ²μ")
    async def search_movie(self, ctx, *, query):
        global emoji_star, ST_AR1, AC
        a = await N.Movie(query=query)
        print(a)
        embed = discord.Embed(colour=discord.Colour.blue())
        num = 1
        for i in a["items"][:3]:
            director = i["director"]
            direct = str(director).replace("|", "\n")
            actor = i["actor"]
            act = str(actor).replace("|", "\n")
            if i["subtitle"] == '':
                sub = 'ERROR! (μ λ³΄μμ)'
            else:
                sub = i["subtitle"]
            title = i["title"]
            tit = title.replace("<b>", "")
            ti = tit.replace("</b>", "")
            embed.add_field(name=f'#{str(num)}\nμ λͺ©: **{ti}({sub})**', value='** **', inline=False)
            embed.add_field(name="κ°λ΄μΌ", value=i["pubDate"])
            dire = f'{act[:10]}...'
            num += 1

            star = i["userRating"]
            STAR1 = star[:1]
            STAR2 = star[2:3]
            if int(STAR2) >= 5:
                ST_AR1 = int(STAR1) + 1
                print(ST_AR1)
            elif int(STAR2) <= 4:
                ST_AR1 = int(STAR1) + 0
                print(ST_AR1)

            if ST_AR1 == 0:
                emoji_star = 'βββββ'
                print('0')
            elif ST_AR1 == 1 or ST_AR1 == 2:
                emoji_star = 'βββββ'
                print('1')
            elif ST_AR1 == 3 or ST_AR1 == 4:
                emoji_star = 'βββββ'
                print('2')
            elif ST_AR1 == 5 or ST_AR1 == 6:
                emoji_star = 'βββββ'
                print('3')
            elif ST_AR1 == 7 or ST_AR1 == 8:
                emoji_star = 'βββββ'
                print('4')
            elif ST_AR1 == 9 or ST_AR1 == 10:
                emoji_star = 'βββββ'
                print('5')
            print(STAR1)
            embed.add_field(name="νμ ", value=f'{STAR1}.{STAR2}μ , λ³μ : {emoji_star}({ST_AR1}μ )')
            embed.add_field(name="κ°λ", value=dire, inline=False)
            if act == '':
                embed.add_field(name="λ°°μ°", value='ERROR! (μ λ³΄μμ)', inline=False)
            else:
                embed.add_field(name="λ°°μ°", value=act, inline=False)
                if len(act) > 15:
                    embed.add_field(name="λ°°μ°", value=f'{act[:15]}...', inline=False)
            embed.add_field(name="λ°λ‘κ°κΈ°", value=f"[μμΈν λ΄μ© λ³΄λ¬κ°κΈ°]({i['link']})\n[ν¬μ€ν°λ³΄λ¬κ°κΈ°]({i['image']})\n{'-----' * 10}")
            embed.set_footer(text='λ³μ μ μμ«μ 1μ μλ¦¬μμ λ°μ¬λ¦Όν κ°μΌλ‘ κ³μ°ν©λλ€.')
            print(i["userRating"])
        await ctx.send(embed=embed)

    @commands.command(name="λ΄μ€κ²μ")
    async def search_news(self, ctx, *, search):
        a = await N.News(query=search)
        print(a)
        embed = discord.Embed(title='λ΄μ€ κ²μκ²°κ³Ό!')
        num = 0
        for i in a["items"][:3]:
            title = i["title"]
            tit = str(title).replace("<b>", "")
            ti = tit.replace("</b>", "")
            T = ti.replace("&quot;", "")
            link = i["originallink"]
            des = i["description"]
            d_e = des.replace("</b>", "")
            d = d_e.replace("<b>", "")
            D = d.replace("&quot;", "")
            DE = D.replace("&amp;", "")
            num += 1
            '''b = str(a["total"])
            c = b[:1]
            d = b[2:5]
            e = b[6:9]'''
            embed.add_field(name=f"#{str(num)}", value=f'κΈ°μ¬μ λͺ©- {str(T)}', inline=False)
            embed.add_field(name="λ―Έλ¦¬λ³΄κΈ°", value=str(DE), inline=False)
            embed.add_field(name="κ²μμΌ", value=i["pubDate"][:-6])
            embed.add_field(name="** **", value=f"[μμΈν λ΄μ© λ³΄λ¬κ°κΈ°](<{str(link)}>)\n{'-----' * 10}", inline=False)
            embed.set_footer(text=f'κ²μλ λ΄μ€ κΈ°μ¬ μ΄κ°―μ: {a["total"]}κ°')
        await ctx.send(embed=embed)
        # await ctx.send(f'{title}\n{link}\n{des}')

    @commands.command(name="μΉ΄νκ²μ")
    async def search_cafe(self, ctx, *, search):
        a = await N.Cafe(query=search)
        print(a)
        embed = discord.Embed(title=f'μΉ΄ν κ²μκΈ κ²μκ²°κ³Ό!\n{"-----" * 10}')
        num = 0
        for i in a["items"][:3]:
            title = i["title"]
            tit = str(title).replace("<b>", "")
            ti = tit.replace("</b>", "")
            T = ti.replace("&quot;", "")
            link = i["link"]
            des = i["description"]
            d_e = des.replace("</b>", "")
            d = d_e.replace("<b>", "")
            D = d.replace("&quot;", "")
            DE = D.replace("&amp;", "")
            num += 1
            embed.add_field(name=f"#{str(num)}\nμ λͺ©", value=str(T), inline=False)
            embed.add_field(name="λ―Έλ¦¬λ³΄κΈ°", value=str(DE), inline=False)
            embed.add_field(name="λ°λ‘κ°κΈ°", value=f"[μμΈν λ΄μ© λ³΄λ¬κ°κΈ°](<{str(link)}>)", inline=False)
            embed.set_footer(text=f'κ²μλ μΉ΄ν κ²μκΈ μ΄κ°―μ: {a["total"]}κ°')
        await ctx.send(embed=embed)

    @commands.command(name="μΉκ²μ")
    async def search_web(self, ctx, *, search):
        a = await N.Webkr(query=search)
        print(a)
        embed = discord.Embed(title=f'λ€μ΄λ² κ²μκ²°κ³Ό!\n{"-----" * 10}')
        num = 0
        for i in a["items"][:3]:
            title = i["title"]
            tit = str(title).replace("<b>", "")
            ti = tit.replace("</b>", "")
            T = ti.replace("&quot;", "")
            link = i["link"]
            des = i["description"]
            d_e = des.replace("</b>", "")
            d = d_e.replace("<b>", "")
            D = d.replace("&quot;", "")
            DE = D.replace("&amp;", "")
            num += 1
            embed.add_field(name=f"#{str(num)}\nμ λͺ©", value=str(T), inline=False)
            embed.add_field(name="λ―Έλ¦¬λ³΄κΈ°", value=str(DE), inline=False)
            embed.add_field(name="λ°λ‘κ°κΈ°", value=f"[μμΈν λ΄μ© λ³΄λ¬κ°κΈ°](<{str(link)}>)", inline=False)
            embed.set_footer(text=f'κ²μλ μ΄κ°―μ: {a["total"]}κ°')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Search(bot))
