from nextcord.ext import commands
import asyncio
from sqliteCommands import sqlCommands
import enemyClass 
import playerClass 
import nextcord
from nextcord.ui import Button, View, Select
import os
from nextcord import Interaction, SlashOption
from typing import Optional
import lootbox

testServerID = int(os.environ['testServerID'])

class AccountCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def getPlayer(self, interaction):
        id = str(interaction.user).split('#')[-1]
        return [sqlCommands.load(id, database='player'), id]

    # helper functions for the functions
    def toString(self, list):
        if list != None:
            return list[0] + ' - ' + list[1]
        else:
            return list
  
    @nextcord.slash_command(guild_ids= [testServerID], description = 'Creating an Account for RPG')
    async def register(self, interaction: Interaction, username:str):
        arr = self.getPlayer(interaction)
        player = arr[0]
        id = arr[1]
        if player:
            await interaction.response.send_message(
                'This User is already linked to a pre-existing account',
                delete_after=20, ephemeral = True)
        else:

            embed = nextcord.Embed(title='Register',
                                    description='Welcome ' +
                                    username)
            embed.add_field(
                name='Warrior',
                value=
                '''Warrior's signature ability allows him to greatly increase his stats for a short burst'''
            )
            embed.add_field(
                name='Mage',
                value=
                '''Mage's signature ability gives them an attack multiplier'''
            )
            embed.set_footer(text='Choose your class: ')
          
            async def warrior_button_callback(interaction):
                member = interaction.user
                role = nextcord.utils.get(member.guild.roles,
                                            name='Warrior')
                await interaction.user.add_roles(role)
                sqlCommands.save(id,
                                    playerClass.Warrior(
                                        username),
                                    database='player')
                embed = nextcord.Embed(
                    title='Thanks for Registering ' +
                    username,
                    description='Welcome to RPG!')
                await interaction.response.edit_message(embed=embed,
                                                view = View())
                await member.edit(nick=username)
                

            async def mage_button_callback(interaction):
                member = interaction.user
                role = nextcord.utils.get(member.guild.roles,
                                            name='Mage')
                await interaction.user.add_roles(role)
                sqlCommands.save(id,
                                    playerClass.Mage(username),
                                    database='player')
                embed = nextcord.Embed(
                    title='Thanks for Registering ' +
                    username,
                    description='Welcome to RPG!')
                await interaction.response.edit_message(embed=embed,
                                                delete_after=20)
                await member.edit(nick=username)
                
            Warrior_Button = Button(label='Warrior')
            Warrior_Button.callback = warrior_button_callback
            Mage_Button = Button(label='Mage')
            Mage_Button.callback = mage_button_callback
            myview = View(timeout=120)
            myview.add_item(Warrior_Button)
            myview.add_item(Mage_Button)

            await interaction.response.send_message(embed=embed, ephemeral = True, view = myview)

    @nextcord.slash_command(guild_ids= [testServerID], description = 'Change name of user')
    async def namechange(self, interaction: Interaction, username:str):
        arr = self.getPlayer(interaction)
        player = arr[0]
        id = arr[1]
        if not player:
            await interaction.response.send_message('You are not registered', delete_after=20, ephemeral = True)
        else:
            temp = player.Name
            player.Name = username
            sqlCommands.save(id, player, database='player')
            await interaction.user.edit(nick=username)
            await interaction.response.send_message('Username has been changed from ' + temp + ' to ' + username, delete_after=20, ephemeral = True)
            
    @nextcord.slash_command(guild_ids= [testServerID], description = 'Get information about user')
    async def info(self, interaction: Interaction, discordtag: Optional[int] = SlashOption(required=False)):  
        if discordtag:
            player = sqlCommands.load(discordtag, database = 'player')
        else:
            arr = self.getPlayer(interaction)
            player = arr[0]
        if not player:
            await interaction.response.send_message('Player not registered', ephemeral = True)
        else:
              # function creates an array that stores formated string of player equipment to be displayed in nextcord.embed
            def playerInfo(player):
                # arr first string will be Stats, next will be equipment, and last will be inventory
                arr = []
                string = 'XP: ' + str(player.CurrentEXP) + '/' + str(
                    player.MaxEXP) + '\n'
                for x, y in player.stats_dictionary.items():
                    if x == 'Max Health':
                        string += 'Health: ' + str(
                            player.CurrentHealth) + '/' + str(y) + '\n'
                    else:
                        string += x + ': ' + str(y) + '\n'
                arr.append(string)
                string = ''
                for r in range(len(player.equipment.index)):
                    player.equipment.iloc[r, 0]
                    string += player.equipment.iloc[r].name + ': ' + str(
                        player.equipment.iloc[r, 0]) + '\n'
                arr.append(string)
                return arr
            playerinfo = playerInfo(player)
            embed = nextcord.Embed(title='Character Info - ' + player.Name +
                                   ' Lvl: ' + str(player.Level),
                                   color=0x000ff)
            embed.add_field(name='Infos', value=playerinfo[0])
            embed.add_field(name='Equipment', value=playerinfo[1])
            embed.add_field(name = 'Ability', value = player.skilldescription)
            await interaction.response.send_message(embed=embed, delete_after=120, ephemeral = True)

    @nextcord.slash_command(guild_ids= [testServerID], description = 'Delete User')
    async def delete(self, interaction: Interaction):
        arr = self.getPlayer(interaction)
        player = arr[0]
        id = arr[1]
        if not player:
            await interaction.response.send_message('You are not registered', delete_after=20, ephemeral = True)
        else:
            confirm = False
            
            async def yesButton_callback(interaction):
                nonlocal confirm
                if confirm == False:
                    await interaction.response.edit_message(content = 'Are you sure you want to delete ' + player.Name + '?')
                    confirm = True
                    return
                sqlCommands.delete(id, database = 'player')
                await interaction.response.edit_message(content ='User ' + player.Name + ' was deleted', view = View())
                return


            async def noButton_callback(interaction):
                await interaction.response.edit_message(content = 'Deletetion Cancelled', delete_after = 20)
                
              
            yesButton = Button(label='✅', style=nextcord.ButtonStyle.green)
            yesButton.callback = yesButton_callback
            noButton = Button(label = '❌', style = nextcord.ButtonStyle.red)
            noButton.callback = noButton_callback
            myview = View()
            myview.add_item(yesButton)
            myview.add_item(noButton)

            await interaction.response.send_message('Do you want to delete ' + player.Name + '?', view = myview, ephemeral = True, delete_after = 20)
            
    @nextcord.slash_command(guild_ids= [testServerID], description = 'Get inventory of user')
    async def inventory(self):  
        pass

    @inventory.subcommand(description = 'Detailed Inventory')
    async def detailed(self, interaction:Interaction):
        arr = self.getPlayer(interaction)
        player = arr[0]
        id = arr[1]
        if not player:
            await interaction.response.send_message('You are not registered', delete_after=20, ephemeral = True)
        else:
              # Converts dataframe inventory to a nested dictionary for nextcord to display
            def playerInventory(player):
                dictionary = {}
                for row in range(len(player.inventory.index)):
                    for colCount, colName in enumerate(player.inventory.columns):
                        if colName != 'Stats' and colCount > 0:
                            dictionary[name][colName] = player.inventory.iloc[row,
                                                                              colCount]
                        elif colName == 'Stats':
                            dictionary[name][colName] = self.toString(
                                player.inventory.iloc[row, colCount])
                        else:
                            name = player.inventory.iloc[row, colCount]
                            dictionary[name] = {}
        
                return dictionary

            playerinv = playerInventory(player)

            def createEmbed(pageNum=0, inline=False):

                pageNum = pageNum % (len(list(playerinv)))
                pageTitle = list(playerinv)[pageNum]
                embed = nextcord.Embed(color=nextcord.Color.dark_orange(),
                                       title=pageTitle)
                for key, val in playerinv[pageTitle].items():
                    embed.add_field(name=key, value=val, inline=inline)
                    embed.set_footer(
                        text=f'Page {pageNum+1} of {len(list(playerinv))}')
                return embed

            currentPage = 0

            async def next_callback(interaction):
                nonlocal currentPage
                currentPage += 1

                await interaction.response.edit_message(embed=createEmbed(pageNum=currentPage),
                                    view=myview)
                

            async def previous_callback(interaction):
                nonlocal currentPage
                currentPage -= 1

                await interaction.response.edit_message(embed=createEmbed(pageNum=currentPage),
                                    view=myview)
                

            async def fast_next_callback(interaction):
                nonlocal currentPage
                currentPage = len(list(playerinv)) - 1

                await interaction.response.edit_message(embed=createEmbed(pageNum=currentPage),
                                    view=myview)
                

            async def fast_previous_callback(interaction):
                nonlocal currentPage
                currentPage = 0

                await interaction.response.edit_message(embed=createEmbed(pageNum=currentPage),
                                    view=myview)
                

            nextButton = Button(label='>', style=nextcord.ButtonStyle.blurple)
            nextButton.callback = next_callback
            previousButton = Button(label='<',
                                    style=nextcord.ButtonStyle.blurple)
            previousButton.callback = previous_callback
            fastNextButton = Button(label='>>',
                                    style=nextcord.ButtonStyle.blurple)
            fastNextButton.callback = fast_next_callback
            fastPreviousButton = Button(label='<<',
                                        style=nextcord.ButtonStyle.blurple)
            fastPreviousButton.callback = fast_previous_callback

            myview = View(timeout=120)
            myview.add_item(fastPreviousButton)
            myview.add_item(previousButton)
            myview.add_item(nextButton)
            myview.add_item(fastNextButton)
            await interaction.response.send_message(embed=createEmbed(pageNum=currentPage),
                                      view=myview, ephemeral = True)

    @inventory.subcommand(description = 'Full Inventory')
    async def general(self, interaction:Interaction):
        arr = self.getPlayer(interaction)
        player = arr[0]
        id = arr[1]
        if not player:
            await interaction.response.send_message('You are not registered', delete_after=20, ephemeral = True)
        else:
            embed = nextcord.Embed(title = player.Name + ' Inventory', description = '\u200b')
            for index, row in player.inventory.iterrows():
                embed.add_field(name = '[' + row['Name'] + ': ' + str(row['Amount']) + ']', value = '\u200b')

            await interaction.response.send_message(embed = embed, ephemeral = True)

    @nextcord.slash_command(guild_ids= [testServerID], description = 'Adjust player stats')
    async def statpoints(self, interaction):
        arr = self.getPlayer(interaction)
        player = arr[0]
        id = arr[1]
        if not player:
            await interaction.response.send_message('You are not registered', delete_after=20)
        else:
            statpoints_original = player.statpoints
            original_dictionary = player.stats_dictionary.copy()
            stat = ''
            amount = 0

            def createEmbed():
                string = ''
                for x, y in player.stats_dictionary.items():
                    string += x + ': ' + str(y) + '\n'
                embed = nextcord.Embed(title='Character Info - ' +
                                       player.Name + ' Lvl: ' +
                                       str(player.Level),
                                       color=0x000ff)
                embed.add_field(name='Infos',
                                value=string + 'Current Stat Points: ' +
                                str(player.statpoints))
                return embed

            selectoptions = [
                nextcord.SelectOption(label='HP'),
                nextcord.SelectOption(label='Attack'),
                nextcord.SelectOption(label='Magic Attack'),
                nextcord.SelectOption(label='Defense'),
                nextcord.SelectOption(label='Magic Defense'),
                nextcord.SelectOption(label='Attack Speed')
            ]

            amountselectoptions = [
                nextcord.SelectOption(label='1'),
                nextcord.SelectOption(label='2'),
                nextcord.SelectOption(label='3'),
                nextcord.SelectOption(label='5'),
                nextcord.SelectOption(label='All')
            ]

            async def dropdown_callback(interaction):
                nonlocal stat
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
              

            async def amountdropdown_callback(interaction):
                nonlocal amount
                
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
                

            async def addButton_callback(interaction):
                nonlocal amount
                if player.statpoints >= amount > 0:
                    player.stats_dictionary[stat] += amount
                    player.statpoints -= amount
                elif amount == 0:
                    await interaction.response.send_message('Choose an Amount', delete_after=20, ephemeral = True)
                else:
                    await interaction.response.send_message('No more Stat Points', delete_after=20, ephemeral = True)
                await interaction.response.edit_message(embed=createEmbed(), view=myview)
            

            async def subtractButton_callback(interaction):
                nonlocal amount
                if player.statpoints == amount:
                    player.statpoints += (player.stats_dictionary[stat] -
                                          1)
                    player.stats_dictionary[stat] -= (
                        player.stats_dictionary[stat] - 1)
                    amount = player.statpoints
                elif player.stats_dictionary[stat] - amount >= 1:
                    player.stats_dictionary[stat] -= amount
                    player.statpoints += amount
                else:
                    await interaction.response.send_message('Cannot decrease any further',
                                   delete_after=20, ephemeral = True)
                await interaction.response.edit_message(embed=createEmbed(), view=myview)
                

            async def confirmButton_callback(interaction):
                if player.stats_dictionary[
                        'Max Health'] < original_dictionary['Max Health']:
                    player.CurrentHealth = player.stats_dictionary[
                        'Max Health']
                sqlCommands.save(id, player, database='player')
                embed = nextcord.Embed(title = 'Stat Points Allocated')
                await interaction.response.edit_message(embed = embed, view = View())
      
                

            async def resetButton_callback(interaction):
                nonlocal original_dictionary
                nonlocal statpoints_original
                player.stats_dictionary = original_dictionary
                player.statpoints = statpoints_original

                statpoints_original = player.statpoints
                original_dictionary = player.stats_dictionary.copy()

                await interaction.response.edit_message(embed=createEmbed(), view=myview)
                

            dropdown = Select(placeholder='Choose Stat', options=selectoptions)
            dropdown.callback = dropdown_callback
            amountdropdown = Select(placeholder='Choose Amount',
                                    options=amountselectoptions)
            amountdropdown.callback = amountdropdown_callback
            addButton = Button(label='+', style=nextcord.ButtonStyle.green)
            addButton.callback = addButton_callback
            subtractButton = Button(label='-', style=nextcord.ButtonStyle.red)
            subtractButton.callback = subtractButton_callback
            confirmButton = Button(label='Confirm',
                                   style=nextcord.ButtonStyle.blurple)
            confirmButton.callback = confirmButton_callback
            resetButton = Button(label='Reset',
                                 style=nextcord.ButtonStyle.danger)
            resetButton.callback = resetButton_callback
            myview = View(timeout=120)
            myview.add_item(dropdown)
            myview.add_item(amountdropdown)
            myview.add_item(addButton)
            myview.add_item(subtractButton)
            myview.add_item(confirmButton)
            myview.add_item(resetButton)

            message = await interaction.response.send_message(embed=createEmbed(),
                                         view=myview,
                                         delete_after=120, ephemeral = True)

    @nextcord.slash_command(guild_ids= [testServerID], description = 'Open shop to buy and sell items. Prices are in gold, listed in the dropdown menus')
    async def shop(self, interaction:Interaction):
        arr = self.getPlayer(interaction)
        player = arr[0]
        id = arr[1]
        if not player:
            await interaction.response.send_message('You are not registered', delete_after=20, ephemeral = True)
        else:
            transaction_dictionary = {}
            costs_dictionary = {
                'Stone': {
                    'Buy': 2,
                    'Sell': 1
                },
                'Meat': {
                    'Buy': 2,
                    'Sell': 1
                },
                'Hide': {
                    'Buy': 2,
                    'Sell': 1
                },
                'Bark': {
                    'Buy': 2,
                    'Sell': 1
                }
            }
            item = ''
            amount = 0

            def createEmbed():
                embed = nextcord.Embed(title='Shop',
                                       description='Buy and Sell Things')
                for x, y in transaction_dictionary.items():
                    embed.add_field(name=x, value=y)
                return embed

            selectoptions = [
                nextcord.SelectOption(label='Stone',
                                      description='Buy: 2\nSell: 1'),
                nextcord.SelectOption(label='Meat',
                                      description='Buy: 2\nSell: 1'),
                nextcord.SelectOption(label='Hide',
                                      description='Buy: 2\nSell: 1'),
                nextcord.SelectOption(label='Bark',
                                      description='Buy: 2\nSell: 1')
            ]

            amountselectoptions = [
                nextcord.SelectOption(label='1'),
                nextcord.SelectOption(label='5'),
                nextcord.SelectOption(label='10')
            ]

            async def dropdown_callback(interaction):
                nonlocal item
                if dropdown.values[0] == 'Stone':
                    item = 'Stone'
                elif dropdown.values[0] == 'Meat':
                    item = 'Meat'
                elif dropdown.values[0] == 'Hide':
                    item = 'Hide'
                elif dropdown.values[0] == 'Bark':
                    item = 'Bark'
                

            async def amountdropdown_callback(interaction):
                nonlocal amount
                if amountdropdown.values[0] == '10':
                    amount = 10
                elif amountdropdown.values[0] == '1':
                    amount = 1
                elif amountdropdown.values[0] == '5':
                    amount = 5
                

            async def increaseAmount_callback(interaction):
                if item not in transaction_dictionary:
                    transaction_dictionary[item] = amount
                else:
                    transaction_dictionary[item] += amount
                await interaction.response.edit_message(embed=createEmbed(), view=myview)
                

            async def decreaseAmount_callback(interaction):
                if item not in transaction_dictionary:
                    transaction_dictionary[item] = -amount
                else:
                    transaction_dictionary[item] -= amount
                await interaction.response.edit_message(embed=createEmbed(), view=myview)
                

            async def confirmButton_callback(interaction):
                if len(transaction_dictionary) < 0 or all(value == 0 for value in transaction_dictionary.values()):
                    embed = nextcord.Embed(title = 'Nothing Bought or Sold')
                    await interaction.response.edit_message(embed = embed, view = View())
                    return
                gold_index = player.inventory.index[(
                    player.inventory['Name'] == 'Gold')][0]
                gold = player.inventory.loc[gold_index, 'Amount']
                original_gold = gold

                order_list = []
    
                for x, y in transaction_dictionary.items():
                    if y >= 0:
                        gold -= costs_dictionary[x]['Buy'] * y
                        order_list.append({'Buy': [x, y]})
                    elif y < 0:
                        try:
                            index = player.inventory.index[(
                                player.inventory['Name'] == x)][0]
                            if player.inventory.loc[index,
                                                    'Amount'] < abs(y):
                                return await interaction.response.send_message(
                                    "Don't have enough " + x + ' to sell',
                                    delete_after=20, ephemeral = True)
                            else:
                                order_list.append({'Sell': [x, y]})
                        except:
                            return await interaction.response.send_message("Don't have enough " +
                                                  x + ' to sell',
                                                  delete_after=20, ephemeral = 20)
                        gold += costs_dictionary[x]['Sell'] * abs(y)

                if gold < 0:
                    await interaction.response.send_message('Not enough Gold', delete_after=20, ephemeral = True)
                else:
                    embed = nextcord.Embed(title = 'Shop Summary', color = nextcord.Color.gold())
                    buy_string = '\u200b'
                    sell_string = '\u200b'
                    for action_dict in order_list:
                        if 'Buy' in action_dict.keys():
                            player.inventory = playerClass.Player.addItem(player, [action_dict['Buy'][0]],[action_dict['Buy'][1]])
                            buy_string += action_dict['Buy'][0] + ': ' + str(action_dict['Buy'][1]) + '\n'
                        elif 'Sell' in action_dict.keys():
                            player.inventory = playerClass.Player.subtractItem(player, [action_dict['Sell'][0]],[abs(action_dict['Sell'][1])])
                            sell_string += action_dict['Sell'][0] + ': ' + str(abs(action_dict['Sell'][1])) + '\n'
                    player.inventory.loc[gold_index, 'Amount'] = gold
                    embed.add_field(name = 'BOUGHT', value = buy_string, inline = True)
                    embed.add_field(name = 'SOLD', value = sell_string, inline = True)
                    embed.add_field (name = 'GOLD', value = str(-(original_gold - gold)), inline = False)
                    await interaction.response.edit_message(embed = embed, view = View())
                    sqlCommands.save(id, player, database='player')

            dropdown = Select(placeholder='Choose Item', options=selectoptions)
            dropdown.callback = dropdown_callback
            amountdropdown = Select(placeholder='Choose Amount',
                                    options=amountselectoptions)
            amountdropdown.callback = amountdropdown_callback
            increaseAmount = Button(label='Buy',
                                    style=nextcord.ButtonStyle.green)
            increaseAmount.callback = increaseAmount_callback
            decreaseAmount = Button(label='Sell',
                                    style=nextcord.ButtonStyle.red)
            decreaseAmount.callback = decreaseAmount_callback
            confirmButton = Button(label='Confirm Order',
                                   style=nextcord.ButtonStyle.blurple)
            confirmButton.callback = confirmButton_callback
            myview = View(timeout=120)
            myview.add_item(dropdown)
            myview.add_item(amountdropdown)
            myview.add_item(increaseAmount)
            myview.add_item(decreaseAmount)
            myview.add_item(confirmButton)

            await interaction.response.send_message(embed=createEmbed(),
                                         view=myview,
                                         delete_after=120, ephemeral = True)

    @nextcord.slash_command(guild_ids= [testServerID], description = 'Loot Boxes')
    async def lootbox(self):
        pass
    @lootbox.subcommand(description = 'Loot Box Exchange')
    async def exchange(self, interaction: Interaction):
        arr = self.getPlayer(interaction)
        player = arr[0]
        id = arr[1]
        if not player:
            await interaction.response.send_message('You are not registered', delete_after=20, ephemeral = True)
        else:
            transaction_dictionary = {}
            items_needed = ['Stone','Hide','Bark','Golden Apple','Panther Tooth','Gem']
            amount_list = []
            for items in items_needed:
                if items in player.inventory.loc[:,'Name'].tolist():
                    index = player.inventory.index[player.inventory['Name'] == items]
                    value = player.inventory.loc[index, 'Amount'].tolist()[0]
                    amount_list.append(value)
                else:
                    amount_list.append(0)
          
            for name, amount in zip(items_needed, amount_list):
                transaction_dictionary[name] = amount
              
            original_transaction_dictionary = transaction_dictionary.copy()

          
            costs_dictionary = {
                'Common Lootbox': {
                    'Stone': 5,
                    'Hide': 5,
                    'Bark': 5
                },
                'Premium Lootbox': {
                    'Panther Tooth': 5,
                    'Golden Apple': 5,
                    'Gem': 5
                }
            }
            common_lootbox_amount = 0
            premium_lootbox_amount = 0
            item = ''
            amount = 0

            def createEmbed():
                embed = nextcord.Embed(title='Lootbox Exchange',
                                       description='Exchange items for lootboxes')
                for x, y in transaction_dictionary.items():
                    embed.add_field(name=x, value='Total: ' + str(y), inline = False)
                embed.add_field(name = 'Common Lootbox', value = common_lootbox_amount, inline = False)
                embed.add_field(name = 'Premium Lootbox', value = premium_lootbox_amount, inline = False)
                return embed

            selectoptions = [
                nextcord.SelectOption(label='Common Lootbox',
                                      description='5 Stone, 5 Hide, 5 Bark'),
                nextcord.SelectOption(label='Premium Lootbox',
                                      description='5 Gem, 5 Panther Tooth, 5 Golden Apple')
            ]

            amountselectoptions = [
                nextcord.SelectOption(label='1'),
                nextcord.SelectOption(label='5'),
                nextcord.SelectOption(label='10')
            ]
            async def dropdown_callback(interaction):
                nonlocal item
                if dropdown.values[0] == 'Common Lootbox':
                    item = 'Common Lootbox'
                elif dropdown.values[0] == 'Premium Lootbox':
                    item = 'Premium Lootbox'

            async def amountdropdown_callback(interaction):
                nonlocal amount
                if amountdropdown.values[0] == '1':
                    amount = 1
                elif amountdropdown.values[0] == '5':
                    amount = 5
                elif amountdropdown.values[0] == '10':
                    amount = 10
                

            async def increaseAmount_callback(interaction):
                nonlocal common_lootbox_amount, premium_lootbox_amount
                for resource, cost in costs_dictionary[item].items():
                    transaction_dictionary[resource] -= cost * amount
                if item == 'Common Lootbox':
                    common_lootbox_amount += amount
                elif item == 'Premium Lootbox':
                    premium_lootbox_amount += amount
                await interaction.response.edit_message(embed=createEmbed(), view=myview)
                

            async def decreaseAmount_callback(interaction):
                nonlocal common_lootbox_amount, premium_lootbox_amount
                for resource, cost in costs_dictionary[item].items():
                    transaction_dictionary[resource] += cost * amount
                if item == 'Common Lootbox':
                    common_lootbox_amount -= amount
                elif item == 'Premium Lootbox':
                    premium_lootbox_amount -= amount
                await interaction.response.edit_message(embed=createEmbed(), view=myview)
                

            async def confirmButton_callback(interaction):
                if common_lootbox_amount == 0 and premium_lootbox_amount == 0:
                    embed = nextcord.Embed(title = 'No Purchase was Made')
                    await interaction.response.edit_message(embed = embed, view = View())
                elif any(value < 0 for value in transaction_dictionary.values()) or common_lootbox_amount < 0 or premium_lootbox_amount < 0:
                    embed = nextcord.Embed(title = 'Transaction Failed')
                    await interaction.response.edit_message(embed = embed, view = View())
                    return
                
                else:
                    items_list, amount_list = [], []
                    for item, original_value, value in zip(original_transaction_dictionary.keys(), original_transaction_dictionary.values(), transaction_dictionary.values()):
                        items_list.append(item)
                        amount_list.append(-(original_value - value))
                    player.inventory = playerClass.Player.updateItem(player, items_list, amount_list)
                    player.inventory = playerClass.Player.updateItem(player, ['Common Loot Box','Premium Loot Box'],[common_lootbox_amount, premium_lootbox_amount])
                    sqlCommands.save(id, player, database = 'player')
                    embed = nextcord.Embed(title = 'Purchase Confirmed', description = 'You got ' + str(common_lootbox_amount) + ' Common Loot Boxes and ' + str(premium_lootbox_amount) + ' Premium Loot Boxes!')
                    await interaction.response.edit_message(embed = embed, view = View())

            dropdown = Select(placeholder='Choose Lootbox', options=selectoptions)
            dropdown.callback = dropdown_callback
            amountdropdown = Select(placeholder='Choose Amount',
                                    options=amountselectoptions)
            amountdropdown.callback = amountdropdown_callback
            increaseAmount = Button(label='Increase',
                                    style=nextcord.ButtonStyle.green)
            increaseAmount.callback = increaseAmount_callback
            decreaseAmount = Button(label='Decrease',
                                    style=nextcord.ButtonStyle.red)
            decreaseAmount.callback = decreaseAmount_callback
            confirmButton = Button(label='Confirm Order',
                                   style=nextcord.ButtonStyle.blurple)
            confirmButton.callback = confirmButton_callback
            myview = View(timeout=120)
            myview.add_item(dropdown)
            myview.add_item(amountdropdown)
            myview.add_item(increaseAmount)
            myview.add_item(decreaseAmount)
            myview.add_item(confirmButton)

            await interaction.response.send_message(embed=createEmbed(),
                                         view=myview,
                                         delete_after=120, ephemeral = True)

    @lootbox.subcommand(description = 'Open Loot Box')
    async def open(self, interaction:Interaction):
        arr = self.getPlayer(interaction)
        player = arr[0]
        id = arr[1]
        if not player:
            await interaction.response.send_message('You are not registered', delete_after=20, ephemeral = True)
        else:
            item = ''
            amount = 0
            def createEmbed(name = '\u200b', text = '\u200b'):
                lootbox_dictionary = {}
                lootbox_list_index = player.inventory.index[player.inventory['Type']=='Loot Box'].tolist()
                for lootbox_index in lootbox_list_index:
                    name = player.inventory.loc[lootbox_index,'Name']
                    cur_amount = player.inventory.loc[lootbox_index, 'Amount']
                    lootbox_dictionary[name] = cur_amount
                embed = nextcord.Embed(title='Lootbox Open')
                for x, y in lootbox_dictionary.items():
                    embed.add_field(name=x, value='Total: ' + str(y), inline = True)
                embed.add_field(name= name, value = text, inline = False)
                return embed

            selectoptions = [
                nextcord.SelectOption(label='Common Loot Box'),
                nextcord.SelectOption(label='Premium Loot Box')
            ]
            amountselectoptions = [
                nextcord.SelectOption(label='1'),
                nextcord.SelectOption(label='5'),
                nextcord.SelectOption(label='10')
            ]
            async def dropdown_callback(interaction):
                nonlocal item
                if dropdown.values[0] == 'Common Loot Box':
                    item = 'Common Loot Box'
                elif dropdown.values[0] == 'Premium Loot Box':
                    item = 'Premium Loot Box'

            async def amountdropdown_callback(interaction):
                nonlocal amount
                if amountdropdown.values[0] == '1':
                    amount = 1
                elif amountdropdown.values[0] == '5':
                    amount = 5
                elif amountdropdown.values[0] == '10':
                    amount = 10
                

            async def confirmButton_callback(interaction):
                index = player.inventory.index[player.inventory['Name'] == item].tolist()[0]
                if index == [] or amount > player.inventory.loc[index,'Amount']:
                    text = 'Not enough ' + item + 'es'
                    await interaction.response.edit_message(embed = createEmbed(name = text), view = myview)
                else:
                    player.inventory = playerClass.Player.updateItem(player, [item], [-amount])
                    lootbox_rewards = lootbox.CommonLootbox().open(amount)
                    player.inventory = playerClass.Player.updateItem(player, lootbox_rewards[0], lootbox_rewards[1])
                    sqlCommands.save(id, player, database = 'player')
                    text = ''
                    for name, freq in zip(lootbox_rewards[0], lootbox_rewards[1]):
                        text += '🎊 ' + name + ': ' + str(freq) + ' 🎊\n'
                    await interaction.response.edit_message(embed = createEmbed(text = text), view = myview)

            dropdown = Select(placeholder='Choose Lootbox', options=selectoptions)
            dropdown.callback = dropdown_callback
            amountdropdown = Select(placeholder='Choose Amount',
                                    options=amountselectoptions)
            amountdropdown.callback = amountdropdown_callback
            confirmButton = Button(label='Confirm Order',
                                   style=nextcord.ButtonStyle.blurple)
            confirmButton.callback = confirmButton_callback
            myview = View(timeout=120)
            myview.add_item(dropdown)
            myview.add_item(amountdropdown)
            myview.add_item(confirmButton)

            await interaction.response.send_message(embed=createEmbed(),
                                         view=myview,
                                         delete_after=120, ephemeral = True)
          
def setup(bot):
    bot.add_cog(AccountCommands(bot))
