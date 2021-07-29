from __future__ import annotations

import datetime as dt
import typing as t

import attr

from .base import UNKNOWN, Unknownish
from .user import User


@attr.frozen()
class Response:
    #: the current application
    application: t.Dict[str, object]
    #: the scopes the user has authorized the application for
    scopes: t.List[str]
    #: when the access token expires
    expires: dt.datetime
    #: the user who has authorized, if the user has authorized with the
    #: identify scope
    user: Unknownish[User] = UNKNOWN
