from __future__ import annotations

import enum

import attr

from bloom.ll.models.base import Snowflake

# docs in this module are copied from the Discord Documentation


@attr.frozen(kw_only=True)
class StageInstance:
    #: The id of this Stage instance
    id: Snowflake
    #: The guild id of the associated Stage channel
    guild_id: Snowflake
    #: The id of the associated Stage channel
    channel_id: Snowflake
    #: The topic of the Stage instance (1-120 characters)
    topic: str
    #: The privacy level of the Stage instance
    privacy_level: PrivacyLevel
    #: Whether or not Stage Discovery is disabled (deprecated)
    discoverable_disabled: bool


class PrivacyLevel(enum.IntEnum):
    #: The Stage instance is visible publicly, such as on Stage Discovery.
    PUBLIC = 1
    #: The Stage instance is visible to only guild members.
    GUILD_ONLY = 2
