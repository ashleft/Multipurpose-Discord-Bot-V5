import discord
from discord.utils import *
from core import Astroz, Cog
from utils.Tools import *
from utils.config import BotName, serverLink
from discord.ext import commands
from discord.ui import Button, View



class Autorole(Cog):
    def __init__(self, bot: Astroz):
        self.bot = bot
        
        
    @commands.Cog.listener(name="on_member_join")
    async def on_member_join(self, member):
        data = getautorole(member.guild.id)
        arb = data["bots"]
        arh = data["humans"]
        if arb == []:
            return
        else:
            if member.bot:
                for role in arb:
                    try:
                        await member.add_roles(discord.Object(id=int(role)), reason=f"{self.bot.user.name} | Autoroles")
                    except Exception as e:
                        print(e)
            else:
                pass                        
                        
    @commands.Cog.listener(name="on_guild_join") 
    async def send_msg_to_adder(self, guild: discord.Guild):
        async for entry in guild.audit_logs(limit=3):  
            if entry.action == discord.AuditLogAction.bot_add: 
                embed = discord.Embed(description=f"Thank you for adding me to your server!\n・ My default prefix is `.`\n・ You can use the `.help` command to get list of commands\n・ Our [support server]({serverLink}) or our team offers detailed information & guides for commands\n・ Feel free to join our [Support Server]({serverLink}) if you need help/support for anything related to the bot",color=0x2f3136)
                embed.set_thumbnail(url=entry.user.avatar.url if entry.user.avatar else entry.user.default_avatar.url)
                inv = Button(label='Invite Me', style=discord.ButtonStyle.link, url=f'https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot%20applications.commands')
                sup = Button(label='Support Server', style=discord.ButtonStyle.link, url=f'{serverLink}')
                vote = Button(label='Vote Me', style=discord.ButtonStyle.link, url=f'https://top.gg/bot/{self.bot.user.id}/vote')
                view = View()
                view.add_item(sup)
                view.add_item(inv)
                if guild.icon is not None:
                    embed.set_author(name=guild.name, icon_url=guild.icon.url)
               # view.add_item(vote)  
                try:
                    await entry.user.send(embed=embed,view=view)
                except Exception as e:
                    print(e)