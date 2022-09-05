import asyncio
import discord
from discord.ext import commands
from config import *
from start import *

bot = commands.Bot(command_prefix=PREFIX)

@client.command()
async def register(ctx, member:discord.Member):
    await ctx.send('What is your Username?')
    try:
        message = await client.wait_for('message', timeout = 60, check= lambda message: message.author == ctx.author and message.channel == ctx.channel)
        if message:
            id = ctx.author.id
            async with aiosqlite.connect("main.db") as db:
                async with db.cursor() as cursor:
                    await cursor.execute('INSERT INTO Players (id, username)')
                    await cursor.execute('VALUES ({})'.format(id, message))
                await db.commit()
    except asyncio.TimeoutError: 
        ctx.send('Command Timedout')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
