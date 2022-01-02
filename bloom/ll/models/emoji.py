from __future__ import annotations

import typing

import attr

from bloom.ll.models.base import UNKNOWN, Snowflake, Unknownish
from bloom.ll.models.user import User

# docs in this module are copied from the Discord Documentation


@attr.frozen(kw_only=True)
class Emoji:
    #: emoji id
    id: typing.Optional[Snowflake]
    #: emoji name
    name: typing.Optional[str]
    #: roles allowed to use this emoji
    roles: Unknownish[typing.List[Snowflake]] = UNKNOWN
    #: user that created this emoji
    user: Unknownish[User] = UNKNOWN
    #: whether this emoji must be wrapped in colons
    require_colons: Unknownish[bool] = UNKNOWN
    #: whether this emoji is managed
    managed: Unknownish[bool] = UNKNOWN
    #: whether this emoji is animated
    animated: Unknownish[bool] = UNKNOWN
    #: whether this emoji can be used, may be false due to loss of Server
    #: Boosts
    available: Unknownish[bool] = UNKNOWN
