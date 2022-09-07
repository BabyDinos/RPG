import nextcord
from nextcord.ext import commands
import aiosqlite
import asyncio
import logging
from config import *
import os
from sqlitedict import SqliteDict


intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix=PREFIX, intents = intents)

@bot.event 
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    if not os.path.exists('player.sqlite'):
        SqliteDict('player.sqlite')
    if not os.path.exists('enemy.sqlite'):
        SqliteDict('enemy.sqlite')

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        # cut off the .py from the file name
        bot.load_extension(f"cogs.{filename[:-3]}")
        print(filename[:-3] + ' has loaded')

bot.run(TOKEN)
