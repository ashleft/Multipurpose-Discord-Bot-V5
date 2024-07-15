from discord.ext import commands
from core import Astroz, Cog
import discord, requests
import json
from utils.Tools import *
from utils.config import serverLink, whBL
from discord.ui import View, Button
import logging
from discord import Webhook


logging.basicConfig(
  level=logging.INFO,
  format=
  "\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
  datefmt="%H:%M:%S",
)


class Guild(Cog):

  def __init__(self, client: Astroz):
    self.client = client

  @commands.Cog.listener(name="on_guild_join")
  async def hacker(self, guild):
    rope = [
      inv for inv in await guild.invites()
      if inv.max_age == 0 and inv.max_uses == 0
    ]
    me = discord.SyncWebhook.from_url(whBL)
    
    channels = len(set(self.client.get_all_channels()))
    
    users = sum(g.member_count for g in self.client.guilds
                if g.member_count != None)
    
    c_at = int(guild.created_at.timestamp())
    
    embed = discord.Embed(color=0x2f3136)
    embed.set_author(name="Guild Joined",icon_url=self.client.user.avatar.url)
    embed.set_footer(text=self.client.user.name,icon_url=self.client.user.avatar.url)
    embed.add_field(
      name="**__Guild Information:__**",
      value=
      f"""Server Name: `{guild.name}`\nServer Id: `{guild.id}`\nServer Owner: [{guild.owner}](https://discord.com/users/{guild.owner.id})\nCreated At: <t:{c_at}:F>\nMember Count: `{len(guild.members)}`\nRoles: `{len(guild.roles)}`\nText Channels: `{len(guild.text_channels)}`\nVoice Channels: `{len(guild.voice_channels)}`\nThreads: `{len(guild.threads)}`\n""",
      inline=True)
    embed.add_field(
      name="**__Bot Info:__**",
      value=
      f"Servers: `{len(self.client.guilds)}`\nUsers: `{users}`\nChannels: `{channels}`",
      inline=False)
    
    if guild.icon is not None:
      embed.set_thumbnail(url=guild.icon.url)
    
    
    
    embed.timestamp = discord.utils.utcnow()
    me.send(f"{guild.id} | {rope[0]}" if rope else f"{guild.id} | No Pre-Made Invite Found",
                  embed=embed)
    if not guild.chunked:
      await guild.chunk()
    embed = discord.Embed(description=f"Thank you for adding me to your server!\n・ My default prefix is `.`\n・ You can use the `.help` command to get list of commands\n・ Our [support server]({serverLink}) or our team offers detailed information & guides for commands\n・ Feel free to join our [Support Server]({serverLink}) if you need help/support for anything related to the bot",color=0x2f3136)
    if guild.icon is not None:
      embed.set_author(name=guild.name, icon_url=guild.icon.url)
    embed.set_thumbnail(url=self.client.user.avatar.url)
    inv = Button(label='Invite Me', style=discord.ButtonStyle.link, url=f'https://discord.com/oauth2/authorize?client_id={self.client.user.id}&permissions=8&scope=bot%20applications.commands')
    sup = Button(label='Support Server', style=discord.ButtonStyle.link, url=f'{serverLink}')
    view = View()
    view.add_item(sup)
    view.add_item(inv)
    channel = discord.utils.get(guild.text_channels, name="general")
    if not channel:
      channels = [
        channel for channel in guild.text_channels
        if channel.permissions_for(guild.me).send_messages
      ]
      channel = channels[0]
      await channel.send(embed=embed,view=view)
      return 










  @commands.Cog.listener(name="on_guild_remove")
  async def on_g_remove(self, guild):
    idk = discord.SyncWebhook.from_url(whBL)
    channels = len(set(self.client.get_all_channels()))
    users = sum(g.member_count for g in self.client.guilds
                if g.member_count != None)
    
    c_at = int(guild.created_at.timestamp())
    embed = discord.Embed(color=0x2f3136)
    embed.set_author(name="Guild Removed",icon_url=self.client.user.avatar.url)
    embed.set_footer(text=self.client.user.name,icon_url=self.client.user.avatar.url)
    embed.add_field(
      name="**__Guild Information:__**",
      value=
      f"""Server Name: `{guild.name}`\nServer Id: `{guild.id}`\nServer Owner: [{guild.owner}](https://discord.com/users/{guild.owner.id})\nCreated At: <t:{c_at}:F>\nMember Count: `{len(guild.members)}`\nRoles: `{len(guild.roles)}`\nText Channels: `{len(guild.text_channels)}`\nVoice Channels: `{len(guild.voice_channels)}`\nThreads: `{len(guild.threads)}`\n""",
      inline=True)
    embed.add_field(
      name="**__Bot Info:__**",
      value=
      f"Servers: `{len(self.client.guilds)}`\nUsers: `{users}`\nChannels: `{channels}`",
      inline=False)
    if guild.icon is not None:
      embed.set_thumbnail(url=guild.icon.url)
    embed.timestamp = discord.utils.utcnow()
    idk.send(embed=embed)
    return 