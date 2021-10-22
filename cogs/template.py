import io
import asyncio
import urllib.request
from datetime import datetime, timezone

import aiosqlite
import discord
import pytz
from PIL import Image
from discord.ext import commands
import discordSuperUtils
class invitetracker(commands.Cog,discordSuperUtils.CogManager.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ImageManager = discordSuperUtils.ImageManager()
        self.TemplateManager = discordSuperUtils.TemplateManager(bot)
        super().__init__()

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

    @commands.Cog.listener()
    async def on_ready(self):
        database = discordSuperUtils.DatabaseManager.connect(
            await aiosqlite.connect("db/db.sqlite")
        )
        await self.TemplateManager.connect_to_database(database,[
            "templates",
            "categories",
            "text_channels",
            "voice_channels",
            "roles",
            "overwrites",
        ],)

    @commands.command(name="템플릿사용")
    @commands.has_permissions(administrator=True)
    async def apply_template(self,ctx, template_id: str):
        # Check permissions here.
        template = await self.TemplateManager.get_template(template_id)
        if not template:
            await ctx.send("해당하는 ID의 템플릿을 찾지 못했어요.")
            return

        await ctx.send(f"다음ID`{template.info.template_id}`의 템플릿을 사용할게요! ")
        await template.apply(ctx.guild)

    @commands.command(name="템플릿삭제")
    @commands.has_permissions(administrator=True)
    async def delete_template(self,ctx, template_id: str):
        template = await self.TemplateManager.get_template(template_id)
        # Here, you could check permissions, I recommend checking if ctx is the template guild.
        if not template:
            await ctx.send("해당하는 템플릿을 찾지못했어요.")
            return
        if template.info.guild != ctx.guild.id:
            await ctx.send("다른 서버의 템플릿을 삭제할 수 없어요!")
            return
        partial_template = await template.delete()
        await ctx.send(f"다음ID`{partial_template.info.template_id}`의 템플릿을 삭제했어요!")

    @commands.command(name="템플릿목록")
    async def get_guild_templates(self,ctx):
        templates = await self.TemplateManager.get_templates()
        em = discord.Embed(
            title=f"템플릿 목록 • 총 {len(templates)}개 등록되어있어요.",
            description="여러 서버가 올린 템플릿으로 쉽게 서버를 구성해보세요!😉\n사용하실려면 요청자님이 관리자 권한이 있어야해요.",
            colour=discord.Colour.random()
        )
        for i in templates:
            text_channels = [j.name for j in i.text_channels[:5]]
            text_channels_list = "\n".join(text_channels)
            voice_channels = [j.name for j in i.voice_channels[:5]]
            voice_channels_list = "\n".join(voice_channels)
            category_channels = [j.name for j in i.categories[:5]]
            category_channels_list = "\n".join(category_channels)
            em.add_field(
                name=f"서버: {self.bot.get_guild(i.info.guild)}",
                value=f"""
```fix
템플릿ID - {i.info.template_id}

텍스트 채널들({len(i.text_channels)}개)
{text_channels_list}
...

음성 채널들({len(i.voice_channels)}개)
{voice_channels_list}
...

카테고리들({len(i.categories)}개)
{category_channels_list}
...

적용하기 - 하린아 템플릿사용 {i.info.template_id}
```
                """
            )
        await ctx.reply(embed=em)
        #await ctx.send(templates[1])

    @commands.command(name="템플릿찾기")
    async def get_templates(self,ctx, id=None):
        if id == None:
            templates = await self.TemplateManager.get_templates(ctx.guild)
            em = discord.Embed(
                title=f"템플릿 목록 • 총 {len(templates)}개 등록되어있어요.",
                description="여러 서버가 올린 템플릿으로 쉽게 서버를 구성해보세요!😉\n사용하실려면 요청자님이 관리자 권한이 있어야해요.",
                colour=discord.Colour.random()
            )
            for i in templates:
                text_channels = [j.name for j in i.text_channels[:5]]
                text_channels_list = "\n".join(text_channels)
                voice_channels = [j.name for j in i.voice_channels[:5]]
                voice_channels_list = "\n".join(voice_channels)
                category_channels = [j.name for j in i.categories[:5]]
                category_channels_list = "\n".join(category_channels)
                em.add_field(
                    name=f"서버: {ctx.guild}",
                    value=f"""
```fix
템플릿ID - {i.info.template_id}

텍스트 채널들({len(i.text_channels)}개)
{text_channels_list}
...

음성 채널들({len(i.voice_channels)}개)
{voice_channels_list}
...

카테고리들({len(i.categories)}개)
{category_channels_list}
...

적용하기 - 하린아 템플릿사용 {i.info.template_id}
```
                            """
                )
            await ctx.reply(embed=em)
        else:
            template = await self.TemplateManager.get_template(id)
            if not template:
                await ctx.send("해당하는 템플릿을 찾지 못했어요.")
                return
            em = discord.Embed(
                title=f"템플릿 상세.",
                description="여러 서버가 올린 템플릿으로 쉽게 서버를 구성해보세요!😉\n사용하실려면 요청자님이 관리자 권한이 있어야해요.",
                colour=discord.Colour.random()
            )
            text_channels = [j.name for j in template.text_channels[:5]]
            text_channels_list = "\n".join(text_channels)
            voice_channels = [j.name for j in template.voice_channels[:5]]
            voice_channels_list = "\n".join(voice_channels)
            category_channels = [j.name for j in template.categories[:5]]
            category_channels_list = "\n".join(category_channels)
            em.add_field(
                name=f"서버: {self.bot.get_guild(template.info.guild)}",
                value=f"""
```fix
템플릿ID - {id}

텍스트 채널들({len(template.text_channels)}개)
{text_channels_list}
...

음성 채널들({len(template.voice_channels)}개)
{voice_channels_list}
...

카테고리들({len(template.categories)}개)
{category_channels_list}
...

적용하기 - 하린아 템플릿사용 {id}
```
                        """
            )
            await ctx.reply(content="다음의 템플릿을 찾았어요",embed=em)
    @commands.command(name="템플릿등록")
    @commands.has_permissions(administrator=True)
    async def create_template(self,ctx):
        # Again, you should check permissions here to make sure this isn't abused.
        # You can also get all the templates a guild has, using TemplateManager.get_templates
        msg = await ctx.reply("등록중이에요! 채널수와 역할수에 따라 오래걸릴 수도있어요")
        template = await self.TemplateManager.create_template(ctx.guild)
        await msg.edit(f"성공적으로 템플릿을 등록했어요! ID - `{template.info.template_id}`")


def setup(bot):
    bot.add_cog(invitetracker(bot))