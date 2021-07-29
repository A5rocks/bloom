from __future__ import annotations

import datetime as dt
import typing as t
from dataclasses import dataclass

from .base import UNKNOWN, Snowflake, Unknownish
from .user import User


@dataclass()
class GuildTemplate:
    #: the template code (unique ID)
    code: str
    #: template name
    name: str
    #: the description for the template
    description: t.Optional[str]
    #: number of times this template has been used
    usage_count: int
    #: the ID of the user who created the template
    creator_id: Snowflake
    #: the user who created the template
    creator: User
    #: when this template was created
    created_at: dt.datetime
    #: when this template was last synced to the source guild
    updated_at: dt.datetime
    #: the ID of the guild this template is based on
    source_guild_id: Snowflake
    #: the guild snapshot this template contains
    serialized_source_guild: t.Dict[str, object]
    #: whether the template has unsynced changes
    is_dirty: t.Optional[bool]
