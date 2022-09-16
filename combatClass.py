import playerClass
import enemyClass
import random
import nextcord
import sqliteCommands

class Combat:

    def __init__(self, player, enemy, id):
        self.id = id
        self.player = player
        self.enemy = enemy
        self.turn = 1
        self.off_cooldown = 0

        # Put Current Health as first item, and so I can display info as combat progresses
        self.player_total_dictionary = player.stats_dictionary.copy()
        self.player.stats_dictionary = {'Current Health': self.player_total_dictionary['Max Health']}
        self.player.stats_dictionary.update(self.player_total_dictionary)
        self.player.stats_dictionary.pop('Max Health')

        # Put Current Health as first item, and so I can display info as combat progresses
        self.enemy_total_dictionary = enemy.stats_dictionary.copy()
        self.enemy.stats_dictionary = {'Current Health': self.enemy_total_dictionary['Max Health']}
        self.enemy.stats_dictionary.update(self.enemy_total_dictionary)
        self.enemy.stats_dictionary.pop('Max Health')

    def createEmbed(self, situation = '\u200b'):
        embed = nextcord.Embed(color=nextcord.Color.red(),
                                title=self.player.Name + ' is Adventuring <:rpg:1018640907542728747>')
        player_string = ''
        for key1, val1, val2 in zip(self.player.stats_dictionary.keys(),
                                    self.player.stats_dictionary.values(),
                                    self.player_total_dictionary.values()):
            player_string += key1 + ': ' + str(val1) + '/' + str(val2) + '\n'
        enemy_string = ''
        for key1, val1, val2 in zip(self.enemy.stats_dictionary.keys(),
                                    self.enemy.stats_dictionary.values(),
                                    self.enemy_total_dictionary.values()):
            enemy_string += key1 + ': ' + str(val1) + '/' + str(val2) + '\n'
        embed.add_field(name=self.player.Name, value=player_string)
        embed.add_field(name=self.enemy.Name, value=enemy_string)
        embed.add_field(name='\u200b', value=situation, inline=False)
        return embed

    @staticmethod
    def enemySpawn(player):
        enemy_choice = random.choices(['Golem', 'Panther', 'Tree Monster'],
                                        weights=[1, 1, 1])
        if enemy_choice[0] == 'Golem':
            enemy = enemyClass.Golem(name='Golem', player=player)
        elif enemy_choice[0] == 'Panther':
            enemy = enemyClass.Panther(name='Panther', player=player)
        elif enemy_choice[0] == 'Tree Monster':
            enemy = enemyClass.TreeMonster(name='Treant', player=player)
        return enemy

    def enemyDecision(self, weights = [1,1,1]):
        return random.choices(['Enemy Attacked', 'Enemy Defended', 'Enemy Poweredup'],weights=weights)

    def playerAttack(self):
        enemy_decisions = self.enemyDecision()
        player_attack = self.player.attack()
        full_damage = player_attack['Attack'] + player_attack['Magic Attack']
        if enemy_decisions[0] == 'Enemy Attacked':
            attackspeed_decision = self.player.attackSpeed(self.enemy)
            if attackspeed_decision == 'Player Goes':
                self.enemy.stats_dictionary['Current Health'] -= full_damage
                situation = self.player.Name + ' swiftly attacks ' + self.enemy.Name + ' for ' + str(full_damage) + ' attack'
            else:
                enemy_attack = self.enemy.enemyAttack()
                enemy_full_damage = sum(list(enemy_attack.values()))
                self.player.stats_dictionary['Current Health'] -= enemy_full_damage
                situation = self.enemy.Name + ' swiftly attacks ' + self.player.Name + ' for ' + str(enemy_full_damage) + ' attack'
        elif enemy_decisions[0] == 'Enemy Defended':
            enemy_defense = self.enemy.enemyDefend()
            full_defend = enemy_defense['Defense'] + enemy_defense['Magic Defense']
            damage = player_attack['Attack'] - enemy_defense['Defense'] + player_attack['Magic Attack'] - enemy_defense['Magic Defense']
            if damage > 0:
                self.enemy.stats_dictionary['Current Health'] -= damage
                situation = self.player.Name + ' attacks ' + self.enemy.Name + ' for ' + str(full_damage) + ' attack, but ' + self.enemy.Name + ' defended for ' + str(full_defend)
            else:
                situation = self.enemy.Name + ' defended all of ' + self.player.Name + "'s damage"
        elif enemy_decisions[0] == 'Enemy Poweredup':
            self.enemy.stats_dictionary['Current Health'] -= full_damage
            self.enemy.enemyPowerUp()
            situation = self.player.Name + ' attacks ' + self.enemy.Name + ' for ' + str(
                full_damage
            ) + ' attack, while ' + self.enemy.Name + ' powers up'
        self.turn += 1
        if self.off_cooldown > self.turn:
            situation += '\nSpecial Ability is On Cooldown'
        else:
            situation += '\nSpecial Ability is Off Cooldown'
        return situation

    def playerDefend(self):
        enemy_decisions = self.enemyDecision()
        player_defend = self.player.defend()
        player_defend = sum(list(player_defend.values()))
        if enemy_decisions[0] == 'Enemy Attacked':
            enemy_attack = self.enemy.enemyAttack()
            enemy_damage = sum(list(enemy_attack.values()))
            if (enemy_damage - player_defend) > 0:
                self.player.stats_dictionary['Current Health'] -= (enemy_damage - player_defend)
                situation = self.player.Name + ' defends ' + str(player_defend) + ' out of ' + str(enemy_damage) + ' dealt by ' + self.enemy.Name
            else:
                situation = self.player.Name + ' defended all the damage from ' + self.enemy.Name
        elif enemy_decisions[0] == 'Enemy Defended':
            situation = 'Both ' + self.player.Name + ' and ' + self.enemy.Name + ' defended'
        elif enemy_decisions[0] == 'Enemy Poweredup':
            self.enemy.enemyPowerUp()
            situation = self.player.Name + ' defended, but ' + self.enemy.Name + ' powered up'
        self.turn += 1
        if self.off_cooldown > self.turn:
            situation += '\nSpecial Ability is On Cooldown'
        else:
            situation += '\nSpecial Ability is Off Cooldown'
        return situation

    def playerPowerUp(self):
        enemy_decisions = self.enemyDecision()
        self.player.powerUp()
        if enemy_decisions[0] == 'Enemy Attacked':
            enemy_attack = self.enemy.enemyAttack()
            enemy_full_damage = sum(list(enemy_attack.values()))
            self.player.stats_dictionary['Current Health'] -= enemy_full_damage
            situation = self.enemy.Name + ' attacked ' + self.player.Name + ' for ' + str(enemy_full_damage) + ', while ' + self.player.Name + ' powered up'
        elif enemy_decisions[0] == 'Enemy Defended':
            situation = self.player.Name + ' powered up while ' + self.enemy.Name + ' defended'
        elif enemy_decisions[0] == 'Enemy Poweredup':
            buffs_enemy = self.enemy.enemyPowerUp()
            situation = self.player.Name + ' and ' + self.enemy.Name + ' powered up'
        self.turn += 1
        if self.off_cooldown > self.turn:
            situation += '\nSpecial Ability is On Cooldown'
        else:
            situation += '\nSpecial Ability is Off Cooldown'
        return situation

    def playerSpecial(self):
        if self.player.role == 'Warrior' and self.off_cooldown <= self.turn:
            self.player.berSerk()
            situation = self.player.Name + ' went Berserk! Their stats have increased\nSpecial Ability is off cooldown in ' + str(self.player.berSerkCooldown) + ' turns'
            self.off_cooldown = self.turn + self.player.berSerkCooldown

        elif self.player.role == 'Mage' and self.off_cooldown <= self.turn:
            damage = self.player.fireBall()
            self.enemy.stats_dictionary['Current Health'] -= damage
            situation = self.player.Name + ' dealt ' + str(damage) + ' magic damage to ' + self.enemy.Name + '\nSpecial Ability is off cooldown in ' + str(self.player.fireBallCooldown) + ' turns'
            self.off_cooldown = self.turn + self.player.fireBallCooldown
        else:
            situation = 'Ability on Cooldown'
        return situation

    def playerWon(self):
        summary_embed = nextcord.Embed(title = '🏆 Player ' + self.player.Name + ' has defeated ' + self.enemy.Name + ' 🏆', description = self.player.Name + 
            ' Rewards:', color=nextcord.Color.green())
        enemy_drops = self.enemy.mobDrop(self.enemy.ListOfDrops,
                                    self.enemy.ListOfDropWeights,
                                    dropnumber=self.enemy.DropNumber)
        self.player.inventory = playerClass.Player.updateItem(self.player, enemy_drops[0], enemy_drops[1])
        self.player.CurrentHealth = self.player.stats_dictionary['Current Health']
        self.player.stats_dictionary = self.player_total_dictionary
        self.player.CurrentEXP += self.enemy.xpDrop()
        self.player.levelUp()
        for x, y in zip(enemy_drops[0], enemy_drops[1]):
            if x == 'Gold':
                x += ' 🪙'
            summary_embed.add_field(name=x, value=y)
        summary_embed.add_field(name='\u200b',value= self.player.Name + ' gained ' + str(self.enemy.xpDrop()) + ' <:exp:1018668173958053888>',inline=False)
        sqliteCommands.sqlCommands.save(self.id, self.player, database='player')
        return summary_embed

    def playerLost(self):
        self.player.stats_dictionary = self.player_total_dictionary
        self.player.CurrentHealth = 0
        summary_embed = nextcord.Embed(title = '☠️ Player ' + self.player.Name + ' has lost to ' + self.enemy.Name + ' ☠️')
        sqliteCommands.sqlCommands.save(self.id, self.player, database='player')
        return summary_embed



