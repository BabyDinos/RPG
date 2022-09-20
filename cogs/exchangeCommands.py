import os
from nextcord.ext import commands
import nextcord
from nextcord import Interaction
import sqliteCommands
import sys
sys.path.insert(1, 'C:/Users/School/OneDrive - The City University of New York/Documents/GitHub/RPG')
import port 

testServerID = int(os.environ['testServerID'])

class excCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def getPlayer(self, interaction):
        id = str(interaction.user).split('#')[-1]
        return [sqliteCommands.sqldictCommands.load(id, database='player'), id]

    @nextcord.slash_command(guild_ids = [testServerID], description = 'Go adventuring for loot, exp, and gold')
    async def buy(self, interaction: Interaction, item:str, action:str, price:int, quantity:int):
        arr = self.getPlayer(interaction)
        player = arr[0]
        id = arr[1]
        if not player:
            await interaction.response.send_message('You are not registered', ephemeral = True)
        else:
            try:
                index = player.inventory.index[player.inventory['Name'] == 'Gold'].tolist()[0]
                if player.inventory.loc[index, 'Amount'] < price*quantity:
                    await interaction.response.send_message('You do not have the neccessary funds', ephemeral = True)
                    return
                
            except:
                pass

    # command to submit buy order - port
    # command to submit sell order - port
    # command to cancel order - port
    # command to see orders - marketdata.py


def setup(bot):
    bot.add_cog(excCommands(bot))