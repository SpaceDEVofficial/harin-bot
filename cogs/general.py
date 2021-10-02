import io
import asyncio
import discord
from discord.ext import commands
class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.reply("pong!")

def setup(bot):
    bot.add_cog(general(bot))
