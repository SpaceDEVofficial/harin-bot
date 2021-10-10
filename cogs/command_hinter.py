import io
import asyncio
import urllib.request
import aiosqlite
import discord
from PIL import Image
from discord.ext import commands
import discordSuperUtils
import random
from typing import List

def random_chat(suggest):
    chatlist = ["혹시 `하린아 {hint}`를 사용하시려고 한건가요?",
                "그 명령어는 없는데 `하린아 {hint}`로 사용해보세요!",
                "한번 `하린아 {hint}`로 명령해보세요!"]
    res = random.choice(chatlist)
    return res.format(hint=suggest)

class MyCommandGenerator(discordSuperUtils.CommandResponseGenerator):
    def generate(self, invalid_command: str, suggestion: List[str]) -> str:
        # This is only an example, you can use the default generator if you want to.
        res = random_chat(suggest=suggestion[0])
        return res


class commandhint(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ImageManager = discordSuperUtils.ImageManager()
        discordSuperUtils.CommandHinter(self.bot, MyCommandGenerator())


def setup(bot):
    bot.add_cog(commandhint(bot))
