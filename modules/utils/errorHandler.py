import disnake
from disnake.ext import commands
from disnake import Embed

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Global slash command error handler
    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        if isinstance(error, commands.errors.MissingPermissions):
            embed = Embed(description=f"**You are missing the following permission:** \n{', '.join(error.missing_permissions)}", color=0xffffff)
        elif isinstance(error, commands.errors.NotOwner):
            embed = Embed(description=f"**You do not own this bot.**", color=0xffffff)
        elif isinstance(error, commands.errors.BadArgument):
            embed = Embed(description=f"**Bad argument: {error}**", color=0xffffff)
        elif isinstance(error, commands.errors.CommandOnCooldown):
            embed = Embed(description=f"Command is on cool down. Try again in {round(error.retry_after)} seconds.", color=0xffffff)
        elif isinstance(error, commands.errors.CommandNotFound):
            pass
        else:
            embed = Embed(description=f"**Unknown error.**", color=0xffffff)
            raise error
        await inter.send(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))