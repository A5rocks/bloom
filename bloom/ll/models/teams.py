from __future__ import annotations

import enum
import typing

import attr

from bloom.ll.models.base import Snowflake

# docs in this module are copied from the Discord Documentation


@attr.frozen(kw_only=True)
class Team:
    #: a hash of the image of the team's icon
    icon: typing.Optional[str]
    #: the unique id of the team
    id: Snowflake
    #: the members of the team
    members: typing.List[TeamMember]
    #: the name of the team
    name: str
    #: the user id of the current team owner
    owner_user_id: Snowflake


@attr.frozen(kw_only=True)
class TeamMember:
    #: the user's membership state on the team
    membership_state: int
    #: will always be ["*"]
    permissions: typing.List[str]
    #: the id of the parent team of which they are a member
    team_id: Snowflake
    #: the avatar, discriminator, id, and username of the user
    user: typing.Dict[str, typing.Any]


class MembershipState(enum.Enum):
    INVITED = 1
    ACCEPTED = 2
