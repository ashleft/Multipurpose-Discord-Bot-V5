from __future__ import annotations
from discord.ext import commands
from utils.config import BotName
from utils.Tools import *
from discord import *
import os
#os.system("pip install Pillow")
from utils.config import OWNER_IDS, No_Prefix
import json, discord
from typing import *
from io import BytesIO
import typing
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator
import time, datetime
from typing import Optional
#from PIL import Image, ImageFont, ImageDraw, ImageChops

def circle(pfp, size = (215,215)):
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")

    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)

    mask = Image.new('L', bigsize, 0)

    draw = ImageDraw.Draw(mask) 

    draw.ellipse((0, 0) + bigsize, fill=255)

    mask = mask.resize(pfp.size, Image.ANTIALIAS)

    mask = ImageChops.darker(mask, pfp.split()[-1])

    pfp.putalpha(mask)

    return pfp
    
blacklisted_commands = ["test_blc", "test1"]
async def add_premium(user, tier, guild_limit, exp_at):

    with open("premium.json", "r") as f:

        data = json.load(f)

    configData = {

        "author_tier": tier,

        "guild_limit": guild_limit,

        "expire_at": exp_at

    }

    data[str(user.id)] = configData

    with open("premium.json", "w") as fo:

        json.dump(data, fo, indent=4)

  

async def remove_premium(user):

    with open("premium.json", "r") as f:

        data = json.load(f)

        if str(user.id) not in data:

            return

        elif str(user.id) in data:

            data.pop(user.id)

    with open("premium.json", "w") as f:

        json.dump(data, f, indent=4)


