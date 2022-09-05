
class Player:
    # base stats
    stats_dictionary = {'Max Health' : 10, 'Attack':5,
                        'Magic Attack':5,'Defense ':5,
                        'Magic Defense': 5, 'Attack Speed':1}
    def __init__(self, name, curHealth = stats_dictionary['Max Health']):
        self.Name = name
        self.CurrentHealth = curHealth


class Warrior(Player):
    stats_dictionary = Player.stats_dictionary.copy()
    stats_dictionary['Max Health'] = 12
    stats_dictionary['Attack'] = 14
    stats_dictionary['Defense'] = 14

class Mage(Player):
    stats_dictionary = Player.stats_dictionary.copy()
    stats_dictionary['Magic Attack'] = 18
    stats_dictionary['Magic Defense'] = 12

def baseDifference(whatClass):

    string = ''
    player = Player('name')
    warrior = Warrior('name')
    mage = Mage('name')

    if whatClass == 'Warrior':
        for (x, y), (a,b) in zip(warrior.stats_dictionary.items(), player.stats_dictionary.items()):
            if y-b == 0:
                string += x + ': ' + str(b) + '\n'
            elif y - b > 0:
                string += x + ': ' + str(b) + ' (+' + str(y-b) + ')' + '\n'
            else:
                string += x + ': ' + str(b) + ' (-' + str(y-b) + ')' + '\n'
    elif whatClass == 'Mage':
        for (x, y), (a,b) in zip(mage.stats_dictionary.items(), player.stats_dictionary.items()):
            if y-b == 0:
                string += x + ': ' + str(b) + '\n'
            elif y - b > 0:
                string += x + ': ' + str(b) + ' (+' + str(y-b) + ')' + '\n'
            else:
                string += x + ': ' + str(b) + ' (-' + str(y-b) + ')' + '\n'
    return string

def playerInfo(player):
    string = ''
    for x, y in vars(player).items():
        string += x + ': ' + str(y) + '\n'
    for x, y in player.stats_dictionary.items():
        string += x + ': ' + str(y) + '\n'   
    return string
