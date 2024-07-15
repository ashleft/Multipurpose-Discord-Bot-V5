import discord
from discord.ext import commands


class hacker1111(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Security commands"""
  
    def help_custom(self):
		      emoji = '🚨'
		      label = "Raidmode Commands"
		      description = "Show You Raidmode Commands"
		      return emoji, label, description

    @commands.group()
    async def __Raidmode__(self, ctx: commands.Context):
        """`automod` , `automod antispam enable` , `automod antispam disable` , `automod antilink disable` ,  `automod antilink enable` , `automod antiinvites disable` ,  `automod antiinvites enable` , `automod punishment` , `automod punishment set` , `automod punishment show` , `automod whitelist` , `automod whitelist add` , `automod whitelist remove` , `automod whitelist show` , `automod whitelist reset` , `automod ignore channel add` , `automod ignore channel remove`"""