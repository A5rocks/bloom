# http models for bloom
from __future__ import annotations

import typing

import attr

from bloom._compat import Literal


@attr.frozen()
class Request:
    method: Literal['GET', 'POST', 'PATCH', 'DELETE', 'PUT']
    route: str
    args: typing.Dict[str, typing.Union[int, str]]

    params: typing.Optional[typing.Dict[str, typing.Any]] = None
    json: typing.Optional[typing.Dict[str, typing.Any]] = None
    headers: typing.Optional[typing.Dict[str, typing.Any]] = None
    data: typing.Optional[typing.Dict[str, typing.Any]] = None
    # TODO: better file type?
    files: typing.Optional[typing.Dict[str, object]] = None

    @property
    def url(self) -> str:
        return self.route.format(**self.args)
