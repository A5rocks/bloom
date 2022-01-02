from __future__ import annotations

import datetime
import typing

import attr

from bloom.ll.models.base import UNKNOWN, Unknownish
from bloom.ll.models.user import User

# docs in this module are copied from the Discord Documentation


@attr.frozen(kw_only=True)
class AuthorizationInformation:
    # TODO: what does partial mean in this context?
    #: the current application
    application: typing.Dict[str, typing.Any]
    #: the scopes the user has authorized the application for
    scopes: typing.List[str]
    #: when the access token expires
    expires: datetime.datetime
    #: the user who has authorized, if the user has authorized with the
    #: identify scope
    user: Unknownish[User] = UNKNOWN
