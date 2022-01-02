from __future__ import annotations

import datetime
import typing

import attr

from bloom.ll.models.base import Snowflake
from bloom.ll.models.user import User

# docs in this module are copied from the Discord Documentation


@attr.frozen(kw_only=True)
class GuildTemplate:
    #: the template code (unique ID)
    code: str
    #: template name
    name: str
    #: the description for the template
    description: typing.Optional[str]
    #: number of times this template has been used
    usage_count: int
    #: the ID of the user who created the template
    creator_id: Snowflake
    #: the user who created the template
    creator: User
    #: when this template was created
    created_at: datetime.datetime
    #: when this template was last synced to the source guild
    updated_at: datetime.datetime
    #: the ID of the guild this template is based on
    source_guild_id: Snowflake
    #: the guild snapshot this template contains
    serialized_source_guild: typing.Dict[str, typing.Any]
    #: whether the template has unsynced changes
    is_dirty: typing.Optional[bool]
