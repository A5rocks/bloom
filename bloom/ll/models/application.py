from __future__ import annotations

import enum
import typing

import attr

from bloom.ll.models.base import UNKNOWN, Snowflake, Unknownish
from bloom.ll.models.teams import Team

# docs in this module are copied from the Discord Documentation


@attr.frozen(kw_only=True)
class Application:
    #: the id of the app
    id: Snowflake
    #: the name of the app
    name: str
    #: the icon hash of the app
    icon: typing.Optional[str]
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
    team: typing.Optional[Team]
    #: an array of rpc origin urls, if rpc is enabled
    rpc_origins: Unknownish[typing.List[str]] = UNKNOWN
    #: the url of the app's terms of service
    terms_of_service_url: Unknownish[str] = UNKNOWN
    #: the url of the app's privacy policy
    privacy_policy_url: Unknownish[str] = UNKNOWN
    #: partial user object containing info on the owner of the application
    owner: Unknownish[typing.Dict[str, typing.Any]] = UNKNOWN
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


class ApplicationFlags(enum.IntFlag):
    GATEWAY_PRESENCE = 1 << 12
    GATEWAY_PRESENCE_LIMITED = 1 << 13
    GATEWAY_GUILD_MEMBERS = 1 << 14
    GATEWAY_GUILD_MEMBERS_LIMITED = 1 << 15
    VERIFICATION_PENDING_GUILD_LIMIT = 1 << 16
    EMBEDDED = 1 << 17
    GATEWAY_MESSAGE_CONTENT = 1 << 18
    GATEWAY_MESSAGE_CONTENT_LIMITED = 1 << 19
