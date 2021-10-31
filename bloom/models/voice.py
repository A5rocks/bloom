from __future__ import annotations

import typing as t
from datetime import datetime

import attr

from .base import UNKNOWN, Snowflake, Unknownish
from .guild import GuildMember


@attr.frozen(kw_only=True)
class VoiceState:
    #: the channel id this user is connected to
    channel_id: t.Optional[Snowflake]
    #: the user id this voice state is for
    user_id: Snowflake
    #: the session id for this voice state
    session_id: str
    #: whether this user is deafened by the server
    deaf: bool
    #: whether this user is muted by the server
    mute: bool
    #: whether this user is locally deafened
    self_deaf: bool
    #: whether this user is locally muted
    self_mute: bool
    #: whether this user's camera is enabled
    self_video: bool
    #: whether this user is muted by the current user
    suppress: bool
    #: the time at which the user requested to speak
    request_to_speak_timestamp: t.Optional[datetime]
    #: the guild id this voice state is for
    guild_id: Unknownish[Snowflake] = UNKNOWN
    #: the guild member this voice state is for
    member: Unknownish[GuildMember] = UNKNOWN
    #: whether this user is streaming using "Go Live"
    self_stream: Unknownish[bool] = UNKNOWN


@attr.frozen(kw_only=True)
class VoiceRegion:
    #: unique ID for the region
    id: str
    #: name of the region
    name: str
    #: true for a single server that is closest to the current user's client
    optimal: bool
    #: whether this is a deprecated voice region (avoid switching to these)
    deprecated: bool
    #: whether this is a custom voice region (used for events/etc)
    custom: bool
