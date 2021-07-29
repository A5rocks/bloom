import typing


class UNKNOWN:
    pass


T = typing.TypeVar("T")

Unknownish = typing.Union[typing.Type[UNKNOWN], T]

Snowflake = typing.NewType("Snowflake", int)
