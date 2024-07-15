import discord
from discord.ext import commands
from discord.utils import get
import os
from utils.Tools import *
from typing import Optional, Union
from discord.ext.commands import Context
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator
from utils import *


class Voice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.color = 0x2f3136

    @commands.group(name="voice", invoke_without_command=True, aliases=['vc'])
    @blacklist_check()
    @ignore_check()
    async def vc(self, ctx: commands.Context):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @vc.command(name="kick",
                help="Dissconnect a member from a voice channel .",
                usage="voice kick <member>")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def _kick(self, ctx, *, member: discord.Member):
        if member.voice is None:
            hacker5 = discord.Embed(
                
                description=
                f"{str(member)} Is not connected in any of the voice channel",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            hacker5.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            return await ctx.reply(embed=hacker5)
        ch = member.voice.channel.mention
        await member.edit(voice_channel=None,
                          reason=f"Disconnected by {str(ctx.author)}")
        hacker = discord.Embed(
            
            description=f"{str(member)} has been disconnected from {ch}",
            color=self.color)
        hacker.set_author(name=ctx.author,
                          icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        hacker.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        return await ctx.reply(embed=hacker)

    @vc.command(name="kickall",
                help="Dissconnect all member from a voice channel .",
                usage="voice kick all")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def _kickall(self, ctx):
        if ctx.author.voice is None:
            hacker5 = discord.Embed(
                
                description=
                f"You are not connected in any of the voice channel",
                color=self.color)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            hacker5.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            return await ctx.reply(embed=hacker5)
        count = 0
        ch = ctx.author.voice.channel.mention
        for member in ctx.author.voice.channel.members:
            await member.edit(
                voice_channel=None,
                reason=f"Disconnected Command Executed By {str(ctx.author)}")
            count += 1
        hacker = discord.Embed(
            
            description=f"Disconnected {count} members from {ch}",
            color=self.color)
        hacker.set_author(name=ctx.author,
                          icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        hacker.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        return await ctx.reply(embed=hacker)

    @vc.command(name="mute",
                help="mute a member in voice channel .",
                usage="voice mute <member>")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def _mute(self, ctx, *, member: discord.Member):
        if member.voice is None:
            error = discord.Embed(
                
                description=
                f"{str(member)} Is not connected in any of the voice channel",
                color=self.color)
            error.set_author(name=ctx.author,
                             icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            error.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            return await ctx.reply(embed=error)
        if member.voice.mute == True:
            hacker5 = discord.Embed(
                
                description=
                f"{str(member)} Is already muted in the voice channel",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            hacker5.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            return await ctx.reply(embed=hacker5)
        ch = member.voice.channel.mention
        hacker = discord.Embed(
            
            description=f"{str(member)} has been muted in {ch}",
            color=self.color)
        hacker.set_author(name=ctx.author,
                          icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        hacker.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        await member.edit(mute=True, reason=f"Muted by {str(ctx.author)}")
        return await ctx.reply(embed=hacker)

    @vc.command(name="unmute",
                help="unmute a member in voice channel .",
                usage="voice unmute <member>")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def vcunmute(self, ctx, *, member: discord.Member):
        if member.voice is None:
            error = discord.Embed(
                
                description=
                f"{str(member)} Is not connected in any of the voice channel",
                color=self.color)
            error.set_author(name=ctx.author,
                             icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            error.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            return await ctx.reply(embed=error)
        if member.voice.mute == False:
            hacker5 = discord.Embed(
                
                description=
                f"{str(member)} Is already unmuted in the voice channel",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            hacker5.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            return await ctx.reply(embed=hacker5)
        ch = member.voice.channel.mention
        hacker = discord.Embed(
            
            description=f"{str(member)} has been unmuted in {ch}",
            color=self.color)
        hacker.set_author(name=ctx.author,
                          icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        hacker.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        await member.edit(mute=False, reason=f"Unmuted by {str(ctx.author)}")
        return await ctx.reply(embed=hacker)

    @vc.command(name="muteall",
                help="mute all member in a voice channel .",
                usage="voice muteall")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def _muteall(self, ctx):
        if ctx.author.voice is None:
            error = discord.Embed(
                
                description=
                f"You are not connected in any of the voice channel",
                color=self.color)
            error.set_author(name=ctx.author,
                             icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            error.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            return await ctx.reply(embed=error)
        count = 0
        ch = ctx.author.voice.channel.mention
        for member in ctx.author.voice.channel.members:
            if member.voice.mute == False:
                await member.edit(
                    mute=True,
                    reason=
                    f"voice muteall Command Executed by {str(ctx.author)}")
                count += 1
        hacker = discord.Embed(
                               description=f"Muted {count} members in {ch}",
                               color=self.color)
        hacker.set_author(name=ctx.author,
                          icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        hacker.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        return await ctx.reply(embed=hacker)

    @vc.command(name="unmuteall",
                help="unmute all member in a voice channel .",
                usage="voice unmuteall")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def _unmuteall(self, ctx):
        if ctx.author.voice is None:
            error = discord.Embed(
                
                description=
                f"You are not connected in any of the voice channel",
                color=self.color)
            error.set_author(name=ctx.author,
                             icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            error.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            return await ctx.reply(embed=error)
        count = 0
        ch = ctx.author.voice.channel.mention
        for member in ctx.author.voice.channel.members:
            if member.voice.mute == True:
                await member.edit(
                    mute=False,
                    reason=
                    f"voice unmuteall Command Executed by {str(ctx.author)}")
                count += 1
        hacker = discord.Embed(
                               description=f"Unmuted {count} members in {ch}",
                               color=self.color)
        hacker.set_author(name=ctx.author,
                          icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        hacker.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        return await ctx.reply(embed=hacker)

    @vc.command(name="deafen",
                help="deafen a member in a voice channel .",
                usage="voice deafen <member>")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def _deafen(self, ctx, *, member: discord.Member):
        if member.voice is None:
            error = discord.Embed(
                
                description=
                f"{str(member)} Is not connected in any of the voice channel",
                color=self.color)
            error.set_author(name=ctx.author,
                             icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            error.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            return await ctx.reply(embed=error)
        if member.voice.deaf == True:
            hacker5 = discord.Embed(
                
                description=
                f"{str(member)} Is already deafen in the voice channel",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            hacker5.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            return await ctx.reply(embed=hacker5)
        ch = member.voice.channel.mention
        hacker = discord.Embed(
            
            description=f"{str(member)} has been Deafen in {ch}",
            color=self.color)
        hacker.set_author(name=ctx.author,
                          icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        hacker.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        await member.edit(deafen=True, reason=f"Deafen by {str(ctx.author)}")
        return await ctx.reply(embed=hacker)

    @vc.command(name="undeafen",
                help="undeafen a member in a voice channel .",
                usage="voice undeafen <member>")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def _undeafen(self, ctx, *, member: discord.Member):
        if member.voice is None:
            error = discord.Embed(
                
                description=
                f"{str(member)} Is not connected in any of the voice channel",
                color=self.color)
            error.set_author(name=ctx.author,
                             icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            error.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            return await ctx.reply(embed=error)
        if member.voice.deaf == False:
            hacker5 = discord.Embed(
                
                description=
                f"{str(member)} Is already undeafen in the voice channel",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            hacker5.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            return await ctx.reply(embed=hacker5)
        ch = member.voice.channel.mention
        hacker = discord.Embed(
            
            description=f"{str(member)} has been undeafen in {ch}",
            color=self.color)
        hacker.set_author(name=ctx.author,
                          icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        hacker.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        await member.edit(deafen=False,
                          reason=f"Undeafen by {str(ctx.author)}")
        return await ctx.reply(embed=hacker)

    @vc.command(name="deafenalll",
                help="deafen all member in a voice channel .",
                usage="voice deafenall")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def _deafenall(self, ctx):
        if ctx.author.voice is None:
            error = discord.Embed(
                
                description=
                "You are not connected in any of the voice channel",
                color=self.color)
            error.set_author(name=ctx.author,
                             icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            error.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            return await ctx.reply(embed=error)
        count = 0
        ch = ctx.author.voice.channel.mention
        for member in ctx.author.voice.channel.members:
            if member.voice.deaf == False:
                await member.edit(
                    deafen=True,
                    reason=
                    f"voice deafenall Command Executed by {str(ctx.author)}")
                count += 1
        hacker = discord.Embed(
                               description=f"Deafened {count} members in {ch}",
                               color=self.color)
        hacker.set_author(name=ctx.author,
                          icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        hacker.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        return await ctx.reply(embed=hacker)

    @vc.command(name="undeafenalll",
                help="undeafen all member in a voice channel .",
                usage="voice undeafenall")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def _undeafall(self, ctx):
        if ctx.author.voice is None:
            error = discord.Embed(
                
                description=
                "You are not connected in any of the voice channel",
                color=self.color)
            error.set_author(name=ctx.author,
                             icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            error.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            return await ctx.reply(embed=error)
        count = 0
        ch = ctx.author.voice.channel.mention
        for member in ctx.author.voice.channel.members:
            if member.voice.deaf == True:
                await member.edit(
                    deafen=False,
                    reason=
                    f"voice undeafenall Command Executed by {str(ctx.author)}")
                count += 1
        hacker = discord.Embed(
            
            description=f"Undeafened {count} members in {ch}",
            color=self.color)
        hacker.set_author(name=ctx.author,
                          icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        hacker.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        return await ctx.reply(embed=hacker)

    @vc.command(name="moveall",
                help="Moves all the members from the voice channel .",
                usage="voice moveall <voice channel>")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def _moveall(self, ctx, *, channel: discord.VoiceChannel):
        if ctx.author.voice is None:
            error = discord.Embed(
                
                description=
                "You are not connected in any of the voice channel",
                color=self.color)
            error.set_author(name=ctx.author,
                             icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            error.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            return await ctx.reply(embed=error)
        try:
            ch = ctx.author.voice.channel.mention
            nch = channel.mention
            count = 0
            for member in ctx.author.voice.channel.members:
                await member.edit(
                    voice_channel=channel,
                    reason=
                    f"voice moveall Command Executed by {str(ctx.author)}")
                count += 1
            hacker = discord.Embed(
                
                description=f"{count} Members Moved From {ch} to {nch}",
                color=self.color)
            hacker.set_author(name=ctx.author,
                              icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            hacker.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker)
        except:
            hacker1 = discord.Embed(
                
                description=f"Invalid Voice channel provided",
                color=self.color)
            hacker1.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            hacker1.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker1)