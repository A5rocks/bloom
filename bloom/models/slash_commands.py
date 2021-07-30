from __future__ import annotations

import typing as t
from enum import Enum

import attr

from .base import UNKNOWN, Snowflake, Unknownish
from .channel import AllowedMentions, Embed
from .message_components import Component
from .user import User


@attr.frozen()
class ApplicationCommand:
    #: unique id of the command
    id: Snowflake
    #: unique id of the parent application
    application_id: Snowflake
    #: 1-32 lowercase character name matching ^[\w-]{1,32}$
    name: str
    #: 1-100 character description
    description: str
    #: guild id of the command, if not global
    guild_id: Unknownish[Snowflake] = UNKNOWN
    #: the parameters for the command
    options: Unknownish[t.List[ApplicationCommandOption]] = UNKNOWN
    #: whether the command is enabled by default when the app is added to a
    #: guild
    default_permission: Unknownish[bool] = UNKNOWN


@attr.frozen()
class ApplicationCommandOption:
    #: value of application command option type
    type: int
    #: 1-32 lowercase character name matching ^[\w-]{1,32}$
    name: str
    #: 1-100 character description
    description: str
    #: if the parameter is required or optional–default false
    required: Unknownish[bool] = UNKNOWN
    #: choices for STRING, INTEGER, and NUMBER types for the user to pick from
    choices: Unknownish[t.List[ApplicationCommandOptionChoice]] = UNKNOWN
    #: if the option is a subcommand or subcommand group type, this nested
    #: options will be the parameters
    options: Unknownish[t.List[ApplicationCommandOption]] = UNKNOWN


class ApplicationCommandOptionType(Enum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    #: Any integer between -2^53 and 2^53
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    #: Includes all channel types + categories
    CHANNEL = 7
    ROLE = 8
    #: Includes users and roles
    MENTIONABLE = 9
    #: Any double between -2^53 and 2^53
    NUMBER = 10


@attr.frozen()
class ApplicationCommandOptionChoice:
    #: 1-100 character choice name
    name: str
    #: value of the choice, up to 100 characters if string
    value: t.Union[str, int, float]


@attr.frozen()
class GuildApplicationCommandPermissions:
    #: the id of the command
    id: Snowflake
    #: the id of the application the command belongs to
    application_id: Snowflake
    #: the id of the guild
    guild_id: Snowflake
    #: the permissions for the command in the guild
    permissions: t.List[ApplicationCommandPermissions]


@attr.frozen()
class ApplicationCommandPermissions:
    #: the id of the role or user
    id: Snowflake
    #: role or user
    type: ApplicationCommandPermissionType
    #: true to allow, false, to disallow
    permission: bool


class ApplicationCommandPermissionType(Enum):
    ROLE = 1
    USER = 2


class InteractionRequestType(Enum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3


@attr.frozen()
class ApplicationCommandInteractionData:
    #: the ID of the invoked command
    id: Snowflake
    #: the name of the invoked command
    name: str
    #: for components, the  of the component
    custom_id: str
    #: for components, the type of the component
    component_type: int
    #: converted users + roles + channels
    resolved: Unknownish[ApplicationCommandInteractionDataResolved] = UNKNOWN
    #: the params + values from the user
    options: Unknownish[t.List[ApplicationCommandInteractionDataOption]] = UNKNOWN


@attr.frozen()
class ApplicationCommandInteractionDataResolved:
    #: the ids and partial Member objects
    members: t.Dict[str, object]
    #: the ids and partial Channel objects
    channels: t.Dict[str, object]
    #: the ids and User objects
    users: Unknownish[t.Dict[str, object]] = UNKNOWN
    #: the ids and Role objects
    roles: Unknownish[t.Dict[str, object]] = UNKNOWN


@attr.frozen()
class ApplicationCommandInteractionDataOption:
    #: the name of the parameter
    name: str
    #: value of application command option type
    type: ApplicationCommandOptionType
    #: the value of the pair
    value: Unknownish[object] = UNKNOWN
    #: present if this option is a group or subcommand
    options: Unknownish[t.List[ApplicationCommandInteractionDataOption]] = UNKNOWN


@attr.frozen()
class InteractionResponse:
    #: the type of response
    type: InteractionCallbackType
    #: an optional response message
    data: Unknownish[InteractionApplicationCommandCallbackData] = UNKNOWN


class InteractionCallbackType(Enum):
    #: ACK a Ping
    PONG = 1
    #: respond to an interaction with a message
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    #: ACK an interaction and edit a response later, the user sees a loading
    #: state
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    #: for components, ACK an interaction and edit the original message later;
    #: the user does not see a loading state
    DEFERRED_UPDATE_MESSAGE = 6
    #: for components, edit the message the component was attached to
    UPDATE_MESSAGE = 7


@attr.frozen()
class InteractionApplicationCommandCallbackData:

    #: is the response TTS
    tts: Unknownish[bool] = UNKNOWN
    #: message content
    content: Unknownish[str] = UNKNOWN
    #: supports up to 10 embeds
    embeds: Unknownish[t.List[Embed]] = UNKNOWN
    #: allowed mentions object
    allowed_mentions: Unknownish[AllowedMentions] = UNKNOWN
    #: interaction application command callback data flags
    flags: Unknownish[int] = UNKNOWN
    #: message components
    components: Unknownish[t.List[Component]] = UNKNOWN


class InteractionApplicationCommandCallbackDataFlags(Enum):
    #: only the user receiving the message can see it
    EPHEMERAL = 64


@attr.frozen()
class MessageInteraction:
    #: id of the interaction
    id: Snowflake
    #: the type of interaction
    type: InteractionRequestType
    #: the name of the application command
    name: str
    #: the user who invoked the interaction
    user: User