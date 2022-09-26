import os
from nextcord.ext import commands
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ui import Button, View
import sqliteCommands
import sys
import pandas as pd
sys.path.insert(1, 'C:/Users/School/OneDrive - The City University of New York/Documents/GitHub/RPG')
import port 
import marketdata

testServerID = int(os.environ['testServerID'])

class excCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.item_list = pd.read_excel('items.xlsx', usecols='A').loc[:,'Name'].tolist()

    def getPlayer(self, interaction):
        id = str(interaction.user).split('#')[-1]
        return [sqliteCommands.sqldictCommands.load(id, database='player'), id]

    @nextcord.slash_command(guild_ids = [testServerID], description = 'Submit an order')
    async def order(self, interaction: Interaction, item:str, price:int, quantity:int, 
        action: str = SlashOption(
        name = 'ordertype', choices={"buy":'Buy', "sell":'Sell'}
    )
    ):
        arr = self.getPlayer(interaction)
        player = arr[0]
        id = arr[1]
        if not player:
            await interaction.response.send_message('You are not registered', ephemeral = True)
        else:
            try:
                if item not in self.item_list:
                    await interaction.response.send_message('Item does not exist', ephemeral= True)
                    return
                if action == 'Buy':
                    index = player.inventory.index[player.inventory['Name'] == 'Gold'].tolist()[0]
                    if player.inventory.loc[index, 'Amount'] < price*quantity:
                        await interaction.response.send_message('You do not have the neccessary funds', ephemeral = True)
                        return
                elif action == 'Sell':
                    index = player.inventory.index[player.inventory['Name'] == item].tolist()[0]
                    if player.inventory.loc[index, 'Amount'] < quantity:
                        await interaction.response.send_message('You do not have enough of the item ' + item, ephemeral = True)
                        return
                feedback = port.Port.order(id, port.Port.serial_number, (item, action, price, quantity))
                if feedback:
                    await interaction.response.send_message('Your order has been successfully placed', ephemeral = True)
            except:
                await interaction.response.send_message('Error in placing order', ephemeral = True)

    @nextcord.slash_command(guild_ids=[testServerID], description = 'See your orders')
    async def orderlist(self, interaction:Interaction):
        arr = self.getPlayer(interaction)
        player = arr[0]
        id = arr[1]
        if not player:
            await interaction.response.send_message('You are not registered', ephemeral = True)
        else:
            try:
                orderlist = sqliteCommands.sqldictCommands.load(id, database='playerorder')
                embed = nextcord.Embed(title = 'Orders', description = player.Name)
                for order in orderlist:
                    order_components = order.split('-')
                    embed.add_field(name = order_components[2], value = order_components[3] + order_components[5] + '@' + order_components[4] + '\n' + order)

                await interaction.response.send_message(embed = embed, ephemeral = True)
            except:
                await interaction.response.send_message('Failed to bring up order list', ephemeral=True)

    @nextcord.slash_command(guild_ids = [testServerID], description = 'Cancel an order')
    async def cancelorder(self, interaction: Interaction, orderid:str):
        arr = self.getPlayer(interaction)
        player = arr[0]
        id = arr[1]
        if not player:
            await interaction.response.send_message('You are not registered', ephemeral = True)
        else:
            try:
                feedback = port.Port.cancelorder(id, port.Port.serial_number, orderid)
                if feedback:
                    await interaction.response.send_message('Order ' + orderid + ' has been cancelled', ephemeral = True)
            except:
                await interaction.response.send_message('Order does not exist', ephemeral=True)

    @nextcord.slash_command(guild_ids=[testServerID], description = 'See market orders')
    async def market(self, interaction:Interaction):
        arr = self.getPlayer(interaction)
        player = arr[0]
        id = arr[1]
        if not player:
            await interaction.response.send_message('You are not registered', ephemeral = True)
        else:
            try:
                market_data = marketdata.MarketData.display()
                items_on_each_page = 10
                total_pages = max((len(market_data) // items_on_each_page), 1)
                currentPage = 0

                def createEmbed(pageNum=0, inline=False):

                    pageNum = pageNum % total_pages
                    embed = nextcord.Embed(title = 'BID | Market | ASK')
                    pointer = items_on_each_page  * pageNum
                    upper_bound = min(len(market_data), (items_on_each_page * (pageNum + 1)))
                    while pointer <= upper_bound-1:
                        entry = ''
                        name = market_data[pointer][0]
                        buy_value_dict = market_data[pointer][1][['Action','Price','Quantity']].to_dict(orient = 'records')
                        sell_value_dict = market_data[pointer][2][['Action','Price','Quantity']].to_dict(orient = 'records')
                        if buy_value_dict == []:
                            entry += '  0 🪙  | '
                        else:
                            entry += '  ' + str(buy_value_dict[0]['Price']) + ' 🪙  | '
                        entry += name
                        if sell_value_dict == []:
                            entry += ' |  0 🪙'
                        else:
                            entry += ' |  ' + str(sell_value_dict[0]['Price']) + ' 🪙'
                        embed.add_field(name=entry, value='\u200b', inline=inline)
                        pointer += 1
                    embed.set_footer(text=f'Page {pageNum+1} of {total_pages}')
                        
                    return embed

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
                    currentPage = total_pages 

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


                await interaction.response.send_message(embed = createEmbed(pageNum = currentPage), view = myview, ephemeral = True)
            except:
                await interaction.response.send_message('Failed to bring up market', ephemeral=True)
    # command to submit buy order - port
    # command to submit sell order - port
    # command to cancel order - port
    # command to see orders - marketdata.py


def setup(bot):
    bot.add_cog(excCommands(bot))

