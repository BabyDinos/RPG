import nextcord
from nextcord.ext import commands
import os
from sqlitedict import SqliteDict
from webserver import keep_alive
import sqlite3

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
intents.messages = True
bot = commands.Bot(intents=intents)

testServerID = int(os.environ['testServerID'])

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    sqlitedict_list = ['player.sqlite','playerorder.sqlite']
    sqlite3_list = ['matchingengine.db']
    for sqlitedict in sqlitedict_list:
      if not os.path.exists(sqlitedict):
          SqliteDict(sqlitedict)
    for database in sqlite3_list:
      connection = sqlite3.connect(database)
      c = connection.cursor()
      c.execute(f"""CREATE TABLE IF NOT EXISTS {database[:-3]} (
                ID INTEGER PRIMARY KEY,
                Item TEXT,
                Action TEXT,
                Price INTEGER,
                Quantity INTEGER
                ) """)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        print(filename[:-3] + ' has loaded')

keep_alive()
TOKEN = os.environ['TOKEN']

try:
  bot.run(TOKEN)
except:
  os.system('kill 1')
