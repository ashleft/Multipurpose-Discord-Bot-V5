from __future__ import annotations
from discord.ext import commands
from utils.Tools import *
import discord
from core import Cog,Astroz, Context
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator


class Raidmode(Cog):
    """Enable/Disable Anti-raid in your server to be protected from unknown raids!"""

    def __init__(self, client: Astroz):
        self.client = client
        self.color = 0x2f3136

    @commands.group(
        name="automod",
        aliases=["Automoderation"],
        help="Shows help about Automoderation feature of bot.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 7, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _automod(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)
    
      
    @_automod.command(name="antispam",
                             aliases=['anti-spam'],
                             help="Enables or Disables anti spam feature")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _antispam(self, ctx: commands.Context, type: str):

        onOroff = type.lower()

        data = getExtra(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if onOroff == "enable":
                if data["antiSpam"] is True:
                    hacker = discord.Embed(
                        description=
                        f"⚠ | Anti-Spam is already enabled for **`{ctx.guild.name}`**",
                        color=self.color)
                    await ctx.reply(embed=hacker, mention_author=False)
                else:
                    data["antiSpam"] = True
                    updateExtra(ctx.guild.id, data)
                    hacker1 = discord.Embed(
        
                        description=
                        f"✅ | Successfully enabled anti-spam for **`{ctx.guild.name}`**",
                        color=self.color)
                    await ctx.reply(embed=hacker1, mention_author=False)

            elif onOroff == "disable":
                data = getExtra(ctx.guild.id)
                data["antiSpam"] = False
                updateExtra(ctx.guild.id, data)
                hacker2 = discord.Embed(
                    description=
                    f"✅ | Successfully disabled anti-spam for **`{ctx.guild.name}`**",
                    color=self.color)
                await ctx.reply(embed=hacker2, mention_author=False)
            else:
                hacker3 = discord.Embed(
                    description=
                    f"⚠ | Invalid Type.\nIt Should Be enable/disable",
                    color=self.color)
                await ctx.reply(embed=hacker3, mention_author=False)

        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5,delete_after=10)  
 


    @_automod.command(aliases=['anti-link'],
                             name="antilink",
                             help="Enables or Disables antilink feature")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _antilink(self, ctx: commands.Context, type: str):

        onOroff = type.lower()

        data = getExtra(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if onOroff == "enable":
                if data["antiLink"] is True:
                    hacker = discord.Embed(
                        description=
                        f"⚠ | Anti-link is already enabled for **`{ctx.guild.name}`**",
                        color=self.color)
                    await ctx.reply(embed=hacker, mention_author=False)
                else:
                    data["antiLink"] = True
                    updateExtra(ctx.guild.id, data)
                    hacker1 = discord.Embed(
                        description=
                        f"✅ | Successfully enabled anti-link for **`{ctx.guild.name}`**",
                        color=self.color)
                    await ctx.reply(embed=hacker1, mention_author=False)

            elif onOroff == "disable":
                data = getExtra(ctx.guild.id)
                data["antiLink"] = False
                updateExtra(ctx.guild.id, data)
                hacker2 = discord.Embed(
                    description=
                    f"✅ | Successfully disabled anti-link for **`{ctx.guild.name}`**",
                    color=self.color)
                await ctx.reply(embed=hacker2, mention_author=False)
            else:
                hacker3 = discord.Embed(
            
                    description=
                    f"⚠ | Invalid Type.\nIt Should Be enable/disable",
                    color=self.color)
                await ctx.reply(embed=hacker3, mention_author=False)

        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5,delete_after=10)  
            
            
    @_automod.command(aliases=['anti-invites'],
                             name="antiinvites",
                             help="Enables or Disables antiinvites feature")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _antiinvites(self, ctx: commands.Context, type: str):

        onOroff = type.lower()

        data = getExtra(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if onOroff == "enable":
                if data["antiinvites"] is True:
                    hacker = discord.Embed(
                        description=
                        f"⚠ | Anti-Invites is already enabled for **`{ctx.guild.name}`**",
                        color=self.color)
                    await ctx.reply(embed=hacker, mention_author=False)
                else:
                    data["antiinvites"] = True
                    updateExtra(ctx.guild.id, data)
                    hacker1 = discord.Embed(
                        description=
                        f"✅ | Successfully enabled anti-invites for **`{ctx.guild.name}`**",
                        color=self.color)
                    await ctx.reply(embed=hacker1, mention_author=False)

            elif onOroff == "disable":
                data = getExtra(ctx.guild.id)
                data["antiinvites"] = False
                updateExtra(ctx.guild.id, data)
                hacker2 = discord.Embed(
                    description=
                    f"✅ | Successfully disabled anti-invites for **`{ctx.guild.name}`**",
                    color=self.color)
                await ctx.reply(embed=hacker2, mention_author=False)
            else:
                hacker3 = discord.Embed(
            
                    description=
                    f"⚠ | Invalid Type.\nIt Should Be enable/disable",
                    color=self.color)
                await ctx.reply(embed=hacker3, mention_author=False)

        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5,delete_after=10)       
            
            
                   
    @_automod.group(name="whitelist",
                     aliases=["wl"],
                     help="Whitelist your TRUSTED users for automod",
                     invoke_without_command=True,
                     usage="Automod whitelist add/remove")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _whitelist(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)
            
            
            
            
    @_whitelist.command(name="add",
                        help="Add a user to whitelisted users for automod events .",
                        usage="Automod whitelist add <user>")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def whitelist_add(self, ctx, user: discord.User):
        data = getExtra(ctx.guild.id)
        wled = data["whitelisted"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if len(wled) == 15:
                hacker = discord.Embed(
                    description=
                    f"⚠ This server have already maximum number of whitelisted users (15)\nRemove one to add another :)",
                    color=self.color)
                await ctx.reply(embed=hacker, mention_author=False)
            else:
                if str(user.id) in wled:
                    hacker1 = discord.Embed(
                        description=
                        f"⚠ | That user is already in my whitelist.",
                        color=self.color)
                    await ctx.reply(embed=hacker1, mention_author=False)
                else:
                    wled.append(str(user.id))
                    updateExtra(ctx.guild.id, data)
                    hacker4 = discord.Embed(
                        color=self.color,
                        description=
                        f"✅ | Successfully Whitelisted {user.mention} For Automod Events"
                    )
                    hacker4.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                    await ctx.reply(embed=hacker4, mention_author=False)

        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5,delete_after=10)  
            
            
            
            
    @_whitelist.command(name="remove",
                        help="Remove a user from whitelisted users for automod events .",
                        usage="Automod whitelist remove <user>")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def whitelist_remove(self, ctx, user: discord.User):
        data = getExtra(ctx.guild.id)
        wled = data["whitelisted"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if str(user.id) in wled:
                wled.remove(str(user.id))
                updateExtra(ctx.guild.id, data)
                hacker = discord.Embed(
                    color=self.color,
                    description=
                    f"✅ | Successfully Unwhitelisted {user.mention} For Automod Events"
                )
                hacker.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                await ctx.reply(embed=hacker, mention_author=False)
            else:
                hacker2 = discord.Embed(
                    color=self.color,
                    description=
                    "⚠ | That user is not in my whitelist."
                )
                await ctx.reply(embed=hacker2, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5,delete_after=10)  
            
            
            
            



    @_whitelist.command(name="show",
                        help="Shows list of whitelisted users for automod events in the server .",
                        usage="Automod whitelist show")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def whitelist_show(self, ctx):
        data = getExtra(ctx.guild.id)
        wled = data["whitelisted"]
        if len(wled) == 0:
            hacker = discord.Embed(
                color=self.color,
                description=
                f"⚠ | There aren\'t any whitelised users for automod events in {ctx.guild.name}"
            )
            await ctx.reply(embed=hacker, mention_author=False)
        else:
            entries = [
                f"`{no}` | <@!{idk}> | ID: [{idk}](https://discord.com/users/{idk})"
                for no, idk in enumerate(wled, start=1)
            ]
            paginator = Paginator(source=DescriptionEmbedPaginator(
                entries=entries,
                title=f"Whitelisted Users For Automod Events In {ctx.guild.name} - {len(wled)}/15",
                description="",
                color=self.color),
                                  ctx=ctx)
            await paginator.paginate()
            
            
            
            
    @_whitelist.command(name="reset",
                        help="removes every user from whitelist database for automod events .",
                        aliases=["clear"],
                        usage="Automod whitelist reset")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def wl_reset(self, ctx: Context):
        data = getExtra(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            data = getExtra(ctx.guild.id)
            data["whitelisted"] = []
            updateExtra(ctx.guild.id, data)
            hacker = discord.Embed(
                color=self.color,
                description=
                f"✅ | Successfully Cleared Whitelist Database For Automod Events In **{ctx.guild.name}**"
            )
            hacker.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5,delete_after=10)  
            
           
            
    @_automod.group(
        name="punishment",
        help="Changes Punishment of antiraid for this server.",
        invoke_without_command=True,
        usage="Automod punishment set/show")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _punishment(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)
            
            
            
            
    @_punishment.command(
        name="set",
        help="Changes Punishment of antinuke and automod for this server.",
        aliases=["change"],
        usage="Antinuke punishment set <none>")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def punishment_set(self, ctx, punishment: str):
        data = getExtra(ctx.guild.id)

        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:

            kickOrBan = punishment.lower()

            if kickOrBan == "kick":
                data = getExtra(ctx.guild.id)
                data["punishment"] = "kick"
                hacker = discord.Embed(
                    description=
                    f"✅ | Successfully Changed Punishment To: **{kickOrBan}** For Automod Events In {ctx.guild.name}",
                    color=self.color)
                await ctx.reply(embed=hacker, mention_author=False)

                updateExtra(ctx.guild.id, data)

            elif kickOrBan == "ban":
                data = getExtra(ctx.guild.id)
                data["punishment"] = "ban"
                hacker1 = discord.Embed(
                   
                    description=
                    f"✅ | Successfully Changed Punishment To: **{kickOrBan}** For Automod Events In {ctx.guild.name}",
                    color=self.color)
                await ctx.reply(embed=hacker1, mention_author=False)

                updateExtra(ctx.guild.id, data)

            elif kickOrBan == "mute":
                data = getExtra(ctx.guild.id)
                data["punishment"] = "none"
                hacker3 = discord.Embed(
                    
                    description=
                    f"✅ | Successfully Changed Punishment To: **{kickOrBan}** For Automod Events In {ctx.guild.name}",
                    color=self.color)
                await ctx.reply(embed=hacker3, mention_author=False)

                updateExtra(ctx.guild.id, data)
            else:
                hacker6 = discord.Embed(
                    
                    description=
                    "Invalid Punishment Type\nValid Punishment Type(s) Are: Kick, Ban, Mute",
                    color=self.color)
                await ctx.reply(embed=hacker6, mention_author=False)

        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5,delete_after=10)  


    @_punishment.command(name="show",
                         help="Shows custom punishment type for automod events in this server .",
                         usage="Automod punishment show")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def punishment_show(self, ctx: Context):
        data = getExtra(ctx.guild.id)
        punish = data["punishment"]
        hacker5 = discord.Embed(
            color=self.color,
            description=
            "Custom punishment of automod event in this server is: **{}**"
            .format(punish.title()))
        await ctx.reply(embed=hacker5, mention_author=False)
       
    
    @_automod.command(
        name="logging",
        help="Setups logging channel for automod logging in the server .",
        invoke_without_command=True,
        usage="Automod logging")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _logging(self, ctx,channel: discord.TextChannel):
        data = getExtra(ctx.guild.id)
        data["channel"] = channel.id
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            updateExtra(ctx.guild.id, data)
            hacker4 = discord.Embed(
                color=self.color,
                
                description=
                f"✅ | Successfully setuped logging channel to {channel.mention} for automod events in {ctx.guild.name}"
            )
            await ctx.reply(embed=hacker4, mention_author=False)
            
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False)  
            
            
            
