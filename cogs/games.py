from discord.ext import commands
from pathlib import Path
import json

cwd = Path(__file__).parents[0]
cwd = str(cwd)

secret_file = json.load(open('D:\\codelel\\rainbow-bot/bot_config/secrets.json'))
riotkey = secret_file['riotapi']


class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = self

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")


def setup(bot):
    bot.add_cog(Games(bot))
