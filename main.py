import nextcord
from nextcord.ext import commands
import os
from sqlitedict import SqliteDict
from webserver import keep_alive

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
intents.messages = True
bot = commands.Bot(intents=intents)

testServerID = int(os.environ['testServerID'])

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    if not os.path.exists('player.sqlite'):
        SqliteDict('player.sqlite')

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        # cut off the .py from the file name
        bot.load_extension(f"cogs.{filename[:-3]}")
        print(filename[:-3] + ' has loaded')

keep_alive()
TOKEN = os.environ['TOKEN']

try:
  bot.run(TOKEN)
except:
  os.system('kill 1')