################


    @_automod.group(name="ignore", invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    async def _ignore(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_ignore.group(name="channel",
                   aliases=["chnl"],
                   invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @blacklist_check()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _channel(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_channel.command(name="add")
    @commands.has_permissions(administrator=True)
    async def channel_add(self, ctx: Context, channel: discord.TextChannel):
        data = getExtra(ctx.guild.id)
        ch= data["ignorechannels"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if str(channel.id) in ch:
                embed = discord.Embed(
                        description=
                        f"| {channel.mention} is already in automod ignore channel list .",
                        color=self.color)
                await ctx.reply(embed=embed, mention_author=False)
            else:
                ch.append(str(channel.id))
                updateExtra(ctx.guild.id, data)
                hacker4 = discord.Embed(
                        color=self.color,
                        description=
                        f"✅ | From Now , {channel.mention} is ignored from automod events in {ctx.guild.name} .")
                hacker4.set_author(name=ctx.author,
                                       icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                await ctx.send(embed=hacker4)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                                       icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5)

    @_channel.command(name="remove")
    @commands.has_permissions(administrator=True)
    async def channel_remove(self, ctx, channel: discord.TextChannel):
        data = getExtra(ctx.guild.id)
        ch= data["ignorechannels"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:   
            if len(ch) == 0:
                hacker = discord.Embed(
                    color=self.color,
                    description=
                    f"<a:error:1002226340516331571> | This server dont have any automod ignore channel setupped yet .")
                hacker.set_author(name=ctx.author,
                                       icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                await ctx.send(embed=hacker)   
            else:
                if str(channel.id) not in ch:   
                    hacker1 = discord.Embed(
                        color=self.color,
                        description=
                        f"<a:error:1002226340516331571> | This channel is not in the automod ignore channels list .")
                    hacker1.set_author(name=ctx.author,
                                       icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                    await ctx.send(embed=hacker1) 
                else:
                    ch.remove(str(channel.id))
                    updateExtra(ctx.guild.id, data)
                    hacker3 = discord.Embed(
                        color=self.color,
                        description=
                        f"✅ | Successfully removed {channel.mention} from automod ignore channel list .")
                    hacker3.set_author(name=ctx.author,
                                       icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                    await ctx.send(embed=hacker3)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                                       icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5)  