import discord
import asyncio
import json
from discord import app_commands
from discord.ext import commands
from discord.utils import get
from utils.Tools import *

# ------------------------ COGS ------------------------ #  

class SetupCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

# ------------------------------------------------------ #  
 
    @commands.hybrid_command(name ='verification',
                        aliases=["captcha", 'captchaverification'],
                        description="Enable or disable the verification system.")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def setup(self, ctx, on_or_off):

        onOrOff = on_or_off.lower()

        if onOrOff == "on":
            embed = discord.Embed(title = "Captcha Verification", description = "Setting up the captcha protection will do some changes in the server:**\n\n- Captcha verification channel\n- Logs channel\n- Temporary role (will be given to unverified users)\n\n**If you want to continue send \"**yes**\" else send \"**no**\".", color = 0x000000)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            
            await ctx.send(embed=embed)
            # Ask if user are sure
            def check(message):
                return message.author == ctx.author and message.content.lower() in ["yes", "no"]

            try:
                msg = await self.bot.wait_for('message', timeout=30.0, check=check)
                if msg.content == "no":
                    embed = discord.Embed(description="Successfully cancelled setup process.", color=0x000000)
                    embed.set_author(name="Cancelled!", icon_url=ctx.author.display_avatar)
                    await ctx.send(embed=embed)
                else:
                    try:
                        embed = discord.Embed(description="Processing", color=0x000000)
                        loading = await ctx.send(embed=embed)

                        # Data
                        data = getConfig(ctx.guild.id)

                        # Create role
                        temporaryRole = await ctx.guild.create_role(name="Unverified")
                        # Hide all channels
                        for channel in ctx.guild.channels:
                            if isinstance(channel, discord.TextChannel):

                                perms = channel.overwrites_for(temporaryRole)
                                perms.read_messages=False
                                await channel.set_permissions(temporaryRole, overwrite=perms)
                                
                            elif isinstance(channel, discord.VoiceChannel):

                                perms = channel.overwrites_for(temporaryRole)
                                perms.read_messages=False
                                perms.connect=False
                                await channel.set_permissions(temporaryRole, overwrite=perms)

                        # Create captcha channel
                        captchaChannel = await ctx.guild.create_text_channel('verification')

                        perms = captchaChannel.overwrites_for(temporaryRole)
                        perms.read_messages=True
                        perms.send_messages=True
                        await captchaChannel.set_permissions(temporaryRole, overwrite=perms)

                        perms = captchaChannel.overwrites_for(ctx.guild.default_role)
                        perms.read_messages=False
                        await captchaChannel.set_permissions(ctx.guild.default_role, overwrite=perms)

                        #await captchaChannel.edit(slowmode_delay= 5) Removed slowmode for captcha channel
                        # Create log channel
                        if data["logChannel"] is False:
                            logChannel = await ctx.guild.create_text_channel(f"verification-logs")

                            perms = logChannel.overwrites_for(ctx.guild.default_role)
                            perms.read_messages=False
                            await logChannel.set_permissions(ctx.guild.default_role, overwrite=perms)

                            data["logChannel"] = logChannel.id
                        
                        # Edit configuration.json
                        # Add modifications
                        data["captcha"] = True
                        data["temporaryRole"] = temporaryRole.id
                        data["captchaChannel"] = captchaChannel.id
                        

                        updateConfig(ctx.guild.id, data)
                        
                        await loading.delete()
                        embed = discord.Embed(description = "Successfully setuped captcha verification.", color = 0x000000)
                        embed.set_author(name="Success!", icon_url=ctx.author.display_avatar)
                        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                        await ctx.send(embed = embed)
                    except Exception as error:
                        embed = discord.Embed(description=f"An error occurred: {error}", color=0xe00000) # Red
                        embed.set_author(name="Error!", icon_url=ctx.author.display_avatar)
                        
                        return await ctx.send(embed=embed)

            
            except (asyncio.TimeoutError):
                embed = discord.Embed(description =f"You exceeded the response time (30s).", color = 0x000000)
                embed.set_author(name="Timed out!", icon_url=ctx.author.display_avatar)
                await ctx.send(embed = embed)

        elif onOrOff == "off":
            embed=discord.Embed(color=0x000000)
            embed.set_author(name="Processing...", icon_url=ctx.author.display_avatar)
            loading = await ctx.send(embed=embed)
            data = getConfig(ctx.guild.id)
            data["captcha"] = False
            
            # Delete all
            noDeleted = []
            try:
                temporaryRole = get(ctx.guild.roles, id= data["temporaryRole"])
                await temporaryRole.delete()
            except:
                noDeleted.append("temporaryRole")
            try:  
                captchaChannel = self.bot.get_channel(data["captchaChannel"])
                await captchaChannel.delete()
            except:
                noDeleted.append("captchaChannel")

            # Add modifications
            data["captchaChannel"] = False
            
            # Edit configuration.json
            updateConfig(ctx.guild.id, data)
            
            await loading.delete()
            embed = discord.Embed(description ="Successfully removed verification system." , color = 0x000000) # Green
            embed.set_author(name="Success!", icon_url=ctx.author.display_avatar)
            await ctx.send(embed = embed)
            if len(noDeleted) > 0:
                errors = ", ".join(noDeleted)
                embed = discord.Embed(description =f"An error occurred while removing verification system\n\n{errors}", color = 0x000000) # Red
                embed.set_author(name="Error!", icon_url=ctx.author.display_avatar)
                await ctx.send(embed = embed)

        else:
            prefix = "/"
            embed = discord.Embed(description= f"The setup argument must be on or off\nFollow the example: `{prefix}setup <on/off>`", color=0x000000) # Red
            embed.set_author(name="Error!", icon_url=ctx.author.display_avatar)
            
            return await ctx.send(embed=embed)
            pass
