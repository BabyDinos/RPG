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
    if not os.path.exists('player.sqlite'):
        SqliteDict('player.sqlite')
    if not os.path.exists('enemy.sqlite'):
        SqliteDict('enemy.sqlite')

# @bot.event
# async def on_message(message):
#     asyncio.sleep(2)
#     commands = ['register','nameChange','info','delete','inventory']
#     commands = [PREFIX + x for x in commands]
#     if message.content not in commands:
#         if message.author == bot.user:
#             pass
#         else: 
#             await message.delete()
#     else:
#         await bot.process_commands(message)


async def main():
    await load()
    await bot.start(TOKEN)

discord.utils.setup_logging()

asyncio.run(main())
