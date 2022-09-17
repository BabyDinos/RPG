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

    def enemyDecision(self, weights = [1,1,1]):
        return random.choices(['Enemy Attacked', 'Enemy Defended', 'Enemy Poweredup'],weights=weights)

    def petAttack(self):
        if self.player.equipment.loc['Pet','Type'] == 'Pet:Attack':
            petattackstat = random.randint(self.equipment.loc['Pet','Stats'][0], self.equipment.loc['Pet','Stats'][1])
            petmagicattackstat = 0
        elif self.player.equipment.loc['Pet','Type'] == 'Pet:Magic Attack':
            petattackstat = 0
            petmagicattackstat = random.randint(self.equipment.loc['Pet','Stats'][0], self.equipment.loc['Pet','Stats'][1])
        else:
            petattackstat = 0
            petmagicattackstat = 0
        if petattackstat == 0 and petmagicattackstat == 0:
            return False
        else:
            context = self.player.equipment.loc['Pet','Name'] + ' aids and attacks for ' + str(petattackstat + petmagicattackstat) + ' damage\n'
        return [context, petattackstat, petmagicattackstat]

    def petDefend(self):
        if self.player.equipment.loc['Pet','Type'] == 'Pet:Defense':
            petdefensestat = random.randint(self.equipment.loc['Pet','Stats'][0], self.equipment.loc['Pet','Stats'][1])
            petmagicdefensestat = 0
        elif self.player.equipment.loc['Pet','Type'] == 'Pet:Magic Defense':
            petdefensestat = 0
            petmagicdefensestat = random.randint(self.equipment.loc['Pet','Stats'][0], self.equipment.loc['Pet','Stats'][1])
        else:
            petdefensestat = 0
            petmagicdefensestat = 0
        if petdefensestat == 0 and petmagicdefensestat == 0:
            return False
        else:
            context = self.player.equipment.loc['Pet','Name'] + ' aids and defends ' + str(petdefensestat + petmagicdefensestat) + ' damage\n'
        return [context, petdefensestat, petmagicdefensestat]

    def playerAttack(self):
        enemy_decisions = self.enemyDecision()
        player_attack = self.player.attack()
        petsummary = self.petAttack()
        full_damage = player_attack['Attack'] + player_attack['Magic Attack']
        enemy_attack = self.enemy.enemyAttack()
        enemy_full_damage = sum(list(enemy_attack.values()))

        if enemy_decisions[0] == 'Enemy Attacked':
            if self.player.stats_dictionary['Attack Speed'] > self.enemy.stats_dictionary['Attack Speed']:
                situation = self.player.Name + ' attacks first!\n'
                if petsummary:
                    full_damage += petsummary[1] + petsummary[2]
                    situation += petsummary[0] 
                self.enemy.stats_dictionary['Current Health'] -= full_damage
                if self.enemy.stats_dictionary['Current Health'] <= 0:
                    situation += self.player.Name + ' defeats ' + self.enemy.Name + ' dealing ' + str(full_damage) + ' damage'
                    return situation
                else:
                    situation += self.player.Name + ' deals ' + str(full_damage) + ' damage to ' + self.enemy.Name + '\n'
                situation += self.enemy.Name + ' attacks next!\n'
                self.player.stats_dictionary['Current Health'] -= enemy_full_damage
                if self.player.stats_dictionary['Current Health'] <= 0:
                    situation += self.enemy.Name + ' defeats ' + self.player.Name + ' with a total of ' + str(enemy_full_damage)
                    return situation
                else:
                    situation += self.enemy.Name + ' deals ' + str(enemy_full_damage) + ' damage to ' + self.player.Name

            else:
                situation = self.enemy.Name + ' attacks first!\n'
                self.player.stats_dictionary['Current Health'] -= enemy_full_damage
                if self.player.stats_dictionary['Current Health'] <= 0:
                    situation += self.enemy.Name + ' defeats ' + self.player.Name + ' dealing ' + str(enemy_full_damage) + ' damage'
                    return situation
                else:
                    situation += self.enemy.Name + ' deals ' + str(enemy_full_damage) + ' damage to ' + self.player.Name + '\n'
                situation += self.player.Name + ' attacks next!\n'
                if petsummary:
                    full_damage += petsummary[1] + petsummary[2]
                    situation += petsummary[0] 
                self.enemy.stats_dictionary['Current Health'] -= full_damage
                if self.enemy.stats_dictionary['Current Health'] <= 0:
                    situation += self.player.Name + ' defeats ' + self.enemy.Name + ' with a total of ' + str(full_damage)
                    return situation
                else:
                    situation += self.player.Name + ' deals ' + str(full_damage) + ' damage to ' + self.enemy.Name


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
        petsummary = self.petDefend()
        if enemy_decisions[0] == 'Enemy Attacked':
            enemy_attack = self.enemy.enemyAttack()
            enemy_damage = sum(list(enemy_attack.values()))
            if petsummary:
                situation += petsummary[0]
                player_defend += petsummary[1] + petsummary[2]
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


class StoneForest(Combat):
    @staticmethod
    def enemySpawn(player):
        enemy_choice = random.choices(['Golem', 'Panther', 'Tree Monster','Gem Golem','Silver Panther','Golden Treant'],
                                        weights=[33,33,33,0.33,0.33,0.33])
        if enemy_choice[0] == 'Golem':
            enemy = enemyClass.Golem(name='Golem', player=player)
        elif enemy_choice[0] == 'Panther':
            enemy = enemyClass.Panther(name='Panther', player=player)
        elif enemy_choice[0] == 'Tree Monster':
            enemy = enemyClass.TreeMonster(name='Treant', player=player)
        elif enemy_choice[0] == 'Gem Golem':
            enemy = enemyClass.TreeMonster(name='Gem Golem', player=player)
        elif enemy_choice[0] == 'Silver Panther':
            enemy = enemyClass.TreeMonster(name='Silver Panther', player=player)
        elif enemy_choice[0] == 'Golden Treant':
            enemy = enemyClass.TreeMonster(name='Golden Treant', player=player)
        return enemy

