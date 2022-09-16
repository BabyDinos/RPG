from sqlitedict import SqliteDict
import playerClass
import pandas as pd


with SqliteDict('player.sqlite') as mydict:
    player = mydict['4777'] 
    newplayer = playerClass.Warrior(player.Name)
    for variable in vars(player).keys():
        vars(newplayer)[variable] = vars(player)[variable]
    names_list = []
    amount_list = []
    for index, row in newplayer.inventory.iterrows():
        names_list.append(newplayer.inventory.loc[index, 'Name'])
        amount_list.append(newplayer.inventory.loc[index, 'Amount'])
    print(newplayer.inventory)
    newplayer.inventory = pd.DataFrame(columns= ['Name','Description','Stats', 'Amount', 'Type'], dtype=object)
    newplayer.inventory = playerClass.Player.updateItem(newplayer, names_list, amount_list)
    print(newplayer.inventory)
    mydict['4777'] = newplayer
    mydict.commit()

