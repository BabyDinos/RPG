from discord.ext import commands
import asyncio
import aiosqlite
from sqlitedict import SqliteDict
from sqliteCommands import sqlCommands
from enemyClass import *
from playerClass import *
import discord

class comCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fight(self, ctx):
        self.id = str(ctx.author).split('#')[-1]
        res = sqlCommands.load(self.id, unit = 'player')
        if not res:
            await ctx.send('You are not registered')
        else:
            enemy = Enemy('Golem')
            player = sqlCommands.load(self.id, units = 'player')
            while enemy.curHealth > 0 and player.curHealth > 0:
                pass

    @commands.command()
    async def equip(self, ctx):
        self.id = str(ctx.author).split('#')[-1]
        player = sqlCommands.load(self.id, unit = 'player')
        if not player:
            await ctx.send('You are not registered', delete_after = 20)
        else:
            try:
                await ctx.send('What would you like to equip?', delete_after = 20)
                equipment_message = await self.bot.wait_for('message', timeout = 20, check= lambda message: message.author == ctx.author and message.channel == ctx.channel)
                if player.equip(equipment_message.content):
                    await ctx.send('Equipment changed to: ' + equipment_message.content, delete_after = 20)
                else:
                    await ctx.send('Equipment not found', delete_after = 20)
                sqlCommands.save(self.id, player, unit = 'player')
            except:
                print('Connection Timedout', delete_after = 20)
                try:
                    await equipment_message.delete()
                except:
                    pass
        await equipment_message.delete()
        await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(comCommands(bot))