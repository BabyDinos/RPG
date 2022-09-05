from discord.ext import commands
import asyncio
import aiosqlite
from sqlitedict import SqliteDict
from sqliteCommands import sqlCommands
from enemyClass import *
from playerClass import *
import discord

class combatCommands(commands.Cog):

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

async def setup(bot):
    await bot.add_cog(combatCommands(bot))