import discord
from discord.ext import commands
import random


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Ignore these errors
        ignored = (commands.CommandNotFound, commands.UserInputError)
        if isinstance(error, ignored):
            return

        # Begin Error Handling
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            if int(h) is 0 and int(m) is 0:
                await ctx.send(f' You Must Wait {int(s)} Seconds To Use This Command!')
            elif int(h) is 0 and int(m) is not 0:
                await ctx.send(f' You Must Wait {int(m)} Minutes And {int(s)} Seconds To Use This Command!')
            else:
                await ctx.send(f' You Must Wait {int(h)} Hours, {int(m)} Minutes And {int(s)} Seconds To Use This Command! ')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You lack permission to use this command")
        raise error


def setup(bot):
    bot.add_cog(Events(bot))