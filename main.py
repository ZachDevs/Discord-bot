# Things to Import
import discord  # For discord
from discord.ext import commands  # For discord
import json
from pathlib import Path  # For paths
import logging
import os
import motor.motor_asyncio

import utils.json_loader
from utils.mongo import Document
import utils.mongo

# Get Current Working Directory
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")


async def get_prefix(bot, message):
    # If dm's
    if not message.guild:
        return commands.when_mentioned_or("~")(bot, message)

    try:
        data = await bot.config.find(message.guild.id)

        # Make sure we have a useable prefix
        if not data or "prefix" not in data:
            return commands.when_mentioned_or("~")(bot, message)
        return commands.when_mentioned_or(data["prefix"])(bot, message)
    except:
        return commands.when_mentioned_or("~")(bot, message)

# Defining a few things


secret_file = utils.json_loader.read_json('secrets')
bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, owner_id=533747233225703444)
bot.config_token = secret_file['token']
bot.connection_url = secret_file['mongo']
logging.basicConfig(level=logging.INFO)

bot.blacklisted_users = []
bot.muted_users = {}
bot.cwd = cwd
bot.version = '0.0.1'


@bot.event
async def on_ready():
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: ~\n-----")
    await bot.change_presence(activity=discord.Game(name=f"My Prefix Is ~ | Use It To Interact With Me"))

    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
    bot.db = bot.mongo["prefixes"]
    bot.config = Document(bot.db, "config")
    bot.mutes = Document(bot.db, "mutes")

    for document in await bot.config.get_all():
        print(document)

    currentMutes = await bot.mutes.get_all()
    for mute in currentMutes:
        bot.muted_users[mute["_id"]] = mute

    print(bot.muted_users)
    print("Initialized Database\n-----")


@bot.event
async def on_message(message):
    # Ignore messages sent by yourself
    if message.author.bot:
        return

    # A way to blacklist users from the bot by not processing commands
    # if the author is in the blacklisted_users list
    if message.author.id in bot.blacklisted_users:
        return

    # Whenever the bot is tagged, respond with its prefix
    if message.content.startswith(f"<@!{bot.user.id}>") and \
        len(message.content) == len(f"<@!{bot.user.id}>"
    ):
        data = await bot.config.get_by_id(message.guild.id)
        if not data or "prefix" not in data:
            prefix = "~"
        else:
            prefix = data["prefix"]
        await message.channel.send(f"My prefix here is `{prefix}`", delete_after=15)

    await bot.process_commands(message)

if __name__ == '__main__':
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")
    bot.run(bot.config_token)  # Runs The Bot
