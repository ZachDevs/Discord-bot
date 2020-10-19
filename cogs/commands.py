import discord
from discord.ext import commands
import platform

import utils.json_loader


class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Commands Cog has been loaded\n-----")

    @commands.command(name='hi', aliases=['hello'])
    async def _hi(self, ctx):
        await ctx.send(f"👉👈 Hi {ctx.author.mention}!")

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def setlogchannel(self, ctx, logchan=''):
        data = utils.json_loader.read_json('logchannel')
        data[str(ctx.message.guild.id)] = logchan
        utils.json_loader.write_json(data, 'logchannel')
        await ctx.send(f"Log channel set to {logchan}")

def setup(bot):
    bot.add_cog(Commands(bot))