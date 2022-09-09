import random
from collections import Counter
import math
from statistics import geometric_mean

class Enemy:
    def __init__(self, name, maxhealthrange, attackrange, defenserange, magicattackrange, magicdefenserange, attackspeedrange):
        self.Name = name
        self.CurrentHealth = random.randint(maxhealthrange[0], maxhealthrange[1])
        self.Attack = random.randint(attackrange[0], attackrange[1])
        self.MagicAttack = random.randint(magicattackrange[0], magicattackrange[1])
        self.Defense = random.randint(defenserange[0], defenserange[1])
        self.MagicDefense = random.randint(magicdefenserange[0], magicdefenserange[1])
        self.AttackSpeed = random.randint(attackspeedrange[0], attackspeedrange[1])


    def enemyAttack(self):
        decision = random.choices(['Attack','Magic Attack'], weights = [self.Attack, self.MagicAttack])
        if decision == ['Attack']:
            attack = random.randint(0, self.Attack)
            return {'Attack':attack}
        else:
            attack = random.randint(0, self.MagicAttack)
            return {'Magic Attack':attack}

    def enemyDefend(self):
        currentdefense = random.randint(0, self.Defense)
        currentmagicdefense = random.randint(0, self.MagicAttack)
        return {'Defense': currentdefense, 'Magic Defense': currentmagicdefense}

    def enemyPowerUp(self):
        temp_attack = self.Attack
        temp_magic_attack = self.MagicAttack
        self.Attack = int(math.ceil(self.Attack * 1.5))
        self.MagicAttack = int(math.ceil(self.MagicAttack * 1.5))
        return self.Attack - temp_attack, self.MagicAttack-temp_magic_attack

    def mobDrop(self, listofdrops, listofdropweights, dropnumber):
        decision = random.choices(listofdrops, weights = listofdropweights, k = dropnumber)
        mobdrops = []
        for decisionindex in range(len(decision)):
            for dropindex in range(len(listofdrops)):
                if decision[decisionindex] == listofdrops[dropindex]:
                    mobdrops.append(listofdrops[dropindex])

        return Counter(mobdrops).keys(), Counter(mobdrops).values()

class Golem(Enemy):
    def __init__(self, name, maxhealthrange, attackrange, defenserange, magicattackrange, magicdefenserange, attackspeedrange, bonusdefense, bonusmagicdefense, bonushealth):
        Enemy.__init__(self, name, maxhealthrange, attackrange, defenserange, magicattackrange, magicdefenserange, attackspeedrange)
        
        self.Defense += random.randint(0, bonusdefense)
        self.MagicDefense += random.randint(0,bonusmagicdefense)
        self.CurrentHealth += random.randint(0, bonushealth)

#golem = Golem('Thuhij',[0,5],[0,5],[0,5],[0,5],[0,5],[0,5],2, 2, 2)

