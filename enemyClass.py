
class Enemy:
    stats_dictionary = {'Max Health' : 5, 'Attack':2,
                        'Magic Attack':2,'Defense ':2,
                        'Magic Defense': 2, 'Attack Speed':1}
    def __init__(self, name, curHealth = stats_dictionary['Max Health']):
        self.Name = name
        self.CurrentHealth = curHealth

