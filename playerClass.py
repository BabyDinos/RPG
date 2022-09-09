import random
import pandas as pd
import math


class Player:
    def __init__(self, name):
        self.Name = name
        self.stats_dictionary = {'Max Health' : 10, 'Attack':5,
                        'Magic Attack':5,'Defense':5,
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

    def attackSpeed(self, enemy):
        decision = random.choices(['Player','Enemy'], weights = [self.stats_dictionary['Attack Speed'], enemy.AttackSpeed])

        if decision[0] == 'Player':
            return 'Player Goes'
        else:
            return 'Enemy Goes'

    def attack(self):
        return random.randint(0, self.stats_dictionary['Attack'])
    
    def magicAttack(self):
        return random.randint(0, self.stats_dictionary['Magic Attack'])

    def defend(self):
        currentdefense = random.randint(0, self.stats_dictionary['Defense'])
        currentmagicdefense = random.randint(0, self.stats_dictionary['Magic Defense'])
        return {'Defense': currentdefense, 'Magic Defense': currentmagicdefense}

    def powerUp(self):
        temp_attack = self.stats_dictionary['Attack']
        temp_magic_attack = self.stats_dictionary['Magic Attack']
        self.stats_dictionary['Attack'] = int(math.ceil(self.stats_dictionary['Attack'] * 1.5))
        self.stats_dictionary['Magic Attack'] = int(math.ceil(self.stats_dictionary['Magic Attack'] * 1.5))
        return self.stats_dictionary['Attack'] - temp_attack, self.stats_dictionary['Magic Attack'] - temp_magic_attack

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


def toList(string):
    if string != 'None':
        string = string.split('-')
        return string

# function for administrators to add items from an excel file into inventories. Will be used to add drops to players inventories
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


