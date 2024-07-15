import discord
from discord.ext import commands


class hacker11(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Security commands"""
  
    def help_custom(self):
		      emoji = '⚒'
		      label = "Moderation Commands"
		      description = "Show You Moderation Commands"
		      return emoji, label, description

    @commands.group()
    async def __Moderation__(self, ctx: commands.Context):
        """`mute` , `unmute` , `kick` , `warn` , `ban` , `unban` , `clone` , `nick` , `slowmode` ,  `unslowmode` , `clear` , `clear all` , `clear bots` , `clear embeds` , `clear files` , `clear mentions` , `clear images` , `clear contains` , `clear reactions` , `clear user` , `clear emoji` , `nuke` , `lock` , `unlock` , `hide` , `unhide` , `hideall` , `unhideall` , `audit` , `role` , `role temp` , `role remove` , `role delete` , `role create` , `role rename` , `enlarge` , `role humans` , `role unverified` , `role bots` , `role all` , `removerole humans` , `removerole unverified` , `removerole bots` , `removerole all` , `admin add` , `admin remove` , `admin show` , `admin role` , `admin reset` , `mod add` , `mod remove` , `mod show` , `mod role` , `mod reset` , `roleicon`, `steal` , `deleteemoji` , `deletesticker` , `addsticker`"""