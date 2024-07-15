from __future__ import annotations
import discord
import asyncio
import os
import logging
from discord.ext import commands
from utils.Tools import *
from discord.ext.commands import Context
from discord import app_commands
import time
import datetime
import re
from typing import *
from time import strftime
from core import Cog, Astroz, Context
from discord.ext import commands

logging.basicConfig(
    level=logging.INFO,
    format=
    "\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)



class BasicView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout = 60):
        super().__init__(timeout=timeout)
        self.ctx = ctx

    
      
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in [246469891761111051]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command .", ephemeral=True)
            return False
        return True
    
    
    
    
class Autodel(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None
        
    @discord.ui.button(label="10s", custom_id='ten', style=discord.ButtonStyle.green)
    async def _10(self, interaction, button):
        self.value = '10'
        self.stop()

    @discord.ui.button(label="15s", custom_id='fifteen', style=discord.ButtonStyle.green)
    async def _15(self, interaction, button):
        self.value = '15'
        self.stop()

    @discord.ui.button(label="20s", custom_id='twenty', style=discord.ButtonStyle.green)
    async def _20(self, interaction, button):
        self.value = '20'
        self.stop()

    @discord.ui.button(label="25s", custom_id='twentyfive', style=discord.ButtonStyle.green)
    async def _25(self, interaction, button):
        self.value = '25'
        self.stop()

    @discord.ui.button(label="30s", custom_id='thirty', style=discord.ButtonStyle.green)
    async def _30(self, interaction, button):
        self.value = '30'
        self.stop()
        
        
        

class Welcomer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.color = 0x2f3136

    @commands.group(name="autorole", invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @blacklist_check()
    @ignore_check()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_autorole.command(name="config")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _ar_config(self, ctx):
        if data := getautorole(ctx.guild.id):
            hum = list(data["humans"])
            bo = list(data["bots"])

            fetched_humans: list = []
            fetched_bots: list = []

            for i in hum:
                role = ctx.guild.get_role(int(i))
                if role is not None:
                    fetched_humans.append(role)

            for i in bo:
                role = ctx.guild.get_role(int(i))
                if role is not None:
                    fetched_bots.append(role)

            hums = "\n".join(i.mention for i in fetched_humans)
            if not hums:
                hums = " Humans Autorole Not Set."

            bos = "\n".join(i.mention for i in fetched_bots)
            if not bos:
                bos = " Bots Autorole Not Set."

            emb = discord.Embed(
                color=self.color,
                title=f"Autorole of - {ctx.guild.name}").add_field(
                    name="__Humans__", value=hums,
                    inline=False).add_field(name="__Bots__",
                                            value=bos,
                                            inline=False)

            await ctx.send(embed=emb)

    @_autorole.group(name="reset",
                     help="Clear autorole config for the server .")
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _autorole_reset(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_autorole_reset.command(name="humans",
                             help="Clear autorole config for the server .")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _autorole_humans_reset(self, ctx):
        data = getautorole(ctx.guild.id)
        rl = data["humans"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if rl == []:
                embed = discord.Embed(
                    description=
                    "⚠ | This server don't have any autoroles setupped .",
                    color=self.color)
                await ctx.send(embed=embed)
            else:
                if rl != []:
                    data["humans"] = []
                    updateautorole(ctx.guild.id, data)
                    hacker = discord.Embed(
                        description=
                        f"✅ | Succesfully cleared all human autoroles for {ctx.guild.name} .",
                        color=self.color)
                    await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)

    @_autorole_reset.command(name="bots")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _autorole_bots_reset(self, ctx):
        data = getautorole(ctx.guild.id)
        rl = data["bots"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if rl == []:
                embed = discord.Embed(
                    description=
                    f"⚠ | This server don't have any autoroles setupped .",
                    color=self.color)
                await ctx.send(embed=embed)
            else:
                if rl != []:
                    data["bots"] = []
                    updateautorole(ctx.guild.id, data)
                    hacker = discord.Embed(
                        description=
                        f"✅ | Succesfully cleared all bot autoroles for this server .",
                        color=self.color)
                    await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)

    @_autorole_reset.command(name="all")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_reset_all(self, ctx):
        data = getautorole(ctx.guild.id)
        brl = data["bots"]
        hrl = data["humans"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if len(brl) == 0 and len(hrl) == 0:
                embed = discord.Embed(
                    description=
                    f"⚠ | This server don't have any autoroles setupped .",
                    color=self.color)
                await ctx.send(embed=embed)
            else:
                if hrl != []:
                    data["bots"] = []
                    data["humans"] = []
                    updateautorole(ctx.guild.id, data)
                    hacker = discord.Embed(
                        description=
                        f"✅ | Succesfully cleared all autoroles for this server .",
                        color=self.color)
                    await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)

    @_autorole.group(name="humans", help="Setup autoroles for human users.")
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_humans(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_autorole_humans.command(name="add",
                              help="Add role to list of autorole humans users."
                              )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_humans_add(self, ctx, *, role: discord.Role):
        data = getautorole(ctx.guild.id)
        rl = data["humans"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if len(rl) == 10:
                embed = discord.Embed(
                    description=
                    f"⚠ | You have reached maximum channel limit for autorole humans which is ten .",
                    color=self.color)
                await ctx.send(embed=embed)
            else:
                if str(role.id) in rl:
                    embed1 = discord.Embed(
                        description=
                        "⚠ | {} is already in human autoroles ."
                        .format(role.mention),
                        color=self.color)
                    await ctx.send(embed=embed1)
                else:
                    rl.append(str(role.id))
                    updateautorole(ctx.guild.id, data)
                    hacker = discord.Embed(
                        description=
                        f"✅ | {role.mention} has been added to human autoroles .",
                        color=self.color)
                    await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)

    @_autorole_humans.command(
        name="remove", help="Remove a role from autoroles for human users.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_humans_remove(self, ctx, *, role: discord.Role):
        data = getautorole(ctx.guild.id)
        rl = data["humans"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if len(rl) == 0:
                embed = discord.Embed(
                    description=
                    f"⚠ | This server dont have any autrole humans setupped yet .",
                    color=self.color)
                await ctx.send(embed=embed)
            else:
                if str(role.id) not in rl:
                    embed1 = discord.Embed(
                        description="{} is not in human autoroles .".format(
                            role.mention),
                        color=self.color)
                    await ctx.send(embed=embed1)
                else:
                    rl.remove(str(role.id))
                    updateautorole(ctx.guild.id, data)
                    hacker = discord.Embed(
                        description=
                        f"✅ | {role.mention} has been removed from human autoroles .",
                        color=self.color)
                    await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)

    @_autorole.group(name="bots", help="Setup autoroles for bots.")
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_bots(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_autorole_bots.command(name="add",
                            help="Add role to list of autorole bot users.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_bots_add(self, ctx, *, role: discord.Role):
        data = getautorole(ctx.guild.id)
        rl = data["bots"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if len(rl) == 5:
                embed = discord.Embed(
                    description=
                    f"⚠ | You have reached maximum role limit for autorole bots which is five.",
                    color=self.color)
                await ctx.send(embed=embed)
            else:
                if str(role.id) in rl:
                    embed1 = discord.Embed(
                        description=
                        "⚠ | {} is already in bot autoroles."
                        .format(role.mention),
                        color=self.color)
                    await ctx.send(embed=embed1)
                else:
                    rl.append(str(role.id))
                    updateautorole(ctx.guild.id, data)
                    hacker = discord.Embed(
                        description=
                        f"✅ | {role.mention} has been added to bot autoroles .",
                        color=self.color)
                    await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)

    @_autorole_bots.command(name="remove",
                            help="Remove a role from autoroles for bot users.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_bots_remove(self, ctx, *, role: discord.Role):
        data = getautorole(ctx.guild.id)
        rl = data["bots"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if len(rl) == 0:
                embed = discord.Embed(
                    description=
                    f"⚠ | This server dont have any autrole humans setupped yet .",
                    color=self.color)
                await ctx.send(embed=embed)
            else:
                if str(role.id) not in rl:
                    embed1 = discord.Embed(
                        description=
                        "⚠ | {} is not in bot autoroles."
                        .format(role.mention),
                        color=self.color)
                    await ctx.send(embed=embed1)
                else:
                    rl.remove(str(role.id))
                    updateautorole(ctx.guild.id, data)
                    hacker = discord.Embed(
                        description=
                        f"✅ | {role.mention} has been removed from bot autoroles.",
                        color=self.color)
                    await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)

    @commands.group(name="greet",
                    aliases=["welcome"],
                    invoke_without_command=True)
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _greet(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_greet.command(name="thumbnail", help="Setups welcome thumbnail .")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _greet_thumbnail(self, ctx, thumbnail_link):
        data = getgreet(ctx.guild.id)
        streamables = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if streamables.search(thumbnail_link):
                data["thumbnail"] = thumbnail_link
                updategreet(ctx.guild.id, data)
                hacker = discord.Embed(
                    color=self.color,
                    description=
                    "✅ | Successfully updated the welcome thumbnail url .")
                hacker.set_author(name=ctx.author,
                                  icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                await ctx.send(embed=hacker)
            else:
                await ctx.send("Oops, Kindly put a valid link.")
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission. - Your top role should be above my top role. 
```""",
                                    color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)

    @_greet.command(name="image", help="Setups welcome image.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _greet_image(self, ctx, *, image_link):
        data = getgreet(ctx.guild.id)
        streamables = re.compile(
            r'^(?:http|ftp)s?://'  
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$',
            re.IGNORECASE)

        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if streamables.search(image_link):
                data["image"] = image_link
                updategreet(ctx.guild.id, data)
                hacker = discord.Embed(
                    color=self.color,
                    description=
                    "✅ | Successfully updated the welcome image url .")
                hacker.set_author(name=ctx.author,
                                  icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                await ctx.send(embed=hacker)
            else:
                await ctx.send("Oops, Kindly put a valid link.")
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission. - Your top role should be above my top role. 
```""",
                                    color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)



    @_greet.command(name="message", help="Setups welcome message .")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _greet_message(self, ctx: commands.Context):
        data = getgreet(ctx.guild.id)

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            msg = discord.Embed(
                color=self.color,
                description=
                """Here are some keywords, which you can use in your welcome message.\n\nSend your welcome message in this channel now.\n\n\n```xml\n<<server.member_count>> = server member count\n<<server.name>> = server name\n<<user.name>> = username of new member\n<<user.mention>> = mention of the new user\n<<user.created_at>> = creation time of account of user\n<<user.joined_at>> = joining time of the user.\n```"""
            )
            await ctx.send(embed=msg)
            try:
                welcmsg = await self.bot.wait_for('message',
                                                  check=check,
                                                  timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send("Oops, too late. bye")
                return
            else:
                data["message"] = welcmsg.content
                updategreet(ctx.guild.id, data)
                hacker = discord.Embed(
                    color=self.color,
                    description=
                    f"✅ | Successfully updated the welcome message .")
                hacker.set_author(name=ctx.author,
                                  icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission. - Your top role should be above my top role. 
```""",
                                    color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)

    @_greet.command(name="embed", help="Toggle embed for greet message .")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _greet_embed(self, ctx):
        data = getgreet(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data["embed"] == True:
                data["embed"] = False
                updategreet(ctx.guild.id, data)
                hacker = discord.Embed(
                    color=self.color,
                    description=
                    f"✅ | Okay, Now your embed is removed and welcome message will be a plain message .")
                hacker.set_author(name=ctx.author,
                                  icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                await ctx.send(embed=hacker)
            elif data["embed"] == False:
                data["embed"] = True
                updategreet(ctx.guild.id, data)
                hacker1 = discord.Embed(
                    color=self.color,
                    description=
                    f"✅ | Okay, Now your embed is enabled and welcome message will be a embed message.")
                hacker1.set_author(name=ctx.author,
                                   icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                await ctx.send(embed=hacker1)
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission. - Your top role should be above my top role. 
```""",
                                    color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)

    @_greet.command(name="ping", help="Toggle embed ping for welcomer.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _greet_ping(self, ctx):
        data = getgreet(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data["ping"] == True:
                data["ping"] = False
                updategreet(ctx.guild.id, data)
                hacker = discord.Embed(
                    color=self.color,
                    description=
                    f"✅ | Okay, Now your embed ping is disabled and users won't get pinged upon welcome .")
                hacker.set_author(name=ctx.author,
                                  icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                await ctx.send(embed=hacker)
            elif data["ping"] == False:
                data["ping"] = True
                updategreet(ctx.guild.id, data)
                hacker1 = discord.Embed(
                    color=self.color,
                    description=
                    f"✅ | Okay, Now your embed ping is enabled and I will ping new users outside the embed .")
                hacker1.set_author(name=ctx.author,
                                   icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                await ctx.send(embed=hacker1)
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission. - Your top role should be above my top role. 
```""",
                                    color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)

    @_greet.group(name="channel", help="Setups welcome channel.")
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _greet_channel(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_greet_channel.command(name="add",
                            help="Add a channel to the welcome channels list.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _greet_channel_add(self, ctx, channel: discord.TextChannel):
        data = getgreet(ctx.guild.id)
        chh = data["channel"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if len(chh) == 1:
                hacker = discord.Embed(
                    color=self.color,
                    description=
                    f"<a:error:1002226340516331571> | You have reached maximum channel limit for channel which is one .")
                hacker.set_author(name=ctx.author,
                                  icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                await ctx.send(embed=hacker)
            else:
                if str(channel.id) in chh:
                    hacker1 = discord.Embed(
                        color=self.color,
                        description=
                        f"<a:error:1002226340516331571> | This channel is already in the welcome channels list .")
                    hacker1.set_author(name=ctx.author,
                                       icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                    await ctx.send(embed=hacker1)
                else:
                    chh.append(str(channel.id))
                    updategreet(ctx.guild.id, data)
                    hacker4 = discord.Embed(
                        color=self.color,
                        description=
                        f"✅ | Successfully added {channel.mention} to welcome channel list .")
                    hacker4.set_author(name=ctx.author,
                                       icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                    await ctx.send(embed=hacker4)
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission. - Your top role should be above my top role. 
```""",
                                    color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)

    @_greet_channel.command(name="remove",
                            help="Remove a chanel from welcome channels list ."
                            )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _greet_channel_remove(self, ctx, channel: discord.TextChannel):
        data = getgreet(ctx.guild.id)
        chh = data["channel"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if len(chh) == 0:
                hacker = discord.Embed(
                    color=self.color,
                    description=
                    f"<a:error:1002226340516331571> | This server dont have any welcome channel setupped yet .")
                hacker.set_author(name=ctx.author,
                                  icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                await ctx.send(embed=hacker)
            else:
                if str(channel.id) not in chh:
                    hacker1 = discord.Embed(
                        color=self.color,
                        description=
                        f"<a:error:1002226340516331571> | This channel is not in the welcome channels list .")
                    hacker1.set_author(name=ctx.author,
                                       icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                    await ctx.send(embed=hacker1)
                else:
                    chh.remove(str(channel.id))
                    updategreet(ctx.guild.id, data)
                    hacker3 = discord.Embed(
                        color=self.color,
                        description=
                        f"✅ | Successfully removed {channel.mention} from welcome channel list .")
                    hacker3.set_author(name=ctx.author,
                                       icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                    await ctx.send(embed=hacker3)
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission. - Your top role should be above my top role. 
```""",
                                    color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)
          
    

    @_greet.command(name="config", help="Get greet config for the server.")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _config(self, ctx):
        data = getgreet(ctx.guild.id)
        msg = data["message"]
        chan = list(data["channel"])
        emtog = data["embed"]
        emping = data["ping"]
        emtog = data["embed"]
        emimage = data["image"]
        emthumbnail = data["thumbnail"]
        emautodel = data["autodel"]


        if chan == []:
            await ctx.reply(
                "First setup Your greet channel by Running `greet channel add #channel/id`"
            )
        else:
            
            embed = discord.Embed(color=self.color,
                                  title=f"Welcome Config For {ctx.guild.name}")
            if emtog == True:                
                em = "Enabled"
            else:
                em = "Disabled"

            if emping == True:
               ping = "Enabled"
            else:
               ping = "Disabled"
            for chh in chan:
                    ch = self.bot.get_channel(int(chh))
            embed.add_field(name="**Welcome Channel:**", value=ch)
            
                                 
            embed.add_field(name="**Welcome Message:**", value=f"{msg}")

            embed.add_field(name="**Welcome Embed:**", value=em)

            embed.add_field(name="**Welcome Ping:**", value=f"{ping}")
            if ctx.guild.icon is not None:
                embed.set_footer(text=ctx.guild.name,
                                 icon_url=ctx.guild.icon.url)
                embed.set_thumbnail(url=ctx.guild.icon.url)

        await ctx.send(embed=embed)


    @_greet.command(name="reset", help="Clear greet config for the server.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _reset(self, ctx):
        data = getgreet(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data["channel"] == []:
                embed = discord.Embed(
                    description=
                    "⚠ | This server don't have any greet channel setuped yet .",
                    color=self.color)
                await ctx.send(embed=embed)
            else:
                data["channel"] = []
                data["image"] = ""
                data["message"] = "<<user.mention>> Welcome To <<server.name>>"
                data["thumbnail"] = ""
                updategreet(ctx.guild.id, data)
                hacker = discord.Embed(
                    description=
                    "✅ | Succesfully cleared all greet config for this server .",
                    color=self.color)
                await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.send(embed=hacker5)


            
    @_greet.command(name="title", help="Setups welcome title .")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _greet_title(self, ctx, *, title):
        data = getgreet(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            data['title'] = title
            updategreet(ctx.guild.id, data)
            hacker = discord.Embed(
                color=self.color,
                description=
                f"✅ | Successfully updated the welcome title .")
            hacker.set_author(name=ctx.author,
                              icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission. - Your top role should be above my top role. 
```""",
                                    color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)
            
            
    @_greet.command(name="footer", help="Setups welcome footer .")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _greet_footer(self, ctx, *, footer):
        data = getgreet(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            data['footer'] = footer
            updategreet(ctx.guild.id, data)
            hacker = discord.Embed(
                color=self.color,
                description=
                f"✅ | Successfully updated the welcome footer .")
            hacker.set_author(name=ctx.author,
                              icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission. - Your top role should be above my top role. 
```""",
                                    color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)



    @_greet.command(name="autodel",
                    help="Automatically delete message after x seconds .")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _greet_autodel(self, ctx):
        data = getgreet(ctx.guild.id)
        autodel = data['autodel'] 
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            view = Autodel(ctx)
            em = discord.Embed(description="Setup greet autodel seconds ?\n", color=self.color)
            msg = await ctx.reply(embed=em, view=view)
            await view.wait()
            if view.value == 'stop':
                return await msg.delete()
            data['autodel'] = view.value
            updategreet(ctx.guild.id, data)
            hacker = discord.Embed(
                color=self.color,
                description=
                f"✅ | Successfully updated the welcome autodelete second to {view.value} .\nFrom now welcome message will be deleted after {view.value} .")
            hacker.set_author(name=ctx.author,
                              icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission. - Your top role should be above my top role. 
```""",
                                    color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)
            
            
            
################
    @_greet.command(name="test",
                    help="Test the welcome message how it will look like.")
    @blacklist_check()
    @ignore_check()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def welctestt(self, ctx):
        data = getgreet(ctx.guild.id)
        msg = data["message"]
        chan = list(data["channel"])
        emtog = data["embed"]
        emping = data["ping"]
        emimage = data["image"]
        emthumbnail = data["thumbnail"]
        emautodel = data["autodel"]
        emtitle = data["title"]
        emfooter = data["footer"]
        user = ctx.author
        if chan == []:
            hacker = discord.Embed(
                color=self.color,
                description=
                f"<a:error:1002226340516331571> | Oops, Kindly setup your welcome channel first .")
            hacker.set_author(name=ctx.author,
                              icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.send(embed=hacker)
        else:
            if "<<server.name>>" in msg:
                msg = msg.replace("<<server.name>>", "%s" % (user.guild.name))
            if "<<server.member_count>>" in msg:
                msg = msg.replace("<<server.member_count>>",
                                  "%s" % (user.guild.member_count))
            if "<<user.name>>" in msg:
                msg = msg.replace("<<user.name>>", "%s" % (user))
            if "<<user.mention>>" in msg:
                msg = msg.replace("<<user.mention>>", "%s" % (user.mention))
            if "<<user.created_at>>" in msg:
                msg = msg.replace("<<user.created_at>>",
                                  f"<t:{int(user.created_at.timestamp())}:F>")
            if "<<user.joined_at>>" in msg:
                msg = msg.replace("<<user.joined_at>>",
                                  f"<t:{int(user.joined_at.timestamp())}:F>")

            if emping == True:
                emping = f"{ctx.author.mention}"
            else:
                emping = ""
            em = discord.Embed(title=emtitle,description=msg, color=self.color)
            em.set_author(name=ctx.author.name,
                          icon_url=ctx.author.avatar.url if ctx.author.avatar
                          else ctx.author.default_avatar.url)
            em.timestamp = discord.utils.utcnow()

            if emimage == "":
                em.set_image(url=None)
            else:
                em.set_image(url=emimage)

            if emthumbnail == "":
                em.set_thumbnail(url=None)
            else:
                em.set_thumbnail(url=emthumbnail)
            if user.guild.icon is not None:
                em.set_footer(text=emfooter,
                              icon_url=user.guild.icon.url)

            for chann in chan:
                channn = self.bot.get_channel(int(chann))
            if emtog == True:
                ok = await channn.send(emping, embed=em)
                return 
                
            else:
                if emtog == False:
                    ok = await channn.send(msg)
                    return