import discord
from discord.ext import commands
from core import Astroz, Cog
from discord.utils import *
from discord import *
from utils.Tools import *

from discord.utils import get




class Vcroles2(Cog):
    def __init__(self, bot: Astroz):
        self.bot = bot



    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        data = getvcrole(member.guild.id)
        if member.bot:
            if data["bots"] == "":
                return
            else:
                if not before.channel and after.channel:
                    r = data["bots"]
                    try:
                        br = get(member.guild.roles, id=r)
                        await member.add_roles(br, reason=f"{self.bot.user.name} | VC Roles (Joined VC)")
                    except Exception as e:
                        print(e)
                        
                    
                elif before.channel and not after.channel:
                    r1 = data["bots"]
                    try:
                        br1 = get(member.guild.roles, id=r1)
                        await member.remove_roles(br1, reason=f"{self.bot.user.name} | VC Roles (Left VC)")
                    except Exception as e:
                        print(e)
                        
                    
        elif member.bot != True:
            if data["humans"] == "":
                return
            else:
                if not before.channel and after.channel:
                    r2 = data["humans"]
                    try:
                        br2 = get(member.guild.roles, id=r2)
                        await member.add_roles(br2, reason=f"{self.bot.user.name} | VC Roles (Joined VC)")
                    except Exception as e:
                        print(e)
                    
                elif before.channel and not after.channel:
                    r3 = data["humans"]
                    try:
                        br3 = get(member.guild.roles, id=r3)
                        await member.remove_roles(br3, reason=f"{self.bot.user.name} | VC Roles (Left VC)")
                    except Exception as e:
                        print(e)
                    