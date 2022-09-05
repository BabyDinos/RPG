from discord.ext import commands
import asyncio
import aiosqlite
from sqlitedict import SqliteDict
from sqliteCommands import sqlCommands
from enemyClass import *
from playerClass import *
import discord

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def register(self, ctx):
        # checking if player exists already, if they do deny re-registering
        self.id = str(ctx.author).split('#')[-1]
        res = sqlCommands.load(self.id, unit = 'player') 
        if res:
            await ctx.send('This User is already linked to a pre-existing account')
        else:
            embed = discord.Embed(
                title = 'Registering',
                description = 'Enter your username: '
            )
            bot_message = await ctx.send(embed = embed)
            
            try:
                self.username_message = await self.bot.wait_for('message', timeout = 20, check= lambda message: message.author == ctx.author and message.channel == ctx.channel)

                embed = discord.Embed(
                    title = 'Register',
                    description = 'Welcome ' + str(self.username_message.content)
                )
                embed.add_field(name = 'Warrior', value = '''Warriors are a class that specializes in swords and deal physical damage\n
                                        {}'''.format(difference('Warrior')))
                embed.add_field(name = 'Mage', value = '''Mages are a class that specializes in staves and deal magical damage\n
                                        {}'''.format(difference('Mage')))          
                embed.set_footer(text = 'Choose your class: ')      

                await bot_message.edit(embed = embed)

                self.class_message = await self.bot.wait_for('message', timeout = 20, check= lambda message: message.author == ctx.author and message.channel == ctx.channel)

                if self.username_message and str(self.class_message.content) in ['Warrior', 'Mage']:
                    match str(self.class_message.content):
                        case 'Warrior':
                            sqlCommands.save(self.id, Warrior(str(self.username_message.content)) , unit = 'player')
                        case 'Mage':
                            sqlCommands.save(self.id, Mage(str(self.username_message.content)) , unit = 'player')
                        case _:
                            return ctx.send('Invalid Class')
                    await ctx.send('Welcome ' + str(self.message.content))
            except asyncio.TimeoutError: 
                await ctx.send('Command Timedout')

    @commands.command()
    async def nameChange(self, ctx):
        self.id = str(ctx.author).split('#')[-1]
        res = sqlCommands.load(self.id, unit = 'player')
        if not res:
            await ctx.send('You are not registered')
        else:
            await ctx.send('What is your new Username?')
            try:
                self.message = await self.bot.wait_for('message', timeout = 20, check= lambda message: message.author == ctx.author and message.channel == ctx.channel)
                if self.message:
                    sqlCommands.save(self.id, str(self.message.content), unit = 'player')
                    await ctx.send('Your name has been changed to ' + str(self.message.content))
            except asyncio.TimeoutError: 
                await ctx.send('Command Timedout')

    @commands.command()
    async def info(self, ctx):
        self.id = str(ctx.author).split('#')[-1]
        res = sqlCommands.load(self.id, unit = 'player')
        if not res:
            await ctx.send('You are not registered')
        else:
            await ctx.send('Your username is: ' + res)

    @commands.command()
    async def delete(self, ctx):
        self.id = str(ctx.author).split('#')[-1]
        res = sqlCommands.load(self.id, unit = 'player')
        if not res:
            await ctx.send('You are not registered')
        else:
            msg = await ctx.send('Are you sure you want to delete?')
            await msg.add_reaction("\U00002705")
            await msg.add_reaction("\U0000274C")

            def check(reaction, user):
                return user.id == ctx.author.id and reaction.message.channel.id == ctx.channel.id and str(reaction.emoji) in ["\U00002705", "\U0000274C"]

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout = 20, check= check)
            except asyncio.TimeoutError:
                await ctx.send('Command Timedout')
                return
            else:
                if str(reaction.emoji) == "\U00002705":
                    sqlCommands.delete(self.id, unit = 'player')
                    await ctx.send('Account has been deleted')
                else:
                    await ctx.send('Deletion Cancelled')

    @commands.command()
    async def fight(self, ctx):
        self.id = str(ctx.author).split('#')[-1]
        res = sqlCommands.load(self.id, unit = 'player')
        if not res:
            await ctx.send('You are not registered')
        else:
            enemy = Enemy('Golem')
            while enemy.curHealth > 0 and sqlCommands.load(self.id, 'player').curHealth > 0:
                pass



async def setup(bot):
    await bot.add_cog(Commands(bot))