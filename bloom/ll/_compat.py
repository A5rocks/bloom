# internal compatibility module
from __future__ import annotations

import sys

if sys.version_info < (3, 8):
    import typing

    from typing_extensions import Literal, TypedDict

    def get_args(tp: object) -> typing.Tuple[object, ...]:
        # this implementation sucks but whatever (it's just a backport :^)
        if isinstance(tp, typing._Final):  # type: ignore[attr-defined]
            args: typing.Tuple[object, ...] = tp.__args__
            return args
        else:
            return ()

else:
    from typing import Literal, TypedDict, get_args

__all__ = ('TypedDict', 'Literal', 'get_args')
