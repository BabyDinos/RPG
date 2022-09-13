from nextcord.ext import commands
import asyncio
from sqliteCommands import sqlCommands
from enemyClass import *
from playerClass import *
import nextcord
import time
from nextcord.ui import View, Button
import os

testServerID = int(os.environ['testServerID'])

class comCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.deathtime = []
        self.healtime = {}
        self.healtimer = 600

    def getPlayer(self, interaction):
        id = str(interaction.user).split('#')[-1]
        return [sqlCommands.load(id, database='player'), id]

    def enemySpawn(self, player):
        enemy_choice = random.choices(['Golem', 'Panther', 'Tree Monster'],
                                      weights=[1, 1, 1])
        if enemy_choice[0] == 'Golem':
            enemy = Golem(name='Golem', player=player)
        elif enemy_choice[0] == 'Panther':
            enemy = Panther(name='Panther', player=player)
        elif enemy_choice[0] == 'Tree Monster':
            enemy = TreeMonster(name='Treant', player=player)
        return enemy

    #cooldown time should be same as timeout time for embed
    @nextcord.slash_command(guild_ids = [testServerID], description = 'Go adventuring for loot, exp, and gold')
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def adventure(self, interaction):
        arr = self.getPlayer(interaction)
        player = arr[0]
        id = arr[1]
        if not player:
            await interaction.response.send_message('You are not registered', delete_after=20, ephemeral = True)
        elif id in self.deathtime:
            await interaction.response.send_message(
                'You are dead. You must heal before venturing again',
                delete_after=10, ephemeral = True)
        else:
            enemy = self.enemySpawn(player)
            # use to store the original dictionary
            player_total_dictionary = player.stats_dictionary.copy()
            player.stats_dictionary = {
                'Current Health': player_total_dictionary['Max Health']
            }
            player.stats_dictionary.update(player_total_dictionary)
            player.stats_dictionary.pop('Max Health')
            enemy_dictionary = enemy.stats_dictionary.copy()
            enemy.stats_dictionary = {
                'Current Health': enemy_dictionary['Max Health']
            }
            enemy.stats_dictionary.update(enemy_dictionary)
            enemy.stats_dictionary.pop('Max Health')
            turn = 1
            off_cooldown = 0

            def createEmbed(situation='\u200b'):
                embed = nextcord.Embed(color=nextcord.Color.red(),
                                       title=player.Name + ' is Adventuring <:rpg:1018640907542728747>')
                player_string = ''
                for key1, val1, val2 in zip(player.stats_dictionary.keys(),
                                            player.stats_dictionary.values(),
                                            player_total_dictionary.values()):
                    player_string += key1 + ': ' + str(val1) + '/' + str(
                        val2) + '\n'
                enemy_string = ''
                for key1, val1, val2 in zip(enemy.stats_dictionary.keys(),
                                            enemy.stats_dictionary.values(),
                                            enemy_dictionary.values()):
                    enemy_string += key1 + ': ' + str(val1) + '/' + str(
                        val2) + '\n'
                embed.add_field(name=player.Name, value=player_string)
                embed.add_field(name=enemy.Name, value=enemy_string)
                embed.add_field(name='\u200b', value=situation, inline=False)
                return embed

            async def attack_callback(interaction):
                nonlocal turn
                nonlocal off_cooldown
                enemy_decisions = random.choices([
                    'Enemy Attacked', 'Enemy Defended', 'Enemy Poweredup'
                ],
                                                 weights=[1, 1, 1])
                player_attack = player.attack()
                full_damage = player_attack['Attack'] + player_attack[
                    'Magic Attack']
                if enemy_decisions[0] == 'Enemy Attacked':
                    attackspeed_decision = player.attackSpeed(enemy)
                    if attackspeed_decision == 'Player Goes':
                        enemy.stats_dictionary[
                            'Current Health'] -= full_damage
                        situation = player.Name + ' swiftly attacks ' + enemy.Name + ' for ' + str(
                            full_damage) + ' attack'
                    else:
                        enemy_attack = enemy.enemyAttack()
                        player.stats_dictionary['Current Health'] -= sum(
                            list(enemy_attack.values()))
                        situation = enemy.Name + ' swiftly attacks ' + player.Name + ' for ' + str(
                            sum(list(enemy_attack.values()))) + ' attack'
                elif enemy_decisions[0] == 'Enemy Defended':
                    enemy_defense = enemy.enemyDefend()
                    full_defend = enemy_defense['Defense'] + enemy_defense[
                        'Magic Defense']
                    damage = player_attack['Attack'] - enemy_defense[
                        'Defense'] + player_attack[
                            'Magic Attack'] - enemy_defense['Magic Defense']
                    if (damage) > 0:
                        enemy.stats_dictionary['Current Health'] -= damage
                        situation = player.Name + ' attacks ' + enemy.Name + ' for ' + str(
                            full_damage
                        ) + ' attack, but ' + enemy.Name + ' defended for ' + str(
                            full_defend)
                    else:
                        situation = enemy.Name + ' defended all of ' + player.Name + "'s damage"
                elif enemy_decisions[0] == 'Enemy Poweredup':
                    enemy.stats_dictionary['Current Health'] -= full_damage
                    enemy.enemyPowerUp()
                    situation = player.Name + ' attacks ' + enemy.Name + ' for ' + str(
                        full_damage
                    ) + ' attack, while ' + enemy.Name + ' powers up'
                turn += 1
                if off_cooldown > turn:
                    situation += '\nSpecial Ability is On Cooldown'
                else:
                    situation += '\nSpecial Ability is Off Cooldown'
                await interaction.response.edit_message(embed=createEmbed(situation),
                                             view=myview)

            async def defend_callback(interaction):
                nonlocal turn
                nonlocal off_cooldown
                enemy_decisions = random.choices([
                    'Enemy Attacked', 'Enemy Defended', 'Enemy Poweredup'
                ],
                                                 weights=[1, 1, 1])
                player_defend = player.defend()
                player_defend = sum(list(player_defend.values()))
                if enemy_decisions[0] == 'Enemy Attacked':
                    enemy_attack = enemy.enemyAttack()
                    enemy_damage = sum(list(enemy_attack.values()))
                    if (enemy_damage - player_defend) > 0:
                        player.stats_dictionary['Current Health'] -= (
                            enemy_damage - player_defend)
                        situation = player.Name + ' defends ' + str(
                            player_defend) + ' out of ' + str(
                                enemy_damage) + ' dealt by ' + enemy.Name
                    else:
                        situation = player.Name + ' defended all the damage from ' + enemy.Name
                elif enemy_decisions[0] == 'Enemy Defended':
                    situation = 'Both ' + player.Name + ' and ' + enemy.Name + ' defended'
                elif enemy_decisions[0] == 'Enemy Poweredup':
                    enemy.enemyPowerUp()
                    situation = player.Name + ' defended, but ' + enemy.Name + ' powered up'
                turn += 1
                if off_cooldown > turn:
                    situation += '\nSpecial Ability is On Cooldown'
                else:
                    situation += '\nSpecial Ability is Off Cooldown'
                await interaction.response.edit_message(embed=createEmbed(situation),
                                             view=myview)


            async def powerup_callback(interaction):
                nonlocal turn
                nonlocal off_cooldown
                enemy_decisions = random.choices([
                    'Enemy Attacked', 'Enemy Defended', 'Enemy Poweredup'
                ],
                                                 weights=[1, 1, 1])
                player.powerUp()

                if enemy_decisions[0] == 'Enemy Attacked':
                    enemy_attack = enemy.enemyAttack()
                    player.stats_dictionary['Current Health'] -= sum(
                        list(enemy_attack.values()))
                    situation = enemy.Name + ' attacked ' + player.Name + ' for ' + str(
                        sum(list(enemy_attack.values()))
                    ) + ', while ' + player.Name + ' powered up'
                elif enemy_decisions[0] == 'Enemy Defended':
                    situation = player.Name + ' powered up while ' + enemy.Name + ' defended'
                elif enemy_decisions[0] == 'Enemy Poweredup':
                    buffs_enemy = enemy.enemyPowerUp()
                    situation = player.Name + ' and ' + enemy.Name + ' powered up'
                turn += 1
                if off_cooldown > turn:
                    situation += '\nSpecial Ability is On Cooldown'
                else:
                    situation += '\nSpecial Ability is Off Cooldown'
                await interaction.response.edit_message(embed=createEmbed(situation),
                                             view=myview)

            async def special_callback(interaction):
                nonlocal turn
                nonlocal off_cooldown
                if player.role == 'Warrior' and off_cooldown <= turn:
                    player.berSerk()
                    situation = player.Name + ' went Berserk! Their stats have increased\nSpecial Ability is off cooldown in ' + str(
                        player.berSerkCooldown) + ' turns'
                    off_cooldown = turn + player.berSerkCooldown

                elif player.role == 'Mage' and off_cooldown <= turn:
                    damage = player.fireBall()
                    enemy.stats_dictionary['Current Health'] -= damage
                    situation = player.Name + ' dealt ' + str(
                        damage
                    ) + ' magic damage to ' + enemy.Name + '\nSpecial Ability is off cooldown in ' + str(
                        player.fireBallCooldown) + ' turns'
                    off_cooldown = turn + player.fireBallCooldown

                else:
                    situation = 'Ability on Cooldown'
                await interaction.response.edit_message(embed=createEmbed(situation),
                                             view=myview)

            attackButton = Button(label = '\u200b', style=nextcord.ButtonStyle.green, emoji='⚔️')
            attackButton.callback = attack_callback
            defendButton = Button(label = '\u200b', style=nextcord.ButtonStyle.primary, emoji='🛡️')
            defendButton.callback = defend_callback
            powerUpButton = Button(label = '\u200b', style=nextcord.ButtonStyle.secondary,emoji='<:buff:1018644262532948099>')
            powerUpButton.callback = powerup_callback
            if player.role == 'Warrior':
                emoji = '<:berserker:1018644776700088410>'
            elif player.role == 'Mage':
                emoji = '<:fireball:1018645075552653322>'
            specialButton = Button(label = '\u200b', style=nextcord.ButtonStyle.red, emoji = emoji)
            specialButton.callback = special_callback
            myview = View(timeout=120)
            myview.add_item(attackButton)
            myview.add_item(defendButton)
            myview.add_item(powerUpButton)
            myview.add_item(specialButton)

            adventure_message = await interaction.response.send_message(embed=createEmbed(),
                                               view=myview, ephemeral = True)

            while enemy.stats_dictionary[
                    'Current Health'] > 0 and player.stats_dictionary[
                        'Current Health'] > 0:
                await asyncio.sleep(1)

            if enemy.stats_dictionary['Current Health'] <= 0:
                summary_embed = nextcord.Embed(title = '🏆 Player ' + player.Name + ' has defeated ' + enemy.Name + ' 🏆', description = player.Name + ' Rewards:', color=nextcord.Color.green())
                enemy_drops = enemy.mobDrop(enemy.ListOfDrops,
                                            enemy.ListOfDropWeights,
                                            dropnumber=enemy.DropNumber)
                player.inventory = addItem(player, enemy_drops[0],
                                           enemy_drops[1])
                player.CurrentHealth = player.stats_dictionary[
                    'Current Health']
                player.stats_dictionary = player_total_dictionary
                player.CurrentLevel += enemy.xpDrop()
                player.levelUp()
                for x, y in zip(enemy_drops[0], enemy_drops[1]):
                    if x == 'Gold':
                      x += ' 🪙'
                    summary_embed.add_field(name=x, value=y)
                summary_embed.add_field(name='\u200b',
                                        value=player.Name + ' gained ' +
                                        str(enemy.xpDrop()) + ' <:exp:1018668173958053888>',
                                        inline=False)
                sqlCommands.save(id, player, database='player')
                await interaction.edit_original_message(embed = summary_embed, view = View())

            elif player.stats_dictionary['Current Health'] <= 0:
                player.stats_dictionary = player_total_dictionary
                player.CurrentHealth = 0
                await interaction.edit_original_message(embed = nextcord.Embed(title = '☠️ Player ' + player.Name + ' has lost to ' +
                               enemy.Name + ' ☠️'), view = View())
                sqlCommands.save(id, player, database='player')
                self.deathtime.append(id)

    @adventure.error
    async def on_error(self, interaction, error):
        if isinstance(error, commands.CommandOnCooldown):
            await interaction.send(
                'This command is ratelimited, please try again in {:.2f}s'.
                format(error.retry_after),
                delete_after=20)
            await interaction.message.delete()
        else:
            raise error

    @commands.command()
    async def equip(self, interaction):
        arr = self.getPlayer(interaction)
        player = arr[0]
        id = arr[1]
        if not player:
            await interaction.send('You are not registered', delete_after=20)
        else:
            try:
                await interaction.send('What would you like to equip?',
                               delete_after=20)
                equipment_message = await self.bot.wait_for(
                    'message',
                    timeout=20,
                    check=lambda message: message.author == interaction.author and
                    message.channel == interaction.channel)
                if player.equip(equipment_message.content):
                    await interaction.send('Equipment changed to: ' +
                                   equipment_message.content,
                                   delete_after=20)
                else:
                    await interaction.send('Equipment not found', delete_after=20)
                sqlCommands.save(id, player, database='player')
            except:
                await interaction.send('Connection Timedout', delete_after=20)
                try:
                    await equipment_message.delete()
                except:
                    pass
        await equipment_message.delete()
        await interaction.message.delete()

    @commands.command()
    async def heal(self, interaction):
        arr = self.getPlayer(interaction)
        player = arr[0]
        id = arr[1]
        if not player:
            await interaction.send('You are not registered', delete_after=20)
        elif id in self.healtime:
            await interaction.send(
                'Heal is on coolddown. Wait {:.2f} seconds until next heal'.
                format(self.healtime[id] - time.time()),
                delete_after=10)
            await interaction.message.delete()
        else:
            if id in self.deathtime:
                self.deathtime.remove(id)
            player.CurrentHealth = player.stats_dictionary['Max Health']
            sqlCommands.save(id, player, database='player')
            await interaction.send('❤️ Player ' + player.Name +
                           ' has healed to full health ❤️',
                           delete_after=20)
            self.healtime[id] = time.time() + self.healtimer
            await interaction.message.delete()
            await asyncio.sleep(self.healtimer)
            if id in self.healtime:
                del self.healtime[id]

    @commands.command()
    async def consume(self, interaction):
        arr = self.getPlayer(interaction)
        player = arr[0]
        id = arr[1]
        if not player:
            await interaction.send('You are not registered', delete_after=20)
        else:
            try:
                await interaction.send('What would you like to consume?',
                               delete_after=20)
                consumeable_message = await self.bot.wait_for(
                    'message',
                    timeout=20,
                    check=lambda message: message.author == interaction.author and
                    message.channel == interaction.channel)
                if player.consume(consumeable_message.content):
                    await interaction.send(player.Name + ' has consumed ' +
                                   consumeable_message.content,
                                   delete_after=20)
                else:
                    await interaction.send(consumeable_message.content +
                                   ' was not found',
                                   delete_after=20)
                sqlCommands.save(id, player, database='player')
            except:
                await interaction.send('Connection Timedout', delete_after=20)
                try:
                    await consumeable_message.delete()
                except:
                    pass
                await consumeable_message.delete()
                await interaction.message.delete()


def setup(bot):
    bot.add_cog(comCommands(bot))
