from __future__ import annotations

import enum
import typing

import attr

from bloom.ll.models.base import UNKNOWN, Snowflake, Unknownish

# docs in this module are copied from the Discord Documentation


# TODO: this should be serialized as a str :(
class BitwisePermissionFlags(enum.IntFlag):
    NONE = 0
    CREATE_INSTANT_INVITE = 1 << 0
    KICK_MEMBERS = 1 << 1
    BAN_MEMBERS = 1 << 2
    ADMINISTRATOR = 1 << 3
    MANAGE_CHANNELS = 1 << 4
    MANAGE_GUILD_ = 1 << 5
    ADD_REACTIONS = 1 << 6
    VIEW_AUDIT_LOG = 1 << 7
    PRIORITY_SPEAKER = 1 << 8
    STREAM = 1 << 9
    VIEW_CHANNEL = 1 << 10
    SEND_MESSAGES = 1 << 11
    SEND_TTS_MESSAGES = 1 << 12
    MANAGE_MESSAGES = 1 << 13
    EMBED_LINKS = 1 << 14
    ATTACH_FILES = 1 << 15
    READ_MESSAGE_HISTORY = 1 << 16
    MENTION_EVERYONE = 1 << 17
    USE_EXTERNAL_EMOJIS = 1 << 18
    VIEW_GUILD_INSIGHTS = 1 << 19
    CONNECT = 1 << 20
    SPEAK = 1 << 21
    MUTE_MEMBERS = 1 << 22
    DEAFEN_MEMBERS = 1 << 23
    MOVE_MEMBERS = 1 << 24
    USE_VAD = 1 << 25
    CHANGE_NICKNAME = 1 << 26
    MANAGE_NICKNAMES = 1 << 27
    MANAGE_ROLES = 1 << 28
    MANAGE_WEBHOOKS = 1 << 29
    MANAGE_EMOJIS_AND_STICKERS = 1 << 30
    USE_APPLICATION_COMMANDS = 1 << 31
    REQUEST_TO_SPEAK = 1 << 32
    MANAGE_EVENTS = 1 << 33
    MANAGE_THREADS_ = 1 << 34
    CREATE_PUBLIC_THREADS = 1 << 35
    CREATE_PRIVATE_THREADS = 1 << 36
    USE_EXTERNAL_STICKERS = 1 << 37
    SEND_MESSAGES_IN_THREADS = 1 << 38
    START_EMBEDDED_ACTIVITIES = 1 << 39
    MODERATE_MEMBERS = 1 << 40


@attr.frozen(kw_only=True)
class Role:
    #: role id
    id: Snowflake
    #: role name
    name: str
    #: integer representation of hexadecimal color code
    color: int
    #: if this role is pinned in the user listing
    hoist: bool
    #: role icon hash
    icon: Unknownish[typing.Optional[str]] = UNKNOWN
    #: role unicode emoji
    unicode_emoji: Unknownish[typing.Optional[str]] = UNKNOWN
    #: position of this role
    position: int
    #: permission bit set
    permissions: str
    #: whether this role is managed by an integration
    managed: bool
    #: whether this role is mentionable
    mentionable: bool
    #: the tags this role has
    tags: Unknownish[typing.Dict[str, typing.Any]] = UNKNOWN


@attr.frozen(kw_only=True)
class RoleTags:
    #: the id of the bot this role belongs to
    bot_id: Unknownish[Snowflake] = UNKNOWN
    #: the id of the integration this role belongs to
    integration_id: Unknownish[Snowflake] = UNKNOWN
    #: whether this is the guild's premium subscriber role
    premium_subscriber: Unknownish[None] = UNKNOWN
