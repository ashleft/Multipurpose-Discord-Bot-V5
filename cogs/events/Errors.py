import discord, json
from discord.ext import commands
from utils.config import serverLink
from core import Astroz, Cog, Context
from utils.Tools import *
class Errors(Cog):
  def __init__(self, client:Astroz):
    self.client = client


  @commands.Cog.listener()
  async def on_command_error(self, ctx: Context, error):
       
    with open('blacklist.json', 'r') as f:
      data = json.load(f)
      
    if isinstance(error, commands.CommandNotFound):
      return
  
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send_help(ctx.command)
      ctx.command.reset_cooldown(ctx) 
    if isinstance(error, commands.CheckFailure):
      data1 = getIgnore(ctx.guild.id)
      ch = data1["channel"]
      iuser = data1["user"]
      bl = discord.Embed(description=f"You are blacklisted from using my commannds.\nreason could be excessive use or spamming commands\nJoin our [Support Server]({serverLink}) to appeal .", color=discord.Colour(0x2f3136))
      embed = discord.Embed(description="This Channel is in ignored channel list try my commands in another channel .", color=discord.Colour(0x2f3136))
      ign = discord.Embed(description=f"You are set as a ignored users for {ctx.guild.name} .\nTry my commands or modules in another guild .", color=discord.Colour(0x2f3136))
        
      if str(ctx.author.id) in data["ids"]:
        return  
       # await ctx.reply(embed=bl, mention_author=False,delete_after=8)

      if str(ctx.channel.id) in ch:
        await ctx.reply(embed=embed,delete_after=8)
        return  
        
      if str(ctx.author.id) in iuser:
        await ctx.reply(embed=ign,delete_after=8)
        return  
      
            
    if isinstance(error, commands.NoPrivateMessage):
      hacker = discord.Embed(color=0x2f3136,description=f"You Can\'t Use My Commands In Dm(s)")
      hacker.set_author(name=ctx.author,
                                       icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
      hacker.set_thumbnail(url =ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
      await ctx.reply(embed=hacker,delete_after=20)
      return  
    if isinstance(error, commands.TooManyArguments):
      await ctx.send_help(ctx.command)
      ctx.command.reset_cooldown(ctx)
      return  
        
            
    if isinstance(error, commands.CommandOnCooldown):
      hacker = discord.Embed(color=0x2f3136,description=f"⚠ | {ctx.author.name} is on cooldown retry after {error.retry_after:.2f} second(s)")
      hacker.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
      hacker.set_thumbnail(url =ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
      await ctx.reply(embed=hacker,delete_after=10)
      return  

    if isinstance(error, commands.MaxConcurrencyReached):
      hacker = discord.Embed(color=0x2f3136,description=f"⚠ | This Command is already going on, let it finish and retry after")
      hacker.set_author(name=ctx.author,
                                       icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
      hacker.set_thumbnail(url =ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
      await ctx.reply(embed=hacker,delete_after=10)
      ctx.command.reset_cooldown(ctx)
      return  

    if isinstance(error, commands.MissingPermissions):
      missing = [
                perm.replace("_", " ").replace("guild", "server").title()
                for perm in error.missing_permissions
            ]
      if len(missing) > 2:
                fmt = "{}, and {}".format(", ".join(missing[:-1]), missing[-1])
      else:
                fmt = " and ".join(missing)
      hacker = discord.Embed(color=0x2f3136,description=f"⚠ | You lack `{fmt}` permission(s) to run `{ctx.command.name}` command!")
      hacker.set_author(name=ctx.author,
                                       icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
      hacker.set_thumbnail(url =ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
      await ctx.reply(embed=hacker,delete_after=6)
      ctx.command.reset_cooldown(ctx)
      return  

    if isinstance(error, commands.BadArgument):
      await ctx.send_help(ctx.command)
      ctx.command.reset_cooldown(ctx)
    if isinstance(error, commands.BotMissingPermissions):
      missing = ", ".join(error.missing_perms)
      await ctx.send(f'| I need the **{missing}** to run the **{ctx.command.name}** command!', delete_after=10)
      return  
      
    if isinstance(error, discord.HTTPException):
      return  
    elif isinstance(error, commands.CommandInvokeError):
      return  
    