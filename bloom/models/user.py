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
    #: the user's banner, or None if unset
    banner: Unknownish[t.Optional[str]] = UNKNOWN
    #: the user's banner color encoded as an integer representation of
    #: hexadecimal color code
    accent_color: Unknownish[t.Optional[int]] = UNKNOWN
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
    #: None
    NONE = 0
    #: Discord Employee
    STAFF = 1 << 0
    #: Partnered Server Owner
    PARTNER = 1 << 1
    #: HypeSquad Events Coordinator
    HYPESQUAD = 1 << 2
    #: Bug Hunter Level 1
    BUG_HUNTER_LEVEL_1 = 1 << 3
    #: House Bravery Member
    HYPESQUAD_ONLINE_HOUSE_1 = 1 << 6
    #: House Brilliance Member
    HYPESQUAD_ONLINE_HOUSE_2 = 1 << 7
    #: House Balance Member
    HYPESQUAD_ONLINE_HOUSE_3 = 1 << 8
    #: Early Nitro Supporter
    PREMIUM_EARLY_SUPPORTER = 1 << 9
    #: User is a team
    TEAM_PSEUDO_USER = 1 << 10
    #: Bug Hunter Level 2
    BUG_HUNTER_LEVEL_2 = 1 << 14
    #: Verified Bot
    VERIFIED_BOT = 1 << 16
    #: Early Verified Bot Developer
    VERIFIED_DEVELOPER = 1 << 17
    #: Discord Certified Moderator
    CERTIFIED_MODERATOR = 1 << 18
    #: Bot uses only HTTP interactions and is shown in the online members list
    BOT_HTTP_INTERACTIONS = 1 << 19


class PremiumTypes(IntEnum):
    NONE = 0
    NITRO_CLASSIC = 1
    NITRO = 2
