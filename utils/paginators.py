from __future__ import annotations
import os 
import discord
from utils.config import BotName
try:
    from discord.ext import menus
    from discord.ext import commands
except ModuleNotFoundError:
    os.system("pip install git+https://github.com/Rapptz/discord-ext-menus")

from .paginator import Paginator as HackerPaginator
from discord.ext.commands import Context, Paginator as CmdPaginator
from typing import Any


class FieldPagePaginator(menus.ListPageSource):

    def __init__(self,
                 entries: list[tuple[Any, Any]],
                 *,
                 per_page: int = 10,
                 inline: bool = False,
                 **kwargs) -> None:
        super().__init__(entries, per_page=per_page)
        self.embed: discord.Embed = discord.Embed(
            title=kwargs.get('title'),
            description=kwargs.get('description'),
            color=0x2f3136)
        self.inline: bool = inline

    async def format_page(self, menu: HackerPaginator,
                          entries: list[tuple[Any, Any]]) -> discord.Embed:
        self.embed.clear_fields()

        for key, value in entries:
            self.embed.add_field(name=key, value=value, inline=self.inline)

        maximum = self.get_max_pages()
        if maximum > 1:
            text = f'{BotName} • Page {menu.current_page + 1}/{maximum}'
            self.embed.set_footer(
                text=text,
                icon_url=
                "https://media.discordapp.net/attachments/1240721769946681556/1241703788671406152/3aaa792d92cd3b2ae109924496677bd2.webp?ex=664b2a44&is=6649d8c4&hm=947b6ef99f909900dfe1869827ac893f51d1336664821119840461c8b83cc37d&=&format=webp&width=458&height=458"
            )
            self.embed.timestamp = discord.utils.utcnow()
        return self.embed


class TextPaginator(menus.ListPageSource):

    def __init__(self, text, *, prefix='```', suffix='```', max_size=2000):
        pages = CmdPaginator(prefix=prefix,
                             suffix=suffix,
                             max_size=max_size - 200)
        for line in text.split('\n'):
            pages.add_line(line)

        super().__init__(entries=pages.pages, per_page=1)

    async def format_page(self, menu, content):
        maximum = self.get_max_pages()
        if maximum > 1:
            return f'{content} {BotName} • Page {menu.current_page + 1}/{maximum}'
        return content


class DescriptionEmbedPaginator(menus.ListPageSource):

    def __init__(self,
                 entries: list[Any],
                 *,
                 per_page: int = 10,
                 **kwargs) -> None:
        super().__init__(entries, per_page=per_page)
        self.embed: discord.Embed = discord.Embed(
            title=kwargs.get('title'),
            color=0x2f3136,
        )

    async def format_page(self, menu: HackerPaginator,
                          entries: list[tuple[Any, Any]]) -> discord.Embed:
        self.embed.clear_fields()

        self.embed.description = '\n'.join(entries)
        self.embed.timestamp = discord.utils.utcnow()
        maximum = self.get_max_pages()
        if maximum > 1:
            text = f'{BotName} • Page {menu.current_page + 1}/{maximum}'
            self.embed.set_footer(
                text=text,
                icon_url=
                "https://media.discordapp.net/attachments/1240721769946681556/1241703788671406152/3aaa792d92cd3b2ae109924496677bd2.webp?ex=664b2a44&is=6649d8c4&hm=947b6ef99f909900dfe1869827ac893f51d1336664821119840461c8b83cc37d&=&format=webp&width=458&height=458"
            )

        return self.embed
