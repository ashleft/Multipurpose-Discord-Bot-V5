import discord
import datetime
from discord.ext import commands, tasks
import httpx
from utils.Tools import *
from core import Astroz, Cog
import aiohttp
from utils.config import TOKEN
import time
import asyncio
import aiohttp
import tasksio
from discord.ext import tasks
import random
import logging 
import sys
import setuptools
from itertools import cycle



logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

proxies = open('proxies.txt').read().split('\n')
proxs = cycle(proxies)
proxies={"http": 'http://' + next(proxs)}

class member_update(commands.Cog):
    def __init__(self, client):
        self.client = client      
        self.headers = {"Authorization": f"Bot {TOKEN}"}


    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member,
                               after: discord.Member) -> None:
        await self.client.wait_until_ready()
        guild = after.guild
        data = getConfig(guild.id)
        anti = getanti(guild.id)
        punishment = data["punishment"]
        wlrole = data['wlrole']  
        wled = data["whitelisted"]
        
        reason = "Updating Member Roles | Not Whitelisted"
        api = random.randint(8,9)
        if not guild:
            return
        if guild and not guild.me.guild_permissions.view_audit_log:
            return            
        async for entry in guild.audit_logs(
                limit=1):    
            if entry.user == guild.owner or str(entry.user.id) in wled or anti == "off" or entry.user.id == self.client.user.id or entry.user.guild_permissions.manage_roles == False:
                return
                                  
            else:
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    if entry.action == discord.AuditLogAction.member_role_update:
                     if punishment == "ban":
                        async with session.put(f"https://discord.com/api/v{api}/guilds/%s/bans/%s" % (guild.id, entry.user.id), json={"reason": reason}) as r:
                            for role in after.roles:
                                if role not in before.roles:
                                    try:
                                        await after.remove_roles(role,reason=reason)
                                    except Exception as e:
                                        print(e)
                            if r.status in (200, 201, 204):
                                logging.info("Successfully banned %s" % (entry.user.id))
                            return 
                                
                     elif punishment == "kick":
                        async with session.delete(f"https://discord.com/api/v{api}/guilds/%s/members/%s" % (guild.id, entry.user.id), json={"reason": reason}) as r2:
                            for role in after.roles:
                                if role not in before.roles:
                                    try:
                                        await after.remove_roles(role,reason=reason)
                                    except Exception as e:
                                        print(e)
                            if r2.status in (200, 201, 204):
                                logging.info("Successfully kicked %s" % (entry.user.id))
                            return 
                     elif punishment == "none":
                        for role in after.roles:
                            if role not in before.roles:
                                try:
                                    await after.remove_roles(role,reason=reason)
                                except Exception as e:
                                    print(e)
                    else:
                        return 
                        
                    