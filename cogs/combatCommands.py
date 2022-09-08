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
    
    #cooldown time should be same as timeout time for embed
    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def fight(self, ctx):
        self.id = str(ctx.author).split('#')[-1]
        player = sqlCommands.load(self.id, database = 'player')
        if not player:
            await ctx.send('You are not registered', delete_after = 20)
        else:
            golem = Golem('Golem',[1,5],[1,3],[2,5],[1,2],[2,5],[1,2],2, 2, 2)
            player.CurrentHealth = 0
            sqlCommands.save(self.id, player, database= 'player')

            await ctx.send(str(player.CurrentHealth))
            await asyncio.sleep(10)

            player.CurrentHealth = 10
            await ctx.send(str(player.CurrentHealth))
        await ctx.message.delete()

    @fight.error
    async def on_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after), delete_after = 20)
        else:
            raise error

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
