from nextcord.ext import commands
import asyncio
import aiosqlite
from sqlitedict import SqliteDict
from sqliteCommands import sqlCommands
from enemyClass import *
from playerClass import *
import nextcord
import time
from nextcord.ui import View, Button

class comCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.fighttime = {}

    
    #cooldown time should be same as timeout time for embed
    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def fight(self, ctx):
        self.id = str(ctx.author).split('#')[-1]
        player = sqlCommands.load(self.id, database = 'player')
        if not player:
            await ctx.send('You are not registered', delete_after = 20)
        if self.id in self.fighttime:
            await ctx.send('You are dead. Wait {:.2f} seconds until respawn'.format(self.fighttime[self.id]-time.time()), delete_after = 10)
        else:
            enemy = Golem('Golem',[1,5],[1,50],[2,5],[1,2],[2,5],[1,2],2, 2, 2)
            self.deathtimer = 120
            # use to store the original dictionary
            player_total_dictionary = player.stats_dictionary.copy()
            player.stats_dictionary = {'Current Health': player_total_dictionary['Max Health']}
            player.stats_dictionary.update(player_total_dictionary)
            player.stats_dictionary.pop('Max Health')
            enemy_dictionary = vars(enemy).copy()

            def createEmbed():
                embed = nextcord.Embed(color = nextcord.Color.red(), title = player.Name + ' is Adventuring')
                player_string = ''
                for key1,val1, val2 in zip(player.stats_dictionary.keys(), player.stats_dictionary.values(), player_total_dictionary.values()):
                    player_string += key1 + ': ' + str(val1) + '/' + str(val2) + '\n' 
                enemy_string = ''
                for key1, val1, val2 in zip(vars(enemy).keys(), vars(enemy).values(), enemy_dictionary.values()):
                    if key1 == 'Name':
                        continue
                    enemy_string += key1 + ': ' + str(val1) + '/' + str(val2) + '\n' 
                embed.add_field(name = player.Name, value = player_string)
                embed.add_field(name = enemy.Name, value = enemy_string)
                return embed
            
            async def attack_callback(interaction):
                enemy_decisions = random.choices(['Enemy Attacked','Enemy Defended','Enemy Poweredup'], weights= [1, 1, 1])
                player_attack = player.attack()
                match enemy_decisions[0]:
                    case 'Enemy Attacked':
                        attackspeed_decision = player.attackSpeed(enemy)
                        await ctx.send(attackspeed_decision, delete_after = 20)
                        if attackspeed_decision == 'Player Goes':
                            enemy.CurrentHealth -= player_attack
                            await ctx.send('Player ' + player.Name + ' attacked faster than ' + enemy.Name + ', hitting '+ enemy.Name + ' for ' + str(player_attack), delete_after = 20)
                        else:
                            enemy_attack = enemy.enemyAttack()
                            player.CurrentHealth -= list(enemy_attack.values())[0]
                            await ctx.send(enemy.Name + ' attacked faster than ' + player.Name + ', hitting ' + player.Name + ' for ' + str(list(enemy_attack.values())[0]), delete_after = 20)
                    case 'Enemy Defended':
                        enemy_defense = enemy.enemyDefend()['Defense']
                        if (player_attack - enemy_defense) > 0:
                            enemy.CurrentHealth -= (player_attack - enemy_defense)
                            await ctx.send('Player ' + player.Name + ' hit ' + enemy.Name + ' for' + str(player_attack - enemy_defense), delete_after = 20)
                        else:
                            await ctx.send('Player ' + player.Name + ' hit ' + enemy.Name + ' for 0 attack', delete_after = 20)
                    case 'Enemy Poweredup':
                        enemy.CurrentHealth -= player_attack
                        buffs = enemy.enemyPowerUp()
                        await ctx.send('Player ' + player.Name + ' hit ' + enemy.Name + ' for ' + str(player_attack), delete_after = 20)
                        await ctx.send(enemy.Name + ' powered up, increasing its attack by ' + str(buffs[0]) + ' and magic attack by ' + str(buffs[1]), delete_after = 20)

                await adventure_message.edit(embed = createEmbed(), view = myview)
                await interaction.response.defer()
                
            async def magicattack_callback(interaction):
                enemy_decisions = random.choices(['Enemy Attacked','Enemy Defended','Enemy Poweredup'], weights= [1, 1, 1])
                player_attack = player.magicAttack()
                match enemy_decisions[0]:
                    case 'Enemy Attacked':
                        attackspeed_decision = player.attackSpeed(enemy)
                        if attackspeed_decision == 'Player Goes':
                            enemy.CurrentHealth -= player_attack
                            await ctx.send('Player ' + player.Name + ' attacked faster than ' + enemy.Name + ', hitting ' + enemy.Name + ' for ' + str(player_attack), delete_after = 20)
                        else:
                            enemy_attack = enemy.enemyAttack()
                            player.CurrentHealth -= list(enemy_attack.values())[0]
                            await ctx.send(enemy.Name + ' attacked faster than ' + player.Name + ', hitting ' + player.Name + ' for ' + str(list(enemy_attack.values())[0]), delete_after = 20)
                    case 'Enemy Defended':
                        enemy_defense = enemy.enemyDefend()['Magic Defense']
                        if (player_attack - enemy_defense) > 0:
                            enemy.CurrentHealth -= (player_attack - enemy_defense)
                            await ctx.send('Player ' + player.Name + ' hit ' + enemy.Name + ' for' + str(player_attack - enemy_defense), delete_after = 20)
                        else:
                            await ctx.send('Player ' + player.Name + ' hit ' + enemy.Name + ' for 0 magic attack', delete_after = 20)
                    case 'Enemy Poweredup':
                        enemy.CurrentHealth -= player_attack
                        buffs = enemy.enemyPowerUp()
                        await ctx.send('Player ' + player.Name + ' hit ' + enemy.Name + ' for ' + str(player_attack), delete_after = 20)
                        await ctx.send(enemy.Name + 'powered up, increasing its attack by' + str(buffs[0]) + ' and magic attack by ' + str(buffs[1]), delete_after = 20)

                await adventure_message.edit(embed = createEmbed(), view = myview)
                await interaction.response.defer()

            async def defend_callback(interaction):
                enemy_decisions = random.choices(['Enemy Attacked','Enemy Defended','Enemy Poweredup'], weights= [1, 1, 1])
                player_defend = player.defend()
                match enemy_decisions[0]:
                    case 'Enemy Attacked':
                        enemy_attack = enemy.enemyAttack()
                        if 'Attack' in enemy_attack.keys():
                            if (enemy_attack['Attack'] - player_defend['Defense']) > 0:
                                player.CurrentHealth -= (enemy_attack['Attack'] - player_defend['Defense'])
                                await ctx.send(player.Name + ' defended ' + str(player_defend['Defense']) + ' attack damage, but took ' + str(enemy_attack['Attack'] - player_defend['Defense']), delete_after = 20)
                            else:
                                await ctx.send(player.Name + ' defended all the damage from ' + enemy.Name, delete_after = 20)
                        else:
                            if (enemy_attack['Magic Attack'] - player_defend['Magic Defense']) > 0:
                                player.CurrentHealth -= (enemy_attack['Magic Attack'] - player_defend['Magic Defense'])
                                await ctx.send(player.Name + ' defended ' + str(player_defend['Magic Defense']) + ' magic damage, but took ' + str(enemy_attack['Magic Attack'] - player_defend['Magic Defense']), delete_after = 20)
                            else:
                                await ctx.send(player.Name + ' defended all the damage from ' + enemy.Name, delete_after = 20)
                    case 'Enemy Defended':
                        await ctx.send('Player ' + player.Name + ' and ' + enemy.Name + ' both defended', delete_after = 20)
                        pass
                    case 'Enemy Poweredup':
                        buffs = enemy.enemyPowerUp()
                        await ctx.send('Player ' + player.Name + ' defended', delete_after = 20)
                        await ctx.send('But '+ enemy.Name + " powered up, increasing its attack by " + str(buffs[0]) + ' and magic attack by ' + str(buffs[1]), delete_after = 20)
                await adventure_message.edit(embed = createEmbed(), view = myview)
                await interaction.response.defer()
            
            async def powerup_callback(interaction):
                enemy_decisions = random.choices(['Enemy Attacked','Enemy Defended','Enemy Poweredup'], weights= [1, 1, 1])
                buffs = player.powerUp()

                match enemy_decisions[0]:
                    case 'Enemy Attacked':
                        player.CurrentHealth -= list(enemy.enemyAttack().values())[0]
                        await ctx.send(enemy.Name + ' hit Player ' + player.Name + ' for ' + str(list(enemy.enemyAttack().values())[0]))
                    case 'Enemy Defended':
                        await ctx.send(enemy.Name + ' defended', delete_after = 20)
                    case 'Enemy Poweredup':
                        buffs_enemy = enemy.enemyPowerUp()
                        await ctx.send(enemy.Name + ' gained ' + str(buffs_enemy[0]) + ' attack and ' + str(buffs_enemy[1]), delete_after = 20)

                await ctx.send(player.Name + ' gained ' + str(buffs[0]) + ' attack and ' + str(buffs[1]) + ' magic attack', delete_after = 20)
                await adventure_message.edit(embed = createEmbed(), view = myview)
                await interaction.response.defer()
            
            attackButton = Button(label = 'A', style = nextcord.ButtonStyle.red)
            attackButton.callback = attack_callback
            magicAttackButton = Button(label = 'M', style = nextcord.ButtonStyle.blurple)
            magicAttackButton.callback = magicattack_callback
            defendButton = Button(label = 'D', style = nextcord.ButtonStyle.gray)
            defendButton.callback = defend_callback
            powerUpButton = Button(label = 'P', style = nextcord.ButtonStyle.green)
            powerUpButton.callback = powerup_callback
            myview = View(timeout = 120)
            myview.add_item(attackButton)
            myview.add_item(magicAttackButton)
            myview.add_item(defendButton)
            myview.add_item(powerUpButton)

            adventure_message = await ctx.send(embed = createEmbed(), view = myview) 

            while enemy.CurrentHealth > 0 and player.CurrentHealth > 0:
                await asyncio.sleep(2)

            if enemy.CurrentHealth <= 0:
                await ctx.send('Player ' + player.Name + ' has defeated ' + enemy.Name, delete_after = 20)
            if player.CurrentHealth <= 0:
                await ctx.send('Player ' + player.Name + ' has lost to ' + enemy.Name, delete_after = 20)
                self.fighttime[self.id] = time.time() + self.deathtimer
            await ctx.message.delete()
            await adventure_message.delete()
            await asyncio.sleep(self.deathtimer)
            if self.id in self.fighttime:
                del self.fighttime[self.id]
            player.stats_dictionary = player_total_dictionary
            player.CurrentHealth = player.stats_dictionary['Max Health']
            sqlCommands.save(self.id, player, database='player')


    @fight.error
    async def on_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after), delete_after = 20)
        else:
            raise error

    @commands.command()
    async def equip(self, ctx):
        self.id = str(ctx.author).split('#')[-1]
        player = sqlCommands.load(self.id, database = 'player')
        if not player:
            await ctx.send('You are not registered', delete_after = 20)
        else:
            try:
                await ctx.send('What would you like to equip?', delete_after = 20)
                equipment_message = await self.bot.wait_for('message', timeout = 20, check= lambda message: message.author == ctx.author and message.channel == ctx.channel)
                if player.equip(equipment_message.content):
                    await ctx.send('Equipment changed to: ' + equipment_message.content, delete_after = 20)
                else:
                    await ctx.send('Equipment not found', delete_after = 20)
                sqlCommands.save(self.id, player, database = 'player')
            except:
                print('Connection Timedout', delete_after = 20)
                try:
                    await equipment_message.delete()
                except:
                    pass
        await equipment_message.delete()
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(comCommands(bot))
