import io
import asyncio
import urllib.request

import aiosqlite
import discord
from PIL import Image
from discord.ext import commands
import discordSuperUtils
class invitetracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ImageManager = discordSuperUtils.ImageManager()
        self.InviteTracker = discordSuperUtils.InviteTracker(self.bot)

    @commands.Cog.listener("on_member_join")
    async def invite_tracker(self,member):
        database = await aiosqlite.connect("db/db.sqlite")
        database = discordSuperUtils.DatabaseManager.connect(database)
        await self.InviteTracker.connect_to_database(database, ["invites"])
        cur = await database.execute("SELECT * FROM invite_tracker WHERE guild = ?",(member.guild.id,))
        data = await cur.fetchone()
        if data != None:
            invite = await self.InviteTracker.get_invite(member)
            inviter = await self.InviteTracker.fetch_inviter(invite)
            await self.InviteTracker.register_invite(invite, member, inviter)

            channel = self.bot.get_channel(data[1])
            if inviter == None:
                await channel.send(
                    f"{member.mention}님은 누군가의 초대로 접속하셨어요. 코드 - {invite.code}"
                )
                return
            await channel.send(
                f"{member.mention}님은 {inviter.mention}님의 초대로 접속하셨어요. 코드 - {invite.code}"
            )

    @commands.command(name="초대정보")
    async def info(self,ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        invited_members = await self.InviteTracker.get_user_info(member).get_invited_users()

        await ctx.send(
            f"{member.mention}님이 초대한 멤버들({len(invited_members)}명): "
            + ", ".join(str(x) for x in invited_members)
        )

def setup(bot):
    bot.add_cog(invitetracker(bot))