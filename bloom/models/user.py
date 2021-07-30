from __future__ import annotations

import typing as t
from enum import IntEnum, IntFlag

import attr

from .base import UNKNOWN, Snowflake, Unknownish


@attr.frozen(kw_only=True)
class User:
    #: the user's id
    id: Snowflake
    #: the user's username, not unique across the platform
    username: str
    #: the user's 4-digit discord-tag
    discriminator: str
    #: the user's avatar hash
    avatar: t.Optional[str]
    #: whether the user belongs to an OAuth2 application
    bot: Unknownish[bool] = UNKNOWN
    #: whether the user is an Official Discord System user (part of the urgent
    #: message system)
    system: Unknownish[bool] = UNKNOWN
    #: whether the user has two factor enabled on their account
    mfa_enabled: Unknownish[bool] = UNKNOWN
    #: the user's chosen language option
    locale: Unknownish[str] = UNKNOWN
    #: whether the email on this account has been verified
    verified: Unknownish[bool] = UNKNOWN
    #: the user's email
    email: Unknownish[t.Optional[str]] = UNKNOWN
    #: the flags on a user's account
    flags: Unknownish[UserFlags] = UNKNOWN
    #: the type of Nitro subscription on a user's account
    premium_type: Unknownish[PremiumTypes] = UNKNOWN
    #: the public flags on a user's account
    public_flags: Unknownish[UserFlags] = UNKNOWN


class UserFlags(IntFlag):
    NONE = 0
    DISCORD_EMPLOYEE = 1
    PARTNERED_SERVER_OWNER = 2
    HYPESQUAD_EVENTS = 4
    BUG_HUNTER_LEVEL_1 = 8
    HOUSE_BRAVERY = 64
    HOUSE_BRILLIANCE = 128
    HOUSE_BALANCE = 256
    EARLY_SUPPORTER = 512
    TEAM_USER = 1024
    BUG_HUNTER_LEVEL_2 = 16384
    VERIFIED_BOT = 65536
    EARLY_VERIFIED_BOT_DEVELOPER = 131072
    DISCORD_CERTIFIED_MODERATOR = 262144


class PremiumTypes(IntEnum):
    NONE = 0
    NITRO_CLASSIC = 1
    NITRO = 2
