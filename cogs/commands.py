import discord
from discord.ext import commands
import platform
import sys
import json
from pathlib import Path

cwd = Path(__file__).parents[0]
cwd = str(cwd)

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Commands Cog has been loaded\n-----")

    @commands.command(
        name='hi', 
        aliases=['hello'],
        description='Says Hello')
    async def _hi(self, ctx):
        await ctx.send(f"👉👈 Hi {ctx.author.mention}!")
        

    @commands.command(
        name='setlogchannel',
        aliases=['slc'],
        description='Set the log output channel for staff commands'
    )
    @commands.has_guild_permissions(administrator=True)
    async def setlogchannel(self, ctx, logchan=''):
        data = {
            'guildId': ctx.guild.id,
            'channelid':  ctx.channel
        }
        await self.bot.logchannel.upsert(data)
        await ctx.send("Test Complete")

def setup(bot):
    bot.add_cog(Commands(bot))
