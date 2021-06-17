# internal compatibility module
from __future__ import annotations

import sys

if sys.version_info < (3, 8):
    from typing_extensions import Literal, TypedDict
else:
    from typing import Literal, TypedDict

__all__ = ('TypedDict', 'Literal')
