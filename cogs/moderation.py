import discord
from discord.ext import commands

import utils.json_loader


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.kick(user=member, reason=reason)

        channel = utils.json_loader.read_json("logchannel")
        embed = discord.Embed(title=f"{ctx.author.name} kicked: {member.name}", description=reason)
        await channel.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.ban(user=member, reason=reason)

        channel = self.bot.get_channel(760628480630849546)
        embed = discord.Embed(title=f"{ctx.author.name} Banned: {member.name}", description=reason)
        await channel.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx, member, *, reason=None):
        member = await self.bot.fetch_user(int(member))
        await ctx.guild.unban(member, reason=reason)

        channel = self.bot.get_channel(760628480630849546)
        embed = discord.Embed(title=f"{ctx.author.name} Unbanned: {member.name}", description=reason)
        await channel.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
    async def purge(self, ctx, amount=15):
        await ctx.channel.purge(limit=amount+1)

        channel = self.bot.get_channel(760628480630849546)
        embed = discord.Embed(title=f"{ctx.author.name} Purged: {ctx.channel.name}", description=f"{amount} messages were cleared")
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))