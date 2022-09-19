import os
from nextcord.ext import commands

testServerID = int(os.environ['testServerID'])

class excCommands(commands.Cog):
    pass

def setup(bot):
    bot.add_cog(excCommands(bot))