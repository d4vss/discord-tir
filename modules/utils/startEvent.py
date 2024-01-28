from disnake.ext import commands
from helpers import db

class StartEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Create tables in database
    async def setup_database(self):
        tables = {
            "threadList" : "guildId INTEGER, threadId INTEGER, clearAfter INTEGER"
        }
        for table in tables:
            await db.create(table, tables[table])

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{"="*10} \nLogged in as {self.bot.user.name}. \nID: {self.bot.user.id} \n{"="*10}')
        await self.setup_database()

def setup(bot):
    bot.add_cog(StartEvent(bot))
