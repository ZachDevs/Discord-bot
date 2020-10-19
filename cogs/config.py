import random
import os
import asyncio
import traceback
import discord
from discord.ext import commands

import utils.json_loader


class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(
        name="prefix",
        aliases=["changeprefix", "setprefix"],
        description="Change your guilds prefix!",
        usage="[prefix]",
    )
    @commands.has_guild_permissions(manage_guild=True)
    async def prefix(self, ctx, *, prefix="~"):
        await self.bot.config.upsert({"_id": ctx.guild.id, "prefix": prefix})
        await ctx.send(
            f"The guild prefix has been set to `{prefix}`. Use `{prefix}prefix [prefix]` to change it again!"
        )

    @commands.command(
        name="deleteprefix", aliases=["dp"], description="Delete your guilds prefix!"
    )
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def deleteprefix(self, ctx):
        await self.bot.config.unset({"_id": ctx.guild.id, "prefix": 1})
        await ctx.send("This guilds prefix has been set back to the default")

    """
    As a viewer, watch up to episode 10 and then attempt to convert the following
    to using a database rather then continuing to use json
    """

    @commands.command(
        name="blacklist", description="Blacklist a user from the bot", usage="<user>"
    )
    @commands.is_owner()
    async def blacklist(self, ctx, user: discord.Member):
        if ctx.message.author.id == user.id:
            await ctx.send("Hey, you cannot blacklist yourself!")
            return

        self.bot.blacklisted_users.append(user.id)
        data = utils.json_loader.read_json("blacklist")
        data["blacklistedUsers"].append(user.id)
        utils.json_loader.write_json(data, "blacklist")
        await ctx.send(f"Hey, I have blacklisted {user.name} for you.")

    @commands.command(
        name="unblacklist",
        description="Unblacklist a user from the bot",
        usage="<user>",
    )
    @commands.is_owner()
    async def unblacklist(self, ctx, user: discord.Member):
        """
        Unblacklist someone from the bot
        """
        self.bot.blacklisted_users.remove(user.id)
        data = utils.json_loader.read_json("blacklist")
        data["blacklistedUsers"].remove(user.id)
        utils.json_loader.write_json(data, "blacklist")
        await ctx.send(f"Hey, I have unblacklisted {user.name} for you.")

    @commands.command(
        name="logout",
        aliases=["disconnect", "close", "stopbot"],
        description="Log the bot out of discord!",
    )
    @commands.is_owner()
    async def logout(self, ctx):
        """
        If the user running the command owns the bot then this will disconnect the bot from discord.
        """
        await ctx.send(f"Hey {ctx.author.mention}, I am now logging out :wave:")
        await self.bot.logout()

    @commands.command(
        name='reload',
        description="Reload all/one of the bots cogs.",
    )
    @commands.is_owner()
    async def reload(self, ctx, cog=None):
        if not cog:
            async with ctx.typing():
                embed = discord.Embed(
                    title="Reloading all cogs!",
                    timestamp=ctx.message.created_at
                )
                for ext in os.listdir('./cogs/'):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.bot.unload_extension(f"cogs.{ext[:-3]}")
                            self.bot.load_extension(f"cogs.{ext[:-3]}")
                            embed.add_field(
                             name=f'Reloaded: `{ext}`',
                             value='\uFEFF',
                             inline=False
                            )
                        except Exception as e:
                            embed.add_field(
                                name=f'Failed to reload: `{ext}`',
                                value=e,
                                inline=False
                            )
                        await asyncio.sleep(0.5)
            await ctx.send(embed=embed)
        else:
            # Reload Specific Cog
            async with ctx.typing():
                embed = discord.Embed(
                    title="Reloading all cogs!",
                    timestamp=ctx.message.created_at
                )
                ext = f'{cog.lower()}.py'
                if not os.path.exists(f'./cogs/{ext}'):
                    # If The Cog Doesn't Exist
                    embed.add_field(
                        name=f'Failed to reload: `{ext}`',
                        value="This cog does not exist"
                    )

                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        self.bot.unload_extension(f"cogs.{ext[:-3]}")
                        self.bot.load_extension(f"cogs.{ext[:-3]}")
                        embed.add_field(
                            name=f'Reloaded: `{ext}`',
                            value='\uFEFF',
                            inline=False
                        )
                    except Exception:
                        desired_trace = traceback.format_exc()
                        embed.add_field(
                            name=f'failed to reload: `{ext}`',
                            value=desired_trace,
                            inline=False
                        )
                await ctx.send(embed=embed)

    @commands.command(
        name='load',
        description="load one of the bots cogs.",
    )
    @commands.is_owner()
    async def load(self, ctx, cog=None):
        async with ctx.typing():
            embed= discord.Embed(
                title=f'Loading cog!',
                timestamp=ctx.message.created_at
            )
            ext = f'{cog.lower()}.py'
            if not os.path.exists(f'./cogs/{ext}'):
                # If The Cog Doesn't Exist
                embed.add_field(
                    name=f'Failed to load: `{ext}`',
                    value="This cog does not exist"
                )
            elif ext.endswith(".py") and not ext.startswith("_"):
                try:
                    self.bot.load_extension(f"cogs.{ext[:-3]}")
                    embed.add_field(
                        name=f'loaded: `{ext}`',
                        value='\uFEFF',
                        inline=False
                    )
                except Exception:
                    desired_trace = traceback.format_exc()
                    embed.add_field(
                        name=f'failed to load: `{ext}`',
                        value=desired_trace,
                        inline=False
                    )
            await ctx.send(embed=embed)

    @commands.command(
        name='unload',
        description="unload one of the bots cogs.",
    )
    @commands.is_owner()
    async def unload(self, ctx, cog=None):
        async with ctx.typing():
            embed= discord.Embed(
                title=f'Unloading cog!',
                timestamp=ctx.message.created_at
            )
            ext = f'{cog.lower()}.py'
            if not os.path.exists(f'./cogs/{ext}'):
                # If The Cog Doesn't Exist
                embed.add_field(
                    name=f'Failed to unload: `{ext}`',
                    value="This cog does not exist"
                )
            elif ext.endswith(".py") and not ext.startswith("_"):
                try:
                    self.bot.unload_extension(f"cogs.{ext[:-3]}")
                    embed.add_field(
                        name=f'unloaded: `{ext}`',
                        value='\uFEFF',
                        inline=False
                    )
                except Exception:
                    desired_trace = traceback.format_exc()
                    embed.add_field(
                        name=f'failed to unload: `{ext}`',
                        value=desired_trace,
                        inline=False
                    )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Config(bot))