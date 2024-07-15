from __future__ import annotations
import os
import discord
from discord.ext import commands
from utils.Tools import *
from discord import *
from utils.config import OWNER_IDS, No_Prefix
import json
import typing
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator
from typing import Optional






class Hacker121(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.color = 0x2f3136


                
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        await self.bot.wait_until_ready()
        if message.guild is None:
            return
        if not message.guild.me.guild_permissions.read_messages:
            return
        if not message.guild.me.guild_permissions.read_message_history:
            return
        if not message.guild.me.guild_permissions.view_channel:
            return
        if not message.guild.me.guild_permissions.send_messages:
            return
        try:
            if message is not None:
                with open("autoresponse.json", "r") as f:
                    autoresponse = json.load(f)
                if str(message.guild.id) in autoresponse:
                    ans = autoresponse[str(
                        message.guild.id)][message.content.lower()]
                    return await message.channel.send(ans)
                return 
            return 
        except:
            pass
                
                


