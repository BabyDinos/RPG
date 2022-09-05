from typing import final


class Player:
    # base stats
    stats_dictionary = {'Max Health' : 10, 'Attack':5,
                        'Magic Attack':5,'Defense ':5,
                        'Magic Defense': 5, 'Attack Speed':1}
    def __init__(self, name, curHealth = stats_dictionary['Max Health']):
        self.name = name
        self.curHealth = curHealth


class Warrior(Player):
    stats_dictionary = Player.stats_dictionary.copy()
    stats_dictionary['Max Health'] = 12
    stats_dictionary['Attack'] = 14
    stats_dictionary['Defense'] = 14

class Mage(Player):
    stats_dictionary = Player.stats_dictionary.copy()
    stats_dictionary['Magic Attack'] = 18
    stats_dictionary['Magic Defense'] = 12

def difference(whatClass):

    arr = []
    player = Player('name')
    warrior = Warrior('name')
    mage = Mage('name')

    if whatClass == 'Warrior':
        for (x, y), (a,b) in zip(warrior.stats_dictionary.items(), player.stats_dictionary.items()):
            if y-b == 0:
                arr.append(x + ': ' + str(b))
            elif y - b > 0:
                arr.append(x + ': ' + str(b) + ' (+' + str(y-b) + ')')
            else:
                arr.append(x + ': ' + str(b) + ' (-' + str(y-b) + ')')
    elif whatClass == 'Mage':
        for (x, y), (a,b) in zip(mage.stats_dictionary.items(), player.stats_dictionary.items()):
            if y - b == 0:
                arr.append(x + ': ' + str(b))
            elif y - b > 0:
                arr.append(x + ': ' + str(b) + ' (+' + str(y-b) + ')')
            else:
                arr.append(x + ': ' + str(b) + ' (-' + str(y-b) + ')')
    final_string = ''
    for string in arr:
        final_string += string + '\n'
    return final_string
