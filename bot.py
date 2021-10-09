import os
import discord
from discord.ext import commands
from tools.autocogs import AutoCogs
from dotenv import load_dotenv
import config
load_dotenv(verbose=True)


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        AutoCogs(self)
        self.remove_command("help")
    async def on_ready(self):
        """Called upon the READY event"""
        await self.change_presence(status=discord.Status.online, activity=discord.Activity(name="TESTING..",
                                                                                               type=discord.ActivityType.playing))
        print("Bot is ready.")

    async def is_owner(self, user):
        if user.id in config.OWNER:
            return True






INTENTS = discord.Intents.all()
my_bot = MyBot(command_prefix=["하린아 ","하린아","ㅎ","ㅎ "], intents=INTENTS)


if __name__ == "__main__":
    my_bot.run(os.getenv('TOKEN'))