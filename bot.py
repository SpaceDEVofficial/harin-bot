import os

import aiosqlite
import discord
import discordSuperUtils
from discord.ext import commands
from tools.autocogs import autocogs
from dotenv import load_dotenv
from pycord_components import PycordComponents
import config

load_dotenv(verbose=True)


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remove_command("help")
        autocogs(self)

    async def on_ready(self):
        """Called upon the READY event"""
        await self.change_presence(status=discord.Status.online,
                                   activity=discord.Activity(name="하린아 도움 | 서버: {}".format(len(self.guilds)),
                                                             type=discord.ActivityType.playing))
        print("Bot is ready.")

    async def is_owner(self, user):
        if user.id in config.OWNER:
            return True

    @staticmethod
    async def create_db_con():
        MyBot.db = discordSuperUtils.DatabaseManager.connect(database=await aiosqlite.connect("db/db.sqlite"))


INTENTS = discord.Intents.all()
my_bot = MyBot(command_prefix=["하린아 ", "하린아", "ㅎ", "ㅎ "], intents=INTENTS)
PycordComponents(my_bot)

if __name__ == "__main__":
    my_bot.loop.run_until_complete(MyBot.create_db_con())
    my_bot.run(os.getenv('TOKEN'))
