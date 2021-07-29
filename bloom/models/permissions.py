from __future__ import annotations

import typing as t
from dataclasses import dataclass
from enum import Enum

from .base import UNKNOWN, Snowflake, Unknownish


class BitwisePermissionFlags(Enum):
    CREATE_INSTANT_INVITE = 1
    KICK_MEMBERS_ = 2
    BAN_MEMBERS_ = 4
    ADMINISTRATOR_ = 8
    MANAGE_CHANNELS_ = 16
    MANAGE_GUILD_ = 32
    ADD_REACTIONS = 64
    VIEW_AUDIT_LOG = 128
    PRIORITY_SPEAKER = 256
    STREAM = 512
    VIEW_CHANNEL = 1024
    SEND_MESSAGES = 2048
    SEND_TTS_MESSAGES = 4096
    MANAGE_MESSAGES_ = 8192
    EMBED_LINKS = 16384
    ATTACH_FILES = 32768
    READ_MESSAGE_HISTORY = 65536
    MENTION_EVERYONE = 131072
    USE_EXTERNAL_EMOJIS = 262144
    VIEW_GUILD_INSIGHTS = 524288
    CONNECT = 1048576
    SPEAK = 2097152
    MUTE_MEMBERS = 4194304
    DEAFEN_MEMBERS = 8388608
    MOVE_MEMBERS = 16777216
    USE_VAD = 33554432
    CHANGE_NICKNAME = 67108864
    MANAGE_NICKNAMES = 134217728
    MANAGE_ROLES_ = 268435456
    MANAGE_WEBHOOKS_ = 536870912
    MANAGE_EMOJIS_AND_STICKERS_ = 1073741824
    USE_SLASH_COMMANDS = 2147483648
    REQUEST_TO_SPEAK = 4294967296
    MANAGE_THREADS_ = 17179869184
    USE_PUBLIC_THREADS = 34359738368
    USE_PRIVATE_THREADS = 68719476736
    USE_EXTERNAL_STICKERS = 137438953472


@dataclass()
class Role:
    #: role id
    id: Snowflake
    #: role name
    name: str
    #: integer representation of hexadecimal color code
    color: int
    #: if this role is pinned in the user listing
    hoist: bool
    #: position of this role
    position: int
    #: permission bit set
    permissions: str
    #: whether this role is managed by an integration
    managed: bool
    #: whether this role is mentionable
    mentionable: bool
    #: the tags this role has
    tags: Unknownish[t.Dict[str, object]] = UNKNOWN


@dataclass()
class RoleTags:

    #: the id of the bot this role belongs to
    bot_id: Unknownish[Snowflake] = UNKNOWN
    #: the id of the integration this role belongs to
    integration_id: Unknownish[Snowflake] = UNKNOWN
    #: whether this is the guild's premium subscriber role
    premium_subscriber: Unknownish[None] = UNKNOWN
