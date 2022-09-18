from nextcord.ext import commands
import asyncio
from sqliteCommands import sqlCommands
import combatClass
import nextcord
from nextcord import Interaction
import time
from nextcord.ui import View, Button
import os

testServerID = int(os.environ['testServerID'])


class comCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.healtime = {}
        self.deathtime = []
        self.healtimer = 600
        self.bosstimer = 1800
        self.bosstime = {}
        self.adventuretime = {}
        self.adventuretimer = 30

    def getPlayer(self, interaction):
        id = str(interaction.user).split('#')[-1]
        return [sqlCommands.load(id, database='player'), id]

    #cooldown time should be same as timeout time for embed
    @nextcord.slash_command(guild_ids = [testServerID], description = 'Go adventuring for loot, exp, and gold')
    async def adventure(self):
        pass

    @adventure.subcommand(description = 'Adventure through the Stone Forest')
    async def stoneforest(self, interaction:Interaction):
        arr = self.getPlayer(interaction)
        player = arr[0]
        id = arr[1]
        if not player:
            await interaction.response.send_message('You are not registered', ephemeral = True)
        elif id in self.deathtime:
            await interaction.response.send_message(
                'You are dead. You must heal before venturing again',
                delete_after=10, ephemeral = True)
        elif id in self.adventuretime:
            await interaction.response.send_message(
                "You're tired after your adventure. Please wait {:.2f} seconds until you can adventure again".
                format(self.adventuretime[id] - time.time()),
                ephemeral = True)
        else:
            enemy = combatClass.StoneForest.enemySpawn(player)
            combat = combatClass.StoneForest(player, enemy, id)
            async def attack_callback(interaction):
                situation = combat.playerAttack()
                await interaction.response.edit_message(embed=combat.createEmbed(situation),view=myview)
            async def defend_callback(interaction):
                situation = combat.playerDefend()
                await interaction.response.edit_message(embed=combat.createEmbed(situation),view=myview)
            async def powerup_callback(interaction):
                situation = combat.playerPowerUp()
                await interaction.response.edit_message(embed=combat.createEmbed(situation),view=myview)
            async def special_callback(interaction):
                situation = combat.playerSpecial()
                await interaction.response.edit_message(embed=combat.createEmbed(situation),view=myview)

            attackButton = Button(label = '\u200b', style=nextcord.ButtonStyle.green, emoji='⚔️')
            attackButton.callback = attack_callback
            defendButton = Button(label = '\u200b', style=nextcord.ButtonStyle.primary, emoji='🛡️')
            defendButton.callback = defend_callback
            powerUpButton = Button(label = '\u200b', style=nextcord.ButtonStyle.secondary,emoji='<:buff:1018644262532948099>')
            powerUpButton.callback = powerup_callback
            if player.role == 'Warrior': emoji = '<:berserker:1018644776700088410>'
            elif player.role == 'Mage': emoji = '<:fireball:1018645075552653322>'
            specialButton = Button(label = '\u200b', style=nextcord.ButtonStyle.red, emoji = emoji)
            specialButton.callback = special_callback
            myview = View(timeout=120)
            myview.add_item(attackButton)
            myview.add_item(defendButton)
            myview.add_item(powerUpButton)
            myview.add_item(specialButton)

            await interaction.response.send_message(embed=combat.createEmbed(),view=myview, ephemeral = True)

            while combat.enemy.stats_dictionary['Current Health'] > 0 and combat.player.stats_dictionary['Current Health'] > 0:
                await asyncio.sleep(1)

            if combat.enemy.stats_dictionary['Current Health'] <= 0:
                summary_player = combat.playerWon()
                await interaction.edit_original_message(embed = summary_player, view = View())
                self.adventuretime[id] = time.time() + self.adventuretimer
                await asyncio.sleep(self.adventuretimer)
                if id in self.adventuretime:
                    del self.adventuretime[id]
                return
            elif combat.player.stats_dictionary['Current Health'] <= 0:
                summary_player = combat.playerLost()
                await interaction.edit_original_message(embed = summary_player, view = View())
                self.deathtime.append(id)
                self.adventuretime[id] = time.time() + self.adventuretimer
                await asyncio.sleep(self.adventuretimer)
                if id in self.adventuretime:
                    del self.adventuretime[id]
                return

    @adventure.subcommand(description = 'Challenge a Boss for more extravagant loot')
    async def bossarena(self, interaction:Interaction):
        arr = self.getPlayer(interaction)
        player = arr[0]
        id = arr[1]
        if not player:
            await interaction.response.send_message('You are not registered', ephemeral = True)
        elif id in self.deathtime:
            await interaction.response.send_message(
                'You are dead. You must heal before venturing again',
                delete_after=10, ephemeral = True)
        elif id in self.bosstime:
            await interaction.response.send_message(
                "You need to wait before challenging a boss again. Please wait {:.2f} seconds until you can challenge again".
                format(self.bosstime[id] - time.time()),
                ephemeral = True)
        else:
            enemy = combatClass.BossArena.enemySpawn(player)
            if enemy.Name == 'Dragon':
                combat = combatClass.Dragon(player, enemy, id) 
            elif enemy.Name == 'Lich':
                combat = combatClass.Lich(player, enemy, id)

            async def attack_callback(interaction):
                situation = combat.playerAttack()
                await interaction.response.edit_message(embed=combat.createEmbed(situation),view=myview)
            async def defend_callback(interaction):
                situation = combat.playerDefend()
                await interaction.response.edit_message(embed=combat.createEmbed(situation),view=myview)
            async def powerup_callback(interaction):
                situation = combat.playerPowerUp()
                await interaction.response.edit_message(embed=combat.createEmbed(situation),view=myview)
            async def special_callback(interaction):
                situation = combat.playerSpecial()
                await interaction.response.edit_message(embed=combat.createEmbed(situation),view=myview)

            attackButton = Button(label = '\u200b', style=nextcord.ButtonStyle.green, emoji='⚔️')
            attackButton.callback = attack_callback
            defendButton = Button(label = '\u200b', style=nextcord.ButtonStyle.primary, emoji='🛡️')
            defendButton.callback = defend_callback
            powerUpButton = Button(label = '\u200b', style=nextcord.ButtonStyle.secondary,emoji='<:buff:1018644262532948099>')
            powerUpButton.callback = powerup_callback
            if player.role == 'Warrior': emoji = '<:berserker:1018644776700088410>'
            elif player.role == 'Mage': emoji = '<:fireball:1018645075552653322>'
            specialButton = Button(label = '\u200b', style=nextcord.ButtonStyle.red, emoji = emoji)
            specialButton.callback = special_callback
            myview = View(timeout=120)
            myview.add_item(attackButton)
            myview.add_item(defendButton)
            myview.add_item(powerUpButton)
            myview.add_item(specialButton)

            await interaction.response.send_message(embed=combat.createEmbed(),view=myview, ephemeral = True)

            while combat.enemy.stats_dictionary['Current Health'] > 0 and combat.player.stats_dictionary['Current Health'] > 0:
                await asyncio.sleep(1)

            if combat.enemy.stats_dictionary['Current Health'] <= 0:
                summary_player = combat.playerWon()
                await interaction.edit_original_message(embed = summary_player, view = View())
                self.bosstime[id] = time.time() + self.bosstimer
                await asyncio.sleep(self.bosstimer)
                if id in self.bosstime:
                    del self.bosstime[id]
                return
            elif combat.player.stats_dictionary['Current Health'] <= 0:
                summary_player = combat.playerLost()
                await interaction.edit_original_message(embed = summary_player, view = View())
                self.deathtime.append(id)
                self.bosstime[id] = time.time() + self.bosstimer
                await asyncio.sleep(self.bosstimer)
                if id in self.bosstime:
                    del self.bosstime[id]
                return

    @nextcord.slash_command(guild_ids = [testServerID], description = 'Equip armor, weapon, or pet')
    async def equip(self, interaction:Interaction, equipment:str):
        arr = self.getPlayer(interaction)
        player = arr[0]
        id = arr[1]
        if not player:
            await interaction.response.send_message('You are not registered', ephemeral = True)
        else:
            if player.equip(equipment):
                await interaction.response.send_message('Equipment changed to: ' +
                               equipment, ephemeral = True)
            else:
                await interaction.response.send_message('Equipment not found', ephemeral = True)
            sqlCommands.save(id, player, database='player')

    @nextcord.slash_command(guild_ids = [testServerID], description = 'Heal your player to full health')
    async def heal(self, interaction):
        arr = self.getPlayer(interaction)
        player = arr[0]
        id = arr[1]
        if not player:
            await interaction.response.send_message('You are not registered', ephemeral = True)
        elif id in self.healtime:
            await interaction.response.send_message(
                'Heal is on coolddown. Wait {:.2f} seconds until next heal'.
                format(self.healtime[id] - time.time()),
                ephemeral = True)
        else:
            if id in self.deathtime:
                self.deathtime.remove(id)
            if id in self.adventuretime:
                del self.adventuretime[id]
            player.CurrentHealth = player.stats_dictionary['Max Health']
            sqlCommands.save(id, player, database='player')
            await interaction.response.send_message('❤️ Player ' + player.Name +
                           ' has healed to full health ❤️',
                           ephemeral = True)
            self.healtime[id] = time.time() + self.healtimer
            await asyncio.sleep(self.healtimer)
            if id in self.healtime:
                del self.healtime[id]

    @nextcord.slash_command(guild_ids = [testServerID], description = 'Eat type consumeables to restore health')
    async def consume(self, interaction, consumeable:str):
        arr = self.getPlayer(interaction)
        player = arr[0]
        id = arr[1]
        if not player:
            await interaction.response.send_message('You are not registered', ephemeral= True)
        else:
            if player.consume(consumeable):
                await interaction.response.send_message(player.Name + ' has consumed ' +
                                consumeable, ephemeral = True)
            else:
                await interaction.response.send_message(consumeable +
                                ' was not found',
                                ephemeral = True)
            sqlCommands.save(id, player, database='player')

def setup(bot):
    bot.add_cog(comCommands(bot))
