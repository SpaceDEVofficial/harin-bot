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
class invitetracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ImageManager = discordSuperUtils.ImageManager()
        self.TemplateManager = discordSuperUtils.TemplateManager(self.bot)


    @commands.command(name="템플릿사용")
    @commands.has_permissions(administrator=True)
    async def apply_template(self,ctx, template_id: str):
        database = self.bot.db
        await self.TemplateManager.connect_to_database(
            database,
            [
                "templates",
                "categories",
                "text_channels",
                "voice_channels",
                "roles",
                "overwrites",
            ],
        )
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
        database = self.bot.db
        await self.TemplateManager.connect_to_database(
            database,
            [
                "templates",
                "categories",
                "text_channels",
                "voice_channels",
                "roles",
                "overwrites",
            ],
        )
        template = await self.TemplateManager.get_template(template_id)
        # Here, you could check permissions, I recommend checking if ctx is the template guild.
        if not template:
            await ctx.send("해당하는 템플릿을 찾지못했어요.")
            return

        partial_template = await template.delete()
        await ctx.send(f"다음ID`{partial_template.info.template_id}`의 템플릿을 삭제했어요!")

    @commands.command(name="템플릿목록")
    async def get_guild_templates(self,ctx):
        await self.TemplateManager.connect_to_database(
            self.bot.db,
            [
                "templates",
                "categories",
                "text_channels",
                "voice_channels",
                "roles",
                "overwrites",
            ],
        )
        templates = await self.TemplateManager.get_templates()
        await ctx.send(templates)

    @commands.command(name="템플릿찾기")
    async def get_templates(self,ctx, id=None):
        await self.TemplateManager.connect_to_database(
            self.bot.db,
            [
                "templates",
                "categories",
                "text_channels",
                "voice_channels",
                "roles",
                "overwrites",
            ],
        )
        if id == None:
            templates = await self.TemplateManager.get_templates(ctx.guild)
            await ctx.send(templates)
        else:
            template = await self.TemplateManager.get_template(id)
            if not template:
                await ctx.send("해당하는 템플릿을 찾지 못했어요.")
                return

            await ctx.send(f"다음의 템플릿을 찾았어요: {template}")
    @commands.command(name="템플릿등록")
    @commands.has_permissions(administrator=True)
    async def create_template(self,ctx):
        await self.TemplateManager.connect_to_database(
            self.bot.db,
            [
                "templates",
                "categories",
                "text_channels",
                "voice_channels",
                "template_roles",
                "overwrites",
            ],
        )
        # Again, you should check permissions here to make sure this isn't abused.
        # You can also get all the templates a guild has, using TemplateManager.get_templates
        template = await self.TemplateManager.create_template(ctx.guild)
        await ctx.send(f"성공적으로 템플릿을 등록했어요! ID - `{template.info.template_id}`")

def setup(bot):
    bot.add_cog(invitetracker(bot))