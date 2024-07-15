import discord
from utils.config import BotName, OWNER_IDS
from discord.ext import commands,tasks

import os

import sys

import datetime, time

import re

#from dateutil.relativedelta import relativedelta

from typing import *

import json

import asyncio
from utils.Tools import *

anp=[289100850285117460,986247254161637396,1031105449736540200,1114412867387654154,1033579545254711336,875617517714964530,859282589046013953,735003878424313908,637114419641581568,323429313032486922,259176352748404736]
def convert(date):

    pos = ["s", "m", "h", "d"]

    time_dic = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}

    i = {"s": "Seconds", "m": "Minutes", "h": "Hours", "d": "Days"}

    unit = date[-1]

    if unit not in pos:

        return -1

    try:

        val = int(date[:-1])

    except ValueError:

        return -2

    if val == 1:

        return val * time_dic[unit], i[unit][:-1]

    else:

        return val * time_dic[unit], i[unit]
async def remove_premium(user):

    with open("premium.json", "r") as f:

        data = json.load(f)

        if str(user.id) not in data:

            return

        elif str(user.id) in data:

            data.pop(user.id)

    with open("premium.json", "w") as f:

        json.dump(data, f, indent=4)

#async def is_guild_premium(guild):

	#with open("premium.json", "r") as file:

	#	data = json.load(file)

#	for userId in data:

		#data1 = data[userId]  
  #  if str(guild.id) in data1["premium_guilds"]:
      #  return True  
    #else:
       # return False
			

		


    

class Premium(commands.Cog):

    def __init__(self, bot):
 
        self.bot = bot
        self.color = 0x2f3136
        self.premium_remover.start()

  #  self._premium = asyncio.Lock()

        

    def cog_unload(self):

        self.premium_remover.cancel()

    @tasks.loop(seconds=5)
    async def premium_remover(self):
        await self.bot.wait_until_ready()

        with open("premium.json", "r") as f:
            data = json.load(f)

        if len(data) == 0:
            return
        for premium_user in list(data.keys()):
            data2 = data[premium_user]

            if int(time.time()) > data2["expire_at"]:
                if str(premium_user) not in data:
                    pass
                else:
                    del data[str(premium_user)]
                    with open("premium.json", "w") as f:
                        json.dump(data, f, indent=4)

      
    @commands.group(

  name="prime", 

  aliases=["pre"],

  invoke_without_command=True

  )
    @commands.is_owner()
    async def _premium(self, ctx):
        prefix=ctx.prefix
        hacker = discord.utils.get(self.bot.users, id=OWNER_IDS)

        listem = discord.Embed(title=f"Premium (9)", colour=self.color,
                                     description=f"""<...> Duty | [...] Optional\n\n
{prefix}premium add <user> <tier>
Give premium to a user.

{prefix}premium remove <user>
Remove a user from premium list.

{prefix}premium status <user>
Show premium status of user.

""")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by {str(hacker)}" ,  icon_url=hacker.avatar.url)
        await ctx.send(embed=listem)   



    @_premium.command(

  name="add", 

  aliases=["a", "set"]

  ) 

    #@commands.is_owner()

    async def _premium_add(self, ctx, user: Union[discord.User, discord.Member], tier_name: str):
      if ctx.author.id in anp:           
        with open("premium.json", "r") as file:

	
      #  with 
  	        data = json.load(file)

        if tier_name.lower() in ["gold", "golden", "g"]:
         

            tier = "Gold Tier"
 
            convert_time = "30d"

            guilds = 10

            tier_act = "1 Month"

        elif tier_name.lower() in ["platinum", "platinium", "pltnm"]:

            tier = "Platinum Tier"

            convert_time = "90d"

            guilds = 20

            tier_act = "3 Months"

        elif tier_name.lower() in ["diamond", "💎", "dmnd"]:

            tier = "Diamond Tier"

            convert_time = "365d"

            guilds = 60

            tier_act = "1 Year"

        converted_time = convert(convert_time)

        now = int(time.time())
        config = {
            "tier": None,
            "guild_limit": 0,
            "premium_guilds": [],
            "expire_at": None
        }
        data[str(user.id)] = config
        if str(user.id) in data:

        
           # del data[str(user.id)]

          

         # data[str(user.id)] = config

            data[str(user.id)]["tier"] = tier

            data[str(user.id)]["guild_limit"] = guilds

            data[str(user.id)]["premium_guilds"] = []

            data[str(user.id)]["expire_at"] = now + converted_time[0]

        if str(user.id) not in data:

          

       #   data[str(user.id)] = config

            data[str(user.id)]["tier"] = tier

            data[str(user.id)]["guild_limit"] = guilds

            data[str(user.id)]["premium_guilds"] = []

            data[str(user.id)]["expire_at"] = now + converted_time[0]

        with open("premium.json", "w") as file1:

            json.dump(data, file1, indent=4)

      	

            _e = discord.Embed(color=self.color,title="",

              description="<:GreenTick:1029990379623292938> | Succesfully activated `{}` premium of {} for `{}`".format(tier, user.mention, tier_act) )
            _e.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.send(embed=_e)
      else:
          await ctx.send(f"this command can only be used by team members of {BotName} !")
  
            
                

    @_premium.command(

  name="status"

  ) 

    @blacklist_check()
    @ignore_check()
    async def _premium_status(self, ctx, user: Optional[discord.User] = None):
        mem = user or ctx.author
        with open("premium.json", "r") as f:
            data = json.load(f)

        if str(mem.id) in data:

            d2 = data[str(mem.id)]

            t = d2["tier"]

            e = d2["expire_at"]

            embed2 = discord.Embed(color=self.color)
            embed2.set_author(
        name=f"Profile For {mem}",
        icon_url=mem.avatar.url if mem.avatar else mem.default_avatar.url)
            embed2.add_field(name=f"{BotName}`s Premium", value=f"**`Type`:**{t}\n**`Expire`:**<t:{e}:F>", inline=False)
            embed2.set_thumbnail(
        url=mem.avatar.url if mem.avatar else mem.default_avatar.url)
            await ctx.reply(embed=embed2, mention_author=False)        

        else:
            embed = discord.Embed(color=self.color,description=f"\n\n* Oops! Looks Like {mem} Don't Have Any Type Of Premium Plans To Be Displayed!*")
            embed.set_thumbnail(
        url=mem.avatar.url if mem.avatar else mem.default_avatar.url)
            embed2.set_author(
        name=f"Profile For {mem}",
        icon_url=mem.avatar.url if mem.avatar else mem.default_avatar.url)
            await ctx.send(embed=embed)




    @_premium.command(name="remove", 
  aliases=["r"]

  ) 
    async def _premium_remove(self, ctx, *,user: Union[discord.User, discord.Member]):
      if ctx.author.id in anp:           
        with open("premium.json", "r") as ok:
  	        data = json.load(ok)
        if str(user.id) not in data:
            pass      
        else:
            del data[str(user.id)]
            with open("premium.json", "w") as ok:
                json.dump(data,ok , indent=4)           
            _e = discord.Embed(color=self.color,title="",

             description=f"<:GreenTick:1029990379623292938> | Succesfully removed premium from {user.name} .")
            _e.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.send(embed=_e)    
      else:
          await ctx.send(f"this command can only be used by team members of {BotName} !")