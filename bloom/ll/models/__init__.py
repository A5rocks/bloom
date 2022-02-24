import cattr

import bloom.ll.models.base as base
import bloom.ll.models.message_components as message_components


def setup_cattrs(converter: cattr.Converter) -> None:
    message_components.setup_cattrs(converter)
    base.setup_cattrs(converter)
