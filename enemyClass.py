import random

class Enemy:
    def __init__(self, name, maxhealthrange, attackrange, defenserange, magicattackrange, magicdefenserange, attackspeedrange):
        self.Name = name
        self.MaxHealth = random.randint(maxhealthrange[0], maxhealthrange[1])
        self.Attack = random.randint(attackrange[0], attackrange[1])
        self.Defense = random.randint(defenserange[0], defenserange[1])
        self.MagicAttack = random.randint(magicattackrange[0], magicattackrange[1])
        self.MagicDefense = random.randint(magicdefenserange[0], magicdefenserange[1])
        self.AttackSpeed = random.randint(attackspeedrange[0], attackspeedrange[1])
        self.CurrentHealth = self.MaxHealth

    def enemyAttack(self):
        decision = random.choices(['Attack','Magic Attack'], weights = [self.Attack, self.MagicAttack])
        if decision == ['Attack']:
            attack = random.randint(0, self.Attack)
            return {'Attack':attack}
        else:
            attack = random.randint(0, self.MagicAttack)
            return {'Magic Attack':attack}

    def mobDrop(self, listofdrops, listofdropweights, dropnumber):
        decision = random.choices(listofdrops, weights = listofdropweights, k = dropnumber)
        mobdrops = []
        for decisionindex in range(len(decision)):
            for dropindex in range(len(listofdrops)):
                if decision[decisionindex] == listofdrops[dropindex]:
                    mobdrops.append(listofdrops[dropindex])
        return mobdrops




class Golem(Enemy):
    def __init__(self, name, maxhealthrange, attackrange, defenserange, magicattackrange, magicdefenserange, attackspeedrange, bonusdefense, bonusmagicdefense, bonushealth):
        Enemy.__init__(self, name, maxhealthrange, attackrange, defenserange, magicattackrange, magicdefenserange, attackspeedrange)
        
        self.Defense += random.randint(0, bonusdefense)
        self.MagicDefense += random.randint(0,bonusmagicdefense)
        self.MaxHealth += random.randint(0, bonushealth)
        self.CurrentHealth = self.MaxHealth

golem = Golem('Thuhij',[0,5],[0,5],[0,5],[0,5],[0,5],[0,5],2, 2, 2)

golem.mobDrop(listofdrops=['Gold','Weapon','Stones','Tree'], listofdropweights=[5, 5, 5, 5], dropnumber=5)