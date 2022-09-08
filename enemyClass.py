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



class Golem(Enemy):
    def __init__(self, name, maxhealthrange, attackrange, defenserange, magicattackrange, magicdefenserange, attackspeedrange, bonusdefense, bonusmagicdefense, bonushealth):
        Enemy.__init__(self, name, maxhealthrange, attackrange, defenserange, magicattackrange, magicdefenserange, attackspeedrange)
        
        self.Defense += random.randint(0, bonusdefense)
        self.MagicDefense += random.randint(0,bonusmagicdefense)
        self.MaxHealth += random.randint(0, bonushealth)
        self.CurrentHealth = self.MaxHealth

