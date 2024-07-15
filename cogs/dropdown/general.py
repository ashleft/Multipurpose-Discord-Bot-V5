import discord
from discord.ext import commands


class hacker1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Security commands"""
  
    def help_custom(self):
		      emoji = '⚙'
		      label = "General Commands"
		      description = "Show You General Commands"
		      return emoji, label, description

    @commands.group()
    async def __General__(self, ctx: commands.Context):
        """`avatar` , `servericon` , `membercount` , `timer`, `poll` , `hack` , `token` , `users` , `italicize` , `strike` , `quote` , `code` , `bold` , `censor` , `underline` , `gender` , `wizz` , `pikachu` , `shorten` , `urban` , `rickroll` , `hash` , `snipe` , `setup` , `setup staff` , `setup girl` , `setup friend` , `setup vip` , `setup guest` , `setup config` , `setup create` , `setup delete` , `setup list` , `staff` , `girl` , `friend` , `vip` , `guest` , `remove staff` , `remove girl` , `remove friend` , `remove vip` , `remove guest` , `ar` , `ar create` , `ar delete` , `ar edit` , `ar config`"""