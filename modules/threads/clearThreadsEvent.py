import asyncio
from disnake.ext import commands, tasks
from datetime import datetime, timedelta
from helpers import db

class ClearThreadsEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clearThreads.start()

    @tasks.loop(seconds=15)
    async def clearThreads(self):
        payload = await db.fetch("threadList", "guildId, threadId, clearAfter", True)
        for threadInfo in payload:
            guildId, threadId, clearAfter = threadInfo
            currentGuild = self.bot.get_guild(guildId)

            if not currentGuild:
                continue

            currentThread = currentGuild.get_thread(threadId)
            if not currentThread:
                await db.delete("threadList", f"WHERE threadId = {threadId}")
                continue

            membersToKick = [str(user.id) for user in await currentThread.fetch_members()]
            threshold_time = datetime.now() - timedelta(seconds=clearAfter)
            messages = await currentThread.history(after=threshold_time).flatten()

            for message in messages:
                if str(message.author.id) in membersToKick:
                    membersToKick.remove(str(message.author.id))

            for userId in membersToKick:
                await currentThread.remove_user(currentGuild.get_member(int(userId)))

    @clearThreads.before_loop
    async def beforeClearThreads(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(1)

def setup(bot):
    bot.add_cog(ClearThreadsEvent(bot))
