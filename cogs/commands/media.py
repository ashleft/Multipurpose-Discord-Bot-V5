import discord
import json
from discord.ext import commands

class Media(commands.Cog):
    def __init__(self, client):
        self.client = client

  
    @commands.Cog.listener()
    async def on_ready(self):
      with open("media.json", "r") as f:
        ok = json.load(f)
      for guild in self.client.guilds:
        if not str(guild.id) in ok:
          ok[str(guild.id)] = {"channel": []}
      with open("media.json", "w") as f:
        json.dump(ok,f,indent=4)

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
      with open("media.json", "r") as f:
        ok = json.load(f)
      for guild in self.client.guilds:
        if not str(guild.id) in ok:
          ok[str(guild.id)] = {"channel": []}
      with open("media.json", "w") as f:
        json.dump(ok,f,indent=4)
    @commands.hybrid_group(invoke_without_command = True)
    async def media(self, ctx):
        prefix = ctx.prefix
        em = discord.Embed(
          title=f"Media (4)",
          description=f"`{prefix}media`\nConfigures the media only channels!\n\n`{prefix}media setup`\nSetups media only channels in the server.\n\n`{prefix}media remove`\nRemoves the media only channels in the server.\n\n`{prefix}media config`\nShows the configured media only channels for the server.\n\n`{prefix}media reset`\nRemoves all the channels from media only channels for the server.", color=0x2f3136)
        await ctx.send(embed=em)
          
    @media.command(name="setup", description="Setups media only channels for the server")
    @commands.has_permissions(administrator = True)
    async def setup(self, ctx, *, channel: discord.TextChannel):
        with open("media.json", "r") as f:
            media = json.load(f)

        media[str(ctx.guild.id)]["channel"].append(channel.id)

        with open("media.json", "w") as f:
            json.dump(media, f, indent = 4)

        await ctx.send(embed=discord.Embed(description=f"<:tick:1199413323595260034> | Successfully added {channel.mention} to my media database.", color=0x2f3136))


    @media.command(name="remove", description="Removes media only channels for the server")
    @commands.has_permissions(administrator = True)
    async def remove(self, ctx, *, channel: discord.TextChannel):
        with open("media.json", "r") as f:
            media = json.load(f)

        media[str(ctx.guild.id)]["channel"].remove(channel.id)

        with open("media.json", "w") as f:
            json.dump(media, f, indent = 4)

        await ctx.send(embed=discord.Embed(description=f"<:tick:1199413323595260034> | Successfully removed {channel.mention} from my media database.", color=0x2f3136))


    @media.command(name="config", aliases=["settings", "show"], description="Shows the configured media only channels for the server")
    @commands.has_permissions(administrator = True)
    async def config(self, ctx):
        with open("media.json", "r") as f:
            media = json.load(f)
        
        chan = media[str(ctx.guild.id)]["channel"]

        channel = list([self.client.get_channel(id).mention for id in media[str(ctx.guild.id)]["channel"]])

        embed = discord.Embed(title = f"Media Only Channels for {ctx.guild.name}", color=0x2f3136)
        num = 0
        for i in channel:
            num += 1
            i = i.replace("['']", "")
            embed.add_field(name = f"{num}", value = i, inline = True)

        embed.set_footer(text = f"Requested by {ctx.author.name}", icon_url = ctx.author.avatar)

        await ctx.send(embed = embed)


    @media.command(name="reset", description="Removes all the channels from media only channels for the server")
    @commands.has_permissions(administrator = True)
    async def reset(self, ctx):
        with open("media.json", "r") as f:
            media = json.load(f)

        media[str(ctx.guild.id)]["channel"] = []

        with open("media.json", "w") as f:
            json.dump(media, f, indent = 4)

        await ctx.send(embed=discord.Embed(description="<:tick:1199413323595260034> | Successfully cleared media database of this server.", color=0x2f3136))


    @commands.Cog.listener()
    async def on_message(self, message):
        try:
           if message.author.bot:
              return
           
           with open("media.json", "r") as f:
                media = json.load(f)
                
           guild_id = str(message.guild.id)

           channel = media[str(message.guild.id)]["channel"]

           if guild_id in media and "channel" in media[guild_id]:
                channel = media[guild_id]["channel"]

                if message.channel.id in channel:
                    if not message.attachments:
                       await message.delete()
                       await message.channel.send(f"<:warn:1199645241729368084> This channel is configured for media only. You are only allowed to send media files.", delete_after = 2)
        
        except Exception as e:
            error_logs = self.bot.get_channel(1199622739502317629)
            await error_logs.send(e)


        