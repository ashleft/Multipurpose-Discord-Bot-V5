from __future__ import annotations
from discord.ext import commands
from utils.Tools import *
from discord import *
from utils.config import OWNER_IDS, No_Prefix
import json, discord
import typing
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator
from typing import Optional
import asyncio
from discord.ui import Button, View
from typing import *

class Owner1(commands.Cog):

  def __init__(self, client):
    self.client = client
    self.color = 0x2f3136



  @commands.group(
    name="blg",
    help="Allows you to add guild in blacklist (owner only command)")
  @commands.is_owner()
  async def _bl(self, ctx):
    if ctx.invoked_subcommand is None:
      await ctx.send_help(ctx.command)

      
  @_bl.command(name="list")
  @commands.is_owner()
  async def bl_list(self, ctx):
    with open("guild-bl.json") as f:
      np = json.load(f)
      nplist = np["guilds"]
      entries = [
          f"`[{no}]` | ID: {mem})"
          for no, mem in enumerate(np['guilds'], start=1)
        ]
      paginator = Paginator(source=DescriptionEmbedPaginator(
        entries=entries,
        title=f"Blacklisted Guilds of {self.client.user.name} - {len(nplist)}",
        description="",
        per_page=10,
        color=self.color),
                            ctx=ctx)
      await paginator.paginate()      
      
  @_bl.command(name="add")
  @commands.is_owner()
  async def bl_add(self, ctx, guild: str):
    with open('guild-bl.json', 'r') as idk:
      data = json.load(idk)
    np = data["guilds"]
    if guild in np:
      embed = discord.Embed(
        description=
        f"**The guild is already blacklisted**",
        color=self.color)
      await ctx.reply(embed=embed)
      return
    else:
      data["guilds"].append(guild)
    with open('guild-bl.json', 'w') as idk:
      json.dump(data, idk, indent=4)
      embed1 = discord.Embed(
        description=
        f"✅ | Successfully Blacklisted {guild} From using me ." ,
        color=self.color)
      await self.client.get_guild(guild).leave()
      await ctx.reply(embed=embed1)

  @_bl.command(name="remove")
  @commands.is_owner()
  async def _bl_remove(self, ctx, guild:str):
    with open('guild-bl.json', 'r') as idk:
      data = json.load(idk)
    np = data["guilds"]
    if guild not in np:
      embed = discord.Embed(
        description="**{} is not in blacklisted guild**".format(guild), color=self.color)
      await ctx.reply(embed=embed)
      return
    else:
      data["guilds"].remove(guild)
    with open('guild-bl.json', 'w') as idk:
      json.dump(data, idk, indent=4)
      embed2 = discord.Embed(
        description=
        f"✅ | Removed from blacklist {guild}",
        color=self.color)

      await ctx.reply(embed=embed2)
    	    
  @commands.Cog.listener(name="on_guild_join")
  async def __guild_blacklist_event__(self, guild):
      with open("guild-bl.json") as f:
          data = json.load(f)
      #with open("lund.json") as ok:
          #data2 = json.load(ok)
      if guild.id in data["guilds"]:
        try:
          await guild.leave()
        except Exception as e:
          await self.client.get_channel(1125826395625488447).send(e)
    #  if guild.owner.id in data2["lund"]:
      #  try:
         # await guild.leave()
       # except Exception as e:
       #   await self.client.get_channel(1125826395625488447).send(e)
      else:
          pass
          
 
        	
        
       
       
       
  @commands.group(
    name="chutiya",
    )
  @commands.is_owner()
  async def _chutiya(self, ctx):
    if ctx.invoked_subcommand is None:
      await ctx.send_help(ctx.command)

      
  @_chutiya.command(name="list")
  @commands.is_owner()
  async def bl_list(self, ctx):
    with open("lund.json") as f:
      np = json.load(f)
      nplist = np["lund"]
      entries = [
          f"`[{no}]` | ID: {mem})"
          for no, mem in enumerate(np['lund'], start=1)
        ]
      paginator = Paginator(source=DescriptionEmbedPaginator(
        entries=entries,
        title=f"Blacklisted Owners of {self.client.user.name} - {len(nplist)}",
        description="",
        per_page=10,
        color=self.color),
                            ctx=ctx)
      await paginator.paginate()      
      
  @_chutiya.command(name="add")
  @commands.is_owner()
  async def chutiya_add(self, ctx, guild:Optional[Union[discord.Member,
                                         discord.User]] = None):
    with open('lund.json', 'r') as idk:
      data = json.load(idk)
    np = data["lund"]
    if guild.id in np:
      embed = discord.Embed(
        description=
        f"**The guild owner is already blacklisted**",
        color=self.color)
      await ctx.reply(embed=embed)
      return
    else:
      data["lund"].append(guild.id)
    with open('lund.json', 'w') as idk:
      json.dump(data, idk, indent=4)
      embed1 = discord.Embed(
        description=
        f"✅ | Successfully Blacklisted {guild} From using me ." ,
        color=self.color)
      await ctx.reply(embed=embed1)

  @_chutiya.command(name="remove")
  @commands.is_owner()
  async def _chutiya_remove(self, ctx, guild:Optional[Union[discord.Member,
                                         discord.User]] = None):
    with open('lund.json', 'r') as idk:
      data = json.load(idk)
    np = data["lund"]
    if guild.id not in np:
      embed = discord.Embed(
        description="**{} is not in blacklisted guild owners**".format(guild), color=self.color)
      await ctx.reply(embed=embed)
      return
    else:
      data["lund"].remove(guild.id)
    with open('lund.json', 'w') as idk:
      json.dump(data, idk, indent=4)
      embed2 = discord.Embed(
        description=
        f"✅ | Removed from blacklist {guild}",
        color=self.color)

      await ctx.reply(embed=embed2)
    	    