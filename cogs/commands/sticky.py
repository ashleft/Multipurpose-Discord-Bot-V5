import asyncio
import discord
from discord.ext import commands, tasks
import json
import os

class Sticky(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stickies_file = "stickies.json"
        self.stickies = self.load_stickies()
        self.update_sticky.start()

    def load_stickies(self):
        if os.path.exists(self.stickies_file):
            with open(self.stickies_file, "r") as f:
                return json.load(f)
        else:
            return {}

    def save_stickies(self):
        with open(self.stickies_file, "w") as f:
            json.dump(self.stickies, f, indent=4)

    def get_sticky_data(self, guild_id):
        return self.stickies.get(str(guild_id), {})

    def get_sticky_content(self, guild_id):
        return self.get_sticky_data(guild_id).get("content", "")

    @tasks.loop(minutes=10)
    async def update_sticky(self):

        try:
            for guild_id, data in self.stickies.items():
                guild = self.bot.get_guild(int(guild_id))

                if guild is None:
                    continue  

                channel_id = data.get("channel")
                content = data.get("content")
                last_message_id = data.get("last")

                if not channel_id or not content:
                    continue  

                channel = guild.get_channel(int(channel_id))

                if channel is None:
                    continue  
          
                if last_message_id:
                    try:
                        last_message = await channel.fetch_message(int(last_message_id))
                        await last_message.delete()
                    except discord.NotFound:
                        pass  

                new_message = await channel.send(content)
                self.stickies[guild_id]["last"] = str(new_message.id)
                self.save_stickies()
        except Exception as e:
            print(f"An error occurred in update_sticky: {e}")

    @commands.hybrid_command(name="sticky")
    async def sticky(self, ctx, channel: discord.TextChannel, *, content):
        guild_id = str(ctx.guild.id)
        if guild_id not in self.stickies:
            self.stickies[guild_id] = {}

        if "content" in self.stickies[guild_id]:
            embed = discord.Embed(title="Error!", description=f"<:warn:1199645241729368084> Only one sticky message is allowed per guild.", color=0x2f3136)
            await ctx.send(embed=embed)
            return

        self.stickies[guild_id] = {"channel": str(channel.id), "content": content}
        self.save_stickies()

        embed = discord.Embed(
            title="Sticky Message Added",
            description=f"{content} - (#{channel.name})",
            color=0x2f3136
        )
        added = await ctx.send(embed=embed)

        content = await channel.send(content)
        self.stickies[guild_id]["last"] = content.id

        await asyncio.sleep(10)
        await added.delete()

    @commands.hybrid_command(name="unsticky")
    async def unsticky(self, ctx):
        guild_id = ctx.guild.id
        data = self.get_sticky_data(guild_id)
        guild_id = str(ctx.guild.id)
        content = data.get('content')
        if guild_id in self.stickies and "content" in self.stickies[guild_id]:
            del self.stickies[guild_id]["content"]
            self.save_stickies()
            embed = discord.Embed(description=f"<:tick:1199413323595260034> Sticky message removed.\n\nMessage: **{content}**", color=0x2f3136)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f"No sticky message found for this guild.", color=0x2f3136)
            await ctx.send(embed=embed)

    @commands.command(name="stickylist")
    async def sticky_list(self, ctx):
        guild_id = str(ctx.guild.id)
        data = self.get_sticky_data(guild_id)
        content = data.get("content", "No sticky message set.")
        embed = discord.Embed(title="Sticky Messages", description=content, color=0x2f3136)
        await ctx.send(embed=embed)
