from sqlitedict import SqliteDict
import playerClass
import pandas as pd


with SqliteDict('player.sqlite') as mydict:
    player = mydict['4777'] 
    newplayer = playerClass.Warrior(player.Name)
    for variable in vars(player).keys():
        vars(newplayer)[variable] = vars(player)[variable]
    mydict['4777'] = newplayer
    mydict.commit()

