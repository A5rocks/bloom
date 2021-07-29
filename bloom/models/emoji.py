from __future__ import annotations

import typing as t
from dataclasses import dataclass

from .base import UNKNOWN, Snowflake, Unknownish
from .user import User


@dataclass()
class Emoji:
    #: emoji id
    id: t.Optional[Snowflake]
    #: emoji name
    name: t.Optional[str]
    #: roles allowed to use this emoji
    roles: Unknownish[t.List[Snowflake]] = UNKNOWN
    #: user that created this emoji
    user: Unknownish[User] = UNKNOWN
    #: whether this emoji must be wrapped in colons
    require_colons: Unknownish[bool] = UNKNOWN
    #: whether this emoji is managed
    managed: Unknownish[bool] = UNKNOWN
    #: whether this emoji is animated
    animated: Unknownish[bool] = UNKNOWN
    #: whether this emoji can be used, may be false due to loss of Server Boosts
    available: Unknownish[bool] = UNKNOWN
