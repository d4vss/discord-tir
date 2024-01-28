import asyncio
import datetime
import disnake
import humanize
from disnake import Embed
from disnake.ext import commands
from helpers import db

class ThreadInactivityRemoverCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def tir(self, inter):
        pass

    @tir.sub_command(description="Add a new thread!🧵")
    @commands.has_permissions(administrator=True)
    async def add(self, inter, thread_id, clear_after: int):
        payload = await db.fetch("threadList", False, f"WHERE threadId = {int(thread_id)}")
        if payload:
            embed = Embed(description="**This thread is already added.\nTo modify the settings, remove it and add it again.**")
            return await inter.send(embed=embed, ephemeral=True)

        thread = inter.guild.get_thread(int(thread_id))
        if not thread:
            embed = Embed(description="**This thread couldn't be found.**")
            return await inter.send(embed=embed, ephemeral=True)

        await db.insert("threadList", "guildId, threadId, clearAfter", f"{inter.guild.id}, {int(thread_id)}, {clear_after}")
        embed = Embed(description="**Thread added.**")
        await inter.send(embed=embed, ephemeral=True)

    @tir.sub_command(description="Remove a thread!🧵")
    @commands.has_permissions(administrator=True)
    async def remove(self, inter, thread_id):
        payload = await db.fetch("threadList", False, f"WHERE threadId = {int(thread_id)}")
        if not payload:
            embed = Embed(description="**There was not thread found with this id.**")
            return await inter.send(embed=embed, ephemeral=True)
        
        await db.delete("threadList", f"WHERE threadId = {int(thread_id)}")
        embed = Embed(description="**Thread removed.**")
        await inter.send(embed=embed, ephemeral=True)

    @tir.sub_command(description="View all active thread inactivity remover.🧵")
    @commands.has_permissions(administrator=True)
    async def view(self, inter):
        payload = await db.fetch("threadList", "threadId, clearAfter", True, f"WHERE guildId = {inter.guild.id}")
        if payload:
            embed = Embed(description="**Active TIRs:**\n\n")

            for thread in payload:
                embed.description += f"<#{thread[0]}> - Removal after **{humanize.precisedelta(datetime.timedelta(seconds=thread[1]))}.**\n"
        else:
            embed = Embed(description="**No active TIRs.**")

        await inter.send(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(ThreadInactivityRemoverCommand(bot))
