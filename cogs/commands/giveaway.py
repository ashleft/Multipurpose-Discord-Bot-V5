from discord.ext import commands, tasks
import datetime, pytz, time as t
from discord.ui import Button, Select, View
import aiosqlite, random, typing
import sqlite3
import asyncio
import discord, logging
from discord.utils import get

connection = sqlite3.connect('giveaways.db')

cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Giveaway (
                    guild_id INTEGER,
                    host_id INTEGER,
                    start_time TIMESTAMP,
                    ends_at TIMESTAMP,
                    prize TEXT,
                    winners INTEGER,
                    message_id INTEGER,
                    channel_id INTEGER,
                    PRIMARY KEY (guild_id, message_id)
                )''')

connection.commit()
connection.close()



def convert(time):
    pos = ["s","m","h","d"]
    time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 86400 , "f" : 259200}

    unit = time[-1]
    if unit not in pos:
     
            
      return
    try:
        val = int(time[:-1])
    except ValueError:
            
            return

    return val * time_dict[unit]

def WinnerConverter(winner):
    try:
        int(winner)
    except ValueError:
        try:
           return int(winner[:-1])
        except:
            return -4
    
    return winner


class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self) -> None:
        self.connection = await aiosqlite.connect('giveaways.db')
        self.cursor = await self.connection.cursor()
        self.GiveawayEnd.start()

    async def cog_unload(self) -> None:
        await self.connection.close()

    @commands.hybrid_command(description="Starts a new giveaway.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.check_any(commands.is_owner(), commands.has_permissions(manage_guild=True))
    async def gstart(self, ctx,
                      time,
                      winners: int,
                      *,
                      prize: str):
        
        await self.cursor.execute("SELECT message_id, channel_id FROM Giveaway WHERE guild_id = ?", (ctx.guild.id,))
        re = await self.cursor.fetchall()

        if winners >=  15:
            embed = discord.Embed(description=f"⚠ Cannot exceed more than 15 winners.", color=0x2f3136)
            message = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
            return

        g_list = [i[0] for i in re]
        if len(g_list) >= 5:
            embed = discord.Embed(description=f"⚠ The maximum limit of giveaways for this guild has been reached.", color=0x2f3136)
            message = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
            return

        converted = self.convert(time)
        if converted / 60 >= 50400:
            embed = discord.Embed(description=f"⚠ Time cannot exceed 31 days!", color=0x2f3136)
            message = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
            return

        if converted == -1:
            embed = discord.Embed(description=f"⚠ Invalid time format", color=0x2f3136)
            message = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
            return
        if converted == -2:
            embed = discord.Embed(description=f"⚠ Invalid time format. Please provide the time in numbers.", color=0x2f3136)
            message = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
            return

        ends = (datetime.datetime.now().timestamp() + converted)

        embed = discord.Embed(description=f"Winner(s): **{winners}**\nReact with 🎉 to participate!\nEnds <t:{round(ends)}:R> (<t:{round(ends)}:f>)\n\nHosted by {ctx.author.mention}", color=0x2f3136)
        
        ends1 = datetime.datetime.utcnow() + datetime.timedelta(seconds=converted)
        ends_utc = ends1.replace(tzinfo=datetime.timezone.utc)

        embed.timestamp = embed.timestamp = ends_utc
        if ctx.guild.icon:
            embed.set_author(icon_url=ctx.guild.icon.url, name=prize)
        else:
            embed.set_author(name=prize,
                             icon_url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"Ends at")

        message = await ctx.send("🎁 **GIVEAWAY** 🎁", embed=embed)
        try:
           await ctx.message.delete()
        except:
            pass

        await self.cursor.execute("INSERT INTO Giveaway(guild_id, host_id, start_time, ends_at, prize, winners, message_id, channel_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (ctx.guild.id, ctx.author.id, datetime.datetime.now(), ends, prize, winners, message.id, ctx.channel.id))

        await message.add_reaction("🎉")
        await self.connection.commit()

    @tasks.loop(seconds=5)
    async def GiveawayEnd(self):
        await self.cursor.execute("SELECT ends_at, guild_id, message_id, host_id, winners, prize, channel_id FROM Giveaway WHERE channel_id IS NOT NULL")
        ends_raw = await self.cursor.fetchall()

        current_time = datetime.datetime.now().timestamp()

        for giveaway in ends_raw:
            if int(current_time) >= round(float(giveaway[0])):
                guild = self.bot.get_guild(int(giveaway[1]))
                channel = self.bot.get_channel(int(giveaway[6]))
                if channel is not None:
                    try:
                        message = await channel.fetch_message(int(giveaway[2]))
                    except discord.NotFound:
                        continue
                    
                    users = [i.id async for i in message.reactions[0].users()]
                    users.remove(self.bot.user.id)

                    if len(users) < 1:
                        await message.reply(f"No one won the **{giveaway[5]}** giveaway, due to not enough participants.")
                        await self.cursor.execute("DELETE FROM Giveaway WHERE message_id = ? AND guild_id = ?", (message.id, message.guild.id))
                        return
                    
                    winner = ', '.join(f'<@!{i}>' for i in random.sample(users, k=int(giveaway[4])))

                    embed = discord.Embed(
                        description=f"Ended <t:{int(current_time)}:R>\nHosted by <@{int(giveaway[3])}>\nWinner(s): {winner}",
                        color=0x2f3136
                    )

                    embed.timestamp = discord.utils.utcnow()

                    embed.set_author(name=giveaway[5])
                    embed.set_footer(text=f"Ended at")
                    try:
                        await message.edit(content="🎁 **GIVEAWAY ENDED** 🎁", embed=embed)
                    except:
                        pass

                    try:
                        await message.reply(f"{winner} 🎉 Congratulations! you won **{giveaway[5]}!**, Hosted by <@{int(giveaway[3])}>")
                    except:
                        pass
                    await self.cursor.execute("DELETE FROM Giveaway WHERE message_id = ? AND guild_id = ?", (message.id, message.guild.id))
                    #print(f"[Natural] Giveaway Ended - {guild.id} ({giveaway[5]})")
        await self.connection.commit()

    @commands.Cog.listener("on_message_delete")
    async def GiveawayMessageDelete(self, message):
        await self.cursor.execute("SELECT message_id FROM Giveaway WHERE guild_id = ?", (message.guild.id,))
        re = await self.cursor.fetchone()

        if message.author != self.bot.user:
            return
        
        if re is not None:
            if message.id == int(re[0]):
                await self.cursor.execute("DELETE FROM Giveaway WHERE channel_id = ? AND message_id = ? AND guild_id = ?", (message.channel.id, message.id, message.guild.id))

                print(f"Giveaway message deleted in {message.guild.name} - {message.guild.id}")
                await self.connection.commit()

    @commands.hybrid_command(name="gend", description="Ends a giveaway early.")
    @commands.check_any(commands.is_owner(), commands.has_permissions(manage_guild=True))
    async def gend(self, ctx, message_id = None):
        if message_id:
            try:
                int(message_id)
            except ValueError:
                embed = discord.Embed(description=f"⚠ The provided message ID is invalid.", color=0x2f3136)
                message = await ctx.send(embed=embed)
                await asyncio.sleep(5)
                await message.delete()
                return
            
        if message_id is not None:
            current_time = datetime.datetime.now().timestamp()
            await self.cursor.execute('SELECT ends_at, guild_id, message_id, host_id, winners, prize, channel_id FROM Giveaway WHERE message_id = ?', (int(message_id),))
            re = await self.cursor.fetchone()

            if re is None:
                embed = discord.Embed(description=f"⚠ The giveaway was not found.", color=0x2f3136)
                message = await ctx.send(embed=embed)
                await asyncio.sleep(5)
                await message.delete()
                return
            
            ch = self.bot.get_channel(int(re[6]))
            message = await ch.fetch_message(int(message_id))

            users = [i.id async for i in message.reactions[0].users()]
            users.remove(self.bot.user.id)

            if len(users) < 1:
                await ctx.send(f"✅ Successfully ended the giveaway in <#{int(re[6])}>")
                await message.reply(f"No one won the **{re[5]}** giveaway, due to not enough participants.")
                await self.cursor.execute("DELETE FROM Giveaway WHERE message_id = ? AND guild_id = ?", (message.id, message.guild.id))
                return
            
            winner = ', '.join(f'<@!{i}>' for i in random.sample(users, k=int(re[4])))

            embed = discord.Embed(
                        description=f"Ended <t:{int(current_time)}:R>\nHosted by <@{int(re[3])}>\nWinner(s): {winner}",
                        color=0x2f3136
                    )
            embed.timestamp = discord.utils.utcnow()

            embed.set_author(name=re[5],
                            icon_url=ctx.guild.icon.url)
            embed.set_footer(text=f"Ended at")

            await message.edit(content="🎁 **GIVEAWAY ENDED** 🎁", embed=embed)

            if int(ctx.channel.id) != int(re[6]):
                await ctx.send(f"✅ Successfully ended the giveaway in <#{int(re[6])}>")

            await message.reply(f"{winner} 🎉 Congratulations! you won **{re[5]}!**, Hosted by <@{int(re[3])}>")
            await self.cursor.execute("DELETE FROM Giveaway WHERE message_id = ? AND guild_id = ?", (message.id, message.guild.id))
            #print(f"[Gend] Giveaway Ended - {message.guild.name} ({message.guild.id}) - ({re[5]})")

        elif ctx.message.reference:
            await self.cursor.execute('SELECT ends_at, guild_id, message_id, host_id, winners, prize, channel_id FROM Giveaway WHERE message_id = ?', (ctx.message.reference.resolved.id,))
            re = await self.cursor.fetchone()

            if re is None:
                return await ctx.send(f"⚠ The giveaway was not found.")
        
            current_time = datetime.datetime.now().timestamp()

            message = await ctx.fetch_message(ctx.message.reference.message_id)

            users = [i.id async for i in message.reactions[0].users()]
            try: users.remove(self.bot.user.id)
            except: pass

            if len(users) < 1:
                await message.reply(f"No one won the **{re[5]}** giveaway, due to not enough participants.")
                await self.cursor.execute("DELETE FROM Giveaway WHERE message_id = ? AND guild_id = ?", (message.id, message.guild.id))
                return
            
            winner = ', '.join(f'<@!{i}>' for i in random.sample(users, k=int(re[4])))

            embed = discord.Embed(
                        description=f"Ended <t:{int(current_time)}:R>\nHosted by <@{int(re[3])}>\nWinner(s): {winner}",
                        color=0x2f3136
                    )
            embed.timestamp = discord.utils.utcnow()

            embed.set_author(name=re[5],
                            icon_url=ctx.guild.icon.url)
            embed.set_footer(text=f"Ended at")

            await message.edit(content="🎁 **GIVEAWAY ENDED** 🎁", embed=embed)

            await message.reply(f"{winner} 🎉 Congratulations! you won **{re[5]}!**, Hosted by <@{int(re[3])}>")
            await self.cursor.execute("DELETE FROM Giveaway WHERE message_id = ? AND guild_id = ?", (message.id, message.guild.id))
            #print(f"[Gend] Giveaway Ended - {message.guild.name} ({message.guild.id}) - ({re[5]})")
            
        else:
            await ctx.send("Please reply to the giveaway message or provide the giveaway ID.")
        await self.connection.commit()

    @commands.hybrid_command(description="Rerolls a giveaway. | Reply to the giveaway message.")
    @commands.check_any(commands.is_owner(), commands.has_permissions(manage_guild=True))
    async def greroll(self, ctx, message_id: typing.Optional[int] = None):
        if not ctx.message.reference:
            embed = discord.Embed(description=f"⚠ Reply with the giveaway message to reroll.", color=0x2f3136)
            message = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
            return
        
        if ctx.message.reference:
            message_id = ctx.message.reference.resolved.id

        message = await ctx.fetch_message(message_id)

        if ctx.message.reference.resolved.author.id != self.bot.user.id:
            embed = discord.Embed(description=f"⚠ The giveaway was not found.", color=0x2f3136)
            message = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
            return
        

        await self.cursor.execute(f"SELECT message_id FROM Giveaway WHERE message_id = ?", (message.id,))
        re = await self.cursor.fetchone()

        if re is not None:
            embed = discord.Embed(description=f"⚠ The giveaway is currently running. Please use the gend command instead to end the giveaway.", color=0x2f3136)
            message = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
            return
        
        users = [i.id async for i in message.reactions[0].users()]
        users.remove(self.bot.user.id)

        if len(users) < 1:
            await message.reply(f"No one won the **{re[5]}** giveaway, due to not enough participants.")
            return
        
        winners = random.sample(users, k=1)
        await message.reply(f"🎉 The new winner is "+", ".join(f"<@{i}>" for i in winners)+". Congratulations!")
        await self.connection.commit()

    def convert(self, time):
        pos = ["s", "m", "h", "d"]
        time_dict = {"s": 1, "m": 60, "h": 3600, "d": 86400, "f": 259200}

        unit = time[-1]
        if unit not in pos:
            return -1

        try:
            val = int(time[:-1])
        except ValueError:
            return -2

        return val * time_dict[unit]
