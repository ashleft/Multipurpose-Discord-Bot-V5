import discord
import asyncio
import datetime
import re
import typing
import typing as t
from typing import *
from utils.Tools import *
from core import Cog, Astroz, Context
from discord.ext.commands import Converter
from discord.ext import commands, tasks
from discord.ui import Button, View
from typing import Union, Optional
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator
from typing import Union, Optional
from io import BytesIO
import requests
import aiohttp
import time
from datetime import datetime, timezone, timedelta
import sqlite3
from typing import *



time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


def convert(argument):
  args = argument.lower()
  matches = re.findall(time_regex, args)
  time = 0
  for key, value in matches:
    try:
      time += time_dict[value] * float(key)
    except KeyError:
      raise commands.BadArgument(
        f"{value} is an invalid time key! h|m|s|d are valid arguments")
    except ValueError:
      raise commands.BadArgument(f"{key} is not a number!")
  return round(time)

async def do_removal(ctx, limit, predicate, *, before=None, after=None):
    if limit > 2000:
        return await ctx.error(f"Too many messages to search given ({limit}/2000)")

    if before is None:
        before = ctx.message
    else:
        before = discord.Object(id=before)

    if after is not None:
        after = discord.Object(id=after)

    try:
        deleted = await ctx.channel.purge(limit=limit, before=before, after=after, check=predicate)
    except discord.Forbidden as e:
        return await ctx.error("I do not have permissions to delete messages.")
    except discord.HTTPException as e:
        return await ctx.error(f"Error: {e} (try a smaller search?)")

    spammers = Counter(m.author.display_name for m in deleted)
    deleted = len(deleted)
    messages = [f'✅ | {deleted} message{" was" if deleted == 1 else "s were"} removed.']
    if deleted:
        messages.append("")
        spammers = sorted(spammers.items(), key=lambda t: t[1], reverse=True)
        messages.extend(f"**{name}**: {count}" for name, count in spammers)

    to_send = "\n".join(messages)

    if len(to_send) > 2000:
        await ctx.send(f"✅ | Successfully removed {deleted} messages.", delete_after=10)
    else:
        await ctx.send(to_send, delete_after=10)
        
        
        
        
