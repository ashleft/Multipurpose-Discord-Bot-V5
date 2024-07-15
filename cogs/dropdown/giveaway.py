import discord
from discord.ext import commands


class Asher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Giveaway commands"""
  
    def help_custom(self):
		      emoji = '🎉'
		      label = "Giveaway Commands"
		      description = "Shows You Giveaway Commands"
		      return emoji, label, description

    @commands.group()
    async def __Giveaway__(self, ctx: commands.Context):
        """`gstart`, `gend`, `greroll`"""