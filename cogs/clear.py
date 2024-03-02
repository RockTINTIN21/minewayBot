from disnake.ext import commands

class ClearChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clear")
    async def clear(self, ctx):
        await ctx.channel.purge(limit=None)  # Очистка всего чата



def setup(bot):
    bot.add_cog(ClearChatCog(bot))