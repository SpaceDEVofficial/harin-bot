import asyncio
import datetime
import random
import io
import chat_exporter
import aiosqlite
import discord
from discord import errors
from discord.ext import commands
from pycord_components import (
    Button,
    ButtonStyle,
    Interaction
)
import html
class badword(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ticket_channel = []
        self.ticket_msg = []
        self.ticket_opentime = {}
        chat_exporter.init_exporter(self.bot)


    @commands.command(name="ν°μΌμ€μ ")
    async def create_ticket_set(self,ctx,channel:discord.TextChannel,role:discord.Role,*,text):
        em = discord.Embed(description=text,colour=discord.Colour.random())
        msg = await channel.send(embed=em,components=[
                                            [
                                                Button(label="π© ν°μΌ μ΄κΈ°",custom_id="ticket_open")
                                            ]
                                         ])
        new_category = await ctx.guild.create_category(name="π«-ν°μΌ")
        db = await aiosqlite.connect('db/db.sqlite')
        await db.execute("INSERT INTO ticket(guild,channel,message,category,role) VALUES (?,?,?,?,?)",
                         (ctx.guild.id,channel.id,msg.id,new_category.id,role.id))
        await db.commit()
        await ctx.reply("μ€μ μ΄ μλ£λμμ΄μ!")

    @commands.command(name="ν°μΌμ­μ ")
    async def create_ticket_delete(self, ctx, channel:discord.TextChannel,msg: int):
        await (await channel.fetch_message(msg)).delete()
        db = await aiosqlite.connect('db/db.sqlite')
        await db.execute("DELETE FROM ticket WHERE message = ?",
                         (msg,))
        await db.commit()
        await ctx.reply("ν°μΌμ΄ μ­μ λμμ΄μ!")


    @commands.Cog.listener('on_button_click')
    async def ticket_create(self,interaction:Interaction):
        custom_id = interaction.custom_id
        message_id = interaction.message.id
        channel_id = interaction.channel_id
        guild_id = interaction.guild_id
        if custom_id == "ticket_open":
            db = await aiosqlite.connect('db/db.sqlite')
            cur = await db.execute("SELECT * FROM ticket WHERE guild = ? AND channel = ? AND message = ?",
                                   ((guild_id,channel_id,message_id)))
            res = await cur.fetchone()
            if not res is None:
                guild = self.bot.get_guild(guild_id)
                member = discord.utils.find(lambda m: m.id == interaction.user.id, guild.members)
                support_role = guild.get_role(res[4])
                get_category = self.bot.get_channel(res[3])
                overwrites = {
                    member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    support_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                }
                channel = await get_category.create_text_channel(name="ν°μΌ - " + member.display_name,overwrites=overwrites,topic=f"{res[4]} {member.id}")
                await channel.set_permissions(guild.default_role,read_messages=False)
                await interaction.send(content=f"ν°μΌμ΄ μμ±λμμ΄μ!\nμλ μ±λλ‘ μ΄λν΄μ£ΌμΈμ!\nμμ±λ ν°μΌ - {channel.mention}",delete_after=5)
                self.ticket_channel.append(channel.id)
                now = datetime.datetime.now()
                year = now.year
                month = now.month
                date = now.day
                hour = now.hour
                minute = now.minute
                second = now.second
                open_time = f"{year}λ {month}μ {date}μΌ {hour}μ {minute}λΆ {second}μ΄"
                self.ticket_opentime[channel.id] = open_time
                embed = discord.Embed(title="λ¬΄μμ λμλλ¦΄κΉμ?",
                                      description=f"```fix\nν°μΌ κ°μ€μΌμ: {open_time}\nν°μΌ κ°μ€ μμ²­μ: {member}({member.id})```",
                                      color=0xf7fcfd)
                embed.add_field(name="π ν°μΌ μ κΈ",
                                value="```νμ¬ ν°μΌμ μ κΆμ.```",
                                inline=False)
                embed.add_field(name="π¨ ν°μΌ μΆμΆ",
                                value="```ν°μΌμμ μ€κ° μ±νλ΄μ©μ μΆμΆν΄μ.```",
                                inline=False)
                embed.add_field(name="β ν°μΌ μ’λ£",
                                value="```νμ¬ ν°μΌμ μ’λ£νκ³  μ±λμ μ­μ ν΄μ.```",
                                inline=False)

                msg = await channel.send(content=f"{support_role.mention}\n{member.mention}",
                                         embed=embed,
                                         components=[
                                            [
                                                Button(label="π ν°μΌ μ κΈ",custom_id="ticket_lock",style=4),
                                                Button(label="π¨ ν°μΌ μΆμΆ",custom_id="ticket_export",style=3),
                                                Button(label="β ν°μΌ μ’λ£",custom_id="ticket_cancel",style=4)
                                            ]
                                         ])
                self.ticket_msg.append(msg.id)
        if custom_id == "ticket_lock":
            if message_id in self.ticket_msg:
                guild = self.bot.get_guild(guild_id)
                channel = self.bot.get_channel(channel_id)
                message = await channel.fetch_message(message_id)
                member = discord.utils.find(lambda m: m.id == interaction.user.id, guild.members)
                if not int(channel.topic.split(" ")[0]) in [r.id for r in member.roles]:
                    return await interaction.respond(content="μ§μνλ§ μ¬μ©ν  μ μμ΄μ!")
                await interaction.respond(content=f"ν°μΌμ κΈμμ²­μ νμ¨μ΄μ!")
                open_time = self.ticket_opentime[channel.id]
                member = discord.utils.find(lambda m: m.id == int(channel.topic.split(" ")[1]), guild.members)
                await channel.set_permissions(member,read_messages=True,send_messages=False)
                embed = discord.Embed(title="λ¬΄μμ λμλλ¦΄κΉμ?",
                                      description=f"```fix\nν°μΌ κ°μ€μΌμ: {open_time}\nν°μΌ κ°μ€ μμ²­μ: {member}({member.id})```",
                                      color=0xf7fcfd)
                embed.add_field(name="π ν°μΌ μ κΈν΄μ ",
                                value="```νμ¬ ν°μΌμ μ κΈν΄μ μ.```",
                                inline=False)
                embed.add_field(name="π¨ ν°μΌ μΆμΆ",
                                value="```ν°μΌμμ μ€κ° μ±νλ΄μ©μ μΆμΆν΄μ.```",
                                inline=False)
                embed.add_field(name="β ν°μΌ μ’λ£",
                                value="```νμ¬ ν°μΌμ μ’λ£νκ³  μ±λμ μ­μ ν΄μ.```",
                                inline=False)
                em = discord.Embed(description="π νμ¬ μ΄ ν°μΌμ μ κ²¨μλ μνμλλ€.", colour=discord.Colour.red())
                await channel.send(embed=em)
                await message.edit(embed=embed,
                                 components=[
                                    [
                                        Button(label="π ν°μΌ μ κΈν΄μ ",custom_id="ticket_unlock",style=4),
                                        Button(label="π¨ ν°μΌ μΆμΆ",custom_id="ticket_export",style=3),
                                        Button(label="β ν°μΌ μ’λ£",custom_id="ticket_cancel",style=4)
                                    ]
                                 ])
        if custom_id == "ticket_unlock":
            if message_id in self.ticket_msg:
                guild = self.bot.get_guild(guild_id)
                channel = self.bot.get_channel(channel_id)
                message = await channel.fetch_message(message_id)
                member = discord.utils.find(lambda m: m.id == interaction.user.id, guild.members)
                if not int(channel.topic.split(" ")[0]) in [r.id for r in member.roles]:
                    return await interaction.respond(content="μ§μνλ§ μ¬μ©ν  μ μμ΄μ!")
                await interaction.respond(content=f"ν°μΌμ κΈν΄μ μμ²­μ νμ¨μ΄μ!")
                open_time = self.ticket_opentime[channel.id]
                member = discord.utils.find(lambda m: m.id == int(channel.topic.split(" ")[1]), guild.members)
                await channel.set_permissions(member,read_messages=True,send_messages=True)
                embed = discord.Embed(title="λ¬΄μμ λμλλ¦΄κΉμ?",
                                      description=f"```fix\nν°μΌ κ°μ€μΌμ: {open_time}\nν°μΌ κ°μ€ μμ²­μ: {member}({member.id})```",
                                      color=0xf7fcfd)
                embed.add_field(name="π ν°μΌ μ κΈ",
                                value="```νμ¬ ν°μΌμ μ κΆμ.```",
                                inline=False)
                embed.add_field(name="π¨ ν°μΌ μΆμΆ",
                                value="```ν°μΌμμ μ€κ° μ±νλ΄μ©μ μΆμΆν΄μ.```",
                                inline=False)
                embed.add_field(name="β ν°μΌ μ’λ£",
                                value="```νμ¬ ν°μΌμ μ’λ£νκ³  μ±λμ μ­μ ν΄μ.```",
                                inline=False)
                em = discord.Embed(description="π ν°μΌμ΄ λ€μ μ΄λ Έμ΄μ!", colour=discord.Colour.red())
                await channel.send(embed=em)
                await message.edit(embed=embed,
                                 components=[
                                    [
                                        Button(label="π ν°μΌ μ κΈ",custom_id="ticket_lock",style=4),
                                        Button(label="π¨ ν°μΌ μΆμΆ",custom_id="ticket_export",style=3),
                                        Button(label="β ν°μΌ μ’λ£",custom_id="ticket_cancel",style=4)
                                    ]
                                 ])
        if custom_id == "ticket_export":
            if message_id in self.ticket_msg:
                channel = self.bot.get_channel(channel_id)
                transcript = await chat_exporter.export(channel,set_timezone="Asia/Seoul")

                if transcript is None:
                    return
                transcript_file = discord.File(io.BytesIO(transcript.encode()),
                                               filename=f"ticket-{channel.id}.html")

                await interaction.send(content="μΆμΆμ΄ μλ£λμμ΄μ! \nμλ νμΌμ λ€μ΄λ°μ λΈλΌμ°μ μμ μ΄μ΄μ£ΌμΈμ!",file=transcript_file)
        if custom_id == "ticket_cancel":
            if message_id in self.ticket_msg:
                channel = self.bot.get_channel(channel_id)
                await interaction.respond(content=f"β ν°μΌ μ’λ£ μμ²­μ νμ¨μ΄μ!\nμ μν μ±λμ΄ μ­μ λ©λλ€.")
                em = discord.Embed(description="β ν°μΌ μ’λ£ μμ²­μ νμ¨μ΄μ!\nμ μν μ±λμ΄ μ­μ λ©λλ€.",colour=discord.Colour.red())
                await channel.send(embed=em)
                await asyncio.sleep(5)
                self.ticket_channel.remove(channel.id)
                self.ticket_msg.remove(message_id)
                del self.ticket_opentime[channel_id]
                await channel.delete()


def setup(bot):
    bot.add_cog(badword(bot))
