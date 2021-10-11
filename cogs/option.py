import asyncio
import platform

import aiosqlite
import discord
from discord.ext import commands
from pycord_components import (
    Select,
    SelectOption
)


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.option_dict = {
            "-HNoLv": "레벨링 무시",
            "wlc": "환영인사",
            "ivt": "초대추적",
            "-HOnNt": "공지수신",
            "-HOnBtd": "생일알림"
            # "-HNoAts":"안티스팸 무시"
        }
        self.option_dict_db = {
            "wlc": "welcome",
            "ivt": "invite_tracker"
        }

    async def cog_before_invoke(self, ctx: commands.Context):
        print(ctx.command)
        if ctx.command.name != '메일':
            database = await aiosqlite.connect("db/db.sqlite")
            cur = await database.execute(
                'SELECT * FROM uncheck WHERE user_id = ?', (ctx.author.id,)
            )

            if await cur.fetchone() is None:
                cur = await database.execute(f"SELECT * FROM mail")
                mails = await cur.fetchall()
                check = sum(1 for _ in mails)
                mal = discord.Embed(
                    title=f'📫하린봇 메일함 | {check}개 수신됨',
                    description="아직 읽지 않은 메일이 있어요.'`하린아 메일`'로 확인하세요.\n주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                    colour=ctx.author.colour,
                )

                return await ctx.send(embed=mal)
            cur = await database.execute('SELECT * FROM mail')
            mails = await cur.fetchall()
            check = sum(1 for _ in mails)
            cur = await database.execute(f"SELECT * FROM uncheck WHERE user_id = ?", (ctx.author.id,))
            check2 = await cur.fetchone()
            if str(check) != str(check2[1]):
                mal = discord.Embed(
                    title=f'📫하린봇 메일함 | {int(check) - int(check2[1])}개 수신됨',
                    description="아직 읽지 않은 메일이 있어요.'`하린아 메일`'로 확인하세요.\n주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                    colour=ctx.author.colour,
                )

                await ctx.send(embed=mal)

    async def check_option(self, ctx):
        on_option = []
        topics = str(ctx.channel.topic).split(" ")
        # values = ["-HNoAts", "-HNoLv"]
        """if "-HNoAts" in topics:
            on_option.append(self.option_dict["-HNoAts"]+" <:activ:896255701641474068>")"""
        if "-HNoLv" in topics:
            on_option.append(self.option_dict["-HNoLv"] + " <:activ:896255701641474068>")
        channels = ctx.guild.text_channels
        for channel in channels:
            if channel.topic is not None:
                if str(channel.topic).find("-HOnNt") != -1:
                    on_option.append(self.option_dict["-HOnNt"] + f"<#{channel.id}> <:activ:896255701641474068>")
                    break
                if str(channel.topic).find("-HOnBtd") != -1:
                    on_option.append(self.option_dict["-HOnBtd"] + f"<#{channel.id}> <:activ:896255701641474068>")
                    break
        database = await aiosqlite.connect("db/db.sqlite")
        cur = await database.execute("SELECT * FROM welcome WHERE guild = ?", (ctx.guild.id,))
        data = await cur.fetchone()
        if data is not None:
            on_option.append(self.option_dict["wlc"] + " <:activ:896255701641474068>")
        cur = await database.execute("SELECT * FROM invite_tracker WHERE guild = ?", (ctx.guild.id,))
        data = await cur.fetchone()
        if data is not None:
            on_option.append(self.option_dict["ivt"] + " <:activ:896255701641474068>")
        if not on_option:
            return "적용된 옵션이 없어요"
        return "\n".join(on_option)

    @commands.command(name="옵션", aliases=["설정"])
    async def option(self, ctx):
        database = self.bot.db
        check_option = await self.check_option(ctx=ctx)
        """
        SelectOption(label="안티스팸 무시",
                                                            description="이 채널에 메세지 도배나 멘션 도배를 무시하는 모드입니다.",
                                                            value="-HNoAts", emoji="👮‍♂️")
        """
        msg = await ctx.reply("옵션을 확인하거나 셋팅하세요\n\n< 적용된 옵션 >\n" + check_option,
                              components=[
                                  Select(placeholder="옵션",
                                         options=[
                                             SelectOption(label="레벨링 무시",
                                                          description="이 채널에 메세지로 경험치를 얻고 레벨업을 무시하는 모드입니다.",
                                                          value="-HNoLv", emoji="🏆"),
                                             SelectOption(label="환영인사", description="유저가 서버에 입장시 자동으로 인사하는 모드입니다.",
                                                          value="wlc", emoji="👋"),
                                             SelectOption(label="초대추적",
                                                          description="유저가 서버에 입장시 누구의 초대로 서버에 들어왔는지 확인할 수 있는 모드입니다.",
                                                          value="ivt", emoji="📈"),
                                             SelectOption(label="봇공지채널",
                                                          description="이 채널을 봇 공지를 받을수있는 채널로 설정해요.",
                                                          value="-HOnNt", emoji="📢"),
                                             SelectOption(label="생일알림채널",
                                                          description="이 채널을 생일알림 채널로 설정해요.",
                                                          value="-HOnBtd", emoji="🎉"),
                                             SelectOption(label="리셋",
                                                          description="적용되어있는 옵션을 리셋합니다.",
                                                          value="reset", emoji="🔄"),
                                             SelectOption(label="취소",
                                                          description="명령어를 취소합니다.",
                                                          value="cancel", emoji="↩")
                                         ]),

                              ],
                              )
        try:
            interaction = await self.bot.wait_for("select_option",
                                                  check=lambda i: i.user.id == ctx.author.id and i.message.id == msg.id,
                                                  timeout=60)
            value = interaction.values[0]
        except asyncio.TimeoutError:
            await msg.edit("시간이 초과되었어요!", components=[])
            return
        if value in ["wlc", "ivt"]:
            database = await aiosqlite.connect("db/db.sqlite")
            if value == "wlc":
                cur = await database.execute("SELECT * FROM welcome WHERE guild = ?", (ctx.guild.id,))
            else:
                cur = await database.execute("SELECT * FROM invite_tracker WHERE guild = ?", (ctx.guild.id,))
            data = await cur.fetchone()
            print(data)
            if data is not None:
                await msg.edit(f"이미 설정되어있어요!\n설정되어있는 채널 - <#{data[1]}>", components=[])
                return
            await msg.delete()
            msg = await ctx.reply(
                f"{self.option_dict[value]}를 선택하셨어요!\n추가 설정을 위해 아래의 질문에 맞는 값을 보내주세요!\n메세지가 보내질 __채널 ID__를 보내주세요.(ex| 123456789)",
                components=[])
            try:
                message = await self.bot.wait_for("message",
                                                  check=lambda i: i.author.id == ctx.author.id and i.channel.id == ctx.channel.id,
                                                  timeout=60)
                message = message.content
            except asyncio.TimeoutError:
                await msg.edit("시간이 초과되었어요!", components=[])
                return
            await msg.edit("저장중이에요!", components=[])
            try:
                await database.execute(f"INSERT INTO {self.option_dict_db[value]}(guild,channel) VALUES (?,?)",
                                       (ctx.guild.id, int(message)))
                await database.commit()
            except Exception as e:
                await msg.edit("에러가 발생했어요! \n에러내역을 개발자에게 발송하였으니 곧 고쳐질거에요!")
                print(e)
                return
            await msg.edit("저장을 완료했어요!\n채널 - <#{ch}>".format(ch=message), components=[])
        if value == "reset":
            if ctx.channel.topic is not None:
                topics = str(ctx.channel.topic).split(" ")
                values = ["-HNoLv", "-HOnNt"]
                for x in values:
                    try:
                        topics.remove(x)
                    except ValueError:
                        pass
                # print(' '.join(topics))
                res_topic = ' '.join(topics)
                channel = ctx.channel
                if res_topic == '':
                    await channel.edit(topic="")
                else:
                    await channel.edit(topic=str(res_topic))
            # noinspection PyBroadException
            try:
                await database.execute("DELETE FROM welcome WHERE guild = ?", (ctx.guild.id,))
            except Exception:
                pass
            # noinspection PyBroadException
            try:
                await database.execute("DELETE FROM invite_tracker WHERE guild = ?", (ctx.guild.id,))
            except Exception:
                pass
            await database.commit()
            await msg.edit(content="초기화를 완료했어요!", components=[])
            await asyncio.sleep(3)
            await msg.delete()

        if value == "cancel":
            await msg.delete()
        if value in ["-HNoLv", "-HNoAts"]:
            try:
                print(value)
                if str(ctx.channel.topic).find(value) != -1:
                    return await msg.edit("이미 설정되어있어요.", components=[])
                topic = value if ctx.channel.topic is None else ctx.channel.topic + " " + value
                await ctx.channel.edit(topic=topic)
                await msg.edit("성공적으로 적용되었어요.", components=[])
            except discord.Forbidden:
                await msg.edit(content='채널 관리 권한이 없어 변경할 수 없어요! 권한을 재설정해주세요!', components=[])
        if value == "-HOnNt":
            channels = ctx.guild.text_channels
            count = []
            for channel in channels:
                if (
                    channel.topic is not None
                    and str(channel.topic).find("-HOnNt") != -1
                ):
                    count.append(channel.id)
                    break
            await self.msg_edit_channel(ctx, msg, count, value)
        if value == "-HOnBtd":
            channels = ctx.guild.text_channels
            count = []
            for channel in channels:
                if (
                    channel.topic is not None
                    and str(channel.topic).find("-HOnBtd") != -1
                ):
                    count.append(channel.id)
                    break
            await self.msg_edit_channel(ctx, msg, count, value)

    @commands.command(name="프사")
    async def avatar(self, ctx, member: discord.Member = None):
        member_obj = member or ctx.author
        em = discord.Embed(
            title=f"{member}님의 프로필 사진!",
            description=f"[링크]({member_obj.avatar_url})",
            colour=discord.Colour.random()
        )
        em.set_image(url=member_obj.avatar_url)
        await ctx.reply(embed=em)

    @commands.command(name="서버정보")
    async def serverinfo(self, ctx):
        server = ctx.guild
        roles = [x.name for x in server.roles]
        role_length = len(roles)
        if role_length > 50:
            roles = roles[:50]
            roles.append(f">>>> [50/{len(roles)}]")
        roles = ", ".join(roles)
        channels = len(server.channels)
        time = str(server.created_at)
        time = time.split(" ")
        time = time[0]

        embed = discord.Embed(
            title="**서버 이름:**",
            description=f"{server}",
            color=0x42F56C
        )
        embed.set_thumbnail(
            url=server.icon_url
        )
        embed.add_field(
            name="서버 ID",
            value=server.id
        )
        embed.add_field(
            name="멤버수",
            value=server.member_count
        )
        embed.add_field(
            name="텍스트/보이스 채널수",
            value=f"{channels}"
        )
        embed.add_field(
            name=f"역할 `({role_length})`개",
            value=roles
        )
        embed.set_footer(
            text=f"생성일시: {time}"
        )
        await ctx.reply(embed=embed)

    @commands.command(name="봇정보")
    async def botinfo(self, ctx):
        """
        Get some useful (or not) information about the bot.
        """

        # This is, for now, only temporary

        embed = discord.Embed(
            description="하린봇 정보",
            color=0x42F56C
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_image(
            url="https://media.discordapp.net/attachments/889514827905630290/896359450544308244/37cae031dc5a6c40.png")
        embed.add_field(
            name="주인:",
            value="gawi#9537(281566165699002379)",
            inline=True
        )
        embed.add_field(
            name="Pycord Version:",
            value=f"{discord.__version__}",
            inline=True
        )
        embed.add_field(
            name="Python Version:",
            value=f"{platform.python_version()}",
            inline=False
        )
        embed.add_field(
            name="OS Platform:",
            value=f"{platform.platform()}",
            inline=False
        )
        embed.add_field(name="Prefix:", value='하린아', inline=True)
        embed.add_field(
            name="Ping:",
            value=str(round(self.bot.latency * 1000)) + "ms",
            inline=True
        )
        await ctx.reply(embed=embed)

    @staticmethod
    async def msg_edit_channel(ctx, msg, count, value):
        if len(count) == 1:
            await msg.edit(f"이미 설정되어있는 채널이 있어요! 채널 - <#{count[0]}>", components=[])
            return
        else:
            topic = value if ctx.channel.topic is None else ctx.channel.topic + " " + value
            await ctx.channel.edit(topic=topic)
            await msg.edit("성공적으로 적용되었어요.", components=[])


def setup(bot):
    bot.add_cog(General(bot))
