import discord
import aiosqlite
import asyncio
from discord.ext import commands
import logging
from config import *
import os
from sqlitedict import SqliteDict

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix=PREFIX, intents = intents)

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await bot.load_extension(f"cogs.{filename[:-3]}")

@bot.command()
async def hello(ctx):
    await ctx.send('hello')

@bot.event 
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    if not os.path.exists('main.sqlite'):
        SqliteDict('main.sqlite')
    # async with aiosqlite.connect("main.db") as db:
    #     async with db.cursor() as cursor:
    #         await cursor.execute('CREATE TABLE IF NOT EXISTS Players (id INTEGER, username CHAR)')
    #     await db.commit()

async def main():
    await load()
    await bot.start(TOKEN)

discord.utils.setup_logging()

asyncio.run(main())
