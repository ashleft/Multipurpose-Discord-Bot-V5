import discord
from discord.ext import commands
import datetime
import re
import json
from core import Astroz, Cog
from utils.Tools import *
import aiohttp
import random 


class automodevent(Cog):
    def __init__(self, client: Astroz):
        self.client = client
        self.spam_cd_mapping = commands.CooldownMapping.from_cooldown(4, 7, commands.BucketType.member)
        self.spam_punish_cooldown_cd_mapping = commands.CooldownMapping.from_cooldown(1, 10, commands.BucketType.member)
        self.headers = {"Authorization": f"Bot OTA2MDg1NTc4OTA5NTQ4NTU0.GY8nds.JJ-k2ckUpGokqxdvbwlgJwmklthFvzqLR0qcwI"}

    @commands.Cog.listener()    
    async def on_message(self, message):
      if not message.guild:
        return
      mem = message.author
      invite_regex = re.compile(r"(?:https?://)?discord(?:app)?\.(?:com/invite|gg)/[a-zA-Z0-9]+/?")
      link_regex = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
      invite_matches = invite_regex.findall(message.content)
      link_matches = link_regex.findall(message.content)
      data = getExtra(message.guild.id)
      antiSpam = data["antiSpam"]
      antiLink = data["antiLink"]
      antiinvites =data["antiinvites"]
      wled = data["whitelisted"]
      ch = data['ignorechannels']  
      hacker = message.guild.get_member(message.author.id)
      
      api = random.randint(8,9)
      reason = f"{self.client.user.name} | Automod Antispam"
      try:
                if antiSpam is True:
                  if str(message.author.id) in wled or message.author == message.guild.owner or message.author.id == self.client.user.id or str(message.channel.id) in ch:
                    return
                  bucket = self.spam_cd_mapping.get_bucket(message)
                  retry = bucket.update_rate_limit()
                  if retry:                     
                      
                      if data["punishment"] == "mute":
                        now = discord.utils.utcnow()
                        await message.author.timeout(now + datetime.timedelta(minutes=15), reason=f"{self.client.user.name} | Automod AntiSpam")
                        hackerok = discord.Embed(color=0x2f3136,description=f"✅ | Successfully Muted {message.author} For Spamming")
                        hackerok.set_author(name=message.author, icon_url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
                        hackerok.set_thumbnail(url =message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
                        await message.channel.send(embed=hackerok,delete_after=6)
                        return await message.delete()
  
                                                      
                      if data["punishment"] == "kick":
                          async with aiohttp.ClientSession(headers=self.headers) as session:
                              async with session.delete(f"https://discord.com/api/v{api}/guilds/%s/members/%s" % (message.guild.id, message.author.id), json={"reason": reason}) as r2:
                                  if r2.status in (200, 201, 204):
                                      hacker = discord.Embed(color=0x2f3136,description=f"✅ | Successfully Kicked {message.author} For Spamming .")
                                      hacker.set_author(name=message.author, icon_url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
                                      hacker.set_thumbnail(url =message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
                                      await message.channel.send(embed=hacker,delete_after=6)
                                      return await message.delete()

                                                                                                
                                  else:
                                      pass
                                      
                        

                      elif data["punishment"] == "ban":
                          async with aiohttp.ClientSession(headers=self.headers) as bansession:
                              async with session.put(f"https://discord.com/api/v{api}/guilds/%s/bans/%s" % (message.guild.id, message.author.id), json={"reason": reason}) as rr:
                                  if rr.status in (200, 201, 204):
                                      hacker1 = discord.Embed(color=0x2f3136,description=f"✅ | Successfully Banned {message.author} For Spamming .")
                                      hacker1.set_author(name=message.author, icon_url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
                                      hacker1.set_thumbnail(url =message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
                                      await message.channel.send(embed=hacker1,delete_after=6)
                                      return await message.delete()
   
                                  else:
                                      pass
                if antiinvites is True:
                    if str(message.author.id) in wled or message.author == message.guild.owner or message.author.id == self.client.user.id or str(message.channel.id) in ch:
                        return
                    if invite_matches:
                        
                        if data["punishment"] == "mute":
                             now = discord.utils.utcnow()
                             await message.author.timeout(now + datetime.timedelta(minutes=15), reason=f"{self.client.user.name} | Anti Discord Invites")
                             hacker5 = discord.Embed(color=0x2f3136,description=f"✅ | Successfully Muted {message.author} For Sending Discord Server Invites")
                             hacker5.set_author(name=message.author, icon_url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
                             hacker5.set_thumbnail(url =message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
                             await message.channel.send(embed=hacker5,delete_after=6)
                             return await message.delete()

                              
                          
                          
                          
                        if data["punishment"] == "kick":
                            reason =f"{self.client.user.name} | Automod Anti Discord Invites"
                            async with aiohttp.ClientSession(headers=self.headers) as session:
                              async with session.delete(f"https://discord.com/api/v{api}/guilds/%s/members/%s" % (message.guild.id, message.author.id), json={"reason": reason}) as r2:
                                  if r2.status in (200, 201, 204):
                                      hacker3 = discord.Embed(color=0x2f3136,description=f"✅ | Successfully Kicked {message.author} For For Sending Discord Server Invites .")
                                      hacker3.set_author(name=message.author, icon_url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
                                      hacker3.set_thumbnail(url =message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
                                      await message.channel.send(embed=hacker3,delete_after=6)
                                      return await message.delete()

                                  else:
                                      pass
                        elif data["punishment"] == "ban":
                            reason =f"{self.client.user.name} | Automod Anti Discord Invites"
                            async with aiohttp.ClientSession(headers=self.headers) as bansession:
                              async with session.put(f"https://discord.com/api/v{api}/guilds/%s/bans/%s" % (message.guild.id, message.author.id), json={"reason": reason}) as rr:
                                  if rr.status in (200, 201, 204):
                                      hacker4= discord.Embed(color=0x2f3136,description=f"✅ | Successfully Banned {message.author} For Sending Discord Server Invites .")
                                      hacker4.set_author(name=message.author, icon_url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
                                      hacker4.set_thumbnail(url =message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
                                      await message.channel.send(embed=hacker4,delete_after=6)
                                      return await message.delete()
    
                                  else:
                                      pass


                             ########################
                if antiLink is True:
                    if str(message.author.id) in wled or message.author == message.guild.owner or message.author.id == self.client.user.id or str(message.channel.id) in ch:
                        return
                    if link_matches:
                        
                        if data["punishment"] == "mute":
                          now = discord.utils.utcnow()
                          await message.author.timeout(now + datetime.timedelta(minutes=15), reason=f"{self.client.user.name} | Automod Anti Link")
                          hacker8 = discord.Embed(color=0x2f3136,description=f"✅ | Successfully Muted {message.author} For Sending Links .")
                          hacker8.set_author(name=message.author, icon_url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
                          hacker8.set_thumbnail(url =message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
                          await message.channel.send(embed=hacker8,delete_after=6)
                          return await message.delete()
                       
                        if data["punishment"] == "kick":
                            reason =f"{self.client.user.name} | Automod Anti Links"
                            async with aiohttp.ClientSession(headers=self.headers) as session:
                              async with session.delete(f"https://discord.com/api/v{api}/guilds/%s/members/%s" % (message.guild.id, message.author.id), json={"reason": reason}) as r2:
                                  if r2.status in (200, 201, 204):
                                      hacker6 = discord.Embed(color=0x2f3136,description=f"✅ | Successfully Kicked {message.author} For For Sending Links .")
                                      hacker6.set_author(name=message.author, icon_url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
                                      hacker6.set_thumbnail(url =message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
                                      await message.channel.send(embed=hacker6,delete_after=6)
                                      return await message.delete()
                                  else:
                                      pass
                                      
                            


                        elif data["punishment"] == "ban":
                            reason =f"{self.client.user.name} | Automod Anti Link"
                            async with aiohttp.ClientSession(headers=self.headers) as bansession:
                              async with session.put(f"https://discord.com/api/v{api}/guilds/%s/bans/%s" % (message.guild.id, message.author.id), json={"reason": reason}) as rr:
                                  if rr.status in (200, 201, 204):
                                      hacker7 = discord.Embed(color=0x2f3136,description=f"✅ | Successfully Kicked {message.author} For For Sending Links .")
                                      hacker7.set_author(name=message.author, icon_url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
                                      hacker7.set_thumbnail(url =message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
                                      await message.channel.send(embed=hacker7,delete_after=6)
                                      return await message.delete()
                                  else:
                                      pass

                    else:
                      return
      except Exception as error:
          print(error)