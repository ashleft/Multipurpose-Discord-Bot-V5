import discord
from discord.ext import commands
from difflib import get_close_matches
from contextlib import suppress
from core import Context
from core.Astroz import Astroz
from core.Cog import Cog
from utils.Tools import getConfig
from itertools import chain
import json
from utils import help as vhelp
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator
import asyncio
from utils.config import serverLink
from utils.Tools import *
client = Astroz()




color = 0x2f3136
           

General = "🗜"
Moderation = "⚒"
Music = "🎵"
Raidmode = "🚨"
Security = "🛡"
Welcomer = "👋🏻"
Logging = "🗒"
Voice = "🎤"
Extra = "✨"


class HelpCommand(commands.HelpCommand):

  async def on_help_command_error(self, ctx, error):
    damn = [
      commands.CommandOnCooldown, commands.CommandNotFound,
      discord.HTTPException, commands.CommandInvokeError
    ]
    if not type(error) in damn:
      await self.context.reply(f"Unknown Error Occurred\n{error.original}",
                               mention_author=False)
    else:
      if type(error) == commands.CommandOnCooldown:
        return

        return await super().on_help_command_error(ctx, error)

  async def command_not_found(self, string: str) -> None:
    with open('blacklist.json', 'r') as f:
      bled = json.load(f)
    data = getIgnore(self.context.guild.id)
    ch = data["channel"]
    iuser = data["user"]
    buser = data["bypassuser"]
    bl = discord.Embed(description=f"You are blacklisted from using my commannds.\nreason could be excessive use or spamming commands\nJoin our [Support Server]({serverLink}) to appeal .", color=discord.Colour(0x2f3136))
    embed = discord.Embed(description="This Channel is in ignored channel list try my commands in another channel .", color=discord.Colour(0x2f3136))
    ign = discord.Embed(description=f"You are set as a ignored users for {self.context.guild.name} .\nTry my commands or modules in another guild .", color=discord.Colour(0x2f3136))

    if str(self.context.author.id) in bled["ids"]:
      return 
    
    if str(self.context.author.id) in iuser and str(self.context.author.id) not in buser: 
      return 

    if self.context.channel.id in ch and self.context.author.id not in buser:
        return
    else:
      
      if string in ("security", "anti", "antinuke"):
        cog = self.context.bot.get_cog("Antinuke")
        with suppress(discord.HTTPException):
          await self.send_cog_help(cog)
      else:
        msg = f"Command `{string}` is not found...\n"
        hacker = await self.context.bot.fetch_user(246469891761111051)
        cmds = (str(cmd) for cmd in self.context.bot.walk_commands())
        mtchs = get_close_matches(string, cmds)
        if mtchs:
          for okaay, okay in enumerate(mtchs, start=1):
            msg += f"Did You Mean: \n`[{okaay}]`. `{okay}`\n"
        return msg

  async def send_bot_help(self, mapping):
    with open('blacklist.json', 'r') as f:
      bled = json.load(f)
    data = getIgnore(self.context.guild.id)
    ch = data["channel"]
    iuser = data["user"]
    buser = data["bypassuser"]
    bl = discord.Embed(description=f"You are blacklisted from using my commannds.\nreason could be excessive use or spamming commands\nJoin our [Support Server]({serverLink}) to appeal .", color=discord.Colour(0x2f3136))
    embed = discord.Embed(description="This Channel is in ignored channel list try my commands in another channel .", color=discord.Colour(0x2f3136))
    ign = discord.Embed(description=f"You are set as a ignored users for {self.context.guild.name} .\nTry my commands or modules in another guild .", color=discord.Colour(0x2f3136))

    if str(self.context.author.id) in bled["ids"]:
      return 
    
    if str(self.context.author.id) in iuser and str(self.context.author.id) not in buser: 
      return 

    if self.context.channel.id in ch and self.context.author.id not in buser:
        return
    embed = discord.Embed(description=f"🔃**Processing the command...**", color=color)
    ok = await self.context.reply(embed=embed)          
    data = getConfig(self.context.guild.id)
    prefix = data["prefix"]
    filtered = await self.filter_commands(self.context.bot.walk_commands(),
                                              sort=True)
    #if self.context.author.id == 875617517714964530 or self.context.author.id == 986247254161637396:
      #  dev_msg = "Hey Developer, How Can I Help You Today ?"
  #  else:
        #dev_msg = " "
    embed = discord.Embed(
      title="Overview",
      description=
      f"The prefix for this server is `{prefix}`\nType `{prefix}help <command/module>` to get more info regarding it\nTotal Commands: `{len(set(self.context.bot.walk_commands()))}` | Usable by you (here): `{len(set(filtered))}`\n [Invite](https://discord.com/oauth2/authorize?client_id={self.context.bot.user.id}&permissions=8&scope=bot%20applications.commands) | [Support server]({serverLink})",
      color=color)
    
    embed.set_author(name=self.context.author,icon_url=self.context.author.avatar.url if self.context.author.avatar else self.context.author.default_avatar.url)

    embed.set_footer(
      text=f"Requested By {self.context.author}",
      icon_url=self.context.author.avatar.url if self.context.author.avatar else self.context.author.default_avatar.url
    )

    embed.add_field(#
      name="Module",
      value=
     f"""{General} General\n{Moderation} Moderation\n{Music} Music\n{Raidmode} Raidmode\n{Security} Security\n{Welcomer} Welcomer\n{Voice} Voice\n{Extra} Extra""",
      inline=True)
    embed.timestamp = discord.utils.utcnow()
    #embed.set_thumbnail(url=self.context.bot.user.display_avatar.url)
    view = vhelp.View(mapping=mapping,
                          ctx=self.context,
                          homeembed=embed,
                          ui=2)
    await ok.edit(embed=embed,view=view)
    

    
    
    

  async def send_command_help(self, command):
    with open('blacklist.json', 'r') as f:
      bled = json.load(f)
    data = getIgnore(self.context.guild.id)
    ch = data["channel"]
    iuser = data["user"]
    buser = data["bypassuser"]
    bl = discord.Embed(description=f"You are blacklisted from using my commannds.\nreason could be excessive use or spamming commands\nJoin our [Support Server]({serverLink}) to appeal .", color=discord.Colour(0x2f3136))
    embed = discord.Embed(description="This Channel is in ignored channel list try my commands in another channel .", color=discord.Colour(0x2f3136))
    ign = discord.Embed(description=f"You are set as a ignored users for {self.context.guild.name} .\nTry my commands or modules in another guild .", color=discord.Colour(0x2f3136))

    if str(self.context.author.id) in bled["ids"]:
      return 
    
    if str(self.context.author.id) in iuser and str(self.context.author.id) not in buser: 
      return 

    if self.context.channel.id in ch and self.context.author.id not in buser:
        return
  
    else:
      hacker = f">>> {command.help}" if command.help else '>>> No Help Provided...'
      embed = discord.Embed(
        description=
        f"""```yaml\n- [] = optional argument\n- <> = required argument\n- Do NOT Type These When Using Commands !```\n{hacker}""",
        color=color)
      alias = ' | '.join(command.aliases)

      embed.add_field(name="**Aliases**",
                      value=f"{alias}" if command.aliases else "No Aliases",
                      inline=False)
      embed.add_field(name="**Usage**",
                      value=f"`{self.context.prefix}{command.signature}`\n")
      embed.set_author(name=f"{command.cog.qualified_name.title()}",
                       icon_url=self.context.bot.user.display_avatar.url)
      await self.context.reply(embed=embed, mention_author=False)

  def get_command_signature(self, command: commands.Command) -> str:
    parent = command.full_parent_name
    if len(command.aliases) > 0:
      aliases = ' | '.join(command.aliases)
      fmt = f'[{command.name} | {aliases}]'
      if parent:
        fmt = f'{parent}'
      alias = f'[{command.name} | {aliases}]'
    else:
      alias = command.name if not parent else f'{parent} {command.name}'
    return f'{alias} {command.signature}'

  def common_command_formatting(self, embed_like, command):
    embed_like.title = self.get_command_signature(command)
    if command.description:
      embed_like.description = f'{command.description}\n\n{command.help}'
    else:
      embed_like.description = command.help or 'No help found...'

  async def send_group_help(self, group):
    with open('blacklist.json', 'r') as f:
      bled = json.load(f)
    data = getIgnore(self.context.guild.id)
    ch = data["channel"]
    iuser = data["user"]
    buser = data["bypassuser"]
    bl = discord.Embed(description=f"You are blacklisted from using my commannds.\nreason could be excessive use or spamming commands\nJoin our [Support Server]({serverLink}) to appeal .", color=discord.Colour(0x2f3136))
    embed = discord.Embed(description="This Channel is in ignored channel list try my commands in another channel .", color=discord.Colour(0x2f3136))
    ign = discord.Embed(description=f"You are set as a ignored users for {self.context.guild.name} .\nTry my commands or modules in another guild .", color=discord.Colour(0x2f3136))

    if str(self.context.author.id) in bled["ids"]:
      return 
    
    if str(self.context.author.id) in iuser and str(self.context.author.id) not in buser: 
      return 

    if self.context.channel.id in ch and self.context.author.id not in buser:
        return
    else:
      entries = [(
        f"`{self.context.prefix}{cmd.qualified_name}`",
        f"{cmd.short_doc if cmd.short_doc else ''}\n\n"
      ) for cmd in group.commands]
      count = 0
      for cmd in group.commands:
        count += 1     
       
    paginator = Paginator(source=FieldPagePaginator(
      entries=entries,
      title=f"{group.qualified_name} ({count})",
      description="<...> Duty | [...] Optional\n\n",
      color=color,
      per_page=10),
                          ctx=self.context)
    await paginator.paginate()
    

  async def send_cog_help(self, cog):
    with open('blacklist.json', 'r') as f:
      bled = json.load(f)
    data = getIgnore(self.context.guild.id)
    ch = data["channel"]
    iuser = data["user"]
    buser = data["bypassuser"]
    bl = discord.Embed(description=f"You are blacklisted from using my commannds.\nreason could be excessive use or spamming commands\nJoin our [Support Server]({serverLink}) to appeal .", color=discord.Colour(0x2f3136))
    embed = discord.Embed(description="This Channel is in ignored channel list try my commands in another channel .", color=discord.Colour(0x2f3136))
    ign = discord.Embed(description=f"You are set as a ignored users for {self.context.guild.name} .\nTry my commands or modules in another guild .", color=discord.Colour(0x2f3136))

    if str(self.context.author.id) in bled["ids"]:
      return 
    
    if str(self.context.author.id) in iuser and str(self.context.author.id) not in buser: 
      return 

    if self.context.channel.id in ch and self.context.author.id not in buser:
        return
  
    entries = [(
      f"`{self.context.prefix}{cmd.qualified_name}`",
      f"{cmd.short_doc if cmd.short_doc else ''}"
      f"\n\n",
    ) for cmd in cog.get_commands()]
    paginator = Paginator(source=FieldPagePaginator(
      entries=entries,
      title=f"{cog.qualified_name.title()} ({len(cog.get_commands())})",
      description="<...> Duty | [...] Optional\n\n",
      color=color,
      per_page=10),
                          ctx=self.context)
    await paginator.paginate()


class Help(Cog, name="help"):

  def __init__(self, client: Astroz):
    self._original_help_command = client.help_command
    attributes = {
      'name':
      "help",
      'aliases': ['h'],
      'cooldown':
      commands.CooldownMapping.from_cooldown(1, 5, commands.BucketType.user),
      'help':
      'Shows help about bot, a command or a category'
    }
    client.help_command = HelpCommand(command_attrs=attributes)
    client.help_command.cog = self

  async def cog_unload(self):
    self.help_command = self._original_help_command
            