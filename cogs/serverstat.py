import asyncio

import aiosqlite
import discord
import discordSuperUtils
from discord.ext import commands

class serverstat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stat = self.bot.loop.create_task(self.stat_loop())

    async def cog_before_invoke(self, ctx: commands.Context):
        print(ctx.command)
        if ctx.command.name != 'λ©μΌ':
            database = await aiosqlite.connect("db/db.sqlite")
            cur = await database.execute(
                'SELECT * FROM uncheck WHERE user_id = ?', (ctx.author.id,)
            )

            if await cur.fetchone() is None:
                cur = await database.execute("SELECT * FROM mail")
                mails = await cur.fetchall()
                check = sum(1 for _ in mails)
                mal = discord.Embed(
                    title=f'π«νλ¦°λ΄ λ©μΌν¨ | {check}κ° μμ λ¨',
                    description="μμ§ μ½μ§ μμ λ©μΌμ΄ μμ΄μ.'`νλ¦°μ λ©μΌ`'λ‘ νμΈνμΈμ.\nμ£ΌκΈ°μ μΌλ‘ λ©μΌν¨μ νμΈν΄μ£ΌμΈμ! μμν μλ°μ΄νΈ λ° μ΄λ²€νΈκ°μ΅λ± μ¬λ¬μμμ νμΈν΄λ³΄μΈμ.",
                    colour=ctx.author.colour,
                )

                return await ctx.send(embed=mal)
            cur = await database.execute('SELECT * FROM mail')
            mails = await cur.fetchall()
            check = sum(1 for _ in mails)
            # noinspection DuplicatedCode
            cur = await database.execute("SELECT * FROM uncheck WHERE user_id = ?", (ctx.author.id,))
            # noinspection DuplicatedCode
            check2 = await cur.fetchone()
            if str(check) != str(check2[1]):
                mal = discord.Embed(
                    title=f'π«νλ¦°λ΄ λ©μΌν¨ | {int(check) - int(check2[1])}κ° μμ λ¨',
                    description="μμ§ μ½μ§ μμ λ©μΌμ΄ μμ΄μ.'`νλ¦°μ λ©μΌ`'λ‘ νμΈνμΈμ.\nμ£ΌκΈ°μ μΌλ‘ λ©μΌν¨μ νμΈν΄μ£ΌμΈμ! μμν μλ°μ΄νΈ λ° μ΄λ²€νΈκ°μ΅λ± μ¬λ¬μμμ νμΈν΄λ³΄μΈμ.",
                    colour=ctx.author.colour,
                )

                await ctx.send(embed=mal)

    async def stat_loop(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            database = await aiosqlite.connect("db/db.sqlite")
            cur = await database.execute("SELECT * FROM serverstat")
            datas = await cur.fetchall()
            for i in datas:
                guild = self.bot.get_guild(i[0])
                all_count = len(guild.members)
                user_count = len([m for m in guild.members if not m.bot])
                bot_count = len([m for m in guild.members if m.bot])
                all_channel = self.bot.get_channel(i[2])
                user_channel = self.bot.get_channel(i[4])
                bot_channel = self.bot.get_channel(i[3])
                try:
                    await all_channel.edit(name=i[6].format(all=all_count))
                    await user_channel.edit(name=i[8].format(user=user_count))
                    await bot_channel.edit(name=i[7].format(bots=bot_count))
                except discord.Forbidden:
                    await guild.owner.send("μλ²μ€νμ μλ°μ΄νΈνλ €λ λμ€ μ±λκ΄λ¦¬κΆνμ΄ λΆμ‘±νμ¬ μ€ν¨νμ΄μ! μ  κΆνμ νμΈν΄μ£ΌμΈμ.")
            await asyncio.sleep(60 * 30)

    def cog_unload(self):
        self.stat.cancel()


def setup(bot):
    bot.add_cog(serverstat(bot))
