from __future__ import annotations

import datetime as dt
import typing as t
from enum import Enum

import attr

from .base import UNKNOWN, Unknownish
from .user import User


@attr.frozen()
class Invite:
    #: the invite code (unique ID)
    code: str
    #: the channel this invite is for
    channel: t.Dict[str, object]
    #: the guild this invite is for
    guild: Unknownish[t.Dict[str, object]] = UNKNOWN
    #: the user who created the invite
    inviter: Unknownish[User] = UNKNOWN
    #: the type of target for this voice channel invite
    target_type: Unknownish[int] = UNKNOWN
    #: the user whose stream to display for this voice channel stream invite
    target_user: Unknownish[User] = UNKNOWN
    #: the embedded application to open for this voice channel embedded
    #: application invite
    target_application: Unknownish[t.Dict[str, object]] = UNKNOWN
    #: approximate count of online members, returned from the
    #: GET /invites/<code> endpoint when with_counts is true
    approximate_presence_count: Unknownish[int] = UNKNOWN
    #: approximate count of total members, returned from the
    #: GET /invites/<code> endpoint when with_counts is true
    approximate_member_count: Unknownish[int] = UNKNOWN
    #: the expiration date of this invite, returned from the
    #: GET /invites/<code> endpoint when with_expiration is true
    expires_at: Unknownish[t.Optional[dt.datetime]] = UNKNOWN
    #: stage instance data if there is a public Stage instance in the Stage
    #: channel this invite is for
    stage_instance: Unknownish[InviteStageInstance] = UNKNOWN


class InviteTargetTypes(Enum):
    STREAM = 1
    EMBEDDED_APPLICATION = 2


@attr.frozen()
class InviteMetadata:
    #: number of times this invite has been used
    uses: int
    #: max number of times this invite can be used
    max_uses: int
    #: duration (in seconds) after which the invite expires
    max_age: int
    #: whether this invite only grants temporary membership
    temporary: bool
    #: when this invite was created
    created_at: dt.datetime


@attr.frozen()
class InviteStageInstance:
    #: the members speaking in the Stage
    members: t.List[t.Dict[str, object]]
    #: the number of users in the Stage
    participant_count: int
    #: the number of users speaking in the Stage
    speaker_count: int
    #: the topic of the Stage instance (1-120 characters)
    topic: str
