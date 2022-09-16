from sqlitedict import SqliteDict
import playerClass
import pandas as pd


with SqliteDict('player.sqlite') as mydict:
    for key in mydict.keys():
        player = mydict[key] 
        if player.role == 'Warrior':
            newplayer = playerClass.Warrior(player.Name)
        elif player.role == 'Mage':
            newplayer = playerClass.Mage(player.Name)
        #Update all variables
        for variable in vars(player).keys():
            vars(newplayer)[variable] = vars(player)[variable]
        #Update inventory with most recent descriptions
        newplayer.inventory = pd.DataFrame(columns= ['Name','Description','Stats', 'Amount', 'Type'], dtype=object)
        item_list = []
        amount_list = []
        for index, row in player.inventory.iterrows():
            item_list.append(player.inventory.loc[index,'Name'])
            amount_list.append(player.inventory.loc[index,'Amount'])
        newplayer.inventory = playerClass.Player.updateItem(newplayer, item_list, amount_list)
        mydict[key] = newplayer
    mydict.commit()

with SqliteDict('player.sqlite') as mydict:
    player = mydict['4777']
    print(player.inventory)