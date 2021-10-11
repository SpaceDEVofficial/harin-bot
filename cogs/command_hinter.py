import random
from typing import List

import discordSuperUtils
from discord.ext import commands


def random_chat(suggest):
    chatlist = ["혹시 `하린아 {hint}`를 사용하시려고 한건가요?",
                "그 명령어는 없는데 `하린아 {hint}`로 사용해보세요!",
                "한번 `하린아 {hint}`로 명령해보세요!"]
    res = random.choice(chatlist)
    return res.format(hint=suggest)


class MyCommandGenerator(discordSuperUtils.CommandResponseGenerator):
    def generate(self, invalid_command: str, suggestion: List[str]) -> str:
        # This is only an example, you can use the default generator if you want to.
        return random_chat(suggest=suggestion[0])


class CommandHint(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ImageManager = discordSuperUtils.ImageManager()
        discordSuperUtils.CommandHinter(self.bot, MyCommandGenerator())


def setup(bot):
    bot.add_cog(CommandHint(bot))
