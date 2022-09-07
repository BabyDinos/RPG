from nextcord.ext import commands
import asyncio
import aiosqlite
from sqlitedict import SqliteDict
from sqliteCommands import sqlCommands
from enemyClass import *
from playerClass import *
import nextcord

class comCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fight(self, ctx):
        self.id = str(ctx.author).split('#')[-1]
        res = sqlCommands.load(self.id, database = 'player')
        if not res:
            await ctx.send('You are not registered', delete_after = 20)
        else:
            await ctx.send('Adding Gold', delete_after = 20)
            res.inventory = addItem(res, ['Gold', 'Gold'], [5, 10])
            sqlCommands.save(self.id, res, database = 'player')

            # enemy = Enemy('Golem')
            # player = sqlCommands.load(self.id, databases = 'player')
            # while enemy.curHealth > 0 and player.curHealth > 0:
            #     pass
        ctx.message.delete()

    @commands.command()
    async def equip(self, ctx):
        self.id = str(ctx.author).split('#')[-1]
        player = sqlCommands.load(self.id, database = 'player')
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
                sqlCommands.save(self.id, player, database = 'player')
            except:
                print('Connection Timedout', delete_after = 20)
                try:
                    await equipment_message.delete()
                except:
                    pass
        await equipment_message.delete()
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(comCommands(bot))
