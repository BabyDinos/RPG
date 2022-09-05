from discord.ext import commands
import asyncio
import aiosqlite
from sqlitedict import SqliteDict

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def register(self, ctx):
        await ctx.send('What is your Username?')
        try:
            self.message = await self.bot.wait_for('message', timeout = 30, check= lambda message: message.author == ctx.author and message.channel == ctx.channel)
            if self.message:
                self.id = str(ctx.author).split('#')[-1]
                async with aiosqlite.connect("main.db") as db:
                    async with db.cursor() as cursor:
                        sql = 'SELECT id FROM Players WHERE id = (?)'
                        result = await cursor.execute(sql, [int(self.id)])
                        result = await result.fetchone()
                        if result:
                            await ctx.send('This User is already linked to a pre-existing account')
                            return
                        records = [int(self.id), str(self.message.content)]
                        sql = '''
                                INSERT INTO Players
                                VALUES (?, ?)
                            '''
                        await cursor.execute(sql, records)
                    await db.commit()
                    await ctx.send('Welcome ' + str(self.message.content))
        except asyncio.TimeoutError: 
            await ctx.send('Command Timedout')

    @commands.command()
    async def nameChange(self, ctx):
        await ctx.send('What is your new Username?')
        try:
            self.message = await self.bot.wait_for('message', timeout = 10, check= lambda message: message.author == ctx.author and message.channel == ctx.channel)
            if self.message:
                self.id = str(ctx.author).split('#')[-1]
                async with aiosqlite.connect("main.db") as db:
                    async with db.cursor() as cursor:
                        records = [str(self.message.content),int(self.id)]
                        sql = '''
                                UPDATE Players
                                SET username = (?)
                                WHERE id = (?)
                            '''
                        await cursor.execute(sql, records)
                    await db.commit()
                    await ctx.send('Your name has been changed to ' + str(self.message.content))
        except asyncio.TimeoutError: 
            await ctx.send('Command Timedout')

async def setup(bot):
    await bot.add_cog(Commands(bot))