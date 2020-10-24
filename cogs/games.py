from discord.ext import commands
from pathlib import Path
import json

cwd = Path(__file__).parents[0]
cwd = str(cwd)



class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = self

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")


def setup(bot):
    bot.add_cog(Games(bot))
