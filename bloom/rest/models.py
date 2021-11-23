# http models for bloom
from __future__ import annotations

import functools
import typing
from typing import Generic

import attr

from bloom._compat import Literal

ReturnT = typing.TypeVar('ReturnT')

if not typing.TYPE_CHECKING:
    # I'M VERY SORRY
    @attr.frozen()
    class GenericHolder:
        inner: object

    class Generic:  # noqa: F811
        __slots__ = ()

        def __class_getitem__(cls, item):
            if isinstance(item, typing.TypeVar):
                return cls
            else:
                return functools.partial(cls, GenericHolder(item))


@attr.frozen()
class Request(Generic[ReturnT]):
    if not typing.TYPE_CHECKING:
        # ugh there has to be a better way
        type_args: GenericHolder
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
