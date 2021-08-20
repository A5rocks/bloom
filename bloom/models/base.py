import typing


class UNKNOWN_TYPE:
    pass


T = typing.TypeVar('T')

UNKNOWN = UNKNOWN_TYPE()
Unknownish = typing.Union[UNKNOWN_TYPE, T]

# TODO: this should serialize as a str
Snowflake = typing.NewType('Snowflake', int)
