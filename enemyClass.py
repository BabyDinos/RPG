import random
from collections import Counter
import math
import numpy as np

class Enemy:
    def __init__(self, name, player):
        self.Name = name
        self.stats_dictionary = {'Max Health':random.randint(2*player.Level,5*player.Level),
                                'Attack':random.randint(1*player.Level,4*player.Level),
                                'Magic Attack':random.randint(2*player.Level,3*player.Level),
                                'Defense':random.randint(1*player.Level,4*player.Level),
                                'Magic Defense':random.randint(2*player.Level,3*player.Level),
                                'Attack Speed':random.randint(1*player.Level,2*player.Level)}
        self.CurrentHealth = self.stats_dictionary['Max Health']
        self.ListOfDrops = []
        self.ListOfDropWeights = []
        self.DropNumber = 0

    def enemyAttack(self):
        attack = random.randint(0, self.stats_dictionary['Attack'])
        magicattack = random.randint(0, self.stats_dictionary['Magic Attack'])
        return {'Attack':attack, 'Magic Attack':magicattack}

    def enemyDefend(self):
        currentdefense = random.randint(0, self.stats_dictionary['Defense'])
        currentmagicdefense = random.randint(0, self.stats_dictionary['Magic Defense'])
        return {'Defense': currentdefense, 'Magic Defense': currentmagicdefense}

    def enemyPowerUp(self):
        self.stats_dictionary['Attack'] = int(math.ceil(self.stats_dictionary['Attack'] * 1.5))
        self.stats_dictionary['Magic Attack'] = int(math.ceil(self.stats_dictionary['Magic Attack'] * 1.5))
        self.stats_dictionary['Attack Speed'] = int(math.ceil(self.stats_dictionary['Attack Speed'] * 1.5))
        return self.stats_dictionary['Attack'], self.stats_dictionary['Magic Attack'], self.stats_dictionary['Attack Speed']

    def mobDrop(self, listofdrops, listofdropweights, dropnumber):
        decision = random.choices(listofdrops, weights = listofdropweights, k = dropnumber)
        mobdrops = {}
        for decisionindex in range(len(decision)):
            name = decision[decisionindex]
            if name in mobdrops.keys():
                mobdrops[name] += 1
            else:
                mobdrops[name] = 1

        return [mobdrops.keys(), mobdrops.values()]

    def xpDrop(self):
        return self.DropNumber * 3

    

class Golem(Enemy):
    def __init__(self, name, player, bonuses = [2,0,0,2,2,0]):
        Enemy.__init__(self, name, player)
        bonuses = np.asarray(bonuses) + player.Level
        for count, key in enumerate(self.stats_dictionary.keys()):
            if bonuses[count] == 0:
                continue
            elif bonuses[count] > 0:
                self.stats_dictionary[key] += random.randint(0, bonuses[count])
            else:
                debuff = random.randint(bonuses[count], 0)
                if abs(debuff) > self.stats_dictionary[key]:
                    self.stats_dictionary[key] = 1
                else:
                    self.stats_dictionary[key] += debuff


        self.ListOfDrops = ['Gold','Stone','Gem']
        self.ListOfDropWeights = [5, 5, 1]
        self.DropNumber = int(np.mean([x for x in self.stats_dictionary.values() if type(x) == int]))

class Panther(Enemy):
    def __init__(self, name, player, bonuses = [0,4,0,0,0,2]):
        Enemy.__init__(self, name, player)
        bonuses = np.asarray(bonuses) + player.Level
        for count, key in enumerate(self.stats_dictionary.keys()):
            if bonuses[count] == 0:
                continue
            elif bonuses[count] > 0:
                self.stats_dictionary[key] += random.randint(0, bonuses[count])
            else:
                debuff = random.randint(bonuses[count], 0)
                if abs(debuff) > self.stats_dictionary[key]:
                    self.stats_dictionary[key] = 1
                else:
                    self.stats_dictionary[key] += debuff

        self.ListOfDrops = ['Gold','Meat','Hide','Panther Tooth']
        self.ListOfDropWeights = [5, 5, 5, 1]
        self.DropNumber = int(np.mean([x for x in self.stats_dictionary.values() if type(x) == int]))

class TreeMonster(Enemy):
    def __init__(self, name, player, bonuses = [3,0,0,0,3,0]):
        Enemy.__init__(self, name, player)
        bonuses = np.asarray(bonuses) + player.Level
        for count, key in enumerate(self.stats_dictionary.keys()):
            if bonuses[count] == 0:
                continue
            elif bonuses[count] > 0:
                self.stats_dictionary[key] += random.randint(0, bonuses[count])
            else:
                debuff = random.randint(bonuses[count], 0)
                if abs(debuff) > self.stats_dictionary[key]:
                    self.stats_dictionary[key] = 1
                else:
                    self.stats_dictionary[key] += debuff

        self.ListOfDrops = ['Gold','Bark','Golden Apple']
        self.ListOfDropWeights = [5, 5, 1]
        self.DropNumber = int(np.mean([x for x in self.stats_dictionary.values() if type(x) == int]))


#golem = Golem('Thuhij',[0,5],[0,5],[0,5],[0,5],[0,5],[0,5],2, 2, 2)

#drops = golem.mobDrop(['Gold','Stone','Gem'],[5,5,0],dropnumber=5)
