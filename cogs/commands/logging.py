import discord
import datetime
from discord.ext import commands, tasks
from utils.Tools import *
from discord import Webhook
import io
from utils.config import BotName



class lundView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout = 60):
        super().__init__(timeout=timeout)
        self.ctx = ctx

    
      
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in [246469891761111051]:
            await interaction.response.send_message(f"Opps , Looks like you are not the author of the command .", ephemeral=True)
            return False
        return True

class antinukesetup(lundView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None
        
    @discord.ui.button(label="Yes", custom_id='yes', style=discord.ButtonStyle.green)
    async def png(self, interaction, button):
        self.value = 'yes'
        self.stop()

    @discord.ui.button(label="No", custom_id='stop', style=discord.ButtonStyle.danger)
    async def cancel(self, interaction, button):
        self.value = 'stop'
        self.stop()
        
        
             
class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x2f3136
        
        
    @commands.group(
        name="logging",
        invoke_without_command=True, description="Shows the logging's help menu"
    )
    async def logging(self, ctx):
        if ctx.prefix == f"<@!{self.bot.user.id}>":
            prefix=f"@{BotName}"
        #elif ctx.prefix != "<@1051314800078094417>":
        else:
            prefix=ctx.prefix
        hacker = discord.utils.get(self.bot.users, id=875617517714964530)
        hasan = discord.utils.get(self.bot.users, id=301502732664307716)
        listem = discord.Embed(title=f"Logging (9)", colour=self.color,
                                     description=f"""<...> Duty | [...] Optional\n\n
{prefix}msglog <channel>
Log message deleted/ edited / bulk deleted.

{prefix}memberlog <channel>
Log when someone joins/leaves/nickname/role update etc..

{prefix}serverlog <channel>
Log server updates like emoji update , icon change, etc.

{prefix}channellog <channel>
Log create/ edit/ delete channel.

{prefix}rolelog <channel>
Log create/ edit/ delete roles.

{prefix}modlog <channel>
Log mod actions in the server.

""")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by {str(hacker)}" ,  icon_url=hacker.avatar.url)
        await ctx.send(embed=listem)
        
        
        


    @commands.hybrid_command(name="msglog", aliases=['messagelogs'],help="Log message deleted/ edited / bulk deleted.")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def msglogs(self, ctx):
        data = getLogging(ctx.guild.id)
        ch= data["message"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if ch is not None:
                embed = discord.Embed(
                     color=self.color,
                    description=f" | Log message deleted/ edited / bulk deleted is already enabled for {ctx.guild.name} .")
                return await ctx.reply(embed=embed)
            else:
                view = antinukesetup(ctx)
                em = discord.Embed(description=F"Are you sure you want to setup logging Of deleted/ edited / bulk deleted messages ?", color=self.color)
                msg = await ctx.reply(embed=em, view=view)
                await view.wait()
                if view.value == 'stop':
                    return await msg.delete()
                     
                await msg.edit(embed=discord.Embed(description="Creating a logging channel for logging Of deleted/ edited / bulk deleted messages .", color=self.color), view=None)
                channel1 = await ctx.guild.create_text_channel(name="msg-logs", topic="This channel is for logging Of deleted/ edited / bulk deleted messages .")
                overwrite = channel1.overwrites_for(ctx.guild.default_role)
                overwrite.view_channel = False
                await channel1.set_permissions(ctx.guild.default_role,
                                  overwrite=overwrite)
                await msg.edit(embed=discord.Embed(description=f"Alright I , created {channel1.mention} for logging Of deleted/ edited / bulk deleted messages .", color=self.color), view=None)                
                web = await channel1.create_webhook(name=f"{str(self.bot.user.name)} | Message Logs")
                await msg.edit(embed=discord.Embed(description="Please wait...", color=self.color), view=None)
                
                data = getLogging(ctx.guild.id)
                data["message"] = web.url
                updateLogging(ctx.guild.id, data)
                hacker = discord.Embed(
                        description=
                        f"<:GreenTick:1029990379623292938> | Successfully setuped message logs for {ctx.guild.name} and created {channel1.mention} for logging Of deleted/ edited / bulk deleted messages .",
                        color=self.color)
                await msg.edit(embed=hacker,view=None)
                
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)                   
                
                
                
                
            
        
        
        
        

    @commands.hybrid_command(name="rolelog", aliases=['rolelogs'], help="Log create/ edit/ delete roles.")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _rolelogs(self, ctx):
        data = getLogging(ctx.guild.id)
        ch= data["role"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if ch is not None:
                embed = discord.Embed(
                     color=self.color,
                    description=f" | Logging of create/ edit/ delete roles is already enabled for {ctx.guild.name} .")
                return await ctx.reply(embed=embed)
            else:
                view = antinukesetup(ctx)
                em = discord.Embed(description=F"Are you sure you want to setup logging Of create/ edit/ delete roles ?", color=self.color)
                msg = await ctx.reply(embed=em, view=view)
                await view.wait()
                if view.value == 'stop':
                    return await msg.delete()
                     
                await msg.edit(embed=discord.Embed(description="Creating a logging channel for logging Of create/ edit/ delete roles .", color=self.color), view=None)
                channel1 = await ctx.guild.create_text_channel(name="role-logs", topic="This channel is for logging Of create/ edit/ delete roles .")
                overwrite = channel1.overwrites_for(ctx.guild.default_role)
                overwrite.view_channel = False
                await channel1.set_permissions(ctx.guild.default_role,
                                  overwrite=overwrite)
                await msg.edit(embed=discord.Embed(description=f"Alright I , created {channel1.mention} for logging Of create/ edit/ delete roles .", color=self.color), view=None)                
                web = await channel1.create_webhook(name=f"{str(self.bot.user.name)} | Role Logs")
                await msg.edit(embed=discord.Embed(description="Please wait...", color=self.color), view=None)
                
                data = getLogging(ctx.guild.id)
                data["role"] = web.url
                updateLogging(ctx.guild.id, data)
                hacker = discord.Embed(
                        description=
                        f"<:GreenTick:1029990379623292938> | Successfully setuped role logs for {ctx.guild.name} and created {channel1.mention} for logging Of create/ edit/ delete roles .",
                        color=self.color)
                await msg.edit(embed=hacker,view=None)
                
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5) 
            
            
            


    @commands.hybrid_command(name="rolelog", aliases=['rolelogs'], help="Log create/ edit/ delete roles.")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _rolelogs(self, ctx):
        data = getLogging(ctx.guild.id)
        ch= data["role"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if ch is not None:
                embed = discord.Embed(
                     color=self.color,
                    description=f" | Logging of create/ edit/ delete roles is already enabled for {ctx.guild.name} .")
                return await ctx.reply(embed=embed)
            else:
                view = antinukesetup(ctx)
                em = discord.Embed(description=F"Are you sure you want to setup logging Of create/ edit/ delete roles ?", color=self.color)
                msg = await ctx.reply(embed=em, view=view)
                await view.wait()
                if view.value == 'stop':
                    return await msg.delete()
                     
                await msg.edit(embed=discord.Embed(description="Creating a logging channel for logging Of create/ edit/ delete roles .", color=self.color), view=None)
                channel1 = await ctx.guild.create_text_channel(name="role-logs", topic="This channel is for logging Of create/ edit/ delete roles .")
                overwrite = channel1.overwrites_for(ctx.guild.default_role)
                overwrite.view_channel = False
                await channel1.set_permissions(ctx.guild.default_role,
                                  overwrite=overwrite)
                await msg.edit(embed=discord.Embed(description=f"Alright I , created {channel1.mention} for logging Of create/ edit/ delete roles .", color=self.color), view=None)                
                web = await channel1.create_webhook(name=f"{str(self.bot.user.name)} | Role Logs")
                await msg.edit(embed=discord.Embed(description="Please wait...", color=self.color), view=None)
                
                data = getLogging(ctx.guild.id)
                data["role"] = web.url
                updateLogging(ctx.guild.id, data)
                hacker = discord.Embed(
                        description=
                        f"<:GreenTick:1029990379623292938> | Successfully setuped role logs for {ctx.guild.name} and created {channel1.mention} for logging Of create/ edit/ delete roles .",
                        color=self.color)
                await msg.edit(embed=hacker,view=None)
                
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5) 
            
            
    @commands.hybrid_command(name="modlog", aliases=['modlogs'], help="Log mod actions in the server.")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _modogs(self, ctx):
        data = getLogging(ctx.guild.id)
        ch= data["mod"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if ch is not None:
                embed = discord.Embed(
                     color=self.color,
                    description=f" | Logging of mod actions in the server is already enabled for {ctx.guild.name} .")
                return await ctx.reply(embed=embed)
            else:
                view = antinukesetup(ctx)
                em = discord.Embed(description=F"Are you sure you want to setup logging Of mod actions in the server ?", color=self.color)
                msg = await ctx.reply(embed=em, view=view)
                await view.wait()
                if view.value == 'stop':
                    return await msg.delete()
                     
                await msg.edit(embed=discord.Embed(description="Creating a logging channel for logging Of mod actions in the server .", color=self.color), view=None)
                channel1 = await ctx.guild.create_text_channel(name="mod-logs", topic="This channel is for logging Of mod actions in the server .")
                overwrite = channel1.overwrites_for(ctx.guild.default_role)
                overwrite.view_channel = False
                await channel1.set_permissions(ctx.guild.default_role,
                                  overwrite=overwrite)
                await msg.edit(embed=discord.Embed(description=f"Alright I , created {channel1.mention} for logging Of mod actions in the server .", color=self.color), view=None)                
                web = await channel1.create_webhook(name=f"{str(self.bot.user.name)} | Mod Logs")
                await msg.edit(embed=discord.Embed(description="Please wait...", color=self.color), view=None)
                
                data = getLogging(ctx.guild.id)
                data["mod"] = web.url
                updateLogging(ctx.guild.id, data)
                hacker = discord.Embed(
                        description=
                        f"<:GreenTick:1029990379623292938> | Successfully setuped mod logs for {ctx.guild.name} and created {channel1.mention} for logging Of mod actions in the server .",
                        color=self.color)
                await msg.edit(embed=hacker,view=None)
                
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5) 
            
            
            
            


    @commands.hybrid_command(name="memberlog", aliases=['memberlogs'], help="Log when someone joins/leaves/nickname/role update etc..")
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    async def _memberogs(self, ctx):
        data = getLogging(ctx.guild.id)
        ch= data["member"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if ch is not None:
                embed = discord.Embed(
                     color=self.color,
                    description=f" | Logging of when someone joins/leaves/nickname/role update etc is already enabled for {ctx.guild.name} .")
                return await ctx.reply(embed=embed)
            else:
                view = antinukesetup(ctx)
                em = discord.Embed(description=F"Are you sure you want to setup logging Of when someone joins/leaves/nickname/role update etc ?", color=self.color)
                msg = await ctx.reply(embed=em, view=view)
                await view.wait()
                if view.value == 'stop':
                    return await msg.delete()
                     
                await msg.edit(embed=discord.Embed(description="Creating a logging channel for when someone joins/leaves/nickname/role update etc .", color=self.color), view=None)
                channel1 = await ctx.guild.create_text_channel(name="member-logs", topic="This channel is for logging when someone joins/leaves/nickname/role update etc .")
                overwrite = channel1.overwrites_for(ctx.guild.default_role)
                overwrite.view_channel = False
                await channel1.set_permissions(ctx.guild.default_role,
                                  overwrite=overwrite)
                await msg.edit(embed=discord.Embed(description=f"Alright I , created {channel1.mention} for logging when someone joins/leaves/nickname/role update etc .", color=self.color), view=None)                
                web = await channel1.create_webhook(name=f"{str(self.bot.user.name)} | Member Logs")
                await msg.edit(embed=discord.Embed(description="Please wait...", color=self.color), view=None)
                
                data = getLogging(ctx.guild.id)
                data["member"] = web.url
                updateLogging(ctx.guild.id, data)
                hacker = discord.Embed(
                        description=
                        f"<:GreenTick:1029990379623292938> | Successfully setuped member logs for {ctx.guild.name} and created {channel1.mention} for logging when someone joins/leaves/nickname/role update etc .",
                        color=self.color)
                await msg.edit(embed=hacker,view=None)
                
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5) 
            
            
            
            
    @commands.hybrid_command(name="channellog", aliases=['channellogs'], help="Log create/ edit/ delete channel.")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _channellogs(self, ctx):
        data = getLogging(ctx.guild.id)
        ch= data["channel"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if ch is not None:
                embed = discord.Embed(
                     color=self.color,
                    description=f" | Logging of create/ edit/ delete channel is already enabled for {ctx.guild.name} .")
                return await ctx.reply(embed=embed)
            else:
                view = antinukesetup(ctx)
                em = discord.Embed(description=F"Are you sure you want to setup logging Of create/ edit/ delete channel ?", color=self.color)
                msg = await ctx.reply(embed=em, view=view)
                await view.wait()
                if view.value == 'stop':
                    return await msg.delete()
                     
                await msg.edit(embed=discord.Embed(description="Creating a logging channel for create/ edit/ delete channel .", color=self.color), view=None)
                channel1 = await ctx.guild.create_text_channel(name="channel-logs", topic="This channel is for logging create/ edit/ delete channel .")
                overwrite = channel1.overwrites_for(ctx.guild.default_role)
                overwrite.view_channel = False
                await channel1.set_permissions(ctx.guild.default_role,
                                  overwrite=overwrite)
                await msg.edit(embed=discord.Embed(description=f"Alright I , created {channel1.mention} for logging of create/ edit/ delete channel .", color=self.color), view=None)                
                web = await channel1.create_webhook(name=f"{str(self.bot.user.name)} | Channel Logs")
                await msg.edit(embed=discord.Embed(description="Please wait...", color=self.color), view=None)
                
                data = getLogging(ctx.guild.id)
                data["channel"] = web.url
                updateLogging(ctx.guild.id, data)
                hacker = discord.Embed(
                        description=
                        f"<:GreenTick:1029990379623292938> | Successfully setuped channel logs for {ctx.guild.name} and created {channel1.mention} for logging of create/ edit/ delete channel .",
                        color=self.color)
                await msg.edit(embed=hacker,view=None)
                
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5) 
            
            
            
            


    @commands.hybrid_command(name="serverlog", aliases=['serverlogs'], help="Log server updates like emoji update , icon change, etc.")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _serverlogs(self, ctx):
        data = getLogging(ctx.guild.id)
        ch= data["server"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if ch is not None:
                embed = discord.Embed(
                     color=self.color,
                    description=f" | Logging of server updates like emoji update , icon change, etc is already enabled for {ctx.guild.name} .")
                return await ctx.reply(embed=embed)
            else:
                view = antinukesetup(ctx)
                em = discord.Embed(description=F"Are you sure you want to setup logging Of server updates like emoji update , icon change, etc ?", color=self.color)
                msg = await ctx.reply(embed=em, view=view)
                await view.wait()
                if view.value == 'stop':
                    return await msg.delete()
                     
                await msg.edit(embed=discord.Embed(description="Creating a logging channel for server updates like emoji update , icon change, etc .", color=self.color), view=None)
                channel1 = await ctx.guild.create_text_channel(name="server-logs", topic="This channel is for logging of server updates like emoji update , icon change, etc .")
                overwrite = channel1.overwrites_for(ctx.guild.default_role)
                overwrite.view_channel = False
                await channel1.set_permissions(ctx.guild.default_role,
                                  overwrite=overwrite)
                await msg.edit(embed=discord.Embed(description=f"Alright I , created {channel1.mention} for logging of server updates like emoji update , icon change, etc .", color=self.color), view=None)                
                web = await channel1.create_webhook(name=f"{str(self.bot.user.name)} | Server Logs")
                await msg.edit(embed=discord.Embed(description="Please wait...", color=self.color), view=None)
                
                data = getLogging(ctx.guild.id)
                data["server"] = web.url
                updateLogging(ctx.guild.id, data)
                hacker = discord.Embed(
                        description=
                        f"<:GreenTick:1029990379623292938> | Successfully setuped server logs for {ctx.guild.name} and created {channel1.mention} for logging of server updates like emoji update , icon change, etc .",
                        color=self.color)
                await msg.edit(embed=hacker,view=None)
                
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5) 
            
            
            
##############EVENTS#################

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await self.bot.wait_until_ready()
        if not member.guild:
            return
        if not member.guild.me.guild_permissions.view_audit_log:
            return
        data = getLogging(member.guild.id)
        ch= data["member"]
        if ch is not None:
            c = discord.SyncWebhook.from_url(ch)
            if c is None:
                return 
            em = discord.Embed(title="A member joined the server", description=f"Username: {str(member)}\nUser id: {member.id}\nAccount created at: <t:{round(member.created_at.timestamp())}:R>", color=self.color)
            if member.bot:
                async for entry in member.guild.audit_logs(limit=1,after=datetime.datetime.now() - datetime.timedelta(minutes=2),action=discord.AuditLogAction.bot_add):
                    em.title = "A bot added to the server"
                    m = entry.user
                    em.add_field(name="Bot added by:", value=f"{str(m)} - [{m.id}] {m.mention}")
            em.set_author(name=f"{str(member)}", icon_url=member.display_avatar.url)
            em.set_footer(text="Joined", icon_url=member.guild.me.display_avatar.url)
            em.timestamp = datetime.datetime.utcnow()
            em.set_thumbnail(url=member.display_avatar.url)
            c.send(embed=em,avatar_url=self.bot.user.avatar.url)     
            return 
        return 
######################################



    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        await self.bot.wait_until_ready()
        if not member.guild:
            return
        if not member.guild.me.guild_permissions.view_audit_log:
            return  
        kick = False   
        if member.guild.me.guild_permissions.view_audit_log:
            async for entry in member.guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(seconds=3),
                action=discord.AuditLogAction.kick):
                x = datetime.datetime.now() - datetime.timedelta(seconds=10)
                if entry.target.id == member.id and x.timestamp() <= entry.created_at.timestamp():
                    kick = True
                    m = entry.user
                    if not m.guild:
                      return
                    if entry.reason:
                        r = entry.reason                         
                          
        data = getLogging(member.guild.id)
        ch= data["member"]
        if ch is not None:
            c = discord.SyncWebhook.from_url(ch)
            if c is None:
                return 
            em = discord.Embed(title="A member left the server", description=f"Username: {str(member)}\nUser id: {member.id}\nAccount created at: <t:{round(member.created_at.timestamp())}:R>", color=self.color)
            em.set_author(name=f"{str(member)}", icon_url=member.display_avatar.url)
            em.set_footer(text="Left", icon_url=member.guild.me.display_avatar.url)
            em.timestamp = datetime.datetime.utcnow()
            em.set_thumbnail(url=member.display_avatar.url)
            c.send(embed=em)
        if kick:
            if ch is not None:
                c = discord.SyncWebhook.from_url(ch)              
                if c is None:
                    return
                em = discord.Embed(title="A member got kicked from the server", description=f"Username: {str(member)}\nUser id: {member.id}\nAccount created at: <t:{round(member.created_at.timestamp())}:R>", color=self.color)
                em.add_field(name="Kicked by:", value=f"{str(m)} - [{m.id}] {m.mention}")
                if r:
                    em.add_field(name="Reason:", value=r)
                em.set_author(name=f"{str(member)}", icon_url=member.display_avatar.url)
                em.set_footer(text="Kicked", icon_url=member.guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                em.set_thumbnail(url=member.display_avatar.url)
                c.send(embed=em,avatar_url=self.bot.user.avatar.url)
                return 
        return 
################################



    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member,
                               after: discord.Member) -> None:
        await self.bot.wait_until_ready()
        if not after.guild:
            return
        if not after.guild is None and not after.guild.me.guild_permissions.view_audit_log:
            return
        data = getLogging(after.guild.id)
        ch= data["member"]
 
        async for entry in after.guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(seconds=3),
                action=discord.AuditLogAction.member_update):
                if ch is not None:
                    c = discord.SyncWebhook.from_url(ch)    
                    if c is None:
                        return
                    member = entry.target
                    if not member.guild:
                      return
                    em = discord.Embed(title="A member updated", color=self.color)
                    em.set_author(name=f"{str(member)}", icon_url=member.display_avatar.url)
                    em.set_footer(text="UPDATED", icon_url=member.guild.me.display_avatar.url)
                    em.timestamp = datetime.datetime.utcnow()
                    em.set_thumbnail(url=member.display_avatar.url)
                    if after.nick != before.nick:
                        em.description=f"Nickname changed:\n`{before.nick}` to `{after.nick}`"
                        em.add_field(name="Nick changed by:", value=f"{str(entry.user)} - [{entry.user.id}] {entry.user.mention}")
                        em.title = "A member's nickname changed"
                        c.send(embed=em)
                        return 
                    if len(after.roles) != len(before.roles):
                        async for ent in after.guild.audit_logs(
                                        limit=1,
                                        after=datetime.datetime.now() - datetime.timedelta(seconds=3),
                                        action=discord.AuditLogAction.member_role_update):
                            check = False
                            if len(after.roles) > len(before.roles):
                                for r in after.roles:
                                    if r.id == after.guild.premium_subscriber_role.id:
                                        continue
                                    if r not in before.roles:
                                        em.add_field(name="Role Added:", value=f"{r.mention} - [{r.id}]")
                                        em.add_field(name="Role Added by:", value=f"{str(ent.user)} - [{ent.user.id}] {ent.user.mention}")
                                        x = "No"
                                        if after.top_role != before.top_role:
                                            x = "Yes"
                                        em.add_field(name="Top role changed?", value=x)
                                        em.title = "A member's role changed"
                                        check = True
                            else:
                                for r in before.roles:
                                    if r.id == after.guild.premium_subscriber_role.id:
                                        continue
                                    if r not in after.roles:
                                        em.add_field(name="Role Removed:", value=f"{r.mention} - [{r.id}]")
                                        em.add_field(name="Role Removed by:", value=f"{str(ent.user)} - [{ent.user.id}] {ent.user.mention}")
                                        x = "No"
                                        if after.top_role != before.top_role:
                                            x = "Yes"
                                        em.add_field(name="Top role changed?", value=x)
                                        em.title = "A member's role changed"
                                        check = True
                            if ent.reason:
                                em.add_field(name="Reason", value=ent.reason)
                            em.set_author(name=f"{str(ent.target)}", icon_url=ent.target.display_avatar.url)
                            em.set_footer(text="UPDATED", icon_url=ent.target.guild.me.display_avatar.url)
                            em.timestamp = datetime.datetime.utcnow()
                            em.set_thumbnail(url=ent.target.display_avatar.url)
                            if check:
                                return c.send(embed=em,avatar_url=self.bot.user.avatar.url)       
                            



    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, member: discord.Member):
        await self.bot.wait_until_ready()
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        data = getLogging(guild.id)
        ch= data["mod"]
        if ch is not None:
            return
        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.utcnow() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.ban):
            if ch is not None:
                m = entry.user
                if not m.guild:
                    return
                c = discord.SyncWebhook.from_url(ch)    
                
                if c is None:
                    return
                em = discord.Embed(title="A member got banned from the server", description=f"Username: {str(member)}\nUser id: {member.id}\nAccount created at: <t:{round(member.created_at.timestamp())}:R>", color=self.color)
                em.add_field(name="Banned by:", value=f"{str(m)} - [{m.id}] {m.mention}")
                if entry.reason:
                    em.add_field(name="Reason:", value=entry.reason)
                em.set_author(name=f"{str(member)}", icon_url=member.display_avatar.url)
                em.set_footer(text="Banned", icon_url=member.guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                em.set_thumbnail(url=member.display_avatar.url)
                c.send(embed=em,avatar_url=self.bot.user.avatar.url) 
                return       
  
  
  
    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, member: discord.Member):
        await self.bot.wait_until_ready()
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        data = getLogging(guild.id)
        ch= data["mod"]
        if ch is None:
            return
        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.now() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.unban):
            if ch is not None:
                m = entry.user
                if not m.guild:
                    return
                c = discord.SyncWebhook.from_url(ch)                   
                if c is None:
                    return
                em = discord.Embed(title="A member got unbanned from the server", description=f"Username: {str(member)}\nUser id: {member.id}\nAccount created at: <t:{round(member.created_at.timestamp())}:R>", color=self.color)
                em.add_field(name="Unbanned by:", value=f"{str(m)} - [{m.id}] {m.mention}")
                if entry.reason:
                    em.add_field(name="Reason:", value=entry.reason)
                em.set_author(name=f"{str(member)}", icon_url=member.display_avatar.url)
                em.set_footer(text="Unbanned", icon_url=guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                em.set_thumbnail(url=member.display_avatar.url)
                c.send(embed=em,avatar_url=self.bot.user.avatar.url)  
                return 
            return     
                
                
                
    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role) -> None:
        await self.bot.wait_until_ready()
        guild = role.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        data = getLogging(role.guild.id)
        ch= data["role"]
        if ch is None:
            return
        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.now() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.role_create):
            if ch is not None:
                m = entry.user
                if not m.guild:
                    return
                c = discord.SyncWebhook.from_url(ch)     
                
                if c is None:
                    return
                em = discord.Embed(title="Role Created", description=f"Role {role.mention} Created by {entry.user.mention}", color=self.color)
                em.add_field(name="Name", value=f"{role.name}")
                em.add_field(name="Colour", value=f"{role.color}")
                em.add_field(name="Mentionable", value=role.mentionable)
                em.add_field(name="Hoist", value=role.hoist)
                em.add_field(name="Position", value=role.position + 1)
                role_perm = ', '.join([str(p[0]).replace("_", " ").title() for p in role.permissions if p[1]])
                if role_perm is None:
                    role_perm = "No Permissions"
                em.add_field(name="Permissions", value=role_perm)
                if entry.reason:
                    em.add_field(name="Reason:", value=entry.reason)
                em.set_author(name=f"{str(entry.user)}", icon_url=entry.user.display_avatar.url)
                em.set_footer(text="Created", icon_url=guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                em.set_thumbnail(url=entry.user.display_avatar.url)
                if len(em.fields) > 0:
                    c.send(embed=em,avatar_url=self.bot.user.avatar.url)
                    return 
                    
                    
                    
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role) -> None:
        await self.bot.wait_until_ready()
        guild = role.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        data = getLogging(role.guild.id)
        ch= data["role"]
        if ch is None:
            return
        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.now() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.role_delete):
            if ch is not None:
                m = entry.user
                if not m.guild:
                    return
                c = discord.SyncWebhook.from_url(ch)     
                
                if c is None:
                    return
                em = discord.Embed(title="Role Deleted", description=f"Role `{role.name}` Deleted by {entry.user.mention}", color=self.color)
                em.add_field(name="Name", value=f"{role.name}")
                em.add_field(name="Colour", value=f"{role.color}")
                em.add_field(name="Mentionable", value=role.mentionable)
                em.add_field(name="Hoist", value=role.hoist)
                em.add_field(name="Members", value=len(role.members))
                role_perm = ', '.join([str(p[0]).replace("_", " ").title() for p in role.permissions if p[1]])
                if role_perm is None:
                    role_perm = "No Permissions"
                em.add_field(name="Permissions", value=role_perm)
                if entry.reason:
                    em.add_field(name="Reason:", value=entry.reason)
                em.set_author(name=f"{str(entry.user)}", icon_url=entry.user.display_avatar.url)
                em.set_footer(text="Deleted", icon_url=guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                em.set_thumbnail(url=entry.user.display_avatar.url)
                if len(em.fields) > 0:
                    c.send(embed=em,avatar_url=self.bot.user.avatar.url)
                    return 
                    
                    
    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role,
                                   after: discord.Role) -> None:
        await self.bot.wait_until_ready()
        guild = after.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        data = getLogging(after.guild.id)
        ch= data["role"]
        if ch is None:
            return
        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.now() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.role_update):
            if ch is not None:
                m = entry.user
                if not m.guild:
                    return
                c = discord.SyncWebhook.from_url(ch)     
                
                if c is None:
                    return
                em = discord.Embed(title="Role Updated", description=f"Role {after.mention} Updated by {entry.user.mention}", color=self.color)
                if before.name != after.name:
                    em.add_field(name="Name changed", value=f"`{before.name}` to `{after.name}`")
                if before.color != after.color:
                    em.add_field(name="Color changed", value=f"{before.color} to {after.color}")
                if before.hoist != after.hoist:
                    em.add_field(name="Hoist changed", value=f'{"False" if after.hoist == True else "True"} to {after.hoist}')
                if before.mentionable != after.mentionable:
                    em.add_field(name="Mentionable changed", value=f'{"False" if after.mentionable == True else "True"} to {after.mentionable}')
                if before.permissions.value != after.permissions.value:
                    all_perm = []
                    b_perm = {}
                    a_perm = {}
                    given_perm = []
                    removed_perm = []
                    for i in before.permissions:
                        b_perm[i[0]] = i[1]
                        all_perm.append(i[0])
                    for i in after.permissions:
                        a_perm[i[0]] = i[1]
                    for i in all_perm:
                        if a_perm[i] != b_perm[i]:
                            if a_perm[i] == True:
                                given_perm.append(i)
                            else:
                                removed_perm.append(i)
                    if len(given_perm) > 0:
                        des = ', '.join([str(p).replace("_", " ").title() for p in given_perm])
                        em.add_field(name="Permissions given", value=des)
                    if len(removed_perm) > 0:
                        des1 = ', '.join([str(p).replace("_", " ").title() for p in removed_perm])
                        em.add_field(name="Permissions removed", value=des1)
                if before.icon != after.icon:
                    if before.icon is None:
                      d = f"None to [New Icon]({after.icon.url})"
                    elif after.icon is None:
                      d = f"[Old Icon]({before.icon.url}) to None"
                    else:
                      d = f"[Old Icon]({before.icon.url}) to [New Icon]({after.icon.url})"
                    em.add_field(name="Role icon changed", value=d)
                if entry.reason:
                    em.add_field(name="Reason:", value=entry.reason)
                em.set_author(name=f"{str(entry.user)}", icon_url=entry.user.display_avatar.url)
                em.set_footer(text="Updated", icon_url=guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                em.set_thumbnail(url=entry.user.display_avatar.url)
                if len(em.fields) > 0:
                    c.send(embed=em,avatar_url=self.bot.user.avatar.url)
                    return 
                   
                   
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel) -> None:
        await self.bot.wait_until_ready()
        guild = channel.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        data = getLogging(channel.guild.id)
        ch= data["channel"]
        if ch is None:
            return
        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.now() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.channel_create):
            if ch is not None:
                m = entry.user
                if not m.guild:
                    return
                c = discord.SyncWebhook.from_url(ch)     
                
                if c is None:
                    return
                if isinstance(channel, discord.TextChannel):
                    em = discord.Embed(title="Text Channel Created", description=f"Text Channel {channel.mention} Created by {entry.user.mention}", color=self.color)
                if isinstance(channel, discord.VoiceChannel):
                    em = discord.Embed(title="Voice Channel Created", description=f"Voice Channel {channel.mention} Created by {entry.user.mention}", color=self.color)
                if isinstance(channel, discord.CategoryChannel):
                    em = discord.Embed(title="Category Created", description=f"Category Channel {channel.mention} Created by {entry.user.mention}", color=self.color)
                if isinstance(channel, discord.StageChannel):
                    em = discord.Embed(title="Stage Channel Created", description=f"Stage Channel {channel.mention} Created by {entry.user.mention}", color=self.color)
                em.add_field(name="Name", value=f"{channel.name}")
                em.add_field(name="Position", value=channel.position + 1)
                overwrite = channel.overwrites_for(guild.default_role)
                em.add_field(name="Private?", value=f'{"Yes" if not overwrite.view_channel else "No"}')
                em.add_field(name="Permissions synced?", value=f'{"Yes" if channel.permissions_synced else "No"}')
                if isinstance(channel, discord.VoiceChannel) or isinstance(channel, discord.StageChannel):
                    em.add_field(name="Bitrate", value=channel.bitrate/1000)
                if channel.category:
                    em.add_field(name="Category", value=f"{channel.category.name} - [{channel.category_id}")
                if entry.reason:
                    em.add_field(name="Reason:", value=entry.reason)
                em.set_author(name=f"{str(entry.user)}", icon_url=entry.user.display_avatar.url)
                em.set_footer(text="Created", icon_url=guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                em.set_thumbnail(url=entry.user.display_avatar.url)
                if len(em.fields) > 0:
                    c.send(embed=em,avatar_url=self.bot.user.avatar.url)
                    return 
                
                

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel) -> None:
        await self.bot.wait_until_ready()
        guild = channel.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        data = getLogging(channel.guild.id)
        ch= data["channel"]
        if ch is None:
            return
        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.now() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.channel_delete):
            if ch is not None:
                m = entry.user
                if not m.guild:
                    return
                c = discord.SyncWebhook.from_url(ch)   
                if c is None:
                    return
                if isinstance(channel, discord.TextChannel):
                    em = discord.Embed(title="Text Channel Deleted", description=f"Text Channel {channel.mention} Deleted by {entry.user.mention}", color=self.color)
                if isinstance(channel, discord.VoiceChannel):
                    em = discord.Embed(title="Voice Channel Deleted", description=f"Voice Channel {channel.mention} Deleted by {entry.user.mention}", color=self.color)
                if isinstance(channel, discord.CategoryChannel):
                    em = discord.Embed(title="Category Deleted", description=f"Category Channel {channel.mention} Deleted by {entry.user.mention}", color=self.color)
                if isinstance(channel, discord.StageChannel):
                    em = discord.Embed(title="Stage Channel Deleted", description=f"Stage Channel {channel.mention} Deleted by {entry.user.mention}", color=self.color)
                em.add_field(name="Name", value=f"{channel.name}")
                em.add_field(name="Position", value=channel.position + 1)
                overwrite = channel.overwrites_for(guild.default_role)
                em.add_field(name="Permissions synced?", value=f'{"Yes" if channel.permissions_synced else "No"}')
                if isinstance(channel, discord.VoiceChannel) or isinstance(channel, discord.StageChannel):
                    em.add_field(name="Bitrate", value=f"{channel.bitrate/1000} kbps")
                if channel.category:
                    em.add_field(name="Category", value=f"{channel.category.name} - [{channel.category_id}")
                if entry.reason:
                    em.add_field(name="Reason:", value=entry.reason)
                em.set_author(name=f"{str(entry.user)}", icon_url=entry.user.display_avatar.url)
                em.set_footer(text="Deleted", icon_url=guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                em.set_thumbnail(url=entry.user.display_avatar.url)
                if len(em.fields) > 0:
                    c.send(embed=em,avatar_url=self.bot.user.avatar.url)
                    return 
                    
                    
                    
    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel,
                                   after: discord.abc.GuildChannel) -> None:
        await self.bot.wait_until_ready()
        guild = after.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        data = getLogging(guild.id)
        ch= data["channel"]
        if ch is None:
            return
        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.now() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.channel_update):
            if ch is not None:
                m = entry.user
                if not m.guild:
                    return
                c = discord.SyncWebhook.from_url(ch)     
                if c is None:
                    return
                if isinstance(after, discord.TextChannel):
                    em = discord.Embed(title="Text Channel Updated", description=f"Text Channel {after.mention} Updated by {entry.user.mention}", color=self.color)
                if isinstance(after, discord.VoiceChannel):
                    em = discord.Embed(title="Voice Channel Updated", description=f"Voice Channel {after.mention} Updated by {entry.user.mention}", color=self.color)
                if isinstance(after, discord.CategoryChannel):
                    em = discord.Embed(title="Category Updated", description=f"Category Channel {after.mention} Updated by {entry.user.mention}", color=self.color)
                if isinstance(after, discord.StageChannel):
                    em = discord.Embed(title="Stage Channel Updated", description=f"Stage Channel {after.mention} Updated by {entry.user.mention}", color=self.color)
                if before.name != after.name:
                    em.add_field(name="Name changed", value=f"`{before.name}` to `{after.name}`")
                if isinstance(after, discord.TextChannel) and isinstance(before, discord.TextChannel):
                    if before.topic != after.topic:
                        em.add_field(name="Channel's topic updated", value=f"`{before.topic}` to `{after.topic}`")
                    if before.slowmode_delay != after.slowmode_delay:
                        em.add_field(name="Slowmode delay updated", value=f"`{before.slowmode_delay} Seconds` to `{after.slowmode_delay} Seconds`")
                    if before.nsfw != after.nsfw:
                        em.add_field(name="NSFW State updated", value=f'{"Yes to No" if before.nsfw else "No to Yes"}')
                if isinstance(after, discord.VoiceChannel) and isinstance(before, discord.VoiceChannel):
                    if before.slowmode_delay != after.slowmode_delay:
                        em.add_field(name="Bitrate updated", value=f"`{before.bitrate/1000} kbps` to `{after.bitrate/1000} kbps`")
                    if before.user_limit != after.user_limit:
                        em.add_field(name="User Limit updated", value=f"`{before.user_limit} users` to `{after.user_limit} users`")
                if entry.reason:
                    em.add_field(name="Reason:", value=entry.reason)
                em.set_author(name=f"{str(entry.user)}", icon_url=entry.user.display_avatar.url)
                em.set_footer(text="Updated", icon_url=guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                em.set_thumbnail(url=entry.user.display_avatar.url)
                if len(em.fields) > 0:
                    c.send(embed=em,avatar_url=self.bot.user.avatar.url)
                    return 
                    
                    
                    
    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild,
                              after: discord.Guild) -> None:
        await self.bot.wait_until_ready()
        guild = after
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        data = getLogging(guild.id)
        ch= data["server"]
        if ch is None:
            return
        async for entry in after.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.guild_update):
            if ch is not None:
                m = entry.user
                if not m.guild:
                    return
                c = discord.SyncWebhook.from_url(ch)   
                if c is None:
                    return
                em = discord.Embed(title="Server Updated", description=f"Server Updated by {entry.user.mention}", color=self.color)
                if before.name != after.name:
                    em.add_field(name="Server Name changed", value=f"`{before.name}` to `{after.name}`")
                if before.icon != after.icon:
                    if before.icon is None:
                      d = f"None to [New Icon]({after.icon.url})"
                    elif after.icon is None:
                      d = f"[Old Icon]({before.icon.url}) to None"
                    else:
                      d = f"[Old Icon]({before.icon.url}) to [New Icon]({after.icon.url})"
                    em.add_field(name="Guild icon changed", value=d)
                if before.banner != after.banner:
                    if before.banner is None:
                      d = f"None to [New Banner]({after.banner.url})"
                    elif after.icon is None:
                      d = f"[Old Banner]({before.banner.url}) to None"
                    else:
                      d = f"[Old Banner]({before.banner.url}) to [New Banner]({after.banner.url})"
                    em.add_field(name="Guild Banner changed", value=d)
                if before.owner_id != after.owner_id:
                    em.add_field(name="Ownership Transfered", value=f"From: {before.owner.mention} - [{before.owner_id}\nTo: {after.owner.mention} - [{after.owner_id}]")
                if 'VANITY_URL' in before.features and 'VANITY_URL' in after.verification_level:
                    bvanity = await before.vanity_invite()
                    avanity = await after.vanity_invite()
                    bvanity = str(bvanity).replace("https://discord.gg/", "")
                    avanity = str(avanity).replace("https://discord.gg/", "")
                    if bvanity != avanity:
                        em.add_field(name="Server Vanity Changed", value=f"`{bvanity}` to `{avanity}`")
                if before.description != after.description:
                    em.add_field(name="Server's Description Updated", value=f"`{str(before.description)}` to `{str(after.description)}`")
                if before.verification_level != after.verification_level:
                    em.add_field(name="Server Verification Updated", value=f"`{str(before.verification_level)}` to `{str(after.verification_level)}`")
                if before.features != after.features:
                    afeat = ['VIP_REGIONS','VANITY_URL','INVITE_SPLASH','VERIFIED','PARTNERED','MORE_EMOJI','DISCOVERABLE','FEATURABLE','COMMUNITY','COMMERCE','PUBLIC','NEWS','BANNER','ANIMATED_ICON','PUBLIC_DISABLED','WELCOME_SCREEN_ENABLED','MEMBER_VERIFICATION_GATE_ENABLED','PREVIEW_ENABLED']
                    fadd = ""
                    fremoved = ""
                    for i in afeat:
                        if i in before.features and i not in after.features:
                            fremoved += f"{i.capitalize()}, "
                        if i not in before.features and i in after.features:
                            fadd += f"{i.capitalize()}, "
                    if len(fadd) > 0:
                        em.add_field(name="Features Added", value=fadd[:-2])
                    if len(fremoved) > 0:
                        em.add_field(name="Features Removed", value=fremoved[:-2])
                if before.system_channel != after.system_channel:
                    if before.system_channel is None:
                        bmen = "None"
                    else:
                        bmen = before.system_channel.mention
                    if after.system_channel is None:
                        amen = "None"
                    else:
                        amen = after.system_channel.mention                    
                    em.add_field(name="Server's System Channel Updated", value=f"{bmen} to {amen}")
                if before.rules_channel != after.rules_channel:
                    if before.rules_channel is None:
                        bmen = "None"
                    else:
                        bmen = before.rules_channel.mention
                    if after.rules_channel is None:
                        amen = "None"
                    else:
                        amen = after.rules_channel.mention       
                    em.add_field(name="Server's Rules Channel Updated", value=f"{bmen} to {amen}")
                if before.afk_channel != after.afk_channel:
                    if before.afk_channel is None:
                        bmen = "None"
                    else:
                        bmen = before.afk_channel.mention
                    if after.afk_channel is None:
                        amen = "None"
                    else:
                        amen = after.afk_channel.mention       
                    em.add_field(name="Afk Channel Updated", value=f"{bmen} to {amen}")
                if before.afk_timeout != after.afk_timeout:
                    em.add_field(name="Afk Timeout Updated", value=f"`{int(before.afk_timeout)} Minutes` to `{int(after.afk_timeout)} Minutes`")
                if entry.reason:
                    em.add_field(name="Reason:", value=entry.reason)
                em.set_author(name=f"{str(entry.user)}", icon_url=entry.user.display_avatar.url)
                em.set_footer(text="Updated", icon_url=guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                em.set_thumbnail(url=entry.user.display_avatar.url)
                if len(em.fields) > 0:
                    c.send(embed=em,avatar_url=self.bot.user.avatar.url)
                    return 
                    
                    
                    
                    
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after:discord.Message):
        await self.bot.wait_until_ready()
        if before.author.bot:
            return
        guild = after.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        data = getLogging(guild.id)
        ch= data["message"]
        if ch is None:
            return
        if ch is not None:
            c = discord.SyncWebhook.from_url(ch)   
            
            if c is None:
                return
            em = discord.Embed(description=f":scroll: Message sent by {after.author.mention} edited in {after.channel.mention} [Jump to message]({after.jump_url})", color=self.color)
            em.add_field(name="Before", value=f"```{before.content}```", inline=False)
            em.add_field(name="After", value=f"```{after.content}```", inline=False)
            em.set_author(name=f"{str(after.author)}", icon_url=after.author.display_avatar.url)
            em.set_footer(text="Edited", icon_url=guild.me.display_avatar.url)
            em.timestamp = datetime.datetime.utcnow()
            if len(em.fields) > 0:
                c.send(embed=em,avatar_url=self.bot.user.avatar.url)
                return

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        await self.bot.wait_until_ready()
        guild = message.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        data = getLogging(guild.id)
        ch= data["message"]
        if ch is None:
            return
        if message.author.bot:
            return
        async for entry in message.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.message_delete):
            if ch is not None:
                c = discord.SyncWebhook.from_url(ch)   
                
                if c is None:
                    return
                em = discord.Embed(description=f":put_litter_in_its_place: Message sent by {message.author.mention} deleted in {message.channel.mention}", color=self.color)
                url = None
                for x in message.attachments:
                    url = x.url
                if message.content == "":
                    content = "***Content Unavailable***"
                else:
                    content = message.content
                em.add_field(name="__Content__:",
                                  value=f"{content}",
                                  inline=False)
                x = datetime.datetime.now() - datetime.timedelta(seconds=5)
                if entry.user is not None and entry.target.id == message.author.id and x.timestamp() <= entry.created_at.timestamp():
                    em.add_field(name="**Deleted By:**",
                                    value=f"{entry.user.mention} (ID: {entry.user.id})")
                if url is not None:
                    if url.startswith("http") or url.startswith("http"):
                        em.set_image(url=url)
                em.set_author(name=f"{str(message.author)}", icon_url=message.author.display_avatar.url)
                em.set_footer(text="Deleted", icon_url=guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                if len(em.fields) > 0:
                    c.send(embed=em,avatar_url=self.bot.user.avatar.url)
                    return 

  