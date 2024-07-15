import discord
import json
from discord.ext import commands
from discord.ui import Button, View
from utils.Tools import *
from utils.config import BotName





class BasicView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout = 60):
        super().__init__(timeout=timeout)
        self.ctx = ctx

    
      
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in [246469891761111051]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command .", ephemeral=True)
            return False
        return True

    
class buttoncolor(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None
        
    @discord.ui.button(label="Button", custom_id='red', style=discord.ButtonStyle.danger)
    async def red(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = 'discord.ButtonStyle.danger'
        self.stop()

    @discord.ui.button(label="Button", custom_id='green', style=discord.ButtonStyle.success)
    async def green(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = 'discord.ButtonStyle.success'
        self.stop()

    @discord.ui.button(label="Button", custom_id='grey', style=discord.ButtonStyle.grey)
    async def grey(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = 'discord.ButtonStyle.grey'
        self.stop()

    @discord.ui.button(label="Button", custom_id='blurple', style=discord.ButtonStyle.blurple)
    async def blurple(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = 'discord.ButtonStyle.blurple'
        self.stop()       



          

class Selfroles(commands.Cog):
  def __init__(self, client):
        self.client = client
        self.color = 0x2f3136
              
  @commands.Cog.listener()
  async def on_interaction(self, interaction):
    with open("gender.json", "r") as f:
      data = json.load(f)
    with open("status.json", "r") as f:
      hacker = json.load(f)
    if interaction.guild is None:
        return 
    if str(interaction.guild.id) not in data or str(interaction.guild.id) not in hacker:
      return
    else:
      if interaction.data["custom_id"] == "male":
        malerole  = interaction.message.guild.get_role(int(data[str(interaction.message.guild.id)]["male"]))
        if malerole in interaction.user.roles:
          await interaction.user.remove_roles(malerole,reason=f"{self.client.user.name} | Gender Selfroles")
          return await interaction.response.send_message(content=f"✅ | Successfully Removed {malerole.name}", ephemeral=True)            
          
        if malerole not in interaction.user.roles:
          await interaction.user.add_roles(malerole,reason=f"{self.client.user.name} | Gender Selfroles")
          return await interaction.response.send_message(content=f"✅ | Successfully Added {malerole.name}", ephemeral=True)  
        
        
      if interaction.data["custom_id"] == "female":
        femalerole  =  interaction.message.guild.get_role(int(data[str(interaction.message.guild.id)]["female"]))
        if femalerole in interaction.user.roles:
          await interaction.user.remove_roles(femalerole,reason=f"{self.client.user.name} | Gender Selfroles")
          return await interaction.response.send_message(content=f"✅ | Successfully Removed {femalerole.name}", ephemeral=True)            
          
        if femalerole not in interaction.user.roles:
          await interaction.user.add_roles(femalerole,reason=f"{self.client.user.name} | Gender Selfroles")
          return await interaction.response.send_message(content=f"✅ | Successfully Added {femalerole.name}", ephemeral=True) 
        #################################3
        
      if interaction.data["custom_id"] == "single":
        singlerole  = interaction.message.guild.get_role(int(hacker[str(interaction.message.guild.id)]["single"]))
        if singlerole in interaction.user.roles:
          await interaction.user.remove_roles(singlerole,reason=f"{self.client.user.name} | Status Selfroles")
          return await interaction.response.send_message(content=f"✅ | Successfully Removed {singlerole.name}", ephemeral=True)            
          
        if singlerole not in interaction.user.roles:
          await interaction.user.add_roles(singlerole,reason=f"{self.client.user.name} | Status Selfroles")
          return await interaction.response.send_message(content=f" | Successfully Added {singlerole.name}", ephemeral=True)  
        
        
      if interaction.data["custom_id"] == "mingle":
        minglerole  = interaction.message.guild.get_role(int(hacker[str(interaction.message.guild.id)]["mingle"]))
        if minglerole in interaction.user.roles:
          await interaction.user.remove_roles(minglerole,reason=f"{self.client.user.name} | Status Selfroles")
          return await interaction.response.send_message(content=f"✅ | Successfully Removed {minglerole.name}", ephemeral=True)            
          
        if minglerole not in interaction.user.roles:
          await interaction.user.add_roles(minglerole,reason=f"{self.client.user.name} | Status Selfroles")
          return await interaction.response.send_message(content=f" | Successfully Added {minglerole.name}", ephemeral=True) 

      if interaction.data["custom_id"] == "broken":
        brokenrole  = interaction.message.guild.get_role(int(hacker[str(interaction.message.guild.id)]["broken"]))
        if brokenrole in interaction.user.roles:
          await interaction.user.remove_roles(brokenrole,reason=f"{self.client.user.name} | Status Selfroles")
          return await interaction.response.send_message(content=f"✅ | Successfully Removed {brokenrole.name}", ephemeral=True)            
          
        if brokenrole not in interaction.user.roles:
          await interaction.user.add_roles(brokenrole,reason=f"{self.client.user.name} | Status Selfroles")
          return await interaction.response.send_message(content=f"✅ | Successfully Added {brokenrole.name}", ephemeral=True) 
      return  
      
                
  @commands.hybrid_group(name="selfrole")
  @commands.has_permissions(administrator = True)
  @commands.cooldown(1, 20, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @blacklist_check()
  @ignore_check()
  async def _selfrole(self, ctx):
        if ctx.prefix == f"<@!{self.bot.user.id}>":
            prefix=f"@{BotName} "

        else:
            prefix=ctx.prefix
        hacker = discord.utils.get(self.client.users, id=246469891761111051)
        hasan = discord.utils.get(self.client.users, id=301502732664307716)
        hacker = discord.Embed(title=f"Selfrole (5)", colour=self.color,
                                     description=f"""<...> Duty | [...] Optional\n\n
{prefix}selfrole


{prefix}selfrole gender `<channel>`
setups gender roles in the server . 

{prefix}selfrole gender disable
clear/reset/delete gender role configuration in the server .

{prefix}selfrole status `<channel>`
setups status roles in the server . 

{prefix}selfrole status disable
clear/reset/delete status role configuration in the server .

""")
        hacker.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        hacker.set_footer(text=f"Made by {str(hacker)} & {str(hasan)}" ,  icon_url=hacker.avatar.url)
        await ctx.send(embed=hacker)
        
        
        
  @_selfrole.group(name="gender")
  @commands.has_permissions(administrator = True)
  @commands.cooldown(1, 20, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @blacklist_check()
  @ignore_check()
  async def _gender(self, ctx, channel: discord.TextChannel):
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
          with open('gender.json', 'r') as f:
              data = json.load(f)  
          def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
            
          if str(ctx.guild.id) not in data:
            embed1 = discord.Embed(
                     color=self.color,
                    description=f" | Setting up gender roles for {ctx.guild.name}...")
            msg = await ctx.send(
                       embed=embed1)
            male = await ctx.guild.create_role(name="Male", reason="Selfrole Gender Command Executed By: {}".format(ctx.author))
            female = await ctx.guild.create_role(name="Female", reason="Selfrole Gender Command Executed By: {}".format(ctx.author))
#####################################################################################


            view = buttoncolor(ctx)
            bembed = discord.Embed(description="Choose the button color from the below options. This action is irreversible!\n", color=self.color)
            bembed.set_image(url="https://media.discordapp.net/attachments/1087809805361631353/1092314933082992740/mUbn7PJ.png?width=209&height=245")
            bembed.set_author(name="Rolemenu creation...", icon_url=self.client.user.avatar.url)
            await msg.edit(embed=bembed, view=view)  
            await view.wait()
            if view.value is None:
                await msg.delete()
            ##########
            buttonstyle =[]
            if view.value == "discord.ButtonStyle.danger":
                buttonstyle.append(discord.ButtonStyle.danger)
                malebutton2 = Button(style=discord.ButtonStyle.danger, label=male.name, custom_id=f"male")
                femalebutton2 = Button(style=discord.ButtonStyle.danger, label=female.name,custom_id=f"female")
                selfr= View()
                selfr.add_item(malebutton2)     
                selfr.add_item(femalebutton2)    
                selfembed= discord.Embed(title="Interact with the following for getting or removing the role that follows",description=f"> Male:{male.mention}\n > Female:{female.mention}",color=self.color) 
                selfembed.set_author(name=f"Gender Roles For {ctx.guild.name}", icon_url=self.client.user.avatar.url)    
                selfrolemsg = await channel.send(embed=selfembed,view=selfr)  
                data[str(ctx.guild.id)] = {
                          'male': str(male.id),
                          'female': str(female.id),
                          'msg': selfrolemsg.id,
                          'channel': channel.id
                           }
                with open("gender.json", "w") as f: 
                    json.dump(data, f, indent=4)  
                
                
            if view.value == "discord.ButtonStyle.success":
                buttonstyle.append(discord.ButtonStyle.success)
                malebutton2 = Button(style=discord.ButtonStyle.success, label=male.name, custom_id=f"male")
                femalebutton2 = Button(style=discord.ButtonStyle.success, label=female.name,custom_id=f"female")
                selfr= View()
                selfr.add_item(malebutton2)     
                selfr.add_item(femalebutton2)    
                selfembed= discord.Embed(title="Interact with the following for getting or removing the role that follows",description=f"> Male:{male.mention}\n > Female:{female.mention}",color=self.color) 
                selfembed.set_author(name=f"Gender Roles For {ctx.guild.name}", icon_url=self.client.user.avatar.url)    
                selfrolemsg = await channel.send(embed=selfembed,view=selfr)  
                data[str(ctx.guild.id)] = {
                          'male': str(male.id),
                          'female': str(female.id),
                          'msg': selfrolemsg.id,
                          'channel': channel.id
                           }
                with open("gender.json", "w") as f: 
                    json.dump(data, f, indent=4)  
                
            if view.value == "discord.ButtonStyle.grey":
                buttonstyle.append(discord.ButtonStyle.grey)
                malebutton2 = Button(style=discord.ButtonStyle.grey, label=male.name, custom_id=f"male")
                femalebutton2 = Button(style=discord.ButtonStyle.grey, label=female.name,custom_id=f"female")
                selfr= View()
                selfr.add_item(malebutton2)     
                selfr.add_item(femalebutton2)    
                selfembed= discord.Embed(title="Interact with the following for getting or removing the role that follows",description=f"> Male:{male.mention}\n > Female:{female.mention}",color=self.color) 
                selfembed.set_author(name=f"Gender Roles For {ctx.guild.name}", icon_url=self.client.user.avatar.url)    
                selfrolemsg = await channel.send(embed=selfembed,view=selfr)  
                data[str(ctx.guild.id)] = {
                          'male': str(male.id),
                          'female': str(female.id),
                          'msg': selfrolemsg.id,
                          'channel': channel.id
                           }
                with open("gender.json", "w") as f: 
                    json.dump(data, f, indent=4)  
                
            if view.value == "discord.ButtonStyle.blurple":
                buttonstyle.append(discord.ButtonStyle.blurple)
                malebutton2 = Button(style=discord.ButtonStyle.blurple, label=male.name, custom_id=f"male")
                femalebutton2 = Button(style=discord.ButtonStyle.blurple, label=female.name,custom_id=f"female")
                selfr= View()
                selfr.add_item(malebutton2)     
                selfr.add_item(femalebutton2)    
                selfembed= discord.Embed(title="Interact with the following for getting or removing the role that follows",description=f"> Male:{male.mention}\n > Female:{female.mention}",color=self.color) 
                selfembed.set_author(name=f"Gender Roles For {ctx.guild.name}", icon_url=self.client.user.avatar.url)    
                selfrolemsg = await channel.send(embed=selfembed,view=selfr)  
                data[str(ctx.guild.id)] = {
                          'male': str(male.id),
                          'female': str(female.id),
                          'msg': selfrolemsg.id,
                          'channel': channel.id
                           }
                with open("gender.json", "w") as f: 
                    json.dump(data, f, indent=4)  
            ####################
            
                
      else:
          hacker5 = discord.Embed(
          description=
          """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
          color=self.color)
          hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
          return await ctx.send(embed=hacker5)           
            
            
            
  @_gender.command(name="disable", description="Disable gender roles in the server .")
  @commands.has_permissions(administrator = True)
  @commands.cooldown(1, 20, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @blacklist_check()
  @ignore_check()
  async def gender_disable(self, ctx):
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
          with open("gender.json", 'r') as f:
              data = json.load(f)
          if str(ctx.guild.id) not in data:
              embed6 = discord.Embed(
                    description=
                    f"⚠ | gender role is not setupped for {ctx.guild.name}",
                    color=self.color)
              await ctx.send(embed=embed6)
          else:
              msg = data[str(ctx.guild.id)]["msg"]
              ch = data[str(ctx.guild.id)]["channel"]
              lame = await self.client.get_channel(ch).fetch_message(int(msg))
             # lame = await ctx.fetch_message(int(msg))
              del data[str(ctx.guild.id)]
              try:
                  await lame.delete()
              except:
                  pass
              with open("gender.json", "w") as f:
                  json.dump(data, f, indent=4)
              hacker = discord.Embed(
                        description=
                        f"✅ | Successfully Deleted Gender Roles for {ctx.guild.name} .",
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
          
          
#########################################



  @_selfrole.group(name="status")
  @commands.has_permissions(administrator = True)
  @commands.cooldown(1, 20, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @blacklist_check()
  @ignore_check()
  async def _status(self, ctx, channel: discord.TextChannel):
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
          with open('status.json', 'r') as f:
              data = json.load(f)  
          def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
            
          if str(ctx.guild.id) not in data:
            embed1 = discord.Embed(
                     color=self.color,
                    description=f" | Setting up status roles for {ctx.guild.name}...")
            msg = await ctx.send(
                       embed=embed1)
            single = await ctx.guild.create_role(name="Single", reason="Selfrole Status Command Executed By: {}".format(ctx.author))
            mingle = await ctx.guild.create_role(name="Mingle", reason="Selfrole Status Command Executed By: {}".format(ctx.author))
            broken = await ctx.guild.create_role(name="Broken", reason="Selfrole Status Command Executed By: {}".format(ctx.author))
#####################################################################################


            view = buttoncolor(ctx)
            bembed = discord.Embed(description="Choose the button color from the below options. This action is irreversible!\n", color=self.color)
            bembed.set_image(url="https://media.discordapp.net/attachments/1087809805361631353/1092314933082992740/mUbn7PJ.png?width=209&height=245")
            bembed.set_author(name="Rolemenu creation...", icon_url=self.client.user.avatar.url)
            await msg.edit(embed=bembed, view=view)  
            await view.wait()
            if view.value is None:
                await msg.delete()
            ##########
            buttonstyle =[]
            if view.value == "discord.ButtonStyle.danger":
                buttonstyle.append(discord.ButtonStyle.danger)
                singlebutton = Button(style=discord.ButtonStyle.danger, label=single.name,custom_id=f"single")
                minglebutton = Button(style=discord.ButtonStyle.danger, label=mingle.name,custom_id=f"mingle")
                brokenbutton = Button(style=discord.ButtonStyle.danger, label=broken.name,custom_id=f"broken")
                selfr= View()
                selfr.add_item(singlebutton)     
                selfr.add_item(minglebutton) 
                selfr.add_item(brokenbutton)   
                selfembed= discord.Embed(color=self.color,title="Interact with the following for getting or removing the role that follows",description=f"> Single:{single.mention}\n > Mingle:{mingle.mention}\n > Broken:{broken.mention}\n") 
                selfembed.set_author(name=f"Status Roles For {ctx.guild.name}", icon_url=self.client.user.avatar.url)    
                selfrolemsg = await channel.send(embed=selfembed,view=selfr) 
                data[str(ctx.guild.id)] = {
                          'single': str(single.id),
                          'mingle': str(mingle.id),
                          'broken': str(broken.id),
                          'msg': selfrolemsg.id,
                          'channel': channel.id
                           }
                with open("status.json", "w") as f: 
                    json.dump(data, f, indent=4)  
                
                
            if view.value == "discord.ButtonStyle.success":
                buttonstyle.append(discord.ButtonStyle.success)
                singlebutton = Button(style=discord.ButtonStyle.success, label=single.name,custom_id=f"single")
                minglebutton = Button(style=discord.ButtonStyle.success, label=mingle.name,custom_id=f"mingle")
                brokenbutton = Button(style=discord.ButtonStyle.success, label=broken.name,custom_id=f"broken")
                selfr= View()
                selfr.add_item(singlebutton)     
                selfr.add_item(minglebutton) 
                selfr.add_item(brokenbutton)   
                selfembed= discord.Embed(color=self.color,title="Interact with the following for getting or removing the role that follows",description=f"> Single:{single.mention}\n > Mingle:{mingle.mention}\n > Broken:{broken.mention}\n") 
                selfembed.set_author(name=f"Status Roles For {ctx.guild.name}", icon_url=self.client.user.avatar.url)    
                selfrolemsg = await channel.send(embed=selfembed,view=selfr) 
                data[str(ctx.guild.id)] = {
                          'single': str(single.id),
                          'mingle': str(mingle.id),
                          'broken': str(broken.id),
                          'msg': selfrolemsg.id,
                          'channel': channel.id
                           }
                with open("status.json", "w") as f: 
                    json.dump(data, f, indent=4)  
                
            if view.value == "discord.ButtonStyle.grey":
                buttonstyle.append(discord.ButtonStyle.grey)
                singlebutton = Button(style=discord.ButtonStyle.grey, label=single.name,custom_id=f"single")
                minglebutton = Button(style=discord.ButtonStyle.grey, label=mingle.name,custom_id=f"mingle")
                brokenbutton = Button(style=discord.ButtonStyle.grey, label=broken.name,custom_id=f"broken")
                selfr= View()
                selfr.add_item(singlebutton)     
                selfr.add_item(minglebutton) 
                selfr.add_item(brokenbutton)   
                selfembed= discord.Embed(color=self.color,title="Interact with the following for getting or removing the role that follows",description=f"> Single:{single.mention}\n > Mingle:{mingle.mention}\n > Broken:{broken.mention}\n") 
                selfembed.set_author(name=f"Status Roles For {ctx.guild.name}", icon_url=self.client.user.avatar.url)    
                selfrolemsg = await channel.send(embed=selfembed,view=selfr) 
                data[str(ctx.guild.id)] = {
                          'single': str(single.id),
                          'mingle': str(mingle.id),
                          'broken': str(broken.id),
                          'msg': selfrolemsg.id,
                          'channel': channel.id
                           }
                with open("status.json", "w") as f: 
                    json.dump(data, f, indent=4)  
                    
                
            if view.value == "discord.ButtonStyle.blurple":
                buttonstyle.append(discord.ButtonStyle.blurple)
                singlebutton = Button(style=discord.ButtonStyle.blurple, label=single.name,custom_id=f"single")
                minglebutton = Button(style=discord.ButtonStyle.blurple, label=mingle.name,custom_id=f"mingle")
                brokenbutton = Button(style=discord.ButtonStyle.blurple, label=broken.name,custom_id=f"broken")
                selfr= View()
                selfr.add_item(singlebutton)     
                selfr.add_item(minglebutton) 
                selfr.add_item(brokenbutton)   
                selfembed= discord.Embed(color=self.color,title="Interact with the following for getting or removing the role that follows",description=f"> Single:{single.mention}\n > Mingle:{mingle.mention}\n > Broken:{broken.mention}\n") 
                selfembed.set_author(name=f"Status Roles For {ctx.guild.name}", icon_url=self.client.user.avatar.url)    
                selfrolemsg = await channel.send(embed=selfembed,view=selfr) 
                data[str(ctx.guild.id)] = {
                          'single': str(single.id),
                          'mingle': str(mingle.id),
                          'broken': str(broken.id),
                          'msg': selfrolemsg.id,
                          'channel': channel.id
                           }
                with open("status.json", "w") as f: 
                    json.dump(data, f, indent=4)  
            ####################
            
                
      else:
          hacker5 = discord.Embed(
          description=
          """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
          color=self.color)
          hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
          return await ctx.send(embed=hacker5)  
      
      


  @_status.command(name="disable", description="Disable status roles in the server .")
  @commands.has_permissions(administrator=True)
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def status_disable(self, ctx):
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
          with open("status.json", 'r') as f:
              data = json.load(f)
          if str(ctx.guild.id) not in data:
              embed6 = discord.Embed(
                    description=
                    f"⚠ | status role is not setupped for {ctx.guild.name}",
                    color=self.color)
              await ctx.send(embed=embed6)
          else:
              msg = data[str(ctx.guild.id)]["msg"]
              ch = data[str(ctx.guild.id)]["channel"]
              lame = await self.client.get_channel(ch).fetch_message(int(msg))
              
             ### lame = await ctx.fetch_message(int(msg))
              del data[str(ctx.guild.id)]
              try:
                  await lame.delete()
              except:
                  pass
              with open("status.json", "w") as f:
                  json.dump(data, f, indent=4)
              hacker = discord.Embed(
                        description=
                        f"✅ | Successfully Deleted status Roles for {ctx.guild.name} .",
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
          