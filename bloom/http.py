# http models for bloom
from __future__ import annotations

import typing

import attr

from ._compat import Literal


@attr.frozen(kw_only=True)
class Request:
    method: Literal['GET', 'POST', 'PATCH', 'DELETE']
    route: str
    args: typing.Dict[str, typing.Union[int, str]]

    params: typing.Optional[typing.Dict[str, typing.Any]] = None
    json: typing.Optional[typing.Dict[str, typing.Any]] = None

    @property
    def url(self) -> str:
        return self.route.format(**self.args)
