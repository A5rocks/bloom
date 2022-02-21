from __future__ import annotations

import datetime
import enum
import typing

import attr

from bloom.ll.models.base import UNKNOWN, Snowflake, Unknownish
from bloom.ll.models.user import User

# docs in this module are copied from the Discord Documentation


@attr.frozen(kw_only=True)
class GuildScheduledEvent:
    #: the id of the scheduled event
    id: Snowflake
    #: the guild id which the scheduled event belongs to
    guild_id: Snowflake
    #: the channel id in which the scheduled event will be hosted, or None if
    #: scheduled entity type is EXTERNAL
    channel_id: typing.Optional[Snowflake]
    #: the id of the user that created the scheduled event
    creator_id: Unknownish[typing.Optional[Snowflake]] = UNKNOWN
    #: the name of the scheduled event (1-100 characters)
    name: str
    #: the description of the scheduled event (1-1000 characters)
    description: str
    #: the time the scheduled event will start
    scheduled_start_time: datetime.datetime
    #: the time the scheduled event will end, required if entity_type is
    #: `EXTERNAL`
    scheduled_end_time: typing.Optional[datetime.datetime]
    #: the privacy level of the scheduled event
    privacy_level: GuildScheduledEventPrivacyLevel
    #: the status of the scheduled event
    status: EventStatus
    #: the type of the scheduled event
    entity_type: GuildScheduledEventEntityType
    #: the id of an entity associated with a guild scheduled event
    entity_id: typing.Optional[Snowflake]
    #: additional metadata for the guild scheduled event
    entity_metadata: typing.Optional[GuildScheduledEventEntityMetadata]
    #: the user that created the scheduled event
    creator: Unknownish[User] = UNKNOWN
    #: the number of users subscribed to the scheduled event
    user_count: Unknownish[int] = UNKNOWN
    #: the cover image hash of the scheduled event
    image: Unknownish[typing.Optional[str]] = UNKNOWN


class GuildScheduledEventPrivacyLevel(enum.IntEnum):
    #: the scheduled event is only accessible to guild members
    GUILD_ONLY = 2


class GuildScheduledEventEntityType(enum.IntEnum):
    STAGE_INSTANCE = 1
    VOICE = 2
    EXTERNAL = 3


class EventStatus(enum.IntEnum):
    SCHEDULED = 1
    ACTIVE = 2
    COMPLETED = 3
    CANCELED = 4


@attr.frozen(kw_only=True)
class GuildScheduledEventEntityMetadata:
    #: location of the event (1-100 characters)
    location: Unknownish[str] = UNKNOWN
