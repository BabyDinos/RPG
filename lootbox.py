import random
from collections import Counter

class lootbox:

    def open(self, amount):
        item_result = random.choices(self.items, weights = self.probabilities, k = amount)
        itemdrops = {}
        for decisionindex in range(len(item_result)):
            name = item_result[decisionindex]
            if name in itemdrops.keys():
                itemdrops[name] += 1
            else:
                itemdrops[name] = 1

        return [itemdrops.keys(), itemdrops.values()]

class CommonLootbox(lootbox):

    def __init__(self):
        self.items = ['Gold','Meat','Hide','Bark','Stone','Stone Sword', 'Stone Staff', 'Hide Armor','Hide Robe','Bark Armor','Bark Robe','Bark Axe','Bark Wand','Panther Cub','Golemite','Twewant']
        self.probabilities = [19,19,19,19,19,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.33,0.33,0.33]

