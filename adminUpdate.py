from sqlitedict import SqliteDict
import playerClass


with SqliteDict('player.sqlite') as mydict:
    player = mydict['4777'] 
    newplayer = playerClass.Warrior(player.Name)
    for variable in vars(player).keys():
        if variable == 'CurrentEXP':
            vars(newplayer)[variable] = 0
        elif variable == 'MaxEXP':
            vars(newplayer)[variable] = 2560
        else:
            vars(newplayer)[variable] = vars(player)[variable]
    print(vars(newplayer))
    mydict['4777'] = newplayer
    mydict.commit()

