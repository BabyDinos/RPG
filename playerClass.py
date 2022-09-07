import random
import pandas as pd


class Player:
    def __init__(self, name):
        self.Name = name
        self.stats_dictionary = {'Max Health' : 10, 'Attack':5,
                        'Magic Attack':5,'Defense ':5,
                        'Magic Defense': 5, 'Attack Speed':1}
        self.inventory = pd.DataFrame(columns= ['Name','Description','Stats', 'Amount', 'Type'])
        self.equipment = pd.DataFrame(data = 'None', columns= ['Name','Stats','Type'],index = ['Weapon','Armor','Pet'])
        self.CurrentHealth = self.stats_dictionary['Max Health']
        self.inventory.loc[len(self.inventory.index)] = ['Gold', 'Currency used in the market and for other applications', 'None', 100, 'Currency']

    def equip(self, equipmentName):
        if equipmentName in self.inventory.loc[:,'Name'].values:
            index = self.inventory.index[(self.inventory['Name'] == equipmentName)].tolist()
            type = self.inventory.loc[index, 'Type'].tolist()[0]
            if type == 'Attack' or type == 'Magic Attack':
                self.equipment.loc['Weapon'] = [equipmentName, self.inventory.loc[index, 'Stats'].tolist()[0], type]
            else:
                self.equipment.loc['Armor'] = [equipmentName, self.inventory.loc[index, 'Stats'].tolist()[0], type]
            return True
        else:
            return False

    def attack(self):
        pass

    def defend(self):
        pass

class Warrior(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        # increasing stats fit for a warrior
        self.stats_dictionary['Max Health'] = 12
        self.stats_dictionary['Attack'] = 14
        self.stats_dictionary['Defense'] = 14
        # eqipping warrior with base weapon and armor
        self.inventory.loc[len(self.inventory.index)] = ['Wooden Sword','The most basic of swords',['0', '3'], 1, 'Attack']
        self.inventory.loc[len(self.inventory.index)] = ['Cloth Armor','The most basic of armors',['0','2'], 1, 'Defense']
        self.equipment.loc['Weapon'] = ['Wooden Sword',['0', '3'], 'Attack']
        self.equipment.loc['Armor'] = ['Cloth Armor',['0','2'], 'Defense']

class Mage(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self.stats_dictionary['Magic Attack'] = 18
        self.stats_dictionary['Magic Defense'] = 12
        self.inventory.loc[len(self.inventory.index)] = ['Wooden Staff','The most basic of staves',['0', '3'], 1, 'Magic Attack']
        self.inventory.loc[len(self.inventory.index)] = ['Cloth Robe','The most basic of robes',['0','2'], 1, 'Magic Defense']
        self.equipment.loc['Weapon'] = ['Wooden Staff', ['0', '3'], 'Magic Attack']
        self.equipment.loc['Armor'] = ['Cloth Robe',['0','2'], 'Magic Defense']

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
    # arr first string will be Stats, next will be equipment, and last will be inventory
    arr = []
    string = ''
    for x, y in player.stats_dictionary.items():
        string += x + ': ' + str(y) + '\n'  
    arr.append(string)
    string = ''
    for r in range(len(player.equipment.index)):
        player.equipment.iloc[r,0]
        string += player.equipment.iloc[r].name + ': ' + str(player.equipment.iloc[r,0]) + '\n'
    arr.append(string)
    return arr

# helper functions for the functions
def toList(string):
    if string != 'None':
        string = string.split('-')
        return string

def toString(list):
    if list != 'None':
        return list[0] + ' - ' + list[1]
    else:
        return list

def playerInventory(player):
    dictionary = {}
    for row in range(len(player.inventory.index)):
        for colCount, colName in enumerate(player.inventory.columns):
            if colName != 'Stats' and colCount > 0:
                dictionary[name][colName] = player.inventory.iloc[row,colCount]
            elif colName == 'Stats':
                dictionary[name][colName] = toString(player.inventory.iloc[row,colCount])
            else:
                name = player.inventory.iloc[row,colCount]
                dictionary[name] = {}

    return dictionary

def addItem(player, nameOfItem, amounts):
    #nameOfItem is a list of names of items
    #amounts is a list of same length as nameOfItem
    df = pd.read_excel('items.xlsx', index_col = [0], converters={'Name':str, 'Description': str, 'Stats': str, 'Amount': int, 'Type': str})
    df['Stats'] = df.apply(lambda x: toList(x['Stats']), axis = 1)

    for name, amount in zip(nameOfItem, amounts):
        if name in player.inventory.loc[:,'Name'].tolist():
            index = player.inventory.index[player.inventory['Name'] == name].tolist()
            newVal = int(player.inventory.loc[index,'Amount']) + amount
            player.inventory.loc[index, 'Amount'] = newVal
        else:
            index = player.inventory.index
            player.inventory.loc[index] = df.loc[name]
            player.inventory.loc[index,'Amount'] = amount

    return player.inventory

player = Warrior('Thuhij')
playerInventory(player)