from sqlitedict import SqliteDict
import playerClass


with SqliteDict('player.sqlite') as mydict:
    player = mydict['4777'] 
    newplayer = playerClass.Warrior(player.Name)
    for variable in vars(player).keys():
        if variable in ['CurrentLevel','MaxLevel','Level']:
            newplayer[variable] = vars(player)[variable]
        else:
            vars(newplayer)[variable] = vars(player)[variable]
    print(vars(newplayer))
    mydict['4777'] = newplayer
    mydict.commit()

