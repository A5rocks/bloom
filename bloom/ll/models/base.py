import typing

import cattr


class UNKNOWN_TYPE:
    pass


T = typing.TypeVar('T')

UNKNOWN = UNKNOWN_TYPE()
Unknownish = typing.Union[UNKNOWN_TYPE, T]


class Snowflake(int):
    pass


def setup_cattrs(converter: cattr.Converter) -> None:
    # mypy cannot infer :(
    def unstructure_snowflake(struct: Snowflake) -> str:
        return str(struct)

    converter.register_unstructure_hook(Snowflake, unstructure_snowflake)
