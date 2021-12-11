from __future__ import annotations

import typing as t
from enum import Enum

import attr

from .base import Snowflake


@attr.frozen(kw_only=True)
class Team:
    #: a hash of the image of the team's icon
    icon: t.Optional[str]
    #: the unique id of the team
    id: Snowflake
    #: the members of the team
    members: t.List[TeamMember]
    #: the name of the team
    name: str
    #: the user id of the current team owner
    owner_user_id: Snowflake


@attr.frozen(kw_only=True)
class TeamMember:
    #: the user's membership state on the team
    membership_state: int
    #: will always be ["*"]
    permissions: t.List[str]
    #: the id of the parent team of which they are a member
    team_id: Snowflake
    #: the avatar, discriminator, id, and username of the user
    user: t.Dict[str, t.Any]


class MembershipState(Enum):
    INVITED = 1
    ACCEPTED = 2
