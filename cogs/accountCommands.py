from nextcord.ext import commands
import asyncio
import aiosqlite
from sqlitedict import SqliteDict
from sqliteCommands import sqlCommands
from enemyClass import *
from playerClass import *
import nextcord
from nextcord.ui import Button, View
import math

class AccountCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def playerExists(self, ctx):
        self.id = str(ctx.author).split('#')[-1]
        return sqlCommands.load(self.id, database = 'player')

    @commands.command()
    async def register(self, ctx):
        # checking if player exists already, if they do deny re-registering
        player = self.playerExists(ctx)
        if player:
            await ctx.send('This User is already linked to a pre-existing account', delete_after = 20)
        else:
            embed = nextcord.Embed(
                title = 'Registering',
                description = 'Enter your username: '
            )
            self.bot_message = await ctx.send(embed = embed)
            
            try:
                self.username_message = await self.bot.wait_for('message', timeout = 20, check= lambda message: message.author == ctx.author and message.channel == ctx.channel)

                embed = nextcord.Embed(
                    title = 'Register',
                    description = 'Welcome ' + str(self.username_message.content)
                )
                embed.add_field(name = 'Warrior', value = '''Warriors are a class that specializes in swords and deal physical damage\n
                                        {}'''.format(baseDifference('Warrior')))
                embed.add_field(name = 'Mage', value = '''Mages are a class that specializes in staves and deal magical damage\n
                                        {}'''.format(baseDifference('Mage')))          
                embed.set_footer(text = 'Choose your class: ')      

                await self.bot_message.edit(embed = embed)

                self.class_message = await self.bot.wait_for('message', timeout = 20, check= lambda message: message.author == ctx.author and message.channel == ctx.channel)

                if self.username_message and str(self.class_message.content) in ['Warrior', 'Mage']:
                    match str(self.class_message.content):
                        case 'Warrior':
                            sqlCommands.save(self.id, Warrior(str(self.username_message.content)) , database = 'player')
                        case 'Mage':
                            sqlCommands.save(self.id, Mage(str(self.username_message.content)) , database = 'player')
                        case _:
                            return ctx.send('Invalid Class')
                    embed = nextcord.Embed(
                        title = 'Thanks for Registering ' + str(self.username_message.content),
                        description = 'Welcome to RPG!'
                    )
                    await self.username_message.delete()
                    await self.class_message.delete()
                    await self.bot_message.edit(embed = embed)
            except asyncio.TimeoutError: 
                await ctx.send('Command Timedout', delete_after = 20)
                asyncio.sleep(20)
                try:
                    await self.username_message.delete()
                except:
                    pass
                try: 
                    await self.class_message.delete()
                except:
                    pass
                await self.bot_message.delete()
        await ctx.message.delete()
                
    @commands.command()
    async def nameChange(self, ctx):
        player = self.playerExists(ctx)
        if not player:
            await ctx.send('You are not registered', delete_after = 20)
        else:
            await ctx.send('What is your new Username?', delete_after = 20)
            try:
                self.message = await self.bot.wait_for('message', timeout = 20, check= lambda message: message.author == ctx.author and message.channel == ctx.channel)
                if self.message:
                    player.Name = str(self.message.content)
                    sqlCommands.save(self.id, player, database = 'player')
                    await ctx.send('Your name has been changed to ' + str(self.message.content), delete_after = 20)
                await self.message.delete()
                await ctx.message.delete()
            except asyncio.TimeoutError: 
                await ctx.send('Command Timedout', delete_after = 20)
                try:
                    await self.message.delete()
                except:
                    pass
        await ctx.message.delete()

    @commands.command()
    async def info(self, ctx):
        player = self.playerExists(ctx)
        if not player:
            await ctx.send('You are not registered', delete_after = 20)
        else:
            playerinfo = playerInfo(player)
            embed = nextcord.Embed(
                title = 'Character Info - ' + player.Name,
                color = 0x000ff
            )
            embed.add_field(name = 'Infos', value = playerinfo[0])
            embed.add_field(name = 'Equipment', value = playerinfo[1])
            await ctx.send(embed = embed, delete_after = 120)
        await ctx.message.delete()

    @commands.command()
    async def delete(self, ctx):
        player = self.playerExists(ctx)
        if not player:
            await ctx.send('You are not registered', delete_after = 20)
        else:
            msg = await ctx.send('Are you sure you want to delete? - ' + player.Name, delete_after = 20)
            await msg.add_reaction("\U00002705")
            await msg.add_reaction("\U0000274C")

            def check(reaction, user):
                return user.id == ctx.author.id and reaction.message.channel.id == ctx.channel.id and str(reaction.emoji) in ["\U00002705", "\U0000274C"]

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout = 20, check= check)
            except asyncio.TimeoutError:
                try:
                    await ctx.message.delete()
                except:
                    pass
                await ctx.send('Command Timedout', delete_after = 20)
                return
            else:
                if str(reaction.emoji) == "\U00002705":
                    sqlCommands.delete(self.id, database = 'player')
                    await ctx.send('Account has been deleted', delete_after = 20)
                else:
                    await ctx.send('Deletion Cancelled', delete_after = 20)
        await ctx.message.delete()

    @commands.command()
    async def inventory(self, ctx):
        player = self.playerExists(ctx)
        if not player:
            await ctx.send('You are not registered', delete_after = 20)
        else:

            playerinv = playerInventory(player)

            def createEmbed(pageNum = 0, inline = False):
                pageNum = pageNum % (len(list(playerinv)))
                pageTitle = list(playerinv)[pageNum]
                embed = nextcord.Embed(color = nextcord.Color.dark_orange(), title = pageTitle)
                for key, val in playerinv[pageTitle].items():
                    embed.add_field(name = key, value = val, inline = inline)
                    embed.set_footer(text = f'Page {pageNum+1} of {len(list(playerinv))}')
                return embed
            
            currentPage = 0

            async def next_callback(interaction):
                nonlocal currentPage, sent_msg
                currentPage += 1
                
                await sent_msg.edit(embed = createEmbed(pageNum = currentPage), view = myview)
                await interaction.response.defer()

            async def previous_callback(interaction):
                nonlocal currentPage, sent_msg
                currentPage -= 1
                
                await sent_msg.edit(embed = createEmbed(pageNum = currentPage), view = myview)
                await interaction.response.defer()

            async def fast_next_callback(interaction):
                nonlocal currentPage, sent_msg
                currentPage = len(list(playerinv))-1

                await sent_msg.edit(embed = createEmbed(pageNum = currentPage), view = myview)
                await interaction.response.defer()

            async def fast_previous_callback(interaction):
                nonlocal currentPage, sent_msg
                currentPage = 0

                await sent_msg.edit(embed = createEmbed(pageNum = currentPage), view = myview)
                await interaction.response.defer()

            nextButton = Button(label = '>', style = nextcord.ButtonStyle.blurple)
            nextButton.callback = next_callback
            previousButton = Button(label = '<', style = nextcord.ButtonStyle.blurple)
            previousButton.callback = previous_callback
            fastNextButton = Button(label = '>>', style = nextcord.ButtonStyle.blurple)
            fastNextButton.callback = fast_next_callback
            fastPreviousButton = Button(label = '<<', style = nextcord.ButtonStyle.blurple)
            fastPreviousButton.callback = fast_previous_callback

            myview = View(timeout = 120)
            myview.add_item(fastPreviousButton)
            myview.add_item(previousButton)
            myview.add_item(nextButton)
            myview.add_item(fastNextButton)
            sent_msg = await ctx.send(embed = createEmbed(pageNum = currentPage), view = myview)

            timed_out = await myview.wait()
            if timed_out:
                await sent_msg.delete()
                await ctx.message.delete()

def setup(bot):
    bot.add_cog(AccountCommands(bot))
