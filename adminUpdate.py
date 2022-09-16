from sqlitedict import SqliteDict
import playerClass


with SqliteDict('player.sqlite') as mydict:
    player = mydict['4777'] 
    newplayer = playerClass.Warrior(player.Name)
    for variable in vars(player).keys():
        if variable in ['CurrentLevel','MaxLevel','Level']:
            vars(newplayer)[variable] = vars(player)[variable]
        elif variable in ['statpoints','totalstatpoints']:
            vars(newplayer)[variable] = 90
        elif variable == 'stats_dictionary':
            vars(newplayer)[variable] = {'Max Health' : 10, 'Attack':5,'Magic Attack':5,'Defense':5,'Magic Defense': 5, 'Attack Speed':1}
        else:
            vars(newplayer)[variable] = vars(player)[variable]
    print(vars(newplayer))
    mydict['4777'] = newplayer
    mydict.commit()

