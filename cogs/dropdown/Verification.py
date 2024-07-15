import discord
from discord.ext import commands


class AsherVerification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Verification commands"""
  
    def help_custom(self):
		      emoji = '🤖'
		      label = "Verification Commands"
		      description = "verification, verification on, giveroleaftercaptcha"
		      return emoji, label, description

    @commands.group()
    async def __verification__(self, ctx: commands.Context):
        """`verification`, `verification on`, `verification off`, `giveroleaftercaptcha`"""