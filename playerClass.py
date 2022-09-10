import random
import pandas as pd
import math


def toList(string):
    if string != 'None':
        string = string.split('-')
        return string

class Player:
    def __init__(self, name):
        self.Name = name
        self.Level = 1
        self.CurrentLevel = 0
        self.MaxLevel = 100
        self.stats_dictionary = {'Max Health' : 10, 'Attack':5,'Magic Attack':5,'Defense':5,'Magic Defense': 5, 'Attack Speed':1}
        self.inventory = pd.DataFrame(columns= ['Name','Description','Stats', 'Amount', 'Type'], dtype=object)
        self.equipment = pd.DataFrame(data = 'None', columns= ['Name','Stats','Type'],index = ['Weapon','Armor','Pet'], dtype=object) 
        self.CurrentHealth = self.stats_dictionary['Max Health']
        self.inventory = addItem(self, ['Gold'],[100])
        self.statpoints = 10
        self.totalstatpoints = 10

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
        lower_bound = int(self.equipment.loc['Weapon','Stats'][0])
        upper_bound = int(self.equipment.loc['Weapon','Stats'][1])
        if self.equipment.loc['Weapon','Type'] == 'Attack':
            currentattack = random.randint(lower_bound, self.stats_dictionary['Attack'] + upper_bound)
            currentmagicattack = random.randint(0, self.stats_dictionary['Magic Attack'])
        else:
            currentattack = random.randint(0, self.stats_dictionary['Attack'])
            currentmagicattack = random.randint(lower_bound, self.stats_dictionary['Magic Attack'] + upper_bound)
        return {'Attack' : currentattack, 'Magic Attack': currentmagicattack} 

    def defend(self):
        lower_bound = int(self.equipment.loc['Armor','Stats'][0])
        upper_bound = int(self.equipment.loc['Armor','Stats'][1])
        if self.equipment.loc['Armor','Type'] == 'Defense':
            currentdefense = random.randint(lower_bound, self.stats_dictionary['Defense'] + upper_bound)
            currentmagicdefense = random.randint(0, self.stats_dictionary['Magic Defense'])
        else:
            currentdefense = random.randint(0, self.stats_dictionary['Defense'])
            currentmagicdefense = random.randint(lower_bound, self.stats_dictionary['Magic Defense'] + upper_bound)
        return {'Defense': currentdefense, 'Magic Defense': currentmagicdefense}

    def powerUp(self):
        self.stats_dictionary['Attack'] = int(math.ceil(self.stats_dictionary['Attack'] * 1.5))
        self.stats_dictionary['Magic Attack'] = int(math.ceil(self.stats_dictionary['Magic Attack'] * 1.5))
        self.stats_dictionary['Attack Speed'] = int(math.ceil(self.stats_dictionary['Attack Speed'] * 1.5))
        return self.stats_dictionary['Attack'], self.stats_dictionary['Magic Attack'], self.stats_dictionary['Attack Speed']

    def levelUp(self):
        while self.CurrentLevel >= self.MaxLevel:
            self.CurrentLevel  = self.CurrentLevel - self.MaxLevel
            self.MaxLevel = int(self.MaxLevel * 1.5)
            self.Level += 1
            self.statpoints += 10
            self.totalstatpoints += 10


class Warrior(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self.inventory = addItem(self, ['Wooden Sword','Cloth Armor'], [1,1])
        self.equip('Wooden Sword')
        self.equip('Cloth Armor')
        self.role = 'Warrior'
        self.berSerkCooldown = 3
    
    def berSerk(self):
        self.CurrentHealth += self.Level
        self.stats_dictionary['Attack'] += self.Level
        self.stats_dictionary['Defense'] += self.Level
        self.stats_dictionary['Attack Speed'] += self.Level
    


class Mage(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self.inventory = addItem(self, ['Wooden Staff','Cloth Robe'],[1,1])
        self.equip('Wooden Staff')
        self.equip('Cloth Robe')
        self.role = 'Mage'
        self.fireBallCooldown = 3

    def fireBall(self):
        return 2 * self.Level 


# function for administrators to add items from an excel file into inventories. Will be used to add drops to players inventories
def addItem(player, nameOfItem, amounts):
    #nameOfItem is a list of names of items
    #amounts is a list of same length as nameOfItems
    df = pd.read_excel('items.xlsx', index_col = [0], converters={'Name':str, 'Description': str, 'Stats': str, 'Amount': int, 'Type': str})
    df['Stats'] = df.apply(lambda x: toList(x['Stats']), axis = 1)

    for name, amount in zip(nameOfItem, amounts):
        if name in player.inventory.loc[:,'Name'].tolist():
            index = player.inventory.index[player.inventory['Name'] == name].tolist()
            newVal = int(player.inventory.loc[index,'Amount']) + amount
            player.inventory.loc[index, 'Amount'] = newVal
        else:
            index = len(player.inventory.index)
            player.inventory.loc[index] = df.loc[name]
            player.inventory.loc[index,'Name'] = name
            player.inventory.loc[index,'Amount'] = amount

    return player.inventory

warrior = Warrior('Bob')

warrior.inventory