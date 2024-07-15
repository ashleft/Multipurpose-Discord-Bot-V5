import discord
import json
from discord import app_commands
from discord.ext import commands
from utils.Tools import *
from discord.ext import commands

# ------------------------ COGS ------------------------ #  

class GiveRoleAfterCaptchaCog(commands.Cog, name="giveRoleAfterCaptcha command"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

# ------------------------------------------------------ #  
    
    @commands.hybrid_command(name = 'giveroleaftercaptcha', 
                        aliases= ["grac", "giverole", "captcharole", "verifiedrole"],
                        description="Enable or disable the role given after the captcha.")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def giveroleaftercaptcha(self, ctx, role: discord.Role):

        try:
            roleId = int(role.id)
            data = getConfig(ctx.guild.id)
            data["roleGivenAfterCaptcha"] = roleId
            

            updateConfig(ctx.guild.id, data)
            
            embed = discord.Embed(description = f"<@&{roleId}> will be given after the captcha is passed.", color = 0x2f3136) # Green
            embed.set_author(name="Success!", icon_url="https://images-ext-2.discordapp.net/external/uEX7ti-VOvwGYMbzkcph9kMSgbmuiuqAFQVLMgwQm_8/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1071808240981127258/524be1996e8d1a3221d02817c0294e40.png?format=webp&quality=lossless&width=468&height=468")
            await ctx.send(embed=embed)
        
        except Exception as error:
            print(f"giveroleaftercaptcha error : {error}")
            roleId = role.id
            if roleId == "off":
                data = getConfig(ctx.guild.id)
                data["roleGivenAfterCaptcha"] = False
                
                updateConfig(ctx.guild.id, data)

            else:
                prefix = "?"
                embed = discord.Embed(description ="INVALID_ARGUMENT", color = 0x2f3136)
                embed.set_author(name="Error", icon_url="https://images-ext-2.discordapp.net/external/uEX7ti-VOvwGYMbzkcph9kMSgbmuiuqAFQVLMgwQm_8/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1071808240981127258/524be1996e8d1a3221d02817c0294e40.png?format=webp&quality=lossless&width=468&height=468")
                await ctx.send(embed=embed)


# ------------------------ BOT ------------------------ #  

async def setup(bot):
      await bot.add_cog(GiveRoleAfterCaptchaCog(bot=bot))