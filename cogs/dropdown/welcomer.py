import discord
from discord.ext import commands


class hacker111111(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Security commands"""
  
    def help_custom(self):
		      emoji = '👋🏻'
		      label = "Welcomer Commands"
		      description = "Show You Welcomer Commands"
		      return emoji, label, description

    @commands.group()
    async def __Welcomer__(self, ctx: commands.Context):
        """`autorole bots add` , `autorole bots remove` , `autorole bots` , `autorole config` , `autorole humans add` , `autorole humans remove` , `autorole humans` , `autorole reset all` , `autorole reset bots` , `autorole reset humans` , `autorole reset` , `autorole`, `greet channel add` , `greet channel remove`, `greet channel` , `greet embed` , `greet image` , `greet message` , `greet ping` , `greet test` , `greet thumbnail` , `greet autodel` , `greet title` , `greet footer` , `greet` """