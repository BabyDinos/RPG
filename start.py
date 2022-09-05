import discord
import aiosqlite
import asyncio
from discord.ext import commands
import logging


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix='$', intents = intents)

@bot.event 
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('CREATE TABLE IF NOT EXISTS Players (id INTEGER, username CHAR)')
        await db.commit()

@bot.command()
async def register(ctx):
    await ctx.send('What is your Username?')
    try:
        message = await bot.wait_for('message', timeout = 10, check= lambda message: message.author == ctx.author and message.channel == ctx.channel)
        if message:
            id = str(ctx.author).split('#')[-1]
            async with aiosqlite.connect("main.db") as db:
                async with db.cursor() as cursor:
                    records = [int(id), str(message.content)]
                    sql = '''
                            INSERT INTO Players
                            VALUES (?, ?)
                          '''
                    await cursor.execute(sql, records)
                await db.commit()
    except asyncio.TimeoutError: 
        await ctx.send('Command Timedout')


@bot.command()
async def info(ctx):
    await ctx.send('What is your Username?')
    try:
        message = await bot.wait_for('message', timeout = 3, check= lambda message: message.author == ctx.author and message.channel == ctx.channel)
        if message:
            await ctx.send(message.content)
    except asyncio.TimeoutError: 
        await ctx.send('Command Timedout')


bot.run("MTAxNjE2MDU3NjIzMTE5MDU2OA.G4R00P.75tIsDcv1Jx9LCG4CslJszN6MhRSalNXRntIr0", log_handler=handler)