class Moderation(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    self.color = 0x2f3136
    self.bot.sniped_messages = {}

  def convert(self, time):
    pos = ["s", "m", "h", "d"]

    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}
    unit = time[-1]
    if unit not in pos:
      return -1
    try:
      val = int(time[:-1])
    except:
      return -2
    return val * time_dict[unit]



  @commands.command()
  async def enlarge(self, ctx,  emoji: Union[discord.Emoji, discord.PartialEmoji, str]):
    ''' Enlarge any emoji '''
    url = emoji.url
    await ctx.send(url)




  @commands.hybrid_command(name="unlockall",
                    help="Unlocks down the server.",
                    usage="unlockall")
  @blacklist_check()
  @ignore_check()
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  @commands.cooldown(1, 5, commands.BucketType.channel)
  async def unlockall(self, ctx):
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
          button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="✅")
          button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="⚠")
          async def button_callback(interaction: discord.Interaction):
              a = 0
              if interaction.user == ctx.author:
                  if interaction.guild.me.guild_permissions.administrator:
                      embed1 = discord.Embed(
                     color=self.color,
                    description=f"Unlocking all channels in {ctx.guild.name} .")
                      await interaction.response.edit_message(
                       embed=embed1, view=None)
                      for channel in interaction.guild.channels:
                          try:
                              await channel.set_permissions(
                                   ctx.guild.default_role,
                                overwrite=discord.PermissionOverwrite(send_messages=True,
                                                 read_messages=True),
                                         reason="Unlockall Command Executed By: {}".format(ctx.author))
                              a += 1  
                          except Exception as e:
                              print(e)
                      await interaction.channel.send(
                              content=f"✅ | Successfully Unlocked {a} Channel(s) .")   
                      return
                  else:
                    await interaction.response.edit_message(
                         content=
                           "I am missing permission.\ntry giving me permissions and retry",
                              embed=None,
                                  view=None)
              else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
        
          async def button1_callback(interaction: discord.Interaction):   
              if interaction.user == ctx.author:  
                  embed2 = discord.Embed(
                     color=self.color,
                    description=f"Ok I will Not Unlock Any Channel .")
                  await interaction.response.edit_message(
                      embed=embed2, view=None)   
              else:
                  await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
          embed = discord.Embed(
                  color=self.color,
                 description=f'**Are you sure you want to unlock all channels in {ctx.guild.name}**')
          view = View()
          button.callback = button_callback
          button1.callback = button1_callback
          view.add_item(button)
          view.add_item(button1)
          embed.set_footer(text=f"Click on either Yes or No to confirm! You have 20 seconds .")
          await ctx.reply(embed=embed, view=view, mention_author=False,delete_after=20)     
     
                      
      else:
          hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
          hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

          await ctx.send(embed=hacker5, mention_author=False)  
                       
                                       
                      
  @commands.hybrid_command(name="lockall",
                    help="locks down the server.",
                    usage="lockall")
  @blacklist_check()
  @ignore_check()
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  @commands.cooldown(1, 5, commands.BucketType.channel)
  async def lockall(self, ctx):
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
          button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="✅")
          button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="⚠")
          async def button_callback(interaction: discord.Interaction):
              a = 0
              if interaction.user == ctx.author:
                  if interaction.guild.me.guild_permissions.administrator:
                      embed1 = discord.Embed(
                     color=self.color,
                    description=f"locking all channels in {ctx.guild.name} .")
                      await interaction.response.edit_message(
                       embed=embed1, view=None)
                      for channel in interaction.guild.channels:
                          try:
                              await channel.set_permissions(ctx.guild.default_role,
                                      overwrite=discord.PermissionOverwrite(
                                        send_messages=False,
                                        read_messages=True),
                                         reason="lockall Command Executed By: {}".format(ctx.author))
                              a += 1  
                          except Exception as e:
                              print(e)
                      await interaction.channel.send(
                              content=f"✅ | Successfully locked {a} Channel(s) .")
                      return
                  else:
                    await interaction.response.edit_message(
                         content=
                           "I am missing permission.\ntry giving me permissions and retry",
                              embed=None,
                                  view=None)
              else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
        
          async def button1_callback(interaction: discord.Interaction):   
              if interaction.user == ctx.author:  
                  embed2 = discord.Embed(
                     color=self.color,
                    description=f"Ok I will Not lock Any Channel .")
                  await interaction.response.edit_message(
                      embed=embed2, view=None)   
              else:
                  await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
          embed = discord.Embed(
                  color=self.color,
                 description=f'**Are you sure you want to lock all channels in {ctx.guild.name}**')
          view = View()
          button.callback = button_callback
          button1.callback = button1_callback
          view.add_item(button)
          view.add_item(button1)
          embed.set_footer(text=f"Click on either Yes or No to confirm! You have 20 seconds .")
          await ctx.reply(embed=embed, view=view, mention_author=False,delete_after=20)     
                      
      else:
          hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
          hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

          await ctx.send(embed=hacker5, mention_author=False)  

  @commands.hybrid_command(name="give",
                    help="Gives the mentioned user a role.",
                    usage="give <user> <role>",
                    aliases=["addrole"])
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 10, commands.BucketType.user)
  #@commands.has_permissions(administrator=True)
  async def give(
    self,
    ctx,
    member: discord.Member, *,role: discord.Role):    
    data = getConfig(ctx.guild.id)
    lol = data['adminrole']
    admin = data["admins"]
    adminrole = ctx.guild.get_role(lol)
    
    if ctx.author == ctx.guild.owner or str(
        ctx.author.id) in admin or adminrole in ctx.author.roles:
      if role not in member.roles:
        try:
          hacker1 = discord.Embed(
            description=
            f"✅ | Changed roles for {member.name}, +{role.name}",
            color=self.color)
          await member.add_roles(role,
                                 reason=f"{ctx.author} (ID: {ctx.author.id})")
          await ctx.send(embed=hacker1)
        except:
          pass
      elif role in member.roles:
        try:
          hacker = discord.Embed(
            description=
            f"✅ | Changed roles for {member.name}, -{role.name}",
            color=self.color)
          await member.remove_roles(
            role, reason=f"{ctx.author} (ID: {ctx.author.id})")
          await ctx.send(embed=hacker)
        except:
          pass
    else:
      error = discord.Embed(color=self.color,
                            description=f"""
- You need certain {self.bot.user.name} Permissions to use this command!
       - You need one of those permissions:
       `Role Command`
       """)
      error.set_author(name="You can't use this command!",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

      await ctx.send(embed=error)

  @commands.hybrid_command(name="hideall", help="Hides all the channels .",
                    usage="hideall")
  @blacklist_check()
  @ignore_check()
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  @commands.cooldown(1, 5, commands.BucketType.channel)
  async def hideall(self, ctx):
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
          button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="✅")
          button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="⚠")
          async def button_callback(interaction: discord.Interaction):
              a = 0
              if interaction.user == ctx.author:
                  if interaction.guild.me.guild_permissions.administrator:
                      embed1 = discord.Embed(
                     color=self.color,
                    description=f"hiding all channels in {ctx.guild.name} .")
                      await interaction.response.edit_message(
                       embed=embed1, view=None)
                      for channel in interaction.guild.channels:
                          try:
                              await channel.set_permissions(ctx.guild.default_role, view_channel=False,
                                         reason="Hideall Command Executed By: {}".format(ctx.author))
                              a += 1  
                          except Exception as e:
                              print(e)
                      await interaction.channel.send(
                              content=f"✅ | Successfully Hidden {a} Channel(s) .")
                      return
                  else:
                    await interaction.response.edit_message(
                         content=
                           "I am missing permission.\ntry giving me permissions and retry",
                              embed=None,
                                  view=None)
              else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
        
          async def button1_callback(interaction: discord.Interaction):   
              if interaction.user == ctx.author:  
                  embed2 = discord.Embed(
                     color=self.color,
                    description=f"Ok I will Not hide Any Channel .")
                  await interaction.response.edit_message(
                      embed=embed2, view=None)   
              else:
                  await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
          embed = discord.Embed(
                  color=self.color,
                 description=f'**Are you sure you want to hide all channels in {ctx.guild.name}**')
          view = View()
          button.callback = button_callback
          button1.callback = button1_callback
          view.add_item(button)
          view.add_item(button1)
          embed.set_footer(text=f"Click on either Yes or No to confirm! You have 20 seconds .")
          await ctx.reply(embed=embed, view=view, mention_author=False,delete_after=20)     
                      
      else:
          hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
          hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

          await ctx.send(embed=hacker5, mention_author=False)  
          
          
          
  @commands.hybrid_command(name="unhideall", help="Unhides all the channels .",
                    usage="unhideall")
  @blacklist_check()
  @ignore_check()
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  @commands.cooldown(1, 5, commands.BucketType.channel)
  async def unhideall(self, ctx):
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
          button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="✅")
          button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="⚠")
          async def button_callback(interaction: discord.Interaction):
              a = 0
              if interaction.user == ctx.author:
                  if interaction.guild.me.guild_permissions.administrator:
                      embed1 = discord.Embed(
                     color=self.color,
                    description=f"Unhiding all channels in {ctx.guild.name} .")
                      await interaction.response.edit_message(
                       embed=embed1, view=None)
                      for channel in interaction.guild.channels:
                          try:
                              await channel.set_permissions(ctx.guild.default_role, view_channel=True,
                                         reason="Unhideall Command Executed By: {}".format(ctx.author))
                              a += 1  
                          except Exception as e:
                              print(e)
                      await interaction.channel.send(
                              content=f"✅ | Successfully Unhidden {a} Channel(s) .")
                      return
                  else:
                    await interaction.response.edit_message(
                         content=
                           "I am missing permission.\ntry giving me permissions and retry",
                              embed=None,
                                  view=None)
              else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
        
          async def button1_callback(interaction: discord.Interaction):   
              if interaction.user == ctx.author:  
                  embed2 = discord.Embed(
                     color=self.color,
                    description=f"Ok I will Not unhide Any Channel .")
                  await interaction.response.edit_message(
                      embed=embed2, view=None)   
              else:
                  await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
          embed = discord.Embed(
                  color=self.color,
                 description=f'**Are you sure you want to unhide all channels in {ctx.guild.name}**')
          view = View()
          button.callback = button_callback
          button1.callback = button1_callback
          view.add_item(button)
          view.add_item(button1)
          embed.set_footer(text=f"Click on either Yes or No to confirm! You have 20 seconds .")
          await ctx.reply(embed=embed, view=view, mention_author=False,delete_after=20)     
                      
      else:
          hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
          hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

          await ctx.send(embed=hacker5, mention_author=False)  
            
            
            

  @commands.hybrid_command(name="unhide", help="Unhides the channel")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_channels=True)
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def _unhide(self, ctx, channel: discord.TextChannel = None):
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
          channel = channel or ctx.channel
          overwrite = channel.overwrites_for(ctx.guild.default_role)
          overwrite.view_channel = True
          button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="✅")
          button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="⚠")
          async def button_callback(interaction: discord.Interaction):
              if interaction.user == ctx.author:
                  if interaction.guild.me.guild_permissions.administrator:
                      embed1 = discord.Embed(
                       color=self.color,
                        description=f"Unhiding {channel.mention} .")
                      await interaction.response.edit_message(embed=embed1, view=None)
                      try:
                          await channel.set_permissions(ctx.guild.default_role,
                                  overwrite=overwrite,
                                  reason=f"Channel Unhidden By {ctx.author}")
                      except Exception as e:
                          print(e)
                      await interaction.channel.send(content=f"✅ | Successfully unhidden {channel.mention} .")
                      return
                  else:
                      await interaction.response.edit_message(
                         content=
                           "I am missing permission.\ntry giving me permissions and retry",
                              embed=None,
                                  view=None)
              else:
                  await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
          async def button1_callback(interaction: discord.Interaction):    
              if interaction.user == ctx.author:
                  embed2 = discord.Embed(
                     color=self.color,
                    description=f"Ok I will Not unhide {channel.mention} .")
                  await interaction.response.edit_message(
                      embed=embed2, view=None)   
              else:
                  await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
                
                                     
          embed = discord.Embed(
                   color=self.color,
                 description=f'**Are you sure you want to unhide {channel.mention}**')
          view = View()
          button.callback = button_callback
          button1.callback = button1_callback
          view.add_item(button)
          view.add_item(button1)
          embed.set_footer(text=f"Click on either Yes or No to confirm! You have 20 seconds .")
          await ctx.reply(embed=embed, view=view, mention_author=False,delete_after=20)     
      else:
          hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
          hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

          await ctx.send(embed=hacker5, mention_author=False)           
          
          
          
  @commands.hybrid_command(name="hide", help="hides the channel .")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_channels=True)
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def _hide(self, ctx, channel: discord.TextChannel = None):
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
          channel = channel or ctx.channel
          overwrite = channel.overwrites_for(ctx.guild.default_role)
          overwrite.view_channel = False
          button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="✅")
          button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="⚠")
          async def button_callback(interaction: discord.Interaction):
              if interaction.user == ctx.author:
                  if interaction.guild.me.guild_permissions.administrator:
                      embed1 = discord.Embed(
                       color=self.color,
                        description=f"hiding {channel.mention} .")
                      await interaction.response.edit_message(embed=embed1, view=None)
                      try:
                          await channel.set_permissions(ctx.guild.default_role,
                                  overwrite=overwrite,
                                  reason=f"Channel hidden By {ctx.author}")
                      except Exception as e:
                          print(e)
                      await interaction.channel.send(content=f"✅ | Successfully hidden {channel.mention} .")
                      return
                  else:
                      await interaction.response.edit_message(
                         content=
                           "I am missing permission.\ntry giving me permissions and retry",
                              embed=None,
                                  view=None)
              else:
                  await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
          async def button1_callback(interaction: discord.Interaction):    
              if interaction.user == ctx.author:
                  embed2 = discord.Embed(
                     color=self.color,
                    description=f"Ok I will Not hide {channel.mention} .")
                  await interaction.response.edit_message(
                      embed=embed2, view=None)   
              else:
                  await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
                
                                     
          embed = discord.Embed(
                   color=self.color,
                 description=f'**Are you sure you want to hide {channel.mention}**')
          view = View()
          button.callback = button_callback
          button1.callback = button1_callback
          view.add_item(button)
          view.add_item(button1)
          embed.set_footer(text=f"Click on either Yes or No to confirm! You have 20 seconds .")
          await ctx.reply(embed=embed, view=view, mention_author=False,delete_after=20)     
      else:
          hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
          hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

          await ctx.send(embed=hacker5, mention_author=False)          
        
        

  @commands.hybrid_command(
    name="prefix",
    aliases=["setprefix", "prefixset"],
    help="Allows you to change prefix of the bot for this server")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def _prefix(self, ctx: commands.Context, prefix):
    data = getConfig(ctx.guild.id)
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      data["prefix"] = str(prefix)
      updateConfig(ctx.guild.id, data)
      await ctx.reply(embed=discord.Embed(
        description=
        f"✅ | Successfully Changed Prefix For **{ctx.guild.name}**\nNew Prefix for **{ctx.guild.name}** is : `{prefix}`\nUse `{prefix}help` For More info .",
        color=self.color))
    else:
      hacker5 = discord.Embed(
        description=
        """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
        color=self.color)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

      await ctx.send(embed=hacker5)

 

  @commands.hybrid_command(name="mute",
                           description="Timeouts someone for specific time.",
                           usage="mute <member> <time>",
                           aliases=["timeout", "stfu"])
  @commands.cooldown(1, 20, commands.BucketType.member)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @blacklist_check()
  @ignore_check()
 # @commands.has_permissions(manage_messages=True)
  async def _mute(self, ctx, member: discord.Member, duration):
    data = getConfig(ctx.guild.id)
    data2 = getExtra(ctx.guild.id)
    mods = data2["mods"]
    modsr = data2["modrole"]
    lol = data['adminrole']
    admin = data["admins"]
    adminrole = ctx.guild.get_role(lol)
    modsrole = ctx.guild.get_role(modsr)
    if ctx.author == ctx.guild.owner or str(ctx.author.id) in admin or adminrole in ctx.author.roles or str(ctx.author.id) in mods or modsrole in ctx.author.roles:
      ok = duration[:-1]
      tame = self.convert(duration)
      till = duration[-1]
      if tame == -1:
        hacker3 = discord.Embed(
          color=self.color,
          description=
          f"<a:error:1002226340516331571> | You didnt didnt gave time with correct unit\nExamples:\n{ctx.prefix}mute{ctx.author} 10m\n{ctx.prefix}mute {ctx.author} 5hr",
          timestamp=ctx.message.created_at)
        await ctx.reply(embed=hacker3, mention_author=False)
      elif tame == -2:
        hacker4 = discord.Embed(
          color=self.color,
          description=
          f"<a:error:1002226340516331571> | Time must be an integer!",
          timestamp=ctx.message.created_at)
        await ctx.reply(embed=hacker4, mention_author=False)
      else:
        if till.lower() == "d":
          t = datetime.timedelta(seconds=tame)
          hacker = discord.Embed(
            color=self.color,
            description=
           f"**Moderator:** {ctx.author.mention} \n**Details:**\n   Duration {ok} Day(s)")
          hacker.set_author(
            name="Timeout result:",
            icon_url=ctx.author.avatar.url
            if ctx.author.avatar else ctx.author.default_avatar.url)

          hacker.add_field(
            name="Successful Timeouts",
            value=f"`{member}`",
            inline=False)
          hacker.add_field(
            name="Unsuccessful Operations",
            value="All users were timed out!",
            inline=False)
        elif till.lower() == "m":
          t = datetime.timedelta(seconds=tame)
          hacker = discord.Embed(
            color=self.color,
            description=
           f"**Moderator:** {ctx.author.mention} \n**Details:**\n   Duration {ok} Minute(s)")
          hacker.set_author(
            name="Timeout result:",
            icon_url=ctx.author.avatar.url
            if ctx.author.avatar else ctx.author.default_avatar.url)

          hacker.add_field(
            name="Successful Timeouts",
            value=f"`{member}`",
            inline=False)
          hacker.add_field(
            name="Unsuccessful Operations",
            value="All users were timed out!",
            inline=False)
        elif till.lower() == "s":
          t = datetime.timedelta(seconds=tame)
          hacker = discord.Embed(
            color=self.color,
            description=
           f"**Moderator:** {ctx.author.mention} \n**Details:**\n   Duration {ok} Second(s)")
          hacker.set_author(
            name="Timeout result:",
            icon_url=ctx.author.avatar.url
            if ctx.author.avatar else ctx.author.default_avatar.url)

          hacker.add_field(
            name="Successful Timeouts",
            value=f"`{member}`",
            inline=False)
          hacker.add_field(
            name="Unsuccessful Operations",
            value="All users were timed out!",
            inline=False)
        elif till.lower() == "h":
          t = datetime.timedelta(seconds=tame)
          hacker = discord.Embed(
            color=self.color,
            description=
           f"**Moderator:** {ctx.author.mention} \n**Details:**\n   Duration {ok} Hour(s)")
          hacker.set_author(
            name="Timeout result:",
            icon_url=ctx.author.avatar.url
            if ctx.author.avatar else ctx.author.default_avatar.url)

          hacker.add_field(
            name="Successful Timeouts",
            value=f"`{member}`",
            inline=False)
          hacker.add_field(
            name="Unsuccessful Operations",
            value="All users were timed out!",
            inline=False)
      try:
        if member.guild_permissions.administrator:
          hacker1 = discord.Embed(
            color=self.color,
            description=
            "<a:error:1002226340516331571> | I can\'t mute administrators")
          await ctx.reply(embed=hacker1)
        else:
          await member.timeout(discord.utils.utcnow() + t,
                               reason="Command Used By: {0}".format(
                                 ctx.author))
          await ctx.send(embed=hacker)

      except:
        pass
    else:
      error = discord.Embed(color=self.color,
                            description=f"""
You need certain {self.bot.user.name} Permissions to use this command!
      You need one of those permissions:
       `Timeout Command`
       """)
      error.set_author(name="You can't use this command!",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
      await ctx.send(embed=error)


  @commands.hybrid_command(name="unmute",
                           description="Unmutes a member .",
                           usage="unmute <member>")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 20, commands.BucketType.member)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  #@commands.has_permissions(administrator=True)
  async def untimeout(self, ctx, member: discord.Member):
    data = getConfig(ctx.guild.id)
    data2 = getExtra(ctx.guild.id)
    mods = data2["mods"]
    modsr = data2["modrole"]
    lol = data['adminrole']
    admin = data["admins"]
    adminrole = ctx.guild.get_role(lol)
    modsrole = ctx.guild.get_role(modsr)
    if ctx.author == ctx.guild.owner or str(ctx.author.id) in admin or adminrole in ctx.author.roles or str(ctx.author.id) in mods or modsrole in ctx.author.roles:
      if member.is_timed_out():
        try:
          await member.edit(timed_out_until=None)
          hacker5 = discord.Embed(
            color=self.color,
            description=
           f"**Moderator:** {ctx.author.mention} \n**Details:**\n   DM-Members: ✅\n")
          hacker5.set_author(
            name="Unmute result:",
            icon_url=ctx.author.avatar.url
            if ctx.author.avatar else ctx.author.default_avatar.url)
          hacker5.add_field(
            name="Successful Unmute",
            value=f"`{member}`",
            inline=False)
          hacker5.add_field(
            name="Unsuccessful Unmute",
            value="All users were unmuted!",
            inline=False)
          await ctx.reply(embed=hacker5)
          await member.send(f"⚠ | You have been unmuted from {ctx.guild.name} by {ctx.author} (ID: {ctx.author.id})")
          return
        except Exception as e:
          hacker = discord.Embed(
            color=self.color,
            description=
            f"<a:error:1002226340516331571> | Unable to Remove Timeout from {member}")
          await ctx.send(embed=hacker)
      else:
        hacker1 = discord.Embed(
          color=self.color,
          description="<a:error:1002226340516331571> | {} Is Unmuted Already .".format(
            member.mention),
          timestamp=ctx.message.created_at)
        await ctx.send(embed=hacker1)
    else:
      error = discord.Embed(color=self.color,
                            description=f"""
You need certain {self.bot.user.name} Permissions to use this command!
      You need one of those permissions:
       `Unmute Command`
       """)
      error.set_author(name="You can't use this command!",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
      await ctx.send(embed=error)



  @commands.hybrid_command( name="kick",
    help=
    "Somebody is breaking rules simply kick him from the server as punishment",
    usage="kick <member>")
  @commands.cooldown(1, 20, commands.BucketType.member)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @blacklist_check()
  @ignore_check()
  async def _kick(self,
                  ctx: commands.Context,
                  member: discord.Member,
                  *,
                  reason=None):
    data = getConfig(ctx.guild.id)
    lol = data['adminrole']
    admin = data["admins"]
    adminrole = ctx.guild.get_role(lol)
    if ctx.author == ctx.guild.owner or str(ctx.author.id) in admin or adminrole in ctx.author.roles:
      mem = await self.bot.fetch_user(member.id)
      button = Button(label="Yes",
                    style=discord.ButtonStyle.green)
      button1 = Button(label="No",
                     style=discord.ButtonStyle.red)
      async def button_callback(interaction: discord.Interaction):
          if interaction.user == ctx.author:
              if interaction.guild.me.guild_permissions.ban_members:
                  await interaction.guild.kick(mem, reason=f"{reason}" + str(ctx.author))
                  #await mem.kick(reason=f"{reason}" + str(ctx.author))
                  hacker = discord.Embed(
                        color=self.color,
                            description=
                             f"**Moderator:** {ctx.author.mention} \n**Details:**\n   Duration: ❌\n   DM-Members: ✅\n   Reason: {reason}\n")
                  hacker.set_author(
                       name="Kick result:",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
                  hacker.add_field(
                      name="Successful Kicks",
                        value=f"`{mem}`",
                          inline=False)
                  hacker.add_field(
                        name="Unsuccessful Kicks",
                         value="All users were kicked!",
                           inline=False)
                  await interaction.response.edit_message(
                       embed=hacker, view=None)
                  await mem.send(f"⚠ | You have been kicked from {ctx.guild.name} for {reason} by {ctx.author} (ID: {ctx.author.id}")
                  return
              else:
                  await interaction.response.edit_message(
                         content=
                           "I am missing permission.\ntry giving me permissions and retry",
                              embed=None,
                                  view=None)
          else:
              await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
              
              
      async def button1_callback(interaction: discord.Interaction):        
          if interaction.user == ctx.author:  
              embed2 = discord.Embed(
                     color=self.color,
                    description=f"**Cancelled**.")
              await interaction.response.edit_message(
                      embed=embed2, view=None)
          else:
              await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)  
      embed = discord.Embed(
                  color=self.color,
                 description=f'''**Target:**\n  {mem}''')
      embed.set_author(name="Do you want to proceed?",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
      embed.set_footer(text=f"Click on either Yes or No to confirm! You have 20 seconds .")
      view = View()
      button.callback = button_callback
      button1.callback = button1_callback
      view.add_item(button)
      view.add_item(button1)
      await ctx.reply(embed=embed, view=view, mention_author=False,delete_after=20)    
    else:
        error = discord.Embed(color=self.color,
                            description=f"""
You need certain {self.bot.user.name} Permissions to use this command!
      You need one of those permissions:
       `Kick Command`
       """)
        error.set_author(name="You can't use this command!",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
        await ctx.send(embed=error)                 
                    
                    
      
      
      

  @commands.hybrid_command(name="warn",
                           help="To warn a specific user.",
                           usage="warn <member>")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def _warn(self,
                  ctx: commands.Context,
                  member: discord.Member,
                  *,
                  reason=None):
    data = getConfig(ctx.guild.id)
    data2 = getExtra(ctx.guild.id)
    mods = data2["mods"]
    modsr = data2["modrole"]
    lol = data['adminrole']
    admin = data["admins"]
    adminrole = ctx.guild.get_role(lol)
    modsrole = ctx.guild.get_role(modsr)
    if ctx.author == ctx.guild.owner or str(ctx.author.id) in admin or adminrole in ctx.author.roles or str(ctx.author.id) in mods or modsrole in ctx.author.roles:
      hacker = discord.Embed(
            color=self.color,
            description=
           f"**Moderator:** {ctx.author.mention} \n**Details:**\n   DM-Members: ✅\n   Reason : {reason}")
      hacker.set_author(
            name="Warn result:",
            icon_url=ctx.author.avatar.url
            if ctx.author.avatar else ctx.author.default_avatar.url)
      hacker.add_field(
            name="Successful Warns",
            value=f"`{member}`",
            inline=False)
      hacker.add_field(
            name="Unsuccessful Warns",
            value="All users were warned!",
            inline=False)

      await ctx.send(embed=hacker)
      hacker1 = discord.Embed(
        color=self.color,
        description=
        f"⚠ | You have been warned in {ctx.guild.name} for: {reason} By [{ctx.author}](https://discord.com/users/{ctx.author.id})"
      )
      await member.send(embed=hacker1)
    else:
      error = discord.Embed(color=self.color,
                            description=f"""
You need certain {self.bot.user.name} Permissions to use this command!
      You need one of those permissions:
       `Warn Command`
       """)
      error.set_author(name="You can't use this command!",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
      await ctx.send(embed=error)
      
      

  @commands.hybrid_command(name="ban",
                            help=
    "Somebody is breaking rules again and again | ban him from the server as punishment",
    usage="ban [member]", aliases=["fuckban", "hackban"])
  @commands.cooldown(1, 10, commands.BucketType.member)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @blacklist_check()
  @ignore_check()
  #@commands.has_permissions(ban_members=True)
  async def _ban(self, ctx, member: Optional[Union[discord.Member,discord.User]] = None,*,reason=None):
    data = getConfig(ctx.guild.id)
    lol = data['adminrole']
    admin = data["admins"]
    adminrole = ctx.guild.get_role(lol)
    
    if ctx.author == ctx.guild.owner or str(ctx.author.id) in admin or adminrole in ctx.author.roles:
      button = Button(label="Yes",
                    style=discord.ButtonStyle.green)
      button1 = Button(label="No",
                     style=discord.ButtonStyle.red)
      async def button_callback(interaction: discord.Interaction):
          if interaction.user == ctx.author:
              if interaction.guild.me.guild_permissions.ban_members:
                  mem = await self.bot.fetch_user(member.id)
                  await interaction.guild.ban(mem, reason=f"{reason}" + str(ctx.author))
                 
                  hacker = discord.Embed(
                        color=self.color,
                            description=
                             f"**Moderator:** {ctx.author.mention} \n**Details:**\n   Duration: ❌\n   DM-Members: ✅\n   Reason: {reason}\n")
                  hacker.set_author(
                       name="Ban result:",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
                  hacker.add_field(
                      name="Successful Bans",
                        value=f"`{mem}`",
                          inline=False)
                  hacker.add_field(
                        name="Unsuccessful Bans",
                         value="All users were banned!",
                           inline=False)
                  await interaction.response.edit_message(
                       embed=hacker, view=None)
                
                  await mem.send(f"⚠ | You have been banned from {ctx.guild.name} for {reason} by {ctx.author} (ID: {ctx.author.id}")
                  return
              else:
                  await interaction.response.edit_message(
                         content=
                           "I am missing permission.\ntry giving me permissions and retry",
                              embed=None,
                                  view=None)
          else:
              await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
              
              
      async def button1_callback(interaction: discord.Interaction):        
          if interaction.user == ctx.author:  
              embed2 = discord.Embed(
                     color=self.color,
                    description=f"**Cancelled**.")
              await interaction.response.edit_message(
                      embed=embed2, view=None)
          else:
              await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True) 
      if member is not None:
          mem = await self.bot.fetch_user(member.id)
          embed = discord.Embed(
                  color=self.color,
                 description=f'''**Target**:\n  {mem}''')
          embed.set_author(name="Do you want to proceed?",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
          embed.set_footer(text=f"Click on either Yes or No to confirm! You have 20 seconds .")
          view = View()
          button.callback = button_callback
          button1.callback = button1_callback
          view.add_item(button)
          view.add_item(button1)
          await ctx.reply(embed=embed, view=view, mention_author=False,delete_after=20)  
      else:
          
          hacker7 = discord.Embed(color=self.color,
                            description=f"```toml\n- [] = optional argument\n- <> = required argument\n- Do NOT Type These When Using Commands !```\n\n> Somebody is breaking rules again and again | ban him from the server as punishment\n")       
          hacker7.add_field(
                        name="Aliases",
                         value="fuckban | hackban",
                           inline=False)
          hacker7.add_field(
                        name="Usage",
                         value="ban <member>",
                           inline=False)
          hacker7.set_author(
                       name="Moderation",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
          await ctx.send(embed=hacker7)
          
    else:
        error = discord.Embed(color=self.color,
                            description=f"""
You need certain {self.bot.user.name} Permissions to use this command!
      You need one of those permissions:
       `Ban Command`
       """)
        error.set_author(name="You can't use this command!",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
        await ctx.send(embed=error)                
                    
                    
        
        

  @commands.hybrid_command(
    name="unban",
    help="If someone realizes his mistake you should unban him",
    usage="unban [user]")
  @blacklist_check()
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.has_permissions(ban_members=True)
  async def _unban(self, ctx: commands.Context, id: int):
    data = getConfig(ctx.guild.id)
    lol = data['adminrole']
    admin = data["admins"]
    adminrole = ctx.guild.get_role(lol)
    if ctx.author == ctx.guild.owner or str(
        ctx.author.id) in admin or adminrole in ctx.author.roles:
      user = await self.bot.fetch_user(id)
      await ctx.guild.unban(user)
      hacker = discord.Embed(
            color=self.color,
            description=
           f"**Moderator:** {ctx.author.mention} \n**Details:**\n   DM-Members: ✅\n")
      hacker.set_author(
            name="Unban result:",
            icon_url=ctx.author.avatar.url
            if ctx.author.avatar else ctx.author.default_avatar.url)
      hacker.add_field(
            name="Successful Unbans",
            value=f"`{user}`",
            inline=False)
      hacker.add_field(
            name="Unsuccessful Unbans",
            value="All users were unbanned!",
            inline=False)
      await ctx.send(embed=hacker)
    else:
      error = discord.Embed(color=self.color,
                            description=f"""
You need certain {self.bot.user.name} Permissions to use this command!
      You need one of those permissions:
       `Unban Command`
       """)
      error.set_author(name="You can't use this command!",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
      await ctx.send(embed=error)

  @commands.hybrid_command(name="clone", help="Clones a channel .")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_channels=True)
  async def clone(self, ctx: commands.Context, channel: discord.TextChannel):
    await channel.clone()
    hacker = discord.Embed(
      color=self.color,
      description=
      f"✅ | {channel.name} has been successfully cloned"
    )
    hacker.set_author(name=f"{ctx.author.name}",
                      icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

    await ctx.send(embed=hacker)

  @commands.hybrid_command(name="nick",
                           aliases=['setnick'],
                           help="To change someone's nickname.",
                           usage="nick [member]")
  @blacklist_check()
  @ignore_check()
  async def changenickname(self, ctx: commands.Context, member: discord.Member,*, name: str = None):
      data = getConfig(ctx.guild.id)
      data2 = getExtra(ctx.guild.id)
      mods = data2["mods"]
      modsr = data2["modrole"]
      lol = data['adminrole']
      admin = data["admins"]
      adminrole = ctx.guild.get_role(lol)
      modsrole = ctx.guild.get_role(modsr)
      if ctx.author == ctx.guild.owner or str(ctx.author.id) in admin or adminrole in ctx.author.roles or str(ctx.author.id) in mods or modsrole in ctx.author.roles:
          try:
              await member.edit(nick=name)
              if name:
                  mem = self.bot.get_user(member.id)
                  hacker = discord.Embed(
                   color=self.color,
                     description=
                        f"✅ | Successfully changed nickname of {mem} to {name} .")
                  await ctx.send(embed=hacker)
              else:
                  hacker1 = discord.Embed(
                   color=self.color,
                     description=
                        f"✅ | Successfully cleared nickname of {member} .")
                  await ctx.send(embed=hacker1)
          except Exception as err:
              print(err)
      else:
          error = discord.Embed(color=self.color,
                            description=f"""
You need certain {self.bot.user.name} Permissions to use this command!
      You need one of those permissions:
       `Nick Command`
       """)
          error.set_author(name="You can't use this command!",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
          await ctx.send(embed=error)

  @commands.hybrid_command(name="nuke", help="Nukes a channel", usage="nuke")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.has_permissions(manage_channels=True)
  async def _nuke(self, ctx: commands.Context):
    button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="✅")
    button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="⚠")

    async def button_callback(interaction: discord.Interaction):
      if interaction.user == ctx.author:
        if interaction.guild.me.guild_permissions.manage_channels:
          channel = interaction.channel
          newchannel = await channel.clone()
          await newchannel.edit(position=channel.position)

          await channel.delete()
          embed = discord.Embed(
            title="nuke",
            description="Channel has been nuked by **`%s`**" % (ctx.author),
            color=self.color)
          embed.set_image(
            url="https://media2.giphy.com/media/HhTXt43pk1I1W/giphy.gif")
          await newchannel.send(embed=embed)
        else:
          await interaction.response.edit_message(
            content=
            "I am missing manage channels permission.\ntry giving me permissions and retry",
            embed=None,
            view=None)
      else:
        await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)

    async def button1_callback(interaction: discord.Interaction):
      if interaction.user == ctx.author:
        await interaction.response.edit_message(
          content="Ok I will Not Nuke Channel", embed=None, view=None)
      else:
        await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)

    embed = discord.Embed(
      color=self.color, description='**Are you sure you want to nuke channel**')

    view = View()
    button.callback = button_callback
    button1.callback = button1_callback
    view.add_item(button)
    view.add_item(button1)
    embed.set_footer(text=f"Click on either Yes or No to confirm! You have 20 seconds .")
    await ctx.reply(embed=embed, view=view, mention_author=False,delete_after=20)     

  @commands.hybrid_command(name="unlock",
                           help="Unlocks a channel",
                           usage="unlock <channel> <reason>",
                           aliases=["unlockdown"])
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_channels=True)
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def _unlock(self,
                    ctx: commands.Context,
                    channel: discord.TextChannel = None, *,reason=None):
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
          if channel is None: channel = ctx.channel
          button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="✅")
          button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="⚠")
          async def button_callback(interaction: discord.Interaction):
              if interaction.user == ctx.author:
                  if interaction.guild.me.guild_permissions.administrator:
                      embed1 = discord.Embed(
                       color=self.color,
                        description=f"Unlocking {channel.mention} .")
                      await interaction.response.edit_message(embed=embed1, view=None)
                      try:
                          await channel.set_permissions(
                           ctx.guild.default_role,
                          overwrite=discord.PermissionOverwrite(send_messages=True),
                                    reason=reason)
                      except Exception as e:
                          print(e)
                      await interaction.channel.send(content=f"✅ | Successfully Unlocked {channel.mention} .")
                      return
                  else:
                      await interaction.response.edit_message(
                         content=
                           "I am missing permission.\ntry giving me permissions and retry",
                              embed=None,
                                  view=None)
              else:
                  await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
          async def button1_callback(interaction: discord.Interaction):    
              if interaction.user == ctx.author:
                  embed2 = discord.Embed(
                     color=self.color,
                    description=f"Ok I will Not unlock {channel.mention} .")
                  await interaction.response.edit_message(
                      embed=embed2, view=None)   
              else:
                  await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
                
                                     
          embed = discord.Embed(
                   color=self.color,
                 description=f'**Are you sure you want to unlock {channel.mention}**')
          view = View()
          button.callback = button_callback
          button1.callback = button1_callback
          view.add_item(button)
          view.add_item(button1)
          embed.set_footer(text=f"Click on either Yes or No to confirm! You have 20 seconds .")
          await ctx.reply(embed=embed, view=view, mention_author=False,delete_after=20)     
      else:
          hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
          hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

          await ctx.send(embed=hacker5, mention_author=False)            
          
          
  @commands.hybrid_command(name="lock",
                           help="locks a channel .",
                           usage="lock <channel> <reason>",
                           aliases=["lockdown"])
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_channels=True)
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def _lock(self,
                    ctx: commands.Context,
                    channel: discord.TextChannel = None, *,reason=None):
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
          if channel is None: channel = ctx.channel
          button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="✅")
          button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="⚠")
          async def button_callback(interaction: discord.Interaction):
              if interaction.user == ctx.author:
                  if interaction.guild.me.guild_permissions.administrator:
                      embed1 = discord.Embed(
                       color=self.color,
                        description=f"Locking {channel.mention} .")
                      await interaction.response.edit_message(embed=embed1, view=None)
                      try:
                          await channel.set_permissions(
                           ctx.guild.default_role,
                          overwrite=discord.PermissionOverwrite(send_messages=False),
                                    reason=reason)
                      except Exception as e:
                          print(e)
                      await interaction.channel.send(content=f"✅ | Successfully Locked {channel.mention} .")
                      return
                  else:
                      await interaction.response.edit_message(
                         content=
                           "I am missing permission.\ntry giving me permissions and retry",
                              embed=None,
                                  view=None)
              else:
                  await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
          async def button1_callback(interaction: discord.Interaction):    
              if interaction.user == ctx.author:
                  embed2 = discord.Embed(
                     color=self.color,
                    description=f"Ok I will Not lock {channel.mention} .")
                  await interaction.response.edit_message(
                      embed=embed2, view=None)   
              else:
                  await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
                
                                     
          embed = discord.Embed(
                   color=self.color,
                 description=f'**Are you sure you want to lock {channel.mention}**')
          view = View()
          button.callback = button_callback
          button1.callback = button1_callback
          view.add_item(button)
          view.add_item(button1)
          embed.set_footer(text=f"Click on either Yes or No to confirm! You have 20 seconds .")
          await ctx.reply(embed=embed, view=view, mention_author=False,delete_after=20)     
      else:
          hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
          hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

          await ctx.send(embed=hacker5, mention_author=False)                   
          
          
                    
  @commands.hybrid_command(name="slowmode",
                           help="Changes the slowmode",
                           usage="slowmode [seconds]",
                           aliases=["slow"])
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 2, commands.BucketType.user)
  @commands.has_permissions(manage_messages=True)
  async def _slowmode(self, ctx: commands.Context, seconds: int = 0):
    if seconds > 120:
      return await ctx.send(
        embed=discord.Embed(title="slowmode",
                            description="Slowmode can not be over 2 minutes",
                            color=self.color))
    if seconds == 0:
      await ctx.channel.edit(slowmode_delay=seconds)
      await ctx.send(embed=discord.Embed(
        title="slowmode", description="Slowmode is disabled", color=self.color))
    else:
      await ctx.channel.edit(slowmode_delay=seconds)
      await ctx.send(
        embed=discord.Embed(title="slowmode",
                            description="Set slowmode to **`%s`**" % (seconds),
                            color=self.color))

  @commands.hybrid_command(name="unslowmode",
                           help="Disables slowmode",
                           usage="unslowmode",
                           aliases=["unslow"])
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 2, commands.BucketType.user)
  @commands.has_permissions(manage_messages=True)
  async def _unslowmode(self, ctx: commands.Context):
    await ctx.channel.edit(slowmode_delay=0)
    await ctx.send(embed=discord.Embed(
      title="unslowmode", description="Disabled slowmode", color=self.color))



  @commands.group(name="role",invoke_without_command=True)
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @blacklist_check()
  async def role(
    self,
    ctx,
    member: discord.Member, *,role: discord.Role):    
    data = getConfig(ctx.guild.id)
    lol = data['adminrole']
    admin = data["admins"]
    adminrole = ctx.guild.get_role(lol)

    if ctx.author == ctx.guild.owner or str(
        ctx.author.id) in admin or adminrole in ctx.author.roles:
      if role not in member.roles:
        try:
          hacker1 = discord.Embed(
            description=
            f"✅ | Changed roles for {member.name}, +{role.name}",
            color=self.color)
          await member.add_roles(role,
                                 reason=f"{ctx.author} (ID: {ctx.author.id})")
          await ctx.send(embed=hacker1)
        except:
          pass
      elif role in member.roles:
        try:
          hacker = discord.Embed(
            description=
            f"✅ | Changed roles for {member.name}, -{role.name}",
            color=self.color)
          await member.remove_roles(
            role, reason=f"{ctx.author} (ID: {ctx.author.id})")
          await ctx.send(embed=hacker)
        except:
          pass
    else:
      error = discord.Embed(color=self.color,
                            description=f"""
You need certain {self.bot.user.name} Permissions to use this command!
      You need one of those permissions:
       `Role Command`
       """)
      error.set_author(name="You can't use this command!",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

      await ctx.send(embed=error)

  @role.command(help="Give a role to member for particular time .")
  @commands.bot_has_permissions(manage_roles=True)
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  async def temp(self, ctx, role: discord.Role, time, *, user: discord.Member):
    '''Temporarily give a role to any member'''
    if role == ctx.author.top_role:
      embed = discord.Embed(
        description=
        f"⚠ | {role} has the same position as your top role!",
        color=self.color)
      return await ctx.send(embed=embed)
    else:
      if role.position >= ctx.guild.me.top_role.position:
        embed1 = discord.Embed(
          description=
          f"⚠ | {role} is higher than my role, move my role above {role}.",
          color=self.color)
        return await ctx.send(embed=embed1)
    seconds = convert(time)
    await user.add_roles(role, reason=None)
    hacker = discord.Embed(
      description=
      f"✅ | Successfully added {role.mention} to {user.mention} .",
      color=self.color)
    await ctx.send(embed=hacker)
    await asyncio.sleep(seconds)
    await user.remove_roles(role)



  @role.command(help="Delete a role in the server .")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  @commands.bot_has_permissions(manage_roles=True)
  async def delete(self, ctx,*, role: discord.Role):
    '''Deletes the role from server'''
    if role == ctx.author.top_role:
      embed = discord.Embed(
        description=
        f"⚠ | {role} has the same position as your top role!",
        color=self.color)
      return await ctx.send(embed=embed)
    else:
      if role.position >= ctx.guild.me.top_role.position:
        embed1 = discord.Embed(
          description=
          f"⚠ | {role} is higher than my role, move my role above {role}.",
          color=self.color)
        return await ctx.send(embed=embed1)
    if role is None:
      embed2 = discord.Embed(
        description=
        f"⚠ | No role named {role} found in this server .",
        color=self.color)
      return await ctx.send(embed=embed2)
    await role.delete()
    hacker = discord.Embed(
      description=
      f"✅ | Successfully deleted {role}",
      color=self.color)
    await ctx.send(embed=hacker)

  @role.command(help="Create a role in the server .")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  @commands.bot_has_permissions(manage_roles=True)
  async def create(self, ctx, *, name):
    '''Creates a role in the server'''
    if ctx.author == ctx.guild.owner or ctx.guild.me.top_role <= ctx.author.top_role:
      hacker = discord.Embed(
        description=
        f"✅ | Successfully created role with the name {name}",
        color=self.color)
      await ctx.guild.create_role(name=name, color=discord.Color.default())
      await ctx.send(embed=hacker)
    else:
      hacker5 = discord.Embed(
        description=
        """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
        color=self.color)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

      await ctx.send(embed=hacker5)

  @role.command(help="Renames a role in the server .")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  @commands.bot_has_permissions(manage_roles=True)
  async def rename(self, ctx, role: discord.Role, *, newname):
    '''Renames any role '''
    if ctx.author == ctx.guild.owner or ctx.guild.me.top_role <= ctx.author.top_role:
      await role.edit(name=newname)
      await ctx.send(
        f"✅ | Role {role.name} has been renamed to {newname}"
      )
    elif role is None:
      embed2 = discord.Embed(
        description=
        f"⚠ | No role named {role} found in this server .",
        color=self.color)
      return await ctx.send(embed=embed2)
    else:
      hacker5 = discord.Embed(
        description=
        """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
        color=self.color)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

      await ctx.send(embed=hacker5)

  @role.command(name="humans", help="Gives a role to all the humans in the server .")
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def role_humans(self, ctx, *,role: discord.Role):
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
        button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="✅")
        button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="⚠")
        async def button_callback(interaction: discord.Interaction):
            a = 0
            if interaction.user == ctx.author:
                if interaction.guild.me.guild_permissions.ban_members:
                    embed1 = discord.Embed(
                     color=self.color,
                    description=f"Adding {role.mention} to all humans .")
                    await interaction.response.edit_message(
                     embed=embed1, view=None)
                    for hacker in interaction.guild.members:
                      if hacker.bot != True and role not in hacker.roles:
                        try:
                          await hacker.add_roles(role,reason="Role Humans Command Executed By: {}".format(ctx.author))
                          a += 1  
                        except Exception as e:
                          print(e)
                                                 
                            
                    await interaction.channel.send(
                           content=f"✅ | Successfully Added {role.mention} To {a} Human(s) .")
                else:
                    await interaction.response.edit_message(
                        content=
                          "I am missing permission.\ntry giving me permissions and retry",
                            embed=None,
                               view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
        async def button1_callback(interaction: discord.Interaction):
            if interaction.user == ctx.author:
                embed2 = discord.Embed(
                     color=self.color,
                    description=f"Ok I will Not Give {role.mention} To Any Humans .")
                await interaction.response.edit_message( embed=embed2, view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
        test = [member for member in ctx.guild.members if all([not member.bot, not role in member.roles])]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"| {role.mention} is already given to all the members of the server .", color=self.color))
        else:
            embed = discord.Embed(
                color=self.color,
                  description=f'**Are you sure you want to give {role.mention} to {len(test)} members**')
            view = View()
            button.callback = button_callback
            button1.callback = button1_callback
            view.add_item(button)
            view.add_item(button1)
            await ctx.reply(embed=embed, view=view, mention_author=False)
            
        
        
    else:
        hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
        hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.send(embed=hacker5, mention_author=False)                    
                            
                    



  @role.command(name="bots", description="Gives a role to all the bots in the server .")
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def role_bots(self, ctx, *,role: discord.Role):
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
        button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="✅")
        button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="⚠")
        async def button_callback(interaction: discord.Interaction):
            a = 0
            if interaction.user == ctx.author:
                if interaction.guild.me.guild_permissions.ban_members:
                    embed1 = discord.Embed(
                     color=self.color,
                    description=f"Adding {role.mention} to all bots .")
                    await interaction.response.edit_message(
                     embed=embed1, view=None)
                    for hacker in interaction.guild.members:
                      if hacker.bot and role not in hacker.roles:
                        try:
                          await hacker.add_roles(role,reason="Role Bots Command Executed By: {}".format(ctx.author))
                          a += 1  
                        except Exception as e:
                          print(e)
                            
                    await interaction.channel.send(
            content=f"✅ | Successfully Added {role.mention} To {a} Bot(s) .")
                else:
                    await interaction.response.edit_message(
                         content=
                           "I am missing permission.\ntry giving me permissions and retry",
                              embed=None,
                                  view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
                
        async def button1_callback(interaction: discord.Interaction):
            if interaction.user == ctx.author:
                embed2 = discord.Embed(
                     color=self.color,
                    description=f"Ok I will Not Give {role.mention} To Any Bots .")
                await interaction.response.edit_message(
          embed=embed2, view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
        test = [member for member in ctx.guild.members if all([member.bot, not role in member.roles])]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"| {role.mention} is already given to all the bots of the server .", color=self.color))
        else:
            embed = discord.Embed(
                color=self.color,
                  description=f'**Are you sure you want to give {role.mention} to {len(test)} bots**')
            view = View()
            button.callback = button_callback
            button1.callback = button1_callback
            view.add_item(button)
            view.add_item(button1)
            await ctx.reply(embed=embed, view=view, mention_author=False)
    else:
        hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
        hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.send(embed=hacker5, mention_author=False)
                            
                            
                    
                    
                    



  @role.command(name="unverified", description="Gives a role to all the unverified members in the server .")
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def role_unverified(self, ctx,*,role: discord.Role):
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
        button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="✅")
        button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="⚠")
        async def button_callback(interaction: discord.Interaction):
            a = 0
            if interaction.user == ctx.author:
                if interaction.guild.me.guild_permissions.ban_members:
                  embed1 = discord.Embed(
                     color=self.color,
                    description=f"Adding {role.mention} to all unverified members .")
                  await interaction.response.edit_message(
                     embed=embed1, view=None)
                  for hacker in interaction.guild.members:
                    if hacker.avatar is None and role not in hacker.roles:
                      try:
                        await hacker.add_roles(role,reason="Role Unverified Command Executed By: {}".format(ctx.author))
                        a += 1 
                      except Exception as e:
                        print(e)
                                                                                                                        
                  await interaction.channel.send(
            content=f"✅ | Successfully Added {role.mention} To {a} Unverified Member(s) .")
                else:
                    await interaction.response.edit_message(
                         content=
                           "I am missing permission.\ntry giving me permissions and retry",
                              embed=None,
                                  view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
                
        async def button1_callback(interaction: discord.Interaction):
            if interaction.user == ctx.author:
                embed2 = discord.Embed(
                     color=self.color,
                    description=f"Ok I will Not Give {role.mention} To Any Unverified Members .")
                await interaction.response.edit_message(
          embed=embed2, view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
        embed = discord.Embed(
      color=self.color,
      description=f'**Are you sure you want to give {role.mention} to all unverified members in this guild?**')
        view = View()
        button.callback = button_callback
        button1.callback = button1_callback
        view.add_item(button)
        view.add_item(button1)
        await ctx.reply(embed=embed, view=view, mention_author=False)
    else:
        hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
        hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.send(embed=hacker5, mention_author=False)     
        
        
        
  @role.command(name="all", description="Gives a role to all the members in the server .")
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def role_all(self, ctx,*,role: discord.Role):
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
        button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="✅")
        button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="⚠")
        async def button_callback(interaction: discord.Interaction):
            a = 0
            if interaction.user == ctx.author:
                if interaction.guild.me.guild_permissions.ban_members:
                  embed1 = discord.Embed(
                     color=self.color,
                    description=f"Adding {role.mention} to all members .")
                  await interaction.response.edit_message(
                     embed=embed1, view=None)
                  for hacker in interaction.guild.members:
                    try:
                        await hacker.add_roles(role,reason="Role All Command Executed By: {}".format(ctx.author))
                        a += 1  
                    except Exception as e:
                        print(e)
                                                                 
                                                                                                                  
                  await interaction.channel.send(
            content=f"✅ | Successfully Added {role.mention} To {a} Member(s) .")
                else:
                    await interaction.response.edit_message(
                         content=
                           "I am missing permission.\ntry giving me permissions and retry",
                              embed=None,
                                  view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
                
        async def button1_callback(interaction: discord.Interaction):
            if interaction.user == ctx.author:
                embed2 = discord.Embed(
                     color=self.color,
                    description=f"Ok I will Not Give {role.mention} To Anyone .")
                await interaction.response.edit_message(
                 embed=embed2, view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
        test = [member for member in ctx.guild.members if role not in member.roles]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"| {role.mention} is already given to all the members of the server .", color=self.color))
        else:
            embed = discord.Embed(
                color=self.color,
                  description=f'**Are you sure you want to give {role.mention} to {len(test)} members**')
            view = View()
            button.callback = button_callback
            button1.callback = button1_callback
            view.add_item(button)
            view.add_item(button1)
            await ctx.reply(embed=embed, view=view, mention_author=False)
    else:
        hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
        hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.send(embed=hacker5, mention_author=False)   
        
               
      
  @commands.hybrid_group(name="admin",
                  help="",
                  invoke_without_command=True,
                  usage="admin add")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def _admin(self, ctx):
    if ctx.subcommand_passed is None:
      await ctx.send_help(ctx.command)
      ctx.command.reset_cooldown(ctx)

  @_admin.command(name="add",
                  help="Add a user to admin list",
                  usage="admin add <user>")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def admin_add(self, ctx, user: discord.User):
    data = getConfig(ctx.guild.id)
    wled = data["admins"]

    if ctx.author == ctx.guild.owner:
      if len(wled) == 100:
        hacker = discord.Embed(
          title=self.bot.user.name,
          description=
          "You are trying to add more users than what it's allowed in [Trusted Admins]!",
          color=self.color)
        hacker.set_author(name="Unsuccessful Operation!",
                          icon_url=ctx.author.avatar.url if ctx.author.avatar
                          else ctx.author.default_avatar.url)
        await ctx.reply(embed=hacker, mention_author=False)
      else:
        if str(user.id) in wled:
          hacker1 = discord.Embed(color=self.color)
          hacker1.add_field(
            name="Successful Operations",
            value="No successful operation!",
            inline=False)
          hacker1.add_field(
            name="Unsuccessful Operations",
            value=
            f"""`{user}` ❌
                                                               ⚠ *Already exists!*""",
            inline=False)
          hacker1.set_author(
            name="Trusted Admins Addition Result:",
            icon_url=ctx.author.avatar.url
            if ctx.author.avatar else ctx.author.default_avatar.url)
          await ctx.reply(embed=hacker1, mention_author=False)
        else:
          wled.append(str(user.id))
          updateConfig(ctx.guild.id, data)
          hacker4 = discord.Embed(color=self.color)
          hacker4.add_field(
            name="Successful Operations",
            value=f"`{user}`",
            inline=False)
          hacker4.add_field(
            name="Unsuccessful Operations",
            value="All operations were successful!",
            inline=False)
          hacker4.set_author(
            name="Trusted Admins Addition Result:",
            icon_url=ctx.author.avatar.url
            if ctx.author.avatar else ctx.author.default_avatar.url)
          await ctx.reply(embed=hacker4, mention_author=False)

    else:
      hacker5 = discord.Embed(
        description=
        """⚠ | Only the server owner can run this command .""",
        color=self.color)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
      await ctx.reply(embed=hacker5, mention_author=False)

  @_admin.command(name="remove",
                  help="Remove a user from admin list",
                  usage="admin remove <user>")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def admin_remove(self, ctx, user: discord.User):
    data = getConfig(ctx.guild.id)
    wled = data["admins"]
    if ctx.author == ctx.guild.owner:
      if str(user.id) in wled:
        wled.remove(str(user.id))
        updateConfig(ctx.guild.id, data)
        hacker = discord.Embed(
          color=self.color,
          title=self.bot.user.name,
          description=
          f"✅ | Successfully Removed {user.mention} From Admin list For {ctx.guild.name}"
        )
        await ctx.reply(embed=hacker, mention_author=False)
      else:
        hacker2 = discord.Embed(
          color=self.color,
          title=self.bot.user.name,
          description=
          "⚠ | That user is not in my admin list .")
        await ctx.reply(embed=hacker2, mention_author=False)
    else:
      hacker5 = discord.Embed(
        description=
        """⚠ | Only the server owner can run this command .""",
        color=self.color)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
      await ctx.reply(embed=hacker5, mention_author=False)

  @_admin.command(name="show",
                  help="Shows list of admin users in the server.",
                  usage="admin show")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def admin_show(self, ctx):
    data = getConfig(ctx.guild.id)
    wled = data["admins"]
    if len(wled) == 0:
      hacker = discord.Embed(
        color=self.color,
        title=self.bot.user.name,
        description=
        f"⚠ | There aren\'t any admin users for this server"
      )
      await ctx.reply(embed=hacker, mention_author=False)
    else:
      entries = [
        f"`{no}` | <@!{idk}> | ID: [{idk}](https://discord.com/users/{idk})"
        for no, idk in enumerate(wled, start=1)
      ]
      paginator = Paginator(source=DescriptionEmbedPaginator(
        entries=entries,
        title=f"Admin Users of {ctx.guild.name} - {len(wled)}",
        description="",
        color=self.color),
                            ctx=ctx)
      await paginator.paginate()

  @_admin.command(name="reset",
                  help="removes every user from admin database",
                  aliases=["clear"],
                  usage="admin reset")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def wl_reset(self, ctx: Context):
    data = getConfig(ctx.guild.id)

    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      data = getConfig(ctx.guild.id)
      data["admins"] = []
      updateConfig(ctx.guild.id, data)
      hacker = discord.Embed(
        color=self.color,
        title=self.bot.user.name,
        description=
        f"✅ | Successfully Cleared Admin Database For **{ctx.guild.name}**"
      )
      await ctx.reply(embed=hacker, mention_author=False)
    else:
      hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
      await ctx.reply(embed=hacker5, mention_author=False)

  @_admin.command(name="role",
                  help="Add a role to admin role",
                  usage="admin role")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def admin_role(self, ctx, *,role: discord.Role):
    data = getConfig(ctx.guild.id)
    data["adminrole"] = role.id
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      updateConfig(ctx.guild.id, data)
      hacker4 = discord.Embed(
        color=self.color,
        title=self.bot.user.name,
        description=
        f"✅ | {role.mention} Has Been Added To Admin Role For {ctx.guild.name}"
      )
      await ctx.reply(embed=hacker4, mention_author=False)

    else:
      hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
      await ctx.reply(embed=hacker5, mention_author=False)
    
    
  @commands.hybrid_group(name="mod",
                  help="",
                  invoke_without_command=True,
                  usage="mod add/remove")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def _mod(self, ctx):
      if ctx.subcommand_passed is None:
          await ctx.send_help(ctx.command)
          ctx.command.reset_cooldown(ctx) 
        
            
  @_mod.command(name="add",
                  help="Add a user to mod list",
                  usage="mod add <user>")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def mod_add(self, ctx, user: discord.User):
      data = getExtra(ctx.guild.id)
      wled = data["mods"]
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
          if len(wled) == 100:
              hacker = discord.Embed(
                     title=self.bot.user.name,
                   description=
                       "You are trying to add more users than what it's allowed in [Trusted Mods]!",
                    color=self.color)
              hacker.set_author(name="Unsuccessful Operation!",
                          icon_url=ctx.author.avatar.url if ctx.author.avatar
                          else ctx.author.default_avatar.url)
              await ctx.reply(embed=hacker, mention_author=False)
          else:
              if str(user.id) in wled:
                  hacker1 = discord.Embed(color=self.color)
                  hacker1.add_field(
                    name="Successful Operations",
                        value="No successful operation!",
                     inline=False)
                  hacker1.add_field(
                    name="Unsuccessful Operations",
                     value=
                      f"""`{user}` ❌
                                                                ⚠ *Already exists!*""",
                      inline=False)
                  hacker1.set_author(
                    name="Trusted Mods Addition Result:",
                    icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                  await ctx.reply(embed=hacker1, mention_author=False)
              else:
                  wled.append(str(user.id))
                  updateExtra(ctx.guild.id, data)
                  hacker4 = discord.Embed(color=self.color)
                  hacker4.add_field(
                        name="Successful Operations",
                           value=f"`{user}`",
                              inline=False)
                  hacker4.add_field(
                              name="Unsuccessful Operations",
                        value="All operations were successful!",
                       inline=False)
                  hacker4.set_author(
                        name="Trusted Mods Addition Result:",
                          icon_url=ctx.author.avatar.url
                      if ctx.author.avatar else ctx.author.default_avatar.url)
                  await ctx.reply(embed=hacker4, mention_author=False)

      else:
          hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
          hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
          await ctx.reply(embed=hacker5, mention_author=False)    
          




  @_mod.command(name="remove",
                  help="Remove a user from mod list",
                  usage="mod remove <user>")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def mod_remove(self, ctx, user: discord.User):
      data = getExtra(ctx.guild.id)
      wled = data["mods"]
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
          if str(user.id) in wled:
              wled.remove(str(user.id))
              updateExtra(ctx.guild.id, data)
              hacker = discord.Embed(color=self.color)
              hacker.add_field(
                name="Successful Operations",
                 value=f"`{user}`",
                inline=False)
              hacker.add_field(
               name="Unsuccessful Operations",
               value="All operations were successful!",
               inline=False)
              hacker.set_author(
               name="Trusted Mods Removal Result:",
               icon_url=ctx.author.avatar.url
               if ctx.author.avatar else ctx.author.default_avatar.url)
              await ctx.reply(embed=hacker, mention_author=False)
              
          else:
              hacker1 = discord.Embed(color=self.color)
              hacker1.add_field(
                    name="Successful Operations",
                        value="No successful operation!",
                     inline=False)
              hacker1.add_field(
                    name="Unsuccessful Operations",
                     value=
                      f"""`{user}` ❌
                                                                ❌ *Already not exists!*""",
                      inline=False)
              hacker1.set_author(
                    name="Trusted Mods Removal Result:",
                    icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
              await ctx.reply(embed=hacker1, mention_author=False)
          
                  

      else:
          hacker5 = discord.Embed(
             description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
             color=self.color)
          hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
          await ctx.reply(embed=hacker5, mention_author=False)   







  @_mod.command(name="show",
                  help="Shows list of mod users in the server.",
                  usage="mod show")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def mod_show(self, ctx):   
        data = getExtra(ctx.guild.id)
        wled = data["mods"]
        if len(wled) == 0:
            hacker = discord.Embed(
           color=self.color,
           title=self.bot.user.name,
        description=
        f"⚠ | There aren\'t any mod users for this server"
      )
            await ctx.reply(embed=hacker, mention_author=False)
        else:
            entries = [
        f"`{no}` | <@!{idk}> | ID: [{idk}](https://discord.com/users/{idk})"
        for no, idk in enumerate(wled, start=1)
      ]
            paginator = Paginator(source=DescriptionEmbedPaginator(
        entries=entries,
        title=f"Mod Users of {ctx.guild.name} - {len(wled)}",
        description="",
        color=self.color),
                            ctx=ctx)
            await paginator.paginate()



  @_mod.command(name="reset",
                  help="removes every user from mod database",
                  aliases=["clear"],
                  usage="mod reset")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def mod_reset(self, ctx):
        data = getExtra(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            data = getExtra(ctx.guild.id)
            data["mods"] = []
            updateExtra(ctx.guild.id, data)
            hacker = discord.Embed(
        color=self.color,
        title=self.bot.user.name,
        description=
        f"✅ | Successfully Cleared Mods Database For **{ctx.guild.name}**"
      )
            await ctx.reply(embed=hacker, mention_author=False)
        else:
            hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
            hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False)




  @_mod.command(name="role",
                  help="Add a role to mod role",
                  usage="mod role")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def mod_role(self, ctx,  *,role: discord.Role):
        data = getExtra(ctx.guild.id)
        data["modrole"] = role.id
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            updateExtra(ctx.guild.id, data)
            hacker4 = discord.Embed(
        color=self.color,
        title=self.bot.user.name,
        description=
        f"✅ | {role.mention} Has Been Added To Mod Role For {ctx.guild.name}"
      )
            await ctx.reply(embed=hacker4, mention_author=False)
        else:
            hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
      
            hacker5.set_author(name=f"{ctx.author.name}",
                           icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False)
    

                
                
                
  @commands.hybrid_command(aliases=['as', 'stealsticker'], description="Adds the sticker to the server")
  @commands.has_permissions(manage_emojis=True)
  async def addsticker(self, ctx: commands.Context, *, name=None):
        if ctx.message.reference is None:
            return await ctx.reply("No replied message found")
        msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if len(msg.stickers) == 0:
            return await ctx.reply("No sticker found")
        n, url = "", ""
        for i in msg.stickers:
            n = i.name
            url = i.url
        if name is None:
            name = n
        try:
            response = requests.get(url)
            if url.endswith("gif"):
                fname = "Sticker.gif"
            else:
                fname = "Sticker.png"
            file = discord.File(BytesIO(response.content), fname)
            s = await ctx.guild.create_sticker(name=name, description= f"Sticker created by {str(self.bot.user)}", emoji="❤️", file=file)
            await ctx.reply(f"✅ | Sucessfully created sticker with name `{name}`", stickers=[s])
        except:
            return await ctx.reply("Failed to create the sticker")
        
        
  @commands.hybrid_command(aliases=["deletesticker", "removesticker"], description="Delete the sticker from the server")
  @commands.has_permissions(manage_emojis=True)
  async def delsticker(self, ctx: commands.Context, *, name=None):
        if ctx.message.reference is None:
            return await ctx.reply("No replied message found")
        msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if len(msg.stickers) == 0:
            return await ctx.reply("No sticker found")
        try:
            name = ""
            for i in msg.stickers:
                name = i.name
                await ctx.guild.delete_sticker(i)
            await ctx.reply(f"✅ | Sucessfully deleted sticker named `{name}`")
        except:
            await ctx.reply("Failed to delete the sticker")
            
            
  @commands.hybrid_command(aliases=["deleteemoji", "removeemoji"], description="Deletes the emoji from the server")
  @commands.has_permissions(manage_emojis=True)
  async def delemoji(self, ctx, emoji = None):
        init = await ctx.reply(f"| Processing the command...", mention_author=False)
        con = None
        if ctx.message.reference is not None:
            message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            con = str(message.content)
        else:
            con = str(ctx.message.content)
        if con is not None:
            x = r"<a?:[a-zA-Z0-9\_]+:([0-9]+)>"
            xxx = re.findall(x, con)
            count = 0
            if len(xxx) != 0:
                if len(xxx) >= 20:
                    await init.delete()
                    return await ctx.reply(f" | Maximum 20 emojis can be deleted by the bot .")
                for i in xxx:
                    emo = discord.PartialEmoji.from_str(i)
                    if emo in ctx.guild.emojis:
                        emoo = await ctx.guild.fetch_emoji(emo.id)
                        await emoo.delete()
                        count+=1
                await init.delete()
                return await ctx.reply(f"✅ | Successfully deleted {count}/{len(xxx)} Emoji(s) .")
        else:
            await init.delete()
            return await ctx.reply("No Emoji found")
        
        
        
  @commands.command(aliases=["steal", 'ae'], description="Adds the emoji to the server")
  @commands.has_permissions(manage_emojis=True)
  async def addemoji(self, ctx: commands.Context, emoji: Union[discord.Emoji, discord.PartialEmoji, str] = None,*,name=None):
        init = await ctx.reply(f"| Processing the command...", mention_author=False)
        con = None
        if ctx.message.reference is not None:
            message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            con = str(message.content)
        else:
            con = str(ctx.message.content)
        x = r"<a?:[a-zA-Z0-9\_]+:([0-9]+)>"
        xxx = re.findall(x, con)
        if len(xxx) == 1:
            con = None
        if con is not None:
            count = 0
            if len(xxx) != 0:
                if len(xxx) >= 20:
                    await init.delete()
                    return await ctx.reply(f"| Maximum 20 emojis can be added by the bot.")
                for i in xxx:
                    emo = discord.PartialEmoji.from_str(i)
                    if emo.animated:
                        url = f"https://cdn.discordapp.com/emojis/{emo.id}.gif"
                    else:
                        url = f"https://cdn.discordapp.com/emojis/{emo.id}.png"
                    try:
                        async with aiohttp.request("GET", url) as r:
                            img = await r.read()
                            emoji = await ctx.guild.create_custom_emoji(name=f"{emo.name}", image=img)
                            count+=1 
                            c = True
                    except:
                        c = False
                await init.delete()
                hacker4 = discord.Embed(
                     color=self.color,
                          description=
                             f"✅ | Successfully created {count}/{len(xxx)} Emojis"
      )
                return await ctx.reply(embed=hacker4)
            else:
                if emoji is None:
                    return await ctx.reply(f"No emoji found")
            if not emoji.startswith("https://"):
                await init.delete()
                return await ctx.reply("Give a valid emoji to add")
            elif name is None:
                await init.delete()
                return await ctx.reply("Please provide a name for emoji")
            async with aiohttp.request("GET", f"{emoji}") as r:
                img = await r.read()
                try:
                  emo = await ctx.guild.create_custom_emoji(name=f"{name}", image=img)
                  await init.delete()
                  return await ctx.reply(f"✅ | Successfully created {emo}")
                except:
                  await init.delete()
                  return await ctx.reply(f"| Failed to create emoji, it might be because the emoji slots are full.")        
        else:
            if name is None:
                name = f"{emoji.name}"
            c = False
            if emoji.animated:
                url = f"https://cdn.discordapp.com/emojis/{emoji.id}.gif"
            else:
                url = f"https://cdn.discordapp.com/emojis/{emoji.id}.png"
            try:
                async with aiohttp.request("GET", url) as r:
                    img = await r.read()
                    emo = await ctx.guild.create_custom_emoji(name=f"{name}", image=img)
                    await init.delete()
                    await ctx.reply(f"✅ | Successfully created {emo}")
                    c = True
            except:
                c = False
            if not c:
                await init.delete()
                return await ctx.reply("| Failed to create emoji, it might be because the emoji slots are full.")
            
            
            
  @commands.command(description="Changes the icon for the role .")
  @commands.has_permissions(administrator=True)
  @commands.bot_has_guild_permissions(manage_roles=True)
  async def roleicon(self, ctx: commands.Context, role: discord.Role, *, icon: Union[discord.Emoji, discord.PartialEmoji, str]=None):
        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"| {role.mention} role is higher than my role, move it to the top!", color=self.color)
        if ctx.author.top_role.position <= role.position:
            em = discord.Embed(description=f"| {role.mention} has the same or higher position from your top role!", color=self.color)
            return await ctx.send(embed=em, delete_after=15)
        if icon is None:
            c = False
            url = None
            for xd in ctx.message.attachments:
                url = xd.url
                c = True
            if c:
                try:
                    async with aiohttp.request("GET", url) as r:
                        img = await r.read()
                        await role.edit(display_icon=img)
                    em = discord.Embed(description=f"✅ | Successfully changed icon of {role.mention}", color=self.color)
                except:
                    return await ctx.reply("Failed to change the icon of the role")
            else:
                await role.edit(display_icon=None)
                em = discord.Embed(description=f"✅ | Successfully removed icon from {role.mention}", color=self.color)
            return await ctx.reply(embed=em, mention_author=False)
        if isinstance(icon, discord.Emoji) or isinstance(icon, discord.PartialEmoji):
            png = f"https://cdn.discordapp.com/emojis/{icon.id}.png"
            try:
              async with aiohttp.request("GET", png) as r:
                img = await r.read()
            except:
              return await ctx.reply("Failed to change the icon of the role")
            await role.edit(display_icon=img)
            em = discord.Embed(description=f"✅ | Successfully changed the icon for {role.mention} to {icon}", color=self.color)
            return await ctx.reply(embed=em, mention_author=False)
        else:
            if not icon.startswith("https://"):
                return await ctx.reply("Give a valid link")
            try:
              async with aiohttp.request("GET", icon) as r:
                img = await r.read()
            except:
              return await ctx.reply("An error occured while changing the icon for the role")
            await role.edit(display_icon=img)
            em = discord.Embed(description=f"✅ | Successfully changed the icon for {role.mention}", color=self.color)
            return await ctx.reply(embed=em, mention_author=False)
          
          
          
          
  @commands.group(invoke_without_command=True, aliases=["purge"], description="Clears the messages")
  @commands.has_permissions(manage_messages=True)
  async def clear(self, ctx, Choice: Union[discord.Member, int], Amount: int = None):
        """
        An all in one purge command.
        Choice can be a Member or a number
        """
        await ctx.message.delete()

        if isinstance(Choice, discord.Member):
            search = Amount or 5
            return await do_removal(ctx, search, lambda e: e.author == Choice)

        elif isinstance(Choice, int):
            return await do_removal(ctx, Choice, lambda e: True)



  @clear.command(description="Clears the messages containing embeds")
  @commands.has_permissions(manage_messages=True)
  async def embeds(self, ctx, search=100):
        """Removes messages that have embeds in them."""
        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: len(e.embeds))


  @clear.command(description="Clears the messages containing files")
  @commands.has_permissions(manage_messages=True)
  async def files(self, ctx, search=100):
        """Removes messages that have attachments in them."""

        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: len(e.attachments))
        
  @clear.command(description="Clears the messages containg images")
  @commands.has_permissions(manage_messages=True)
  async def images(self, ctx, search=100):
        """Removes messages that have embeds or attachments."""

        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: len(e.embeds) or len(e.attachments))
        
        
  @clear.command(name="all", description="Clears all messages")
  @commands.has_permissions(manage_messages=True)
  async def _remove_all(self, ctx, search=100):
        """Removes all messages."""

        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: True)

  @clear.command(description="Clears the messages of a specific user")
  @commands.has_permissions(manage_messages=True)
  async def user(self, ctx, member: discord.Member, search=100):
        """Removes all messages by the member."""

        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: e.author == member)
        
        
        
  @clear.command(description="Clears the messages containing a specifix string")
  @commands.has_permissions(manage_messages=True)
  async def contains(self, ctx, *, string: str):
        """Removes all messages containing a substring.
        The substring must be at least 3 characters long.
        """

        await ctx.message.delete()
        if len(string) < 3:
            await ctx.error("The substring length must be at least 3 characters.")
        else:
            await do_removal(ctx, 100, lambda e: string in e.content)

  @clear.command(name="bot", aliases=["bots","b"], description="Clears the messages sent by bot")
  @commands.has_permissions(manage_messages=True)
  async def _bot(self, ctx, prefix=None, search=100):
        """Removes a bot user's messages and messages with their optional prefix."""

        await ctx.message.delete()

        def predicate(m):
            return (m.webhook_id is None and m.author.bot) or (prefix and m.content.startswith(prefix))

        await do_removal(ctx, search, predicate)

  @clear.command(name="emoji", aliases=["emojis"], description="Clears the messages having emojis")
  @commands.has_permissions(manage_messages=True)
  async def _emoji(self, ctx, search=100):
        """Removes all messages containing custom emoji."""

        await ctx.message.delete()
        custom_emoji = re.compile(r"<a?:[a-zA-Z0-9\_]+:([0-9]+)>")

        def predicate(m):
            return custom_emoji.search(m.content)

        await do_removal(ctx, search, predicate)

  @clear.command(name="reactions", description="Clears the reaction from the messages")
  @commands.has_permissions(manage_messages=True)
  async def _reactions(self, ctx, search=100):
        """Removes all reactions from messages that have them."""

        await ctx.message.delete()

        if search > 2000:
            return await ctx.send(f"Too many messages to search for ({search}/2000)")

        total_reactions = 0
        async for message in ctx.history(limit=search, before=ctx.message):
            if len(message.reactions):
                total_reactions += sum(r.count for r in message.reactions)
                await message.clear_reactions()

        await ctx.success(f"✅ | Successfully removed {total_reactions} reactions.")
        
        
        
        
  @commands.Cog.listener()
  async def on_message_delete(self, message: discord.Message):
      if not message.guild:
        return
      if not message.guild.me.guild_permissions.view_audit_log:
         return
      if not message.author.bot:
        async for i in message.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.message_delete):
            url = None
            for x in message.attachments:
                url = x.url
            if message.content == "":
                content = "***Content Unavailable***"
            else:
                content = message.content
            if i.target == message.author:
                self.bot.sniped_messages[message.guild.id] = (content, url, message.author,
                                                        message.channel,
                                                        i.user,
                                                        message.created_at)
            else:
                self.bot.sniped_messages[message.guild.id] = (content, url, message.author,
                                                        message.channel,
                                                        None,
                                                        message.created_at)

  @commands.command(description="Snipes the recent message deleted in the channel")
  async def snipe(self, ctx, channel: discord.TextChannel = None):
        if not channel:
            channel = ctx.channel
        try:
            contents, url, author, channel_xyz, mod, time = self.bot.sniped_messages[ctx.guild.id]
        except:
            await ctx.channel.send("| Couldn't find a message to snipe!")
            return
        if channel_xyz == channel:
            embed = discord.Embed(description=f":put_litter_in_its_place: Message sent by {author.mention} deleted in {channel_xyz.mention}",
                                color=self.color,
                                timestamp=time)
            embed.add_field(name="__Content__:",
                                  value=f"{contents}",
                                  inline=False)
            if mod is not None:
                embed.add_field(name="**Deleted By:**",
                                value=f"{mod.mention} (ID: {mod.id})")
            if url is not None:
                if url.startswith("http") or url.startswith("http"):
                    embed.set_image(url=url)
            embed.set_footer(text=f"Requested By {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
            return await ctx.channel.send(embed=embed)
        return await ctx.channel.send("| Couldn't find a message to snipe!")
      
      
      
##########################33
  @commands.group(name="removerole",invoke_without_command=True,aliases=['rrole'],
                   help="remove a role from all members .",)
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @blacklist_check()
  @commands.has_permissions(administrator=True)
  async def rrole(self,ctx):
    if ctx.subcommand_passed is None:
      await ctx.send_help(ctx.command)
      ctx.command.reset_cooldown(ctx)
      

  @rrole.command( description="Removes a role from all the humans in the server .")
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.has_permissions(administrator=True)
  async def rrole_humans(self, ctx, *,role: discord.Role):
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
        button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="✅")
        button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="⚠")
        async def button_callback(interaction: discord.Interaction):
            a = 0
            if interaction.user == ctx.author:
                if interaction.guild.me.guild_permissions.ban_members:
                    embed1 = discord.Embed(
                     color=self.color,
                    description=f"Removing {role.mention} from all humans .")
                    await interaction.response.edit_message(
                     embed=embed1, view=None)
                    for hacker in interaction.guild.members:
                      if hacker.bot != True and role in hacker.roles:
                        try:
                          await hacker.remove_roles(role,reason="Removerole Humans Command Executed By: {}".format(ctx.author))
                          a += 1  
                        except Exception as e:
                          print(e)
                                                 
                            
                    await interaction.channel.send(
                           content=f"✅ | Successfully Removed {role.mention} From {a} Human(s) .")
                else:
                    await interaction.response.edit_message(
                        content=
                          "I am missing permission.\ntry giving me permissions and retry",
                            embed=None,
                               view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
        async def button1_callback(interaction: discord.Interaction):
            if interaction.user == ctx.author:
                embed2 = discord.Embed(
                     color=self.color,
                    description=f"Ok I will Not Remove {role.mention} From Any Humans .")
                await interaction.response.edit_message( embed=embed2, view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
        test = [member for member in ctx.guild.members if all([not member.bot, role in member.roles])]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"| Already No Humans Have {role.mention} .", color=self.color))
        else:
            embed = discord.Embed(
      color=self.color,
      description=f'**Are you sure you want to remove {role.mention} from {len(test)} humans in this guild?**') 
            view = View()
            button.callback = button_callback
            button1.callback = button1_callback
            view.add_item(button)
            view.add_item(button1)
            await ctx.reply(embed=embed, view=view, mention_author=False)
    else:
        hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
        hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.send(embed=hacker5, mention_author=False)                    
                            
                    



  @rrole.command( description="Removes a role from all the bots in the server .")
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.has_permissions(administrator=True)
  async def rrole_bots(self, ctx, *,role: discord.Role):
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
        button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="✅")
        button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="⚠")
        async def button_callback(interaction: discord.Interaction):
            a = 0
            if interaction.user == ctx.author:
                if interaction.guild.me.guild_permissions.ban_members:
                    embed1 = discord.Embed(
                     color=self.color,
                    description=f"Removing {role.mention} from all bots .")
                    await interaction.response.edit_message(
                     embed=embed1, view=None)
                    for hacker in interaction.guild.members:
                      if hacker.bot and role in hacker.roles:
                        try:
                          await hacker.remove_roles(role,reason="Removerole Bots Command Executed By: {}".format(ctx.author))
                          a += 1  
                        except Exception as e:
                          print(e)
                            
                    await interaction.channel.send(
            content=f"✅ | Successfully Removed {role.mention} From {a} Bot(s) .")
                else:
                    await interaction.response.edit_message(
                         content=
                           "I am missing permission.\ntry giving me permissions and retry",
                              embed=None,
                                  view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
                
        async def button1_callback(interaction: discord.Interaction):
            if interaction.user == ctx.author:
                embed2 = discord.Embed(
                     color=self.color,
                    description=f"Ok I will Not Remove {role.mention} From Any Bots .")
                await interaction.response.edit_message(
          embed=embed2, view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
        test = [member for member in ctx.guild.members if all([member.bot, role in member.roles])]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"| Already No Bots Have {role.mention} .", color=self.color))
        else:
            embed = discord.Embed(
      color=self.color,
      description=f'**Are you sure you want to remove {role.mention} from {len(test)} bots in this guild?**') 
            view = View()
            button.callback = button_callback
            button1.callback = button1_callback
            view.add_item(button)
            view.add_item(button1)
            await ctx.reply(embed=embed, view=view, mention_author=False)
    else:
        hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
        hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.send(embed=hacker5, mention_author=False)
                            
                            
                    
                    
                    



  @rrole.command( description="Removes a role from all the unverified members in the server .")
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.has_permissions(administrator=True)
  async def rrole_unverified(self, ctx, *,role: discord.Role):
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
        button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="✅")
        button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="⚠")
        async def button_callback(interaction: discord.Interaction):
            a = 0
            if interaction.user == ctx.author:
                if interaction.guild.me.guild_permissions.ban_members:
                  embed1 = discord.Embed(
                     color=self.color,
                    description=f"Removing {role.mention} from all unverifed members .")
                  await interaction.response.edit_message(
                     embed=embed1, view=None)
                  for hacker in interaction.guild.members:
                    if hacker.avatar is None and role in hacker.roles:
                      try:
                        await hacker.remove_roles(role,reason="Removerole Unverifed Command Executed By: {}".format(ctx.author))
                        a += 1 
                      except Exception as e:
                        print(e)
                                                                                                                        
                  await interaction.channel.send(
            content=f"✅ | Successfully Removed {role.mention} From {a} Unverified Member(s) .")
                else:
                    await interaction.response.edit_message(
                         content=
                           "I am missing permission.\ntry giving me permissions and retry",
                              embed=None,
                                  view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
                
        async def button1_callback(interaction: discord.Interaction):
            if interaction.user == ctx.author:
                embed2 = discord.Embed(
                     color=self.color,
                    description=f"Ok I will Not Remove {role.mention} From Any Unverified Members .")
                await interaction.response.edit_message(
          embed=embed2, view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
        embed = discord.Embed(
      color=self.color,
      description=f'**Are you sure you want to remove {role.mention} from all unverified members in this guild?**')
        view = View()
        button.callback = button_callback
        button1.callback = button1_callback
        view.add_item(button)
        view.add_item(button1)
        await ctx.reply(embed=embed, view=view, mention_author=False)
    else:
        hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
        hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.send(embed=hacker5, mention_author=False)     
        
        
        
  @rrole.command(name="all", description="Removes a role from all members in the server .")
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.has_permissions(administrator=True)
  async def rrole_all(self, ctx, *,role: discord.Role):
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
        button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="✅")
        button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="⚠")
        async def button_callback(interaction: discord.Interaction):
            a = 0
            if interaction.user == ctx.author:
                if interaction.guild.me.guild_permissions.ban_members:
                  embed1 = discord.Embed(
                     color=self.color,
                    description=f"Removing {role.mention} from all members .")
                  await interaction.response.edit_message(
                     embed=embed1, view=None)
                  for hacker in interaction.guild.members:
                    try:
                        await hacker.remove_roles(role,reason="Removerole All Command Executed By: {}".format(ctx.author))
                        a += 1  
                    except Exception as e:
                        print(e)
                                                                 
                                                                                                                  
                  await interaction.channel.send(
            content=f"✅ | Successfully Removed {role.mention} From {a} Member(s) .")
                else:
                    await interaction.response.edit_message(
                         content=
                           "I am missing permission.\ntry giving me permissions and retry",
                              embed=None,
                                  view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
                
        async def button1_callback(interaction: discord.Interaction):
            if interaction.user == ctx.author:
                embed2 = discord.Embed(
                     color=self.color,
                    description=f"Ok I will Not Remove {role.mention} From Anyone .")
                await interaction.response.edit_message(
                 embed=embed2, view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
        test = [member for member in ctx.guild.members if role in member.roles]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"| Already No Bots Have {role.mention} .", color=self.color))
        else:
            embed = discord.Embed(
                color=self.color,
                  description=f'**Are you sure you want to remove {role.mention} from {len(test)} members**')
            view = View()
            button.callback = button_callback
            button1.callback = button1_callback
            view.add_item(button)
            view.add_item(button1)
            await ctx.reply(embed=embed, view=view, mention_author=False)
    else:
        hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
        hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.send(embed=hacker5, mention_author=False) 