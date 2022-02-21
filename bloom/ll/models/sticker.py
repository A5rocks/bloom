from __future__ import annotations

import enum
import typing

import attr

from bloom.ll.models.base import UNKNOWN, Snowflake, Unknownish
from bloom.ll.models.user import User

# docs in this module are copied from the Discord Documentation


@attr.frozen(kw_only=True)
class Sticker:
    #: id of the sticker
    id: Snowflake
    #: name of the sticker
    name: str
    #: description of the sticker
    description: typing.Optional[str]
    #: autocomplete/suggestion tags for the sticker (max 200 characters)
    tags: str
    #: Deprecated previously the sticker asset hash, now an empty string
    asset: Unknownish[str] = UNKNOWN
    #: type of sticker
    type: int
    #: type of sticker format
    format_type: int
    #: for standard stickers, id of the pack the sticker is from
    pack_id: Unknownish[Snowflake] = UNKNOWN
    #: whether this guild sticker can be used, may be false due to loss of
    #: Server Boosts
    available: Unknownish[bool] = UNKNOWN
    #: id of the guild that owns this sticker
    guild_id: Unknownish[Snowflake] = UNKNOWN
    #: the user that uploaded the guild sticker
    user: Unknownish[User] = UNKNOWN
    #: the standard sticker's sort order within its pack
    sort_value: Unknownish[int] = UNKNOWN


class StickerTypes(enum.Enum):
    #: an official sticker in a pack, part of Nitro or in a removed
    #: purchasable pack
    STANDARD = 1
    #: a sticker uploaded to a Boosted guild for the guild's members
    GUILD = 2


class StickerFormatTypes(enum.Enum):
    PNG = 1
    APNG = 2
    LOTTIE = 3


@attr.frozen(kw_only=True)
class StickerItem:
    #: id of the sticker
    id: Snowflake
    #: name of the sticker
    name: str
    #: type of sticker format
    format_type: int


@attr.frozen(kw_only=True)
class StickerPack:
    #: id of the sticker pack
    id: Snowflake
    #: the stickers in the pack
    stickers: typing.List[Sticker]
    #: name of the sticker pack
    name: str
    #: id of the pack's SKU
    sku_id: Snowflake
    #: description of the sticker pack
    description: str
    #: id of the sticker pack's banner image
    banner_asset_id: Unknownish[Snowflake] = UNKNOWN
    #: id of a sticker in the pack which is shown as the pack's icon
    cover_sticker_id: Unknownish[Snowflake] = UNKNOWN


@attr.frozen(kw_only=True)
class NitroStickerPacks:
    #: the sticker packs included with nitro
    sticker_packs: typing.List[StickerPack]
