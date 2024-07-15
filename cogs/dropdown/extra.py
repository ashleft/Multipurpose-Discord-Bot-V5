import discord
from discord.ext import commands


class hacker111111111(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Security commands"""
  
    def help_custom(self):
		      emoji = '✨'
		      label = "Extra Commands"
		      description = "Show You Extra Commands"
		      return emoji, label, description

    @commands.group()
    async def __Extra__(self, ctx: commands.Context):
        """`botinfo` , `stats` , `invite` , `serverinfo` , `userinfo` , `roleinfo` , `botinfo` , `status` ,  `boosts` , `unbanall` ,  `joined-at` , `ping` , `github` , `vcinfo` , `channelinfo` , `badges` , `sticky`, `unsticky`, `media`, `media setup`, `media remove`, `media config`, `media reset`,  `list boosters` , `list inrole` , `list emojis` , `list bots` , `list admins` , `list invoice` , `list mods` , `list early` , `list activedeveloper` , `list createpos` , `list roles` , `banner user` , `banner server` , `ignore channel add` , `ignore channel remove` , `ignore user add` , `ignore user remove` , `ignore user show` , `ignore bypass user add` , `ignore bypass user show` , `ignore bypass user remove`"""