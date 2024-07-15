import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from utils.Tools import *
import json

tick = "✅"
cross = "❌"
error = "⚠"

class Server(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.color =0x2f3136
    async def add_role(self, *, role: int, member: discord.Member):
        if member.guild.me.guild_permissions.manage_roles:
            role = discord.Object(id=int(role))
            await member.add_roles(role, reason=f"{self.bot.user.name} | Customroles")
        

    async def remove_role(self, *, role: int, member: discord.Member):
        if member.guild.me.guild_permissions.manage_roles:
            role = discord.Object(id=int(role))
            await member.remove_roles(role, reason=f"{self.bot.user.name} | Customroles")
 

    @commands.hybrid_command(name="staff",
                             description="Gives the staff role to the user .",
                             aliases=['official'],
                             help="Gives the staff role to the user .")
    @blacklist_check()
    @ignore_check()
    
    async def _staff(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            lol = data['reqrole']
            own = data['staff']  
            role = context.guild.get_role(own)
            if data["reqrole"] != None:
                req = context.guild.get_role(lol)
                if context.author == context.guild.owner or req in context.author.roles:
                    if data["staff"] != None:
                        if role not in member.roles:
                            await self.add_role(role=own, member=member)
                            
                            hacker = discord.Embed(
                description=
                f"{tick} | Successfully Given <@&{own}> To {member.mention}",
                color=self.color)
                            hacker.set_author(name=context.author,
                              icon_url=context.author.display_avatar.url)
                            await context.send(embed=hacker)
                        elif role in member.roles:
                            await self.remove_role(role=own, member=member)
                            hacker6 = discord.Embed(
                description=
                f"{tick} | Successfully Removed <@&{own}> From {member.mention}",
                color=self.color)
                            hacker6.set_author(name=context.author,
                              icon_url=context.author.display_avatar.url)
                            await context.send(embed=hacker6)                             
                    else:
                        hacker1 = discord.Embed(
                description=
                f"{error} | Staff role is not setuped in {context.guild.name}",
                color=self.color)
                        hacker1.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                        hacker1.set_thumbnail(url=context.author.display_avatar.url)
                        await context.send(embed=hacker1)
                else:
                    hacker3 = discord.Embed(
                description=
                f"{error} | You need {req.mention} to run this command .",
                color=self.color)
                    hacker3.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                    
                    await context.send(embed=hacker3)

            else:
                hacker4 = discord.Embed(
                description=
                f"{error} | Req role is not setuped in {context.guild.name}",
                color=self.color)
                hacker4.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                
                await context.send(embed=hacker4)  


    @commands.hybrid_command(name="girl",
                             description="Gives the girl role to the user .",
                             aliases=['cuties', 'qt'],
                             help="Gives the girl role to the user .")
    @blacklist_check()
    @ignore_check()
  #  @commands.has_permissions(administrator=True)
    async def _girl(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            lol = data['reqrole']
            own = data['girl']  
            role = context.guild.get_role(own)
            if data["reqrole"] != None:
                req = context.guild.get_role(lol)
                if context.author == context.guild.owner or req in context.author.roles:
                    if data["girl"] != None:
                        if role not in member.roles:
                            await self.add_role(role=own, member=member)
                            
                            hacker = discord.Embed(
                description=
                f"{tick} | Successfully Given <@&{own}> To {member.mention}",
                color=self.color)
                            hacker.set_author(name=context.author,
                              icon_url=context.author.display_avatar.url)
                            await context.send(embed=hacker)
                        elif role in member.roles:
                            await self.remove_role(role=own, member=member)
                            hacker6 = discord.Embed(
                description=
                f"{tick} | Successfully Removed <@&{own}> From {member.mention}",
                color=self.color)
                            hacker6.set_author(name=context.author,
                              icon_url=context.author.display_avatar.url)
                            await context.send(embed=hacker6)       
                    else:
                        hacker1 = discord.Embed(
                description=
                f"{error} | Girl role is not setuped in {context.guild.name}",
                color=self.color)
                        hacker1.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                        hacker1.set_thumbnail(url=context.author.display_avatar.url)
                        await context.send(embed=hacker1)
                else:
                    hacker3 = discord.Embed(
                description=
                f"{error} | You need {req.mention} to run this command .",
                color=self.color)
                    hacker3.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                    
                    await context.send(embed=hacker3)

            else:
                hacker4 = discord.Embed(
                description=
                f"{error} | Req role is not setuped in {context.guild.name}",
                color=self.color)
                hacker4.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                
                await context.send(embed=hacker4)  
    
    @commands.hybrid_command(name="vip",
                             description="Gives the vip role to the user .",
                             help="Gives the vip role to the user .")
    @blacklist_check()
    @ignore_check()
    
    async def _vip(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            lol = data['reqrole']
            own = data['vip']  
            role = context.guild.get_role(own)
            if data["reqrole"] != None:
                req = context.guild.get_role(lol)
                if context.author == context.guild.owner or req in context.author.roles:
                    if data["vip"] != None:
                        if role not in member.roles:
                            await self.add_role(role=own, member=member)
                            
                            hacker = discord.Embed(
                description=
                f"{tick} | Successfully Given <@&{own}> To {member.mention}",
                color=self.color)
                            hacker.set_author(name=context.author,
                              icon_url=context.author.display_avatar.url)
                            await context.send(embed=hacker)
                        elif role in member.roles:
                            await self.remove_role(role=own, member=member)
                            hacker6 = discord.Embed(
                description=
                f"{tick} | Successfully Removed <@&{own}> From {member.mention}",
                color=self.color)
                            hacker6.set_author(name=context.author,
                              icon_url=context.author.display_avatar.url)
                            await context.send(embed=hacker6)       
                    else:
                        hacker1 = discord.Embed(
                description=
                f"{error} | Vip role is not setuped in {context.guild.name}",
                color=self.color)
                        hacker1.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                        hacker1.set_thumbnail(url=context.author.display_avatar.url)
                        await context.send(embed=hacker1)
                else:
                    hacker3 = discord.Embed(
                description=
                f"{error} | You need {req.mention} to run this command .",
                color=self.color)
                    hacker3.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                    
                    await context.send(embed=hacker3)

            else:
                hacker4 = discord.Embed(
                description=
                f"{error} | Req role is not setuped in {context.guild.name}",
                color=self.color)
                hacker4.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                
                await context.send(embed=hacker4)


    @commands.hybrid_command(name="guest",
                             description="Gives the guest role to the user .",
                             help="Gives the guest role to the user .")
    @blacklist_check()
   # @commands.has_permissions(administrator=True)
    async def _guest(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            lol = data['reqrole']
            own = data['guest']
            role = context.guild.get_role(own)  
            if data["reqrole"] != None:
                req = context.guild.get_role(lol)
                if context.author == context.guild.owner or req in context.author.roles:
                    if data["guest"] != None:
                        if role not in member.roles:
                            await self.add_role(role=own, member=member)
                            
                            hacker = discord.Embed(
                description=
                f"{tick} | Successfully Given <@&{own}> To {member.mention}",
                color=self.color)
                            hacker.set_author(name=context.author,
                              icon_url=context.author.display_avatar.url)
                            await context.send(embed=hacker)
                        elif role in member.roles:
                            await self.remove_role(role=own, member=member)
                            hacker6 = discord.Embed(
                description=
                f"{tick} | Successfully Removed <@&{own}> From {member.mention}",
                color=self.color)
                            hacker6.set_author(name=context.author,
                              icon_url=context.author.display_avatar.url)
                            await context.send(embed=hacker6)       
                    else:
                        hacker1 = discord.Embed(
                description=
                f"{error} | Guest role is not setuped in {context.guild.name}",
                color=self.color)
                        hacker1.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                        hacker1.set_thumbnail(url=context.author.display_avatar.url)
                        await context.send(embed=hacker1)
                else:
                    hacker3 = discord.Embed(
                description=
                f"{error} | You need {req.mention} to run this command .",
                color=self.color)
                    hacker3.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                    
                    await context.send(embed=hacker3)

            else:
                hacker4 = discord.Embed(
                description=
                f"{error} | Req role is not setuped in {context.guild.name}",
                color=self.color)
                hacker4.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                
                await context.send(embed=hacker4)

    
    @commands.hybrid_command(name="friend",
                             description="Gives the friend role to the user .",
                             aliases=['frnd'],
                             help="Gives the friend role to the user .")
    @ignore_check()
    @blacklist_check()
   # @commands.has_permissions(administrator=True)
    async def _friend(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            lol = data['reqrole']
            own = data['frnd'] 
            role = context.guild.get_role(own) 
            if data["reqrole"] != None:
                req = context.guild.get_role(lol)
                if context.author == context.guild.owner or req in context.author.roles:
                    if data["frnd"] != None:
                        if role not in member.roles:
                            await self.add_role(role=own, member=member)
                            
                            hacker = discord.Embed(
                description=
                f"{tick} | Successfully Given <@&{own}> To {member.mention}",
                color=self.color)
                            hacker.set_author(name=context.author,
                              icon_url=context.author.display_avatar.url)
                            await context.send(embed=hacker)
                        elif role in member.roles:
                            await self.remove_role(role=own, member=member)
                            hacker6 = discord.Embed(
                description=
                f"{tick} | Successfully Removed <@&{own}> From {member.mention}",
                color=self.color)
                            hacker6.set_author(name=context.author,
                              icon_url=context.author.display_avatar.url)
                            await context.send(embed=hacker6)       
                    else:
                        hacker1 = discord.Embed(
                description=
                f"{error} | Friend role is not setuped in {context.guild.name}",
                color=self.color)
                        hacker1.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                        hacker1.set_thumbnail(url=context.author.display_avatar.url)
                        await context.send(embed=hacker1)
                else:
                    hacker3 = discord.Embed(
                description=
                f"{error} | You need {req.mention} to run this command .",
                color=self.color)
                    hacker3.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                    
                    await context.send(embed=hacker3)

            else:
                hacker4 = discord.Embed(
                description=
                f"{error} | Req role is not setuped in {context.guild.name}",
                color=self.color)
                hacker4.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                
                await context.send(embed=hacker4)

    @commands.group(
        name="logging",
        invoke_without_command=True, description="Shows the logging's help menu"
    )
    async def logging(self, ctx):
        if ctx.prefix == "<@!1051314800078094417>":
            prefix="@Krypton "
        #elif ctx.prefix != "<@1051314800078094417>":
        else:
            prefix=ctx.prefix
        hacker = discord.utils.get(self.bot.users, id=246469891761111051)
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
        listem.set_footer(text=f"Made by {str(hacker)} & {str(hasan)}" ,  icon_url=hacker.avatar.url)
        await ctx.send(embed=listem)
    
    @commands.hybrid_group(name="setup",
                           description="Setups custom roles for the server .",
                           help="Setups custom roles for the server .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def set(self, ctx: Context):
        prefix=ctx.prefix
        hacker = discord.utils.get(self.bot.users, id=246469891761111051)
        hasan = discord.utils.get(self.bot.users, id=301502732664307716)
        listem = discord.Embed(title=f"Setup (9)", colour=self.color,
                                     description=f"""<...> Duty | [...] Optional\n\n
`{prefix}setup staff <role>` 
Setups girl role for the server .

`{prefix}setup girl <role>`
Setups girl role for the server .

`{prefix}setup friend <role>`
Setups friend role for the server .

`{prefix}setup vip <role>`
Setups vip role for the server .

`{prefix}setup guest <role>`
Setups guest role for the server .

`{prefix}setup reqrole` 
Setups reqrole for customrole commands .

`{prefix}setup create <aliases> <role>`
Setups custom aliase role for the server .

`{prefix}setup delete <aliases>`
Delete a custom aliase role for the server .

`{prefix}setup list` 
Shows custom aliases role for the server .

""")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by {str(hacker)} & {str(hasan)}" ,  icon_url=hacker.avatar.url)
        await ctx.send(embed=listem)

    @set.command(name="staff",
                 description="Setups staff role for the server .",
                 help="Setups staff role for the server .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be added")
    async def staff(self, context: Context, *, role: discord.Role) -> None:
        if context.author == context.guild.owner or context.author.top_role.position > context.guild.me.top_role.position:
            if data := getConfig(context.guild.id):

                data['staff'] = role.id
                updateConfig(context.guild.id, data)
                hacker = discord.Embed(
                    description=
                    f"{tick} | Successfully Setuped `Staff` Role To {role.mention}",
                    color=self.color)
                hacker.set_author(name=context.author,
                                  icon_url=context.author.display_avatar.url)
                hacker.set_thumbnail(url=context.author.display_avatar.url)
                await context.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
            await context.send(embed=hacker5)

    @set.command(name="girl",
                 description="Setups girl role for the server .",
                 help="Setups girl role for the server .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be added")
    async def girl(self, context: Context, *, role: discord.Role) -> None:
        if context.author == context.guild.owner or context.author.top_role.position > context.guild.me.top_role.position:
            if data := getConfig(context.guild.id):

                data['girl'] = role.id
                updateConfig(context.guild.id, data)
                hacker = discord.Embed(
                    description=
                    f"{tick} | Successfully Setuped `girl` Role To {role.mention}",
                    color=self.color)
                hacker.set_author(name=context.author,
                                  icon_url=context.author.display_avatar.url)
                hacker.set_thumbnail(url=context.author.display_avatar.url)
                await context.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
            await context.send(embed=hacker5)

    @set.command(name="vip",
                 description="Setups vip role for the server .",
                 help="Setups vip role for the server .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be added")
    async def vip(self, context: Context, *, role: discord.Role) -> None:
        if context.author == context.guild.owner or context.author.top_role.position > context.guild.me.top_role.position:
            if data := getConfig(context.guild.id):

                data['vip'] = role.id
                updateConfig(context.guild.id, data)
                hacker = discord.Embed(
                    description=
                    f"{tick} | Successfully Setuped `vip` Role To {role.mention}",
                    color=self.color)
                hacker.set_author(name=context.author,
                                  icon_url=context.author.display_avatar.url)
                hacker.set_thumbnail(url=context.author.display_avatar.url)
                await context.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
            await context.send(embed=hacker5)

    @set.command(name="guest",
                 description="Setups guest role for the server .",
                 help="Setups guest role for the server .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be added")
    async def guest(self, context: Context, *, role: discord.Role) -> None:
        if context.author == context.guild.owner or context.author.top_role.position > context.guild.me.top_role.position:
            if data := getConfig(context.guild.id):

                data['guest'] = role.id
                updateConfig(context.guild.id, data)
                hacker = discord.Embed(
                    description=
                    f"{tick} | Successfully Setuped `guest` Role To {role.mention}",
                    color=self.color)
                hacker.set_author(name=context.author,
                                  icon_url=context.author.display_avatar.url)
                hacker.set_thumbnail(url=context.author.display_avatar.url)
                await context.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
            await context.send(embed=hacker5)

    @set.command(name="friend",
                 description="Setups friend role for the server .",
                 help="Setups friend role for the server .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be added")
    async def friend(self, context: Context, *, role: discord.Role) -> None:
        if context.author == context.guild.owner or context.author.top_role.position > context.guild.me.top_role.position:
            if data := getConfig(context.guild.id):

                data['frnd'] = role.id
                updateConfig(context.guild.id, data)
                hacker = discord.Embed(
                    description=
                    f"{tick} | Successfully Setuped `friend` Role To {role.mention}",
                    color=self.color)
                hacker.set_author(name=context.author,
                                  icon_url=context.author.display_avatar.url)
                hacker.set_thumbnail(url=context.author.display_avatar.url)
                await context.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
            await context.send(embed=hacker5)



    @set.command(name="config",
                 description="Shows custom role settings for the server .",
                 aliases=['show'],
                 help="Shows custom role settings for the server .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def rsta(self, context: Context) -> None:
        if data := getConfig(context.guild.id):
            with open("alias_role.json", "r") as f:
                autoresponse = json.load(f)            
            staff = data['staff']
            girl = data['girl']
            vip = data['vip']
            guest = data['guest']
            friends = data['frnd']
            req = data["reqrole"]

            if data["staff"] != None:
                stafff = discord.utils.get(context.guild.roles, id=staff)
                staffr = stafff.mention
            else:
                staffr = "Staff role is not set"
            if data["girl"] != None:
                girll = discord.utils.get(context.guild.roles, id=girl)
                girlr = girll.mention
            else:
                girlr = "Girl role is not set"
            if data["vip"] != None:
                vipp = discord.utils.get(context.guild.roles, id=vip)
                vipr = vipp.mention
            else:
                vipr = "Vip role is not set"
            if data["guest"] != None:
                guestt = discord.utils.get(context.guild.roles, id=guest)
                guestr = guestt.mention
            else:
                guestr = "Guest role is not set"
            if data["frnd"] != None:
                frndr = discord.utils.get(context.guild.roles, id=friends)
                frndr = frndr.mention
            else:
                frndr = "Friend role is not set"
            if data["reqrole"] != None:
                reqrole = discord.utils.get(context.guild.roles, id=req)
                reqr = reqrole.mention
            else:
                reqr = "Req role is not set"


            embed = discord.Embed(
                title=f"Custom roles Settings For {context.guild.name}",
                color=self.color)
            embed.add_field(
                name="<a:im_arrowr:1038029121881636884> Req Role:",
                value=f"{reqr}",
                inline=False)
            embed.add_field(
                name="<a:im_arrowr:1038029121881636884> Staff Role:",
                value=f"{staffr}",
                inline=False)
            embed.add_field(
                name="<a:im_arrowr:1038029121881636884> Girl Role:",
                value=f"{girlr}",
                inline=False)
            embed.add_field(name="<a:im_arrowr:1038029121881636884> Vip Role:",
                            value=f"{vipr}",
                            inline=False)
            embed.add_field(
                name="<a:im_arrowr:1038029121881636884> Guest Role:",
                value=f"{guestr}",
                inline=False)
            embed.add_field(
                name="<a:im_arrowr:1038029121881636884> Friend Role:",
                value=f"{frndr}",
                inline=False)
            des = ""
            if str(context.guild.id) in autoresponse:
                for i in autoresponse[str(context.guild.id)]:
                    scdl = autoresponse[str(context.guild.id)][i]
                    r = discord.utils.get(context.guild.roles, id=int(scdl))
                    if r is None:
                         ro = "Role was deleted"
                    elif r is not None:
                        ro = r.mention
                    des+=f"{i.capitalize()} : {ro}\n"
                    if des == "":
                        des = "No custom aliases setuped in this server"
                embed.add_field(name="<a:im_arrowr:1038029121881636884> Custom Aliases:", value=des, inline=False)                            
                    
            if context.guild.icon is not None:
                embed.set_thumbnail(url = context.guild.icon.url)
                await context.send(embed=embed)  
#######################################
    @set.command(name="create")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1,2,commands.BucketType.user)
    @commands.max_concurrency(1,per=commands.BucketType.default,wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _custom_create(self, ctx, aliase, *, role:discord.Role):
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            with open("alias_role.json", "r") as f:
                aliases = json.load(f)
            numbers = []
            if str(ctx.guild.id) in aliases:
                for autoresponsecount in aliases[str(ctx.guild.id)]:
                    numbers.append(autoresponsecount)
                if len(numbers) >= 20:
                    hacker6 = discord.Embed(
                    
                    description=
                    f"{cross} You can\'t add more than 20 custom aliases in {ctx.guild.name} .",
                    color=self.color)
                    hacker6.set_author(name=f"{ctx.author}",
                                   icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                    hacker6.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                    return await ctx.send(embed=hacker6)
                
            if str(ctx.guild.id) in aliases:
                if aliase in aliases[str(ctx.guild.id)]:
                    hacker = discord.Embed(
                    
                    description=
                    f"{cross} | The custom role aliases with the name `{aliase}` is already in {ctx.guild.name} .",
                    color=self.color)
                    hacker.set_author(name=f"{ctx.author}",
                                  icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                    hacker.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                    return await ctx.send(embed=hacker)
                
            if str(ctx.guild.id) in aliases:
                aliases[str(ctx.guild.id)][aliase] = str(role.id)
                with open("alias_role.json", "w") as f:
                    json.dump(aliases, f, indent=4)
                hacker1 = discord.Embed(
                description=
                f"{tick} | Custom aliase {aliase.capitalize()} is set to {role.mention}\nJust type `{aliase.lower()} <member>` to give or `r{aliase.lower()} <member>` to take {role.mention} .",
                color=self.color)
                hacker1.set_author(name=f"{ctx.author}",
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                hacker1.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                return await ctx.reply(embed=hacker1)
          #  data = {
           # aliase: str(role.id),
           # }
            aliases[str(ctx.guild.id)] = {
                aliase: str(role.id),
                }
            with open("alias_role.json", "w") as f:
                json.dump(aliases, f, indent=4)
                hacker2 = discord.Embed(

                description=
                f"{tick} | Custom aliase {aliase.capitalize()} is set to {role.mention}\nJust type `{aliase.lower()} <member>` to give or `r{aliase.lower()} <member>` to take {role.mention} .",
                color=self.color)
                hacker2.set_author(name=f"{ctx.author}",
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                hacker2.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                return await ctx.reply(embed=hacker2)
            
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5, mention_author=False)               
                        
                	
    @set.command(name="list")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1,2,commands.BucketType.user)
    @commands.max_concurrency(1,per=commands.BucketType.default,wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _list(self, ctx):
        with open("alias_role.json", "r") as f:
            autoresponse = json.load(f)
        guild = ctx.guild
        des = ""
        rope = ""
        embed = discord.Embed(color=self.color)
 
        if str(ctx.guild.id) in autoresponse:
            for no, i in enumerate(autoresponse[str(ctx.guild.id)]):
                scdl = autoresponse[str(ctx.guild.id)][i]
                r = discord.utils.get(ctx.guild.roles, id=int(scdl))
                if r is None:
                    ro = "Role was deleted"
                elif r is not None:
                    ro = r.mention
                des+=f"**{no+1}. {i.title()}**\n`-` {ro}\n\n"
                #rope+=f"{ro}"
                if des == "":
                    des = "No custom aliase setuped in this server"
            #embed = discord.Embed( color=self.color)
            embed.add_field(name="Custom Role Lists.", value=des, inline=False)
            embed.set_author(name=f"Custom Aliases Roles For {ctx.guild.name}",
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            if ctx.guild.icon is not None:
                embed.set_thumbnail(url = ctx.guild.icon.url)               
            await ctx.send(embed=embed)
            return



    @set.command(name="delete")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1,2,commands.BucketType.user)
    @commands.max_concurrency(1,per=commands.BucketType.default,wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _setupdelete(self, ctx, aliases):
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            with open("alias_role.json", "r") as f:
                custom = json.load(f)
            if str(ctx.guild.id) in custom:
                if aliases in custom[str(ctx.guild.id)]:
                    del custom[str(ctx.guild.id)][aliases]
                    with open("alias_role.json", "w") as f:
                        json.dump(custom, f, indent=4)
                    hacker1 = discord.Embed(
                    
                    description=
                    f"{tick} | Custom aliase {aliases.capitalize()} is removed from assigning any role",
                     color=self.color)
                    hacker1.set_author(name=f"{ctx.author}",
                                   icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                    return await ctx.reply(embed=hacker1)
            
                else:
                    hacker = discord.Embed(
                    
                    description=
                    f"{cross} | There is no custom aliase with {aliases} which is assigning any role .",
                    color=self.color)
                    hacker.set_author(name=f"{ctx.author}",
                                  icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                    return await ctx.reply(embed=hacker)
                
            else:
                hacker2 = discord.Embed(
                
                description=
                f"{cross} | There is no custom aliase with {aliases} which is assigning any role .",
                color=self.color)
                hacker2.set_author(name=f"{ctx.author}",
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                return await ctx.reply(embed=hacker2)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5, mention_author=False)
            return
            
            
            
                        

    @set.command(name="reset",
                 description="Clear custom roles config for the server."
               ,
                 help="Clear custom roles config for the server.")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _reset(self, ctx):
        data = getConfig(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            data['girl'] = None
            data['vip'] = None
            data['guest'] = None
            data['frnd'] = None
            data['reqrole'] = None
            updateConfig(ctx.guild.id, data)
            hacker = discord.Embed(
                    description=
                    f"{tick} | Succesfully cleared all custom roles config for {ctx.guild.name} .",
                    color=self.color)
            await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=ctx.author.display_avatar.url)
            await ctx.send(embed=hacker5)

    @set.command(name="reqrole",
                 description="setup reqrole for custom role commands .",
                 aliases=['r'],
                 help="setup reqrole for custom role commands .")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def req_role(self, ctx, role: discord.Role):
        data = getConfig(ctx.guild.id)
        data["reqrole"] = role.id
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            updateConfig(ctx.guild.id, data)
            hacker4 = discord.Embed(
                color=self.color,
                
                description=
                f"{tick} | Reqiured role to run custom role commands is set to {role.mention} For {ctx.guild.name}"
            )
            await ctx.reply(embed=hacker4, mention_author=False)

        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=ctx.author.display_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False)


            




    @commands.hybrid_group(name="remove",
                           description="remove roles",
                           aliases=['r'])
    @blacklist_check()
    @ignore_check()
    
    async def remove(self, context: Context):
        if context.subcommand_passed is None:
            await context.send_help(context.command)
            context.command.reset_cooldown(context)

    @remove.command(name="staff",
                    description="Removes the staff role from the member .",
                    aliases=['official'],
                    help="Removes the staff role from the member .")
    @blacklist_check()
    @ignore_check()
   # @commands.has_permissions(administrator=True)
    async def rstaff(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            lol = data['reqrole']
            own = data['staff'] 
            role = context.guild.get_role(own) 
            if data["reqrole"] != None:
                req = context.guild.get_role(lol)
                if context.author == context.guild.owner or req in context.author.roles:
                    if data["staff"] != None:
                        if role in member.roles:
                            await self.remove_role(role=own, member=member)
                         
                            hacker = discord.Embed(
                description=
                f"{tick} | Successfully Removed <@&{own}> From {member.mention}",
                color=self.color)
                            hacker.set_author(name=context.author,
                              icon_url=context.author.display_avatar.url)
                            await context.send(embed=hacker)
                        elif role not in member.roles:
                            pass 
                    else:
                        hacker1 = discord.Embed(
                description=
                f"{error} | Staff role is not setuped in {context.guild.name}",
                color=self.color)
                        hacker1.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                        hacker1.set_thumbnail(url=context.author.display_avatar.url)
                        await context.send(embed=hacker1)
                else:
                    hacker3 = discord.Embed(
                description=
                f"{error} | You need {req.mention} to run this command .",
                color=self.color)
                    hacker3.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                    
                    await context.send(embed=hacker3)

            else:
                hacker4 = discord.Embed(
                description=
                f"{error} | Req role is not setuped in {context.guild.name}",
                color=self.color)
                hacker4.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                
                await context.send(embed=hacker4)



    @remove.command(name="girl",
                    description="Removes the girl role from the member .",
                    aliases=['cuties', 'qt'],
                    hep="Removes the girl role from the member .")
    @blacklist_check()
    @ignore_check()
  #  @commands.has_permissions(administrator=True)
    async def rgirl(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            lol = data['reqrole']
            own = data['girl'] 
            role = context.guild.get_role(own) 
            if data["reqrole"] != None:
                req = context.guild.get_role(lol)
                if context.author == context.guild.owner or req in context.author.roles:
                    if data["girl"] != None:
                        if role in member.roles:
                            await self.remove_role(role=own, member=member)
                         
                            hacker = discord.Embed(
                description=
                f"{tick} | Successfully Removed <@&{own}> From {member.mention}",
                color=self.color)
                            hacker.set_author(name=context.author,
                              icon_url=context.author.display_avatar.url)
                            await context.send(embed=hacker)
                        elif role not in member.roles:
                            pass 
                    else:
                        hacker1 = discord.Embed(
                description=
                f"{error} | Girl role is not setuped in {context.guild.name}",
                color=self.color)
                        hacker1.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                        hacker1.set_thumbnail(url=context.author.display_avatar.url)
                        await context.send(embed=hacker1)
                else:
                    hacker3 = discord.Embed(
                description=
                f"{error} | You need {req.mention} to run this command .",
                color=self.color)
                    hacker3.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                    
                    await context.send(embed=hacker3)

            else:
                hacker4 = discord.Embed(
                description=
                f"{error} | Req role is not setuped in {context.guild.name}",
                color=self.color)
                hacker4.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                
                await context.send(embed=hacker4)


    @remove.command(name="vip",
                    description="Removes the vip role from the member .",
                    help="Removes the vip role from the member .")
    @blacklist_check()
    @ignore_check()
  #  @commands.has_permissions(administrator=True)
    async def rvip(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            lol = data['reqrole']
            own = data['vip'] 
            role = context.guild.get_role(own) 
            if data["reqrole"] != None:
                req = context.guild.get_role(lol)
                if context.author == context.guild.owner or req in context.author.roles:
                    if data["vip"] != None:
                        if role in member.roles:
                            await self.remove_role(role=own, member=member)
                         
                            hacker = discord.Embed(
                description=
                f"{tick} | Successfully Removed <@&{own}> From {member.mention}",
                color=self.color)
                            hacker.set_author(name=context.author,
                              icon_url=context.author.display_avatar.url)
                            await context.send(embed=hacker)
                        elif role not in member.roles:
                            pass 
                    else:
                        hacker1 = discord.Embed(
                description=
                f"{error} | Vip role is not setuped in {context.guild.name}",
                color=self.color)
                        hacker1.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                        hacker1.set_thumbnail(url=context.author.display_avatar.url)
                        await context.send(embed=hacker1)
                else:
                    hacker3 = discord.Embed(
                description=
                f"{error} | You need {req.mention} to run this command .",
                color=self.color)
                    hacker3.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                    
                    await context.send(embed=hacker3)

            else:
                hacker4 = discord.Embed(
                description=
                f"{error} | Req role is not setuped in {context.guild.name}",
                color=self.color)
                hacker4.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                
                await context.send(embed=hacker4)

    

    @remove.command(name="guest",
                    description="Removes the guest role from the member .",
                    help="Removes the guest role from the member .")
    @blacklist_check()
    @ignore_check()
  #  @commands.has_permissions(administrator=True)
    async def rguest(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            lol = data['reqrole']
            own = data['guest'] 
            role = context.guild.get_role(own) 
            if data["reqrole"] != None:
                req = context.guild.get_role(lol)
                if context.author == context.guild.owner or req in context.author.roles:
                    if data["guest"] != None:
                        if role in member.roles:
                            await self.remove_role(role=own, member=member)
                         
                            hacker = discord.Embed(
                description=
                f"{tick} | Successfully Removed <@&{own}> From {member.mention}",
                color=self.color)
                            hacker.set_author(name=context.author,
                              icon_url=context.author.display_avatar.url)
                            await context.send(embed=hacker)
                        elif role not in member.roles:
                            pass 
                    else:
                        hacker1 = discord.Embed(
                description=
                f"{error} | Guest role is not setuped in {context.guild.name}",
                color=self.color)
                        hacker1.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                        hacker1.set_thumbnail(url=context.author.display_avatar.url)
                        await context.send(embed=hacker1)
                else:
                    hacker3 = discord.Embed(
                description=
                f"{error} | You need {req.mention} to run this command .",
                color=self.color)
                    hacker3.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                    
                    await context.send(embed=hacker3)

            else:
                hacker4 = discord.Embed(
                description=
                f"{error} | Req role is not setuped in {context.guild.name}",
                color=self.color)
                hacker4.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                
                await context.send(embed=hacker4)


    @remove.command(name="friend",
                    description="Removes the friend role from the member .",
                    aliases=['frnd'],
                    help="Removes the friend role from the member .")
    @blacklist_check()
    @ignore_check()
   # @commands.has_permissions(administrator=True)
    async def rfriend(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            lol = data['reqrole']
            own = data['frnd'] 
            role = context.guild.get_role(own) 
            if data["reqrole"] != None:
                req = context.guild.get_role(lol)
                if context.author == context.guild.owner or req in context.author.roles:
                    if data["frnd"] != None:
                        if role in member.roles:
                            await self.remove_role(role=own, member=member)
                         
                            hacker = discord.Embed(
                description=
                f"{tick} | Successfully Removed <@&{own}> From {member.mention}",
                color=self.color)
                            hacker.set_author(name=context.author,
                              icon_url=context.author.display_avatar.url)
                            await context.send(embed=hacker)
                        elif role not in member.roles:
                            pass 
                    else:
                        hacker1 = discord.Embed(
                description=
                f"{error} | Friend role is not setuped in {context.guild.name}",
                color=self.color)
                        hacker1.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                        hacker1.set_thumbnail(url=context.author.display_avatar.url)
                        await context.send(embed=hacker1)
                else:
                    hacker3 = discord.Embed(
                description=
                f"{error} | You need {req.mention} to run this command .",
                color=self.color)
                    hacker3.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                    
                    await context.send(embed=hacker3)

            else:
                hacker4 = discord.Embed(
                description=
                f"{error} | Req role is not setuped in {context.guild.name}",
                color=self.color)
                hacker4.set_author(name=context.author,
                               icon_url=context.author.display_avatar.url)
                
                await context.send(embed=hacker4)

    



    @commands.group(name="autoresponder",
                    invoke_without_command=True,
                    aliases=['ar'])
    @blacklist_check()
    @ignore_check()
    async def _ar(self, ctx: commands.Context):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_ar.command(name="create")
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    async def _create(self, ctx, name, *, message):
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            with open("autoresponse.json", "r") as f:
                autoresponse = json.load(f)
            numbers = []
            if str(ctx.guild.id) in autoresponse:
                for autoresponsecount in autoresponse[str(ctx.guild.id)]:
                    numbers.append(autoresponsecount)
                if len(numbers) >= 20:
                    hacker6 = discord.Embed(
                    
                    description=
                    f"{cross} You can\'t add more than 20 autoresponses in {ctx.guild.name}",
                    color=self.color)
                    hacker6.set_author(name=f"{ctx.author}",
                                   icon_url=ctx.author.display_avatar.url)
                    hacker6.set_thumbnail(url=ctx.author.display_avatar.url)
                    return await ctx.send(embed=hacker6)
            if str(ctx.guild.id) in autoresponse:
                if name in autoresponse[str(ctx.guild.id)]:
                    hacker = discord.Embed(
                    
                    description=
                    f"{cross} The autoresponse with the `{name}` is already in {ctx.guild.name}",
                    color=self.color)
                    hacker.set_author(name=f"{ctx.author}",
                                  icon_url=ctx.author.display_avatar.url)
                    hacker.set_thumbnail(url=ctx.author.display_avatar.url)
                    return await ctx.send(embed=hacker)
            if str(ctx.guild.id) in autoresponse:
                autoresponse[str(ctx.guild.id)][name] = message
                with open("autoresponse.json", "w") as f:
                    json.dump(autoresponse, f, indent=4)
                hacker1 = discord.Embed(
                description=
                f"{tick} | Successfully Created Autoresponder in {ctx.guild.name} with the `{name}`",
                color=self.color)
                hacker1.set_author(name=f"{ctx.author}",
                               icon_url=ctx.author.display_avatar.url)
                hacker1.set_thumbnail(url=ctx.author.display_avatar.url)
                return await ctx.reply(embed=hacker1)
            data = {
            name: message,
            }
            autoresponse[str(ctx.guild.id)] = data
            with open("autoresponse.json", "w") as f:
                json.dump(autoresponse, f, indent=4)
                hacker2 = discord.Embed(

                description=
                f"{tick} | Successfully Created Autoresponder  in {ctx.guild.name} with the name `{name}`",
                color=self.color)
                hacker2.set_author(name=f"{ctx.author}",
                               icon_url=ctx.author.display_avatar.url)
                hacker2.set_thumbnail(url=ctx.author.display_avatar.url)
                return await ctx.reply(embed=hacker2)
            
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=ctx.author.display_avatar.url)

            await ctx.send(embed=hacker5, mention_author=False)
                
                    
    @_ar.command(name="delete")
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    async def _delete(self, ctx, name):
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            with open("autoresponse.json", "r") as f:
                autoresponse = json.load(f)
            if str(ctx.guild.id) in autoresponse:
                if name in autoresponse[str(ctx.guild.id)]:
                    del autoresponse[str(ctx.guild.id)][name]
                    with open("autoresponse.json", "w") as f:
                        json.dump(autoresponse, f, indent=4)
                    hacker1 = discord.Embed(
                    
                    description=
                    f"{tick} | Successfully Deleted Autoresponder in {ctx.guild.name} with the `{name}`",
                     color=self.color)
                    hacker1.set_author(name=f"{ctx.author}",
                                   icon_url=ctx.author.display_avatar.url)
                    return await ctx.reply(embed=hacker1)
            
                else:
                    hacker = discord.Embed(
                    
                    description=
                    f"{cross} No Autoresponder Found With The Name `{name}` In {ctx.guild.name}",
                    color=self.color)
                    hacker.set_author(name=f"{ctx.author}",
                                  icon_url=ctx.author.display_avatar.url)
                    return await ctx.reply(embed=hacker)
                
            else:
                hacker2 = discord.Embed(
                
                description=
                f"{cross} There is no Autoresponder in {ctx.guild.name}",
                color=self.color)
                hacker2.set_author(name=f"{ctx.author}",
                               icon_url=ctx.author.display_avatar.url)
                return await ctx.reply(embed=hacker2)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=ctx.author.display_avatar.url)

            await ctx.send(embed=hacker5, mention_author=False)

    @_ar.command(name="config")
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    async def _config(self, ctx):
        with open("autoresponse.json", "r") as f:
            autoresponse = json.load(f)
        autoresponsenames = []
        guild = ctx.guild
        if str(ctx.guild.id) in autoresponse:
            for autoresponsecount in autoresponse[str(ctx.guild.id)]:
                autoresponsenames.append(autoresponsecount)
            embed = discord.Embed(color=self.color)
            st, count = "", 1
            for autoresponse in autoresponsenames:
                st += f"`{'0' + str(count) if count < 20 else count}. `    **{autoresponse.upper()}**\n"
                test = count
                count += 1

                embed.title = f"{test} Autoresponders In {guild}"
        embed.description = st
        embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    @_ar.command(name="edit")
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    async def _edit(self, ctx, name, *, message):
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            with open("autoresponse.json", "r") as f:
                autoresponse = json.load(f)
            if str(ctx.guild.id) in autoresponse:
                if name in autoresponse[str(ctx.guild.id)]:
                    autoresponse[str(ctx.guild.id)][name] = message
                    with open("autoresponse.json", "w") as f:
                        json.dump(autoresponse, f, indent=4)
                    hacker1 = discord.Embed(
                    
                    description=
                    f"{tick} | Successfully Edited Autoresponder in {ctx.guild.name} with the `{name}`",
                    color=self.color)
                    hacker1.set_author(name=f"{ctx.author}",
                                   icon_url=ctx.author.display_avatar.url)
                    return await ctx.send(embed=hacker1)
                else:
                    hacker2 = discord.Embed(
                
                description=
                f"{cross} No Autoresponder Found With The Name `{name}` In {ctx.guild.name}",
                color=self.color)
                    hacker2.set_author(name=f"{ctx.author}",
                               icon_url=ctx.author.display_avatar.url)
                    return await ctx.send(embed=hacker2)
            
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=ctx.author.display_avatar.url)

            await ctx.send(embed=hacker5, mention_author=False)     
            
    @commands.Cog.listener()
    async def on_message(self, message: discord.message):
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
        else:
            with open("alias_role.json", "r") as f:
                ls = json.load(f)
            if str(message.guild.id) in ls:
                    content = ""
                    content = message.content.lower()
                    pre = ['.']
                    for k in pre:
                        if content.startswith(k):
                            content = content.replace(k, "").strip()
                            prefix = k 
                    customrole = ls[str(message.guild.id)]
                    for trigger in customrole:
                        if content.startswith(trigger): 
                            u = None                                             
                            for botss in message.mentions:
                                if botss.bot:
                                    continue
                                else:
                                    u = botss
                                    break
                            if u is None:
                                em = discord.Embed(description=f"<:cross_hacker:1148075305576177686> You forgot to mention the user argument.\nDo it like: `{trigger} <member>`", color=self.color)
                               
                                return await message.reply(embed=em, delete_after=7)
                            if u.id == message.author.id:
                                em = discord.Embed(description=f"<:cross_hacker:1148075305576177686> You cant change your own roles", color=self.color)
                               
                                return await message.reply(embed=em, delete_after=7)
                            else:
                                    data = getConfig(message.guild.id)
                                    lol = data['reqrole']                       
                                    req = discord.utils.get(message.guild.roles, id=lol)
                                    if req is None:
                                        pass
                                    else:
                                        if req not in message.author.roles:
                                            em = discord.Embed(description=f"<:cross_hacker:1148075305576177686> You need {req.mention} role to use this command.", color=self.color)
                                            
                                            return await message.reply(embed=em)
                                        
                                        scdl = customrole[(trigger)]
                                        Role = discord.utils.get(message.guild.roles, id=int(scdl))
                                        if Role.position >= message.guild.me.top_role.position:
                                            em = discord.Embed(description=f"<:cross_hacker:1148075305576177686> {Role.mention} is above my top role.", color=self.color)
                                            
                                            return await message.reply(embed=em)
                                        if Role in u.roles:
                                            await u.remove_roles(Role)
                                            em=discord.Embed(description=f"{tick} | Successfully Removed {Role.mention} from {u.mention}", color=self.color)
                                            
                                            return await message.reply(embed=em)
                                        else:
                                            await u.add_roles(Role)
                                            em=discord.Embed(description=f"{tick} | Successfully Given {Role.mention} to {u.mention}", color=self.color)
                                           
                                            return await message.reply(embed=em)
                    return 
            return 
