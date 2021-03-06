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
        if ctx.command.name != 'λ©μΌ':
            database = await aiosqlite.connect("db/db.sqlite")
            cur = await database.execute(f"SELECT * FROM uncheck WHERE user_id = ?", (ctx.author.id,))
            if await cur.fetchone() == None:
                cur = await database.execute(f"SELECT * FROM mail")
                mails = await cur.fetchall()
                check = 0
                for j in mails:
                    check += 1
                mal = discord.Embed(title=f"π«νλ¦°λ΄ λ©μΌν¨ | {str(check)}κ° μμ λ¨",
                                    description="μμ§ μ½μ§ μμ λ©μΌμ΄ μμ΄μ.'`νλ¦°μ λ©μΌ`'λ‘ νμΈνμΈμ.\nμ£ΌκΈ°μ μΌλ‘ λ©μΌν¨μ νμΈν΄μ£ΌμΈμ! μμν μλ°μ΄νΈ λ° μ΄λ²€νΈκ°μ΅λ± μ¬λ¬μμμ νμΈν΄λ³΄μΈμ.",
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
                mal = discord.Embed(title=f"π«νλ¦°λ΄ λ©μΌν¨ | {str(int(check) - int(CHECK[1]))}κ° μμ λ¨",
                                    description="μμ§ μ½μ§ μμ λ©μΌμ΄ μμ΄μ.'`νλ¦°μ λ©μΌ`'λ‘ νμΈνμΈμ.\nμ£ΌκΈ°μ μΌλ‘ λ©μΌν¨μ νμΈν΄μ£ΌμΈμ! μμν μλ°μ΄νΈ λ° μ΄λ²€νΈκ°μ΅λ± μ¬λ¬μμμ νμΈν΄λ³΄μΈμ.",
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

    @commands.command(name="ννλ¦Ώμ¬μ©")
    @commands.has_permissions(administrator=True)
    async def apply_template(self,ctx, template_id: str):
        # Check permissions here.
        template = await self.TemplateManager.get_template(template_id)
        if not template:
            await ctx.send("ν΄λΉνλ IDμ ννλ¦Ώμ μ°Ύμ§ λͺ»νμ΄μ.")
            return

        await ctx.send(f"λ€μID`{template.info.template_id}`μ ννλ¦Ώμ μ¬μ©ν κ²μ! ")
        await template.apply(ctx.guild)

    @commands.command(name="ννλ¦Ώμ­μ ")
    @commands.has_permissions(administrator=True)
    async def delete_template(self,ctx, template_id: str):
        template = await self.TemplateManager.get_template(template_id)
        # Here, you could check permissions, I recommend checking if ctx is the template guild.
        if not template:
            await ctx.send("ν΄λΉνλ ννλ¦Ώμ μ°Ύμ§λͺ»νμ΄μ.")
            return
        if template.info.guild != ctx.guild.id:
            await ctx.send("λ€λ₯Έ μλ²μ ννλ¦Ώμ μ­μ ν  μ μμ΄μ!")
            return
        partial_template = await template.delete()
        await ctx.send(f"λ€μID`{partial_template.info.template_id}`μ ννλ¦Ώμ μ­μ νμ΄μ!")

    @commands.command(name="ννλ¦Ώλͺ©λ‘")
    async def get_guild_templates(self,ctx):
        templates = await self.TemplateManager.get_templates()
        em = discord.Embed(
            title=f"ννλ¦Ώ λͺ©λ‘ β’ μ΄ {len(templates)}κ° λ±λ‘λμ΄μμ΄μ.",
            description="μ¬λ¬ μλ²κ° μ¬λ¦° ννλ¦ΏμΌλ‘ μ½κ² μλ²λ₯Ό κ΅¬μ±ν΄λ³΄μΈμ!π\nμ¬μ©νμ€λ €λ©΄ μμ²­μλμ΄ κ΄λ¦¬μ κΆνμ΄ μμ΄μΌν΄μ.",
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
                name=f"μλ²: {self.bot.get_guild(i.info.guild)}",
                value=f"""
```fix
ννλ¦ΏID - {i.info.template_id}

νμ€νΈ μ±λλ€({len(i.text_channels)}κ°)
{text_channels_list}
...

μμ± μ±λλ€({len(i.voice_channels)}κ°)
{voice_channels_list}
...

μΉ΄νκ³ λ¦¬λ€({len(i.categories)}κ°)
{category_channels_list}
...

μ μ©νκΈ° - νλ¦°μ ννλ¦Ώμ¬μ© {i.info.template_id}
```
                """
            )
        await ctx.reply(embed=em)
        #await ctx.send(templates[1])

    @commands.command(name="ννλ¦Ώμ°ΎκΈ°")
    async def get_templates(self,ctx, id=None):
        if id == None:
            templates = await self.TemplateManager.get_templates(ctx.guild)
            em = discord.Embed(
                title=f"ννλ¦Ώ λͺ©λ‘ β’ μ΄ {len(templates)}κ° λ±λ‘λμ΄μμ΄μ.",
                description="μ¬λ¬ μλ²κ° μ¬λ¦° ννλ¦ΏμΌλ‘ μ½κ² μλ²λ₯Ό κ΅¬μ±ν΄λ³΄μΈμ!π\nμ¬μ©νμ€λ €λ©΄ μμ²­μλμ΄ κ΄λ¦¬μ κΆνμ΄ μμ΄μΌν΄μ.",
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
                    name=f"μλ²: {ctx.guild}",
                    value=f"""
```fix
ννλ¦ΏID - {i.info.template_id}

νμ€νΈ μ±λλ€({len(i.text_channels)}κ°)
{text_channels_list}
...

μμ± μ±λλ€({len(i.voice_channels)}κ°)
{voice_channels_list}
...

μΉ΄νκ³ λ¦¬λ€({len(i.categories)}κ°)
{category_channels_list}
...

μ μ©νκΈ° - νλ¦°μ ννλ¦Ώμ¬μ© {i.info.template_id}
```
                            """
                )
            await ctx.reply(embed=em)
        else:
            template = await self.TemplateManager.get_template(id)
            if not template:
                await ctx.send("ν΄λΉνλ ννλ¦Ώμ μ°Ύμ§ λͺ»νμ΄μ.")
                return
            em = discord.Embed(
                title=f"ννλ¦Ώ μμΈ.",
                description="μ¬λ¬ μλ²κ° μ¬λ¦° ννλ¦ΏμΌλ‘ μ½κ² μλ²λ₯Ό κ΅¬μ±ν΄λ³΄μΈμ!π\nμ¬μ©νμ€λ €λ©΄ μμ²­μλμ΄ κ΄λ¦¬μ κΆνμ΄ μμ΄μΌν΄μ.",
                colour=discord.Colour.random()
            )
            text_channels = [j.name for j in template.text_channels[:5]]
            text_channels_list = "\n".join(text_channels)
            voice_channels = [j.name for j in template.voice_channels[:5]]
            voice_channels_list = "\n".join(voice_channels)
            category_channels = [j.name for j in template.categories[:5]]
            category_channels_list = "\n".join(category_channels)
            em.add_field(
                name=f"μλ²: {self.bot.get_guild(template.info.guild)}",
                value=f"""
```fix
ννλ¦ΏID - {id}

νμ€νΈ μ±λλ€({len(template.text_channels)}κ°)
{text_channels_list}
...

μμ± μ±λλ€({len(template.voice_channels)}κ°)
{voice_channels_list}
...

μΉ΄νκ³ λ¦¬λ€({len(template.categories)}κ°)
{category_channels_list}
...

μ μ©νκΈ° - νλ¦°μ ννλ¦Ώμ¬μ© {id}
```
                        """
            )
            await ctx.reply(content="λ€μμ ννλ¦Ώμ μ°Ύμμ΄μ",embed=em)
    @commands.command(name="ννλ¦Ώλ±λ‘")
    @commands.has_permissions(administrator=True)
    async def create_template(self,ctx):
        # Again, you should check permissions here to make sure this isn't abused.
        # You can also get all the templates a guild has, using TemplateManager.get_templates
        msg = await ctx.reply("λ±λ‘μ€μ΄μμ! μ±λμμ μ­ν μμ λ°λΌ μ€λκ±Έλ¦΄ μλμμ΄μ")
        template = await self.TemplateManager.create_template(ctx.guild)
        await msg.edit(f"μ±κ³΅μ μΌλ‘ ννλ¦Ώμ λ±λ‘νμ΄μ! ID - `{template.info.template_id}`")


def setup(bot):
    bot.add_cog(invitetracker(bot))