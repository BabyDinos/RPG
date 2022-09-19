import random

class lootbox:

    def open(self, amount):
        item_result = random.choices(self.items, weights = self.probabilities, k = amount)
        itemdrops = {}
        for name in item_result:
            if name in itemdrops.keys():
                itemdrops[name] += 1
            else:
                itemdrops[name] = 1

        return [itemdrops.keys(), itemdrops.values()]

class CommonLootbox(lootbox):

    def __init__(self):
        self.items = ['Gold','Meat','Hide','Bark','Stone','Stone Sword', 'Stone Staff', 'Hide Armor','Hide Robe','Bark Armor','Bark Robe','Bark Axe','Bark Wand','Panther Cub','Golemite','Twewant']
        self.probabilities = [19,19,19,19,19,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.33,0.33,0.33]

class PremiumLootBox(lootbox):

    def __init__(self):
        self.items = ['Gold','Gem','Panther Tooth','Golden Apple','Tooth Spear', 'Tooth Scepter', 'Gem Armor','Gem Robe','Golden Armor','Golden Robe','Golden Daggers','Golden Staff','Silver Fanged Panther','Gem Golem','Golden Treant']
        self.probabilities = [23.75,23.75,23.75,23.75,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.33,0.33,0.33]

class MythicalLootBox(lootbox):

    def __init__(self):
        self.items = ['Mythical Long Sword','Mythical Staff','Mythical Armor','Mythical Robe','Griffin','Sphinx','Unicorn']
        self.probabilities = [1,1,1,1,1,1,1]

class ChallengerLootBox(lootbox):

    def __init__(self):
        self.items = ['Dragon Katana','Dragon Crown','Baby Dragon','Lich Spellbook','Lich Cloak','Lich Apprentice','Tentacle Sai','Sucker Armor','Giant Squid','Giant Troll Club','Giant Troll T-Shirt',
        'Mini Troll']
        self.probabilities = [1,1,1,1,1,1,1,1,1,1,1,1]
