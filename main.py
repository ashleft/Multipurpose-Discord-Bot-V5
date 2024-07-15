import os
from core.Astroz import Astroz
from utils.config import whCL, TOKEN
from discord.ext.commands import Context
from discord.ext import commands
from discord import app_commands
import time
try:
    import asyncio
    import jishaku, cogs
    import traceback
    from utils.Tools import *
    from discord import Webhook
except ModuleNotFoundError:
    #os.system("pip install tasksio && pip install httpx && pip install psutil && pip install requests && pip install git+https://github.com/PythonistaGuild/Wavelink")
    os.system("pip install git+https://github.com/Gorialis/jishaku")
    os.system("pip install git+https://github.com/Rapptz/discord-ext-menus")


os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"

token = TOKEN

client = Astroz()
tree = client.tree


@client.event
async def on_command_completion(context: Context) -> None:

    full_command_name = context.command.qualified_name
    split = full_command_name.split("\n")
    executed_command = str(split[0])
    hacker = discord.SyncWebhook.from_url(f"{whCL}")
    if not context.message.content.startswith("."):
        pcmd = f"`.{context.message.content}`"
    else:
        pcmd = f"`{context.message.content}`"
    if context.guild is not None:
        try:
            
            embed = discord.Embed(color=0x2f3136)
            embed.set_author(
                name=
                f"Executed {executed_command} Command By : {context.author}",
                icon_url=f"{context.author.avatar}")
            embed.set_thumbnail(url=f"{context.author.avatar}")
            embed.add_field(
                name="Command Name :",
                value=f"{executed_command}",
                inline=False)
            embed.add_field(
                name="Command Content :",
                value="{}".format(pcmd),
                inline=False)
            embed.add_field(
                name="Command Executed By :",
                value=
                f"{context.author} | ID: [{context.author.id}](https://discord.com/users/{context.author.id})",
                inline=False)
            embed.add_field(
                name="Command Executed In :",
                value=
                f"{context.guild.name}  | ID: [{context.guild.id}](https://discord.com/users/{context.author.id})",
                inline=False)
            embed.add_field(
                name=
                "Command Executed In Channel :",
                value=
                f"{context.channel.name}  | ID: [{context.channel.id}](https://discord.com/channel/{context.channel.id})",
                inline=False)
            embed.set_footer(text=f"Thank you for choosing  {client.user.name}",
                             icon_url=client.user.display_avatar.url)
            hacker.send(embed=embed)
        except:
            print('Error logging the command to webhook')
    else:
        try:

            embed1 = discord.Embed(color=0x2f3136)
            embed1.set_author(
                name=
                f"Executed {executed_command} Command By : {context.author}",
                icon_url=f"{context.author.avatar}")
            embed1.set_thumbnail(url=f"{context.author.avatar}")
            embed1.add_field(
                name="Command Name :",
                value=f"{executed_command}",
                inline=False)
            embed1.add_field(
                name="Command Executed By :",
                value=
                f"{context.author} | ID: [{context.author.id}](https://discord.com/users/{context.author.id})",
                inline=False)
            embed1.set_footer(text=f"Thank you for choosing  {client.user.name}",
                              icon_url=client.user.display_avatar.url)
            hacker.send(embed=embed1)
        except:
            print('Error logging the command to webhook')


@commands.cooldown(1, 2, commands.BucketType.user)
@commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
@commands.guild_only()
@client.command(name='muted')
async def muted_(ctx, *, reason: str):


  embed = discord.Embed(title="Robi | Automoderation",
                        description=f"Successfully muted Ash for {reason}.",
                        color=0x2f3136)


  await ctx.send(embed=embed)


@client.event
async def on_ready():     
    print("Loaded & Online!")
    print(f"Logged in as: {client.user}")
    print(f"Connected to: {len(client.guilds)} guilds")
    print(f"Connected to: {len(client.users)} users")
    time.sleep(1)
    try:
        synced = await client.tree.sync()
        print(f"synced {len(synced)} commands")
    except Exception as e:
        print (e)

async def main():
    async with client:
        os.system("cls")
        await client.load_extension("cogs")
        await client.load_extension("jishaku")
        await client.start(token)

if __name__ == "__main__":
    asyncio.run(main())
