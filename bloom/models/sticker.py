from __future__ import annotations

import typing as t
from dataclasses import dataclass
from enum import Enum

from .base import UNKNOWN, Snowflake, Unknownish
from .user import User


@dataclass()
class Sticker:
    #: id of the sticker
    id: Snowflake
    #: name of the sticker
    name: str
    #: description of the sticker
    description: t.Optional[str]
    #: for guild stickers, the Discord name of a unicode emoji representing the sticker's expression. for standard stickers, a comma-separated list of related expressions.
    tags: str
    #: Deprecated previously the sticker asset hash, now an empty string
    asset: str
    #: type of sticker
    type: int
    #: type of sticker format
    format_type: int
    #: for standard stickers, id of the pack the sticker is from
    pack_id: Unknownish[Snowflake] = UNKNOWN
    #: whether this guild sticker can be used, may be false due to loss of Server Boosts
    available: Unknownish[bool] = UNKNOWN
    #: id of the guild that owns this sticker
    guild_id: Unknownish[Snowflake] = UNKNOWN
    #: the user that uploaded the guild sticker
    user: Unknownish[User] = UNKNOWN
    #: the standard sticker's sort order within its pack
    sort_value: Unknownish[int] = UNKNOWN


class StickerTypes(Enum):
    #: an official sticker in a pack, part of Nitro or in a removed purchasable pack
    STANDARD = 1
    #: a sticker uploaded to a Boosted guild for the guild's members
    GUILD = 2


class StickerFormatTypes(Enum):
    PNG = 1
    APNG = 2
    LOTTIE = 3


@dataclass()
class StickerItem:
    #: id of the sticker
    id: Snowflake
    #: name of the sticker
    name: str
    #: type of sticker format
    format_type: int


@dataclass()
class StickerPack:
    #: id of the sticker pack
    id: Snowflake
    #: the stickers in the pack
    stickers: t.List[Sticker]
    #: name of the sticker pack
    name: str
    #: id of the pack's SKU
    sku_id: Snowflake
    #: description of the sticker pack
    description: str
    #: id of the sticker pack's banner image
    banner_asset_id: Snowflake
    #: id of a sticker in the pack which is shown as the pack's icon
    cover_sticker_id: Unknownish[Snowflake] = UNKNOWN


class ResponseStructure(Enum):
    STICKER_PACKS = "array of"
