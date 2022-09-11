from nextcord.ext import commands
import asyncio
import aiosqlite
from sqlitedict import SqliteDict
from sqliteCommands import sqlCommands
from enemyClass import *
from playerClass import *
import nextcord
from nextcord.ui import Button, View, Select
import math
import pandas as pd

class AccountCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def playerExists(self, ctx):
        self.id = str(ctx.author).split('#')[-1]
        return [sqlCommands.load(self.id, database = 'player'), self.id]

    # function creates an array that stores formated string of player equipment to be displayed in nextcord.embed
    def playerInfo(self, player):
        # arr first string will be Stats, next will be equipment, and last will be inventory
        arr = []
        string = 'XP: ' + str(player.CurrentLevel) + '/' + str(player.MaxLevel) + '\n'
        for x, y in player.stats_dictionary.items():
            if x == 'Max Health':
                string += 'Health: ' + str(player.CurrentHealth) + '/' + str(y) + '\n' 
            else:
                string += x + ': ' + str(y) + '\n'  
        arr.append(string)
        string = ''
        for r in range(len(player.equipment.index)):
            player.equipment.iloc[r,0]
            string += player.equipment.iloc[r].name + ': ' + str(player.equipment.iloc[r,0]) + '\n'
        arr.append(string)
        return arr

    # helper functions for the functions
    def toString(self, list):
        if list != None:
            return list[0] + ' - ' + list[1]
        else:
            return list

    # Converts dataframe inventory to a nested dictionary for nextcord to display 
    def playerInventory(self, player):
        dictionary = {}
        for row in range(len(player.inventory.index)):
            for colCount, colName in enumerate(player.inventory.columns):
                if colName != 'Stats' and colCount > 0:
                    dictionary[name][colName] = player.inventory.iloc[row,colCount]
                elif colName == 'Stats':
                    dictionary[name][colName] = self.toString(player.inventory.iloc[row,colCount])
                else:
                    name = player.inventory.iloc[row,colCount]
                    dictionary[name] = {}

        return dictionary

    @commands.command()
    async def register(self, ctx): #uses baseDifference
        # checking if player exists already, if they do deny re-registering
        arr = self.playerExists(ctx)
        player = arr[0]
        id = arr[1]
        if player:
            await ctx.send('This User is already linked to a pre-existing account', delete_after = 20)
        else:
            embed = nextcord.Embed(
                title = 'Registering',
                description = 'Enter your username: '
            )
            bot_message = await ctx.send(embed = embed)
            
            try:
                username_message = await self.bot.wait_for('message', timeout = 20, check= lambda message: message.author == ctx.author and message.channel == ctx.channel)

                embed = nextcord.Embed(
                    title = 'Register',
                    description = 'Welcome ' + str(username_message.content)
                )

                embed.add_field(name = 'Warrior', value = '''Warrior's signature ability allows him to greatly increase his stats for a short burst''')
                embed.add_field(name = 'Mage', value = '''Mage's signature ability gives them an attack multiplier''')          
                embed.set_footer(text = 'Choose your class: ')      
                
                async def warrior_button_callback(interaction):
                    if interaction.user.id == ctx.author.id:
                        member = ctx.message.author
                        role = nextcord.utils.get(member.guild.roles, name = 'Warrior')
                        await interaction.user.add_roles(role)
                        sqlCommands.save(id, Warrior(str(username_message.content)) , database = 'player')
                        embed = nextcord.Embed(
                            title = 'Thanks for Registering ' + str(username_message.content),
                            description = 'Welcome to RPG!'
                        )
                        register_msg = await ctx.send(embed = embed, delete_after = 20)
                        await username_message.delete()
                        await bot_message.delete()
                        await ctx.message.delete()
                        await member.edit(nick = username_message.content)
                        await interaction.response.defer()

                async def mage_button_callback(interaction):
                    if interaction.user.id == ctx.author.id:
                        member = ctx.message.author
                        role = nextcord.utils.get(member.guild.roles, name = 'Mage')
                        await interaction.user.add_roles(role)
                        sqlCommands.save(id, Mage(str(username_message.content)) , database = 'player')
                        embed = nextcord.Embed(
                            title = 'Thanks for Registering ' + str(username_message.content),
                            description = 'Welcome to RPG!'
                        )
                        register_msg = await ctx.send(embed = embed, delete_after = 20)
                        await username_message.delete()
                        await bot_message.delete()
                        await ctx.message.delete()
                        await member.edit(nick = username_message.content)
                        await interaction.response.defer()
                    

                Warrior_Button = Button(label = 'Warrior')
                Warrior_Button.callback = warrior_button_callback
                Mage_Button = Button(label = 'Mage')
                Mage_Button.callback = mage_button_callback
                myview = View(timeout = 120)
                myview.add_item(Warrior_Button)
                myview.add_item(Mage_Button)

                await bot_message.edit(embed = embed, view = myview)
            except asyncio.TimeoutError: 
                await ctx.send('Command Timedout', delete_after = 20)
                await username_message.delete()
                await bot_message.delete()
                await ctx.message.delete()
 
    @commands.command()
    async def nameChange(self, ctx):
        arr = self.playerExists(ctx)
        player = arr[0]
        id = arr[1]
        if not player:
            await ctx.send('You are not registered', delete_after = 20)
        else:
            await ctx.send('What is your new Username?', delete_after = 20)
            try:
                message = await self.bot.wait_for('message', timeout = 20, check= lambda message: message.author == ctx.author and message.channel == ctx.channel)
                if message:
                    player.Name = str(message.content)
                    sqlCommands.save(id, player, database = 'player')
                    await ctx.send('Your name has been changed to ' + str(message.content), delete_after = 20)
                await message.delete()
                await ctx.message.delete()
            except asyncio.TimeoutError: 
                await ctx.send('Command Timedout', delete_after = 20)
                try:
                    await message.delete()
                except:
                    pass
        await ctx.message.delete()

    @commands.command()
    async def info(self, ctx): #uses playerInfo
        arr = self.playerExists(ctx)
        player = arr[0]
        id = arr[1]
        if not player:
            await ctx.send('You are not registered', delete_after = 20)
        else:
            playerinfo = self.playerInfo(player)
            embed = nextcord.Embed(
                title = 'Character Info - ' + player.Name + ' Lvl: ' + str(player.Level),
                color = 0x000ff
            )
            embed.add_field(name = 'Infos', value = playerinfo[0])
            embed.add_field(name = 'Equipment', value = playerinfo[1])
            await ctx.send(embed = embed, delete_after = 120)
        await ctx.message.delete()

    @commands.command()
    async def delete(self, ctx):
        arr = self.playerExists(ctx)
        player = arr[0]
        id = arr[1]
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
                member = ctx.message.author
                for role in ['Warrior','Mage']:
                    try:
                        role = nextcord.utils.get(member.guild.roles, name = role)
                        await member.remove_roles(role)
                        await member.edit(nick = None)
                    except:
                        pass
            except asyncio.TimeoutError:
                try:
                    await ctx.message.delete()
                except:
                    pass
                await ctx.send('Command Timedout', delete_after = 20)
                return
            else:
                if str(reaction.emoji) == "\U00002705":
                    sqlCommands.delete(id, database = 'player')
                    await ctx.send('Account has been deleted', delete_after = 20)
                else:
                    await ctx.send('Deletion Cancelled', delete_after = 20)
        await ctx.message.delete()

    @commands.command()
    async def inventory(self, ctx): #uses playerInventory
        arr = self.playerExists(ctx)
        player = arr[0]
        id = arr[1]
        if not player:
            await ctx.send('You are not registered', delete_after = 20)
        else:

            playerinv = self.playerInventory(player)

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
                if interaction.user.id == ctx.author.id:
                    nonlocal currentPage, sent_msg
                    currentPage += 1
                    
                    await sent_msg.edit(embed = createEmbed(pageNum = currentPage), view = myview)
                    await interaction.response.defer()

            async def previous_callback(interaction):
                if interaction.user.id == ctx.author.id:
                    nonlocal currentPage, sent_msg
                    currentPage -= 1
                    
                    await sent_msg.edit(embed = createEmbed(pageNum = currentPage), view = myview)
                    await interaction.response.defer()

            async def fast_next_callback(interaction):
                if interaction.user.id == ctx.author.id:
                    nonlocal currentPage, sent_msg
                    currentPage = len(list(playerinv))-1

                    await sent_msg.edit(embed = createEmbed(pageNum = currentPage), view = myview)
                    await interaction.response.defer()

            async def fast_previous_callback(interaction):
                if interaction.user.id == ctx.author.id:
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
            await ctx.message.delete()
    
    @commands.command()
    async def statPoints(self, ctx):
        arr = self.playerExists(ctx)
        player = arr[0]
        id = arr[1]
        if not player:
            await ctx.send('You are not registered', delete_after = 20)
        else:
            statpoints_original = player.statpoints
            original_dictionary = player.stats_dictionary.copy()
            stat = ''
            amount = 0

            def createEmbed():
                string = ''
                for x, y in player.stats_dictionary.items():
                    string += x + ': ' + str(y) + '\n'  
                embed = nextcord.Embed(
                    title = 'Character Info - ' + player.Name + ' Lvl: ' + str(player.Level),
                    color = 0x000ff
                )
                embed.add_field(name = 'Infos', value = string + 'Current Stat Points: ' + str(player.statpoints))
                return embed

            selectoptions = [
            nextcord.SelectOption(label = 'HP'), nextcord.SelectOption(label = 'Attack'), nextcord.SelectOption(label = 'Magic Attack'),
            nextcord.SelectOption(label = 'Defense'), nextcord.SelectOption(label = 'Magic Defense'), nextcord.SelectOption(label = 'Attack Speed')
            ]

            amountselectoptions = [
                nextcord.SelectOption(label = '1'), nextcord.SelectOption(label = '2'), nextcord.SelectOption(label = '3'), 
                nextcord.SelectOption(label = '5'), nextcord.SelectOption(label = 'All')
            ]

            async def dropdown_callback(interaction):
                nonlocal stat
                if interaction.user.id == ctx.author.id:
                    if dropdown.values[0] == 'HP':
                        stat = 'Max Health'
                    elif dropdown.values[0] == 'Attack':
                        stat = 'Attack'
                    elif dropdown.values[0] == 'Magic Attack':
                        stat = 'Magic Attack'
                    elif dropdown.values[0] == 'Defense':
                        stat = 'Defense'
                    elif dropdown.values[0] == 'Magic Defense':
                        stat = 'Magic Defense'
                    elif dropdown.values[0] == 'Attack Speed':
                        stat = 'Attack Speed'
                    await interaction.response.defer()

            async def amountdropdown_callback(interaction):
                nonlocal amount
                if interaction.user.id == ctx.author.id:
                    if amountdropdown.values[0] == 'All':
                        amount = player.statpoints
                    elif amountdropdown.values[0] == '1':
                            amount = 1
                    elif amountdropdown.values[0] == '2':
                            amount = 2
                    elif amountdropdown.values[0] == '3':
                            amount = 3
                    elif amountdropdown.values[0] == '5':
                            amount = 5
                    await interaction.response.defer()

            async def addButton_callback(interaction):
                if interaction.user.id == ctx.author.id:
                    if player.statpoints >= amount > 0:
                        player.stats_dictionary[stat] +=  amount
                        player.statpoints -= amount
                    elif amount == 0:
                        await ctx.send('Choose an Amount', delete_after = 20)
                    else:
                        await ctx.send('No more Stat Points', delete_after = 20)
                    await bot_message.edit(embed = createEmbed(), view = myview)
                    await interaction.response.defer()

            async def subtractButton_callback(interaction):
                nonlocal amount
                if interaction.user.id == ctx.author.id:
                    if player.statpoints == amount:
                        player.statpoints += (player.stats_dictionary[stat] - 1)
                        player.stats_dictionary[stat] -= (player.stats_dictionary[stat] - 1)
                        amount = player.statpoints
                    elif player.stats_dictionary[stat] - amount >= 1 :
                        player.stats_dictionary[stat] -= amount
                        player.statpoints += amount
                    else:
                        await ctx.send('Cannot decrease any further', delete_after = 20)
                    await bot_message.edit(embed = createEmbed(), view = myview)
                    await interaction.response.defer()

            async def confirmButton_callback(interaction):
                if interaction.user.id == ctx.author.id:
                    if player.stats_dictionary['Max Health'] < original_dictionary['Max Health']:
                        player.CurrentHealth = player.stats_dictionary['Max Health']
                    sqlCommands.save(id, player, database='player')
                    await bot_message.delete()
                    await interaction.response.defer()

            async def resetButton_callback(interaction):
                nonlocal original_dictionary
                nonlocal statpoints_original
                if interaction.user.id == ctx.author.id:
                    player.stats_dictionary = original_dictionary
                    player.statpoints = statpoints_original

                    statpoints_original = player.statpoints
                    original_dictionary = player.stats_dictionary.copy()
                    
                    await bot_message.edit(embed = createEmbed(), view = myview)
                    await interaction.response.defer()

            dropdown = Select(placeholder = 'Choose Stat', options = selectoptions)    
            dropdown.callback = dropdown_callback        
            amountdropdown = Select(placeholder = 'Choose Amount', options = amountselectoptions)
            amountdropdown.callback = amountdropdown_callback
            addButton = Button(label = '+', style = nextcord.ButtonStyle.green)
            addButton.callback = addButton_callback
            subtractButton = Button(label = '-', style = nextcord.ButtonStyle.red)
            subtractButton.callback = subtractButton_callback
            confirmButton = Button(label = 'Confirm', style = nextcord.ButtonStyle.blurple)
            confirmButton.callback = confirmButton_callback
            resetButton = Button(label = 'Reset', style = nextcord.ButtonStyle.danger)
            resetButton.callback = resetButton_callback
            myview = View(timeout = 120)
            myview.add_item(dropdown)
            myview.add_item(amountdropdown)
            myview.add_item(addButton)
            myview.add_item(subtractButton)
            myview.add_item(confirmButton)
            myview.add_item(resetButton)

            bot_message = await ctx.send(embed = createEmbed(), view = myview, delete_after = 120)

            timed_out = await myview.wait()
            if timed_out:
                await bot_message.delete()
                await ctx.message.delete()

    @commands.command()
    async def shop(self, ctx):
        arr = self.playerExists(ctx)
        player = arr[0]
        id = arr[1]
        if not player:
            await ctx.send('You are not registered', delete_after = 20)
        else:

            transaction_dictionary = {}
            costs_dictionary = {'Stone':{'Buy':2,'Sell':1},'Meat':{'Buy':2,'Sell':1},'Hide':{'Buy':2,'Sell':1},'Bark':{'Buy':2,'Sell':1}}
            item = ''
            amount = 0

            def createEmbed():
                embed = nextcord.Embed(title = 'Shop', description = 'Buy and Sell Things')
                for x, y in transaction_dictionary.items():
                    embed.add_field(name = x, value = y)
                return embed
            
            selectoptions = [
            nextcord.SelectOption(label = 'Stone', description ='Buy: 2\nSell: 1'), nextcord.SelectOption(label = 'Meat', description ='Buy: 2\nSell: 1'), 
            nextcord.SelectOption(label = 'Hide', description ='Buy: 2\nSell: 1'), nextcord.SelectOption(label = 'Bark', description ='Buy: 2\nSell: 1')
            ]

            amountselectoptions = [
                nextcord.SelectOption(label = '1'), nextcord.SelectOption(label = '5'), nextcord.SelectOption(label = '10')
            ]
            async def dropdown_callback(interaction):
                nonlocal item
                if interaction.user.id == ctx.author.id:
                    if dropdown.values[0] == 'Stone':
                        item = 'Stone'
                    elif dropdown.values[0] == 'Meat':
                        item = 'Meat'
                    elif dropdown.values[0] == 'Hide':
                        item = 'Hide'
                    elif dropdown.values[0] == 'Bark':
                        item = 'Bark'
                    await interaction.response.defer()

            async def amountdropdown_callback(interaction):
                nonlocal amount
                if interaction.user.id == ctx.author.id:
                    if amountdropdown.values[0] == '10':
                        amount = 10
                    elif amountdropdown.values[0] == '1':
                        amount = 1
                    elif amountdropdown.values[0] == '5':
                        amount = 5
                    await interaction.response.defer()

            async def increaseAmount_callback(interaction):
                if interaction.user.id == ctx.author.id:
                    if item not in transaction_dictionary:
                        transaction_dictionary[item] = amount
                    else:
                        transaction_dictionary[item] += amount
                    await bot_message.edit(embed = createEmbed(), view = myview)
                    await interaction.response.defer()

            async def decreaseAmount_callback(interaction):
                if interaction.user.id == ctx.author.id:
                    if item not in transaction_dictionary:
                        transaction_dictionary[item] = -amount
                    else:
                        transaction_dictionary[item] -= amount
                    await bot_message.edit(embed = createEmbed(), view = myview)
                    await interaction.response.defer()

            async def confirmButton_callback(interaction):
                if interaction.user.id == ctx.author.id:
                    gold_index = player.inventory.index[(player.inventory['Name'] == 'Gold')][0]
                    gold = player.inventory.loc[gold_index, 'Amount']

                    order_list = []

                    for x, y in transaction_dictionary.items():
                        if y >= 0:
                            gold -= costs_dictionary[x]['Buy'] * y
                            order_list.append({'Buy':[x, y]})
                        elif y < 0:
                            try:
                                index = player.inventory.index[(player.inventory['Name'] == x)][0]
                                if player.inventory.loc[index, 'Amount'] < abs(y):
                                    return await ctx.send("Don't have enough " + x + ' to sell', delete_after = 20)
                                else:
                                    order_list.append({'Sell':[x,y]})
                            except:
                                return await ctx.send("Don't have enough " + x + ' to sell', delete_after = 20)
                            gold += costs_dictionary[x]['Sell'] * abs(y)

                    if gold < 0:
                        await ctx.send('Not enough Gold', delete_after = 20)
                    else:
                        for action_dict in order_list:
                            if 'Buy' in action_dict.keys():
                                player.inventory = addItem(player, [action_dict['Buy'][0]],[action_dict['Buy'][1]])
                            elif 'Sell' in action_dict.keys():
                                player.inventory = subtractItem(player, [action_dict['Sell'][0]],[abs(action_dict['Sell'][1])])
                        player.inventory.loc[gold_index, 'Amount'] = gold
                        sqlCommands.save(id, player, database='player')
                        await bot_message.delete()
                        await interaction.response.defer()


            dropdown = Select(placeholder = 'Choose Item', options = selectoptions)    
            dropdown.callback = dropdown_callback        
            amountdropdown = Select(placeholder = 'Choose Amount', options = amountselectoptions)
            amountdropdown.callback = amountdropdown_callback
            increaseAmount = Button(label = 'Buy', style = nextcord.ButtonStyle.green)
            increaseAmount.callback = increaseAmount_callback
            decreaseAmount = Button(label = 'Sell', style = nextcord.ButtonStyle.red)
            decreaseAmount.callback = decreaseAmount_callback
            confirmButton = Button(label = 'Finish', style = nextcord.ButtonStyle.blurple)
            confirmButton.callback = confirmButton_callback
            myview = View(timeout = 120)
            myview.add_item(dropdown)
            myview.add_item(amountdropdown)
            myview.add_item(increaseAmount)
            myview.add_item(decreaseAmount)
            myview.add_item(confirmButton)

            bot_message = await ctx.send(embed = createEmbed(), view = myview, delete_after = 120)

            timed_out = await myview.wait()
            if timed_out:
                await bot_message.delete()
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(AccountCommands(bot))
