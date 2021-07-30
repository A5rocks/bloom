from __future__ import annotations

import typing as t
from enum import Enum

import attr

from .base import UNKNOWN, Snowflake, Unknownish
from .teams import Team


@attr.frozen(kw_only=True)
class Application:
    #: the id of the app
    id: Snowflake
    #: the name of the app
    name: str
    #: the icon hash of the app
    icon: t.Optional[str]
    #: the description of the app
    description: str
    #: when false only app owner can join the app's bot to guilds
    bot_public: bool
    #: when true the app's bot will only join upon completion of the full
    #: oauth2 code grant flow
    bot_require_code_grant: bool
    #: if this application is a game sold on Discord, this field will be the
    #: summary field for the store page of its primary sku
    summary: str
    #: the hex encoded key for verification in interactions and the GameSDK's
    #: GetTicket
    verify_key: str
    #: if the application belongs to a team, this will be a list of the
    #: members of that team
    team: t.Optional[Team]
    #: an array of rpc origin urls, if rpc is enabled
    rpc_origins: Unknownish[t.List[str]] = UNKNOWN
    #: the url of the app's terms of service
    terms_of_service_url: Unknownish[str] = UNKNOWN
    #: the url of the app's privacy policy
    privacy_policy_url: Unknownish[str] = UNKNOWN
    #: partial user object containing info on the owner of the application
    owner: Unknownish[t.Dict[str, t.Any]] = UNKNOWN
    #: if this application is a game sold on Discord, this field will be the
    #: guild to which it has been linked
    guild_id: Unknownish[Snowflake] = UNKNOWN
    #: if this application is a game sold on Discord, this field will be the
    #: id of the "Game SKU" that is created, if exists
    primary_sku_id: Unknownish[Snowflake] = UNKNOWN
    #: if this application is a game sold on Discord, this field will be the
    #: URL slug that links to the store page
    slug: Unknownish[str] = UNKNOWN
    #: the application's default rich presence invite cover image hash
    cover_image: Unknownish[str] = UNKNOWN
    #: the application's public flags
    flags: Unknownish[int] = UNKNOWN


class ApplicationFlags(Enum):
    GATEWAY_PRESENCE = 4096
    GATEWAY_PRESENCE_LIMITED = 8192
    GATEWAY_GUILD_MEMBERS = 16384
    GATEWAY_GUILD_MEMBERS_LIMITED = 32768
    VERIFICATION_PENDING_GUILD_LIMIT = 65536
    EMBEDDED = 131072