class Owner(commands.Cog):

  def __init__(self, client):
    self.client = client
    self.color = 0x2f3136
    
  @commands.command(name="pft")
  @commands.is_owner()
  async def pft(self, ctx, member: Union[discord.Member, discord.User]=None):
    if not member:
        member = ctx.author
        
    name = str(member)
    member = discord.utils.get(self.client.users, id=member.id)
    profile_base = Image.open("Profile-base.png").convert("RGBA")
    pfp = member.avatar_url_as(sizs=256)
    BIOD = BytesIO(await pfp.read())
    pfp = Image.open(BIOD).convert("RGBA")
    
 #   pfp = Image.open(BIOD).convert("RGBA")

    

    name = f"{name[:15]}..." if len(name)>15 else name

    

    draw = ImageDraw.Draw(BIOD)

    pfp = circle(pfp,(215,215))

    font = ImageFont.truetype("Nunito-Regular.ttf", 38)

    subufont = ImageFont.truetype("Nunito-Regular.ttf", 27)
    subbfont = ImageFont.truetype("Nunito-Regular.ttf", 44)
    with BytesIO() as a:
        a.seek(0)
        await ctx.send(file=discord.File(a, "profile.png"))
    

  @commands.command(name="test1")
  @commands.is_owner()
  async def test1(self, ctx):
    await ctx.send(str(ctx.bot.walk_commands.name))
    if str(ctx.bot.walk_commands()) in blacklisted_commands:
      await ctx.send(" this is blacklisted commands")
    else:
      await ctx.send("None")
    
  @commands.command(name="slist")
  @commands.is_owner()
  async def _slist(self, ctx):
    vg = ["Void's Hub"]
    hasanop = ([hasan for hasan in self.client.guilds])
    hasanop = sorted(hasanop,
                     key=lambda hasan: hasan.member_count,
                     reverse=True)
    entries = [
      f"`[{i}]` | [{f'{BotName}’s Hub' if g.name in vg else g.name}](https://discord.com/channels/{g.id}) - {g.member_count}"
      for i, g in enumerate(hasanop, start=1)
    ]
    paginator = Paginator(source=DescriptionEmbedPaginator(
      entries=entries,
      description="",
      title=f"Server List of {self.client.user.name} - {len(self.client.guilds)}",
      color=self.color,
      per_page=10),
                          ctx=ctx)
    await paginator.paginate()

  @commands.command(name="restartbot", help="Restarts the client.")
  @commands.is_owner()
  async def _restart(self, ctx):
          embed = discord.Embed(
            description=f"| Restarting {self.client.user.name} .",
            color=discord.Colour(self.color))
          embed.set_author(name=ctx.author,icon_url=ctx.author.display_avatar.url)
          restart_program()
          await ctx.reply(embed=embed, mention_author=False)
    
          
          


  @commands.group(name="blacklist",
                  help="let's you add someone in blacklist",
                  aliases=["bl"])
  @commands.is_owner()
  async def blacklist(self, ctx):
    if ctx.invoked_subcommand is None:
      with open("blacklist.json") as file:
        blacklist = json.load(file)
        entries = [
          f"`[{no}]` | <@!{mem}> (ID: {mem})"
          for no, mem in enumerate(blacklist['ids'], start=1)
        ]
        paginator = Paginator(source=DescriptionEmbedPaginator(
          entries=entries,
          title=f"List of Blacklisted users of {self.client.user.name} - {len(blacklist['ids'])}",
          description="",
          per_page=10,
          color=self.color),
                              ctx=ctx)
        await paginator.paginate()

  @blacklist.command(name="add")
  @commands.is_owner()
  async def blacklist_add(self, ctx,*, member: Optional[Union[discord.Member,
                                         discord.User]] = None):
    try:
      with open('blacklist.json', 'r') as bl:
        blacklist = json.load(bl)
        if str(member.id) in blacklist["ids"]:
          embed = discord.Embed(
            title="Error!",
            description=f"{member.name} is already blacklisted",
            color=discord.Colour(self.color))
          await ctx.reply(embed=embed, mention_author=False)
        else:
          add_user_to_blacklist(member.id)
          embed = discord.Embed(
            title="Blacklisted",
            description=f"Successfully Blacklisted {member.name}",
            color=discord.Colour(self.color))
          with open("blacklist.json") as file:
            blacklist = json.load(file)
            embed.set_footer(
              text=
              f"There are now {len(blacklist['ids'])} users in the blacklist")
            await ctx.reply(embed=embed, mention_author=False)
    except:
      embed = discord.Embed(title="Error!",
                            description=f"An Error Occurred",
                            color=discord.Colour(self.color))
      await ctx.reply(embed=embed, mention_author=False)

  @blacklist.command(name="remove")
  @commands.is_owner()
  async def blacklist_remove(self, ctx, *, member: Optional[Union[discord.Member,
                                         discord.User]] = None):
    try:
      remove_user_from_blacklist(member.id)
      embed = discord.Embed(
        title="User removed from blacklist",
        description=
        f"✅ | **{member.name}** has been successfully removed from the blacklist",
        color=self.color)
      with open("blacklist.json") as file:
        blacklist = json.load(file)
        embed.set_footer(
          text=f"There are now {len(blacklist['ids'])} users in the blacklist")
        await ctx.reply(embed=embed, mention_author=False)
    except:
      embed = discord.Embed(
        title="Error!",
        description=f"**{member.name}** is not in the blacklist.",
        color=self.color)
      embed.set_thumbnail(url=f"{self.client.user.display_avatar.url}")
      await ctx.reply(embed=embed, mention_author=False)



  @commands.command(name="owners")
  @commands.is_owner()
  async def own_list(self, ctx):
    with open("info.json") as f:
      np = json.load(f)
      nplist = np["OWNER_IDS"]
      npl = ([await self.client.fetch_user(nplu) for nplu in nplist])
      npl = sorted(npl, key=lambda nop: nop.created_at)
      entries = [
        f"`[{no}]` | [{mem}](https://discord.com/users/{mem.id}) (ID: {mem.id})"
        for no, mem in enumerate(npl, start=1)
      ]
      paginator = Paginator(source=DescriptionEmbedPaginator(
        entries=entries,
        title=f"Owner list of {self.client.user.name} - {len(nplist)}",
        description="",
        per_page=10,
        color=self.color),
                            ctx=ctx)
      await paginator.paginate()



  @commands.command()
  @commands.is_owner()
  async def dm(self, ctx, user: discord.User, *, message: str):
    """ DM the user of your choice """
    try:
      await user.send(message)
      await ctx.send(
        f"✅ | Successfully Sent a DM to **{user}**"
      )
    except discord.Forbidden:
      await ctx.send("This user might DMs blocked or it's a bot account")

  @commands.group()
  @commands.is_owner()
  async def change(self, ctx):
    if ctx.invoked_subcommand is None:
      await ctx.send_help(str(ctx.command))

  @change.command(name="nickname")
  @commands.is_owner()
  async def change_nickname(self, ctx, *, name: str = None):
    """ Change nickname. """
    try:
      await ctx.guild.me.edit(nick=name)
      if name:
        await ctx.send(
          f"✅ | Successfully changed nickname to **{name}**"
        )
      else:
        await ctx.send(
          "✅ | Successfully removed nickname")
    except Exception as err:
      await ctx.send(err)

   
  @commands.command(name="leave")
  @commands.is_owner()
  async def l(self, ctx,*,guild_id):
    g = self.client.get_guild(guild_id)
    await g.leave()
    return await ctx.send(f"Left {g.name}")

