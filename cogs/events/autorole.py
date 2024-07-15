import discord
from discord.utils import *
import aiohttp
from core import Astroz, Cog
import json
from utils.Tools import *
from discord.ext import commands




class Autorole2(Cog):
    def __init__(self, bot: Astroz):
        self.bot = bot
        self.headers = {"Authorization": f"Bot OTA2MDg1NTc4OTA5NTQ4NTU0.GY8nds.JJ-k2ckUpGokqxdvbwlgJwmklthFvzqLR0qcwI"}



    @Cog.listener()
    async def on_member_join(self, member):
        data = getautorole(member.guild.id)
        arb = data["bots"]
        arh = data["humans"]
        if arb == []:
            return
        else:
            if member.bot != True:
                return
            elif member.bot:
                for role in arb:
                    try:
                        await member.add_roles(discord.Object(id=int(role)), reason=f"{self.bot.user.name} | Auto Role")
                    except Exception as e:
                        print(e)
                    
          

    @Cog.listener()
    async def on_member_join(self, member):
        data = getautorole(member.guild.id)
        arb = data["bots"]
        arh = data["humans"]
        reason = f"{self.bot.user.name} | Autorole"
        if arh == []:
            return
        else:
            if member.bot:
                return
            elif member.bot != True:
                async with aiohttp.ClientSession(headers=self.headers, connector=None) as session:
                    for role in arh:
                        try:
                            async with session.put(f"https://discord.com/api/v10/guilds/{member.guild.id}/members/{member.id}/roles/{int(role)}", json={"reason": reason}) as req:
                                print(req.status)
                        except:
                            pass
                       