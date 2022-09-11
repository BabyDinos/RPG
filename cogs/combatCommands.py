from nextcord.ext import commands
import asyncio
from sqliteCommands import sqlCommands
from enemyClass import *
from playerClass import *
import nextcord
import time
from nextcord.ui import View, Button


class comCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.deathtime = []
        self.healtime = {}
        self.healtimer = 120

    def playerExists(self, ctx):
        self.id = str(ctx.author).split('#')[-1]
        return [sqlCommands.load(self.id, database='player'), self.id]

    def enemySpawn(self, player):
        enemy_choice = random.choices(['Golem', 'Panther', 'Tree Monster'],
                                      weights=[1, 1, 1])
        if enemy_choice[0] == 'Golem':
            enemy = Golem(name='Golem', player=player)
        elif enemy_choice[0] == 'Panther':
            enemy = Panther(name='Panther', player=player)
        elif enemy_choice[0] == 'Tree Monster':
            enemy = TreeMonster(name='Tree Monster', player=player)
        return enemy

    #cooldown time should be same as timeout time for embed
    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def adventure(self, ctx):
        arr = self.playerExists(ctx)
        player = arr[0]
        id = arr[1]
        if not player:
            await ctx.send('You are not registered', delete_after=20)
            await ctx.message.delete()
        elif id in self.deathtime:
            await ctx.send(
                'You are dead. You must heal before venturing again',
                delete_after=10)
            await ctx.message.delete()
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
                                       title=player.Name + ' is Adventuring')
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
                if interaction.user.id == ctx.author.id:
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
                    await adventure_message.edit(embed=createEmbed(situation),
                                                 view=myview)
                    await interaction.response.defer()

            async def defend_callback(interaction):
                nonlocal turn
                nonlocal off_cooldown
                if interaction.user.id == ctx.author.id:
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
                    await adventure_message.edit(embed=createEmbed(situation),
                                                 view=myview)
                    await interaction.response.defer()

            async def powerup_callback(interaction):
                nonlocal turn
                nonlocal off_cooldown
                if interaction.user.id == ctx.author.id:
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
                    await adventure_message.edit(embed=createEmbed(situation),
                                                 view=myview)
                    await interaction.response.defer()

            async def special_callback(interaction):
                nonlocal turn
                nonlocal off_cooldown
                if interaction.user.id == ctx.author.id:
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
                    await adventure_message.edit(embed=createEmbed(situation),
                                                 view=myview)
                    await interaction.response.defer()

            attackButton = Button(label='Attack',
                                  style=nextcord.ButtonStyle.green)
            attackButton.callback = attack_callback
            defendButton = Button(label='Defend',
                                  style=nextcord.ButtonStyle.primary)
            defendButton.callback = defend_callback
            powerUpButton = Button(label='PowerUp',
                                   style=nextcord.ButtonStyle.secondary)
            powerUpButton.callback = powerup_callback
            specialButton = Button(label='Special Ability',
                                   style=nextcord.ButtonStyle.red)
            specialButton.callback = special_callback
            myview = View(timeout=120)
            myview.add_item(attackButton)
            myview.add_item(defendButton)
            myview.add_item(powerUpButton)
            myview.add_item(specialButton)

            adventure_message = await ctx.send(embed=createEmbed(),
                                               view=myview)

            while enemy.stats_dictionary[
                    'Current Health'] > 0 and player.stats_dictionary[
                        'Current Health'] > 0:
                await asyncio.sleep(2)

            if enemy.stats_dictionary['Current Health'] <= 0:
                await ctx.send('Player ' + player.Name + ' has defeated ' +
                               enemy.Name,
                               delete_after=20)
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
                summary_embed = nextcord.Embed(title=player.Name + ' Rewards',
                                               color=nextcord.Color.green())
                for x, y in zip(enemy_drops[0], enemy_drops[1]):
                    summary_embed.add_field(name=x, value=y)
                summary_embed.add_field(name='\u200b',
                                        value=player.Name + ' gained ' +
                                        str(enemy.xpDrop()) + ' XP',
                                        inline=False)
                sqlCommands.save(id, player, database='player')
                await ctx.send(embed=summary_embed, delete_after=20)

            elif player.stats_dictionary['Current Health'] <= 0:
                player.stats_dictionary = player_total_dictionary
                player.CurrentHealth = 0
                await ctx.send('Player ' + player.Name + ' has lost to ' +
                               enemy.Name,
                               delete_after=20)
                sqlCommands.save(id, player, database='player')
                self.deathtime.append(id)

            await ctx.message.delete()
            await adventure_message.delete()

    @adventure.error
    async def on_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                'This command is ratelimited, please try again in {:.2f}s'.
                format(error.retry_after),
                delete_after=20)
            await ctx.message.delete()
        else:
            raise error

    @commands.command()
    async def equip(self, ctx):
        arr = self.playerExists(ctx)
        player = arr[0]
        id = arr[1]
        if not player:
            await ctx.send('You are not registered', delete_after=20)
        else:
            try:
                await ctx.send('What would you like to equip?',
                               delete_after=20)
                equipment_message = await self.bot.wait_for(
                    'message',
                    timeout=20,
                    check=lambda message: message.author == ctx.author and
                    message.channel == ctx.channel)
                if player.equip(equipment_message.content):
                    await ctx.send('Equipment changed to: ' +
                                   equipment_message.content,
                                   delete_after=20)
                else:
                    await ctx.send('Equipment not found', delete_after=20)
                sqlCommands.save(id, player, database='player')
            except:
                await ctx.send('Connection Timedout', delete_after=20)
                try:
                    await equipment_message.delete()
                except:
                    pass
        await equipment_message.delete()
        await ctx.message.delete()

    @commands.command()
    async def heal(self, ctx):
        arr = self.playerExists(ctx)
        player = arr[0]
        id = arr[1]
        if not player:
            await ctx.send('You are not registered', delete_after=20)
        elif id in self.healtime:
            await ctx.send(
                'Heal is on coolddown. Wait {:.2f} seconds until next heal'.
                format(self.healtime[id] - time.time()),
                delete_after=10)
            await ctx.message.delete()
        else:
            if id in self.deathtime:
                self.deathtime.remove(id)
            player.CurrentHealth = player.stats_dictionary['Max Health']
            sqlCommands.save(id, player, database='player')
            await ctx.send('Player ' + player.Name +
                           ' has healed to full health',
                           delete_after=20)
            self.healtime[id] = time.time() + self.healtimer
            await ctx.message.delete()
            await asyncio.sleep(self.healtimer)
            if id in self.healtime:
                del self.healtime[id]

    @commands.command()
    async def consume(self, ctx):
        arr = self.playerExists(ctx)
        player = arr[0]
        id = arr[1]
        if not player:
            await ctx.send('You are not registered', delete_after=20)
        else:
            try:
                await ctx.send('What would you like to consume?',
                               delete_after=20)
                consumeable_message = await self.bot.wait_for(
                    'message',
                    timeout=20,
                    check=lambda message: message.author == ctx.author and
                    message.channel == ctx.channel)
                if player.consume(consumeable_message.content):
                    await ctx.send(player.Name + ' has consumed ' +
                                   consumeable_message.content,
                                   delete_after=20)
                else:
                    await ctx.send(consumeable_message.content +
                                   ' was not found',
                                   delete_after=20)
                sqlCommands.save(id, player, database='player')
            except:
                await ctx.send('Connection Timedout', delete_after=20)
                try:
                    await consumeable_message.delete()
                except:
                    pass
                await consumeable_message.delete()
                await ctx.message.delete()


def setup(bot):
    bot.add_cog(comCommands(bot))
