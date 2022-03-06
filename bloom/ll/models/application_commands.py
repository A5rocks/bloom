from __future__ import annotations

import enum
import typing

import attr

from bloom.ll.models.base import UNKNOWN, Snowflake, Unknownish
from bloom.ll.models.channel import AllowedMentions, Attachment, ChannelTypes, Embed
from bloom.ll.models.message_components import Component, SelectOption
from bloom.ll.models.permissions import Role
from bloom.ll.models.user import User

# docs in this module are copied from the Discord Documentation


@attr.frozen(kw_only=True)
class ApplicationCommand:
    #: unique id of the command
    id: Snowflake
    #: unique id of the parent application
    application_id: Snowflake
    #: 1-32 lowercase character name matching ^[\w-]{1,32}$ if this is a
    #: CHAT_INPUT command, else 1-32 chars.
    name: str
    #: 1-100 character description
    description: str
    #: autoincrementing version identifier updated during substantial record
    #: changes
    version: Snowflake
    #: guild id of the command, if not global
    guild_id: Unknownish[Snowflake] = UNKNOWN
    #: the parameters for the command (this is only on CHAT_INPUT commands)
    options: Unknownish[typing.List[ApplicationCommandOption]] = UNKNOWN
    #: whether the command is enabled by default when the app is added to a
    #: guild
    default_permission: Unknownish[bool] = UNKNOWN
    #: the type of the application command
    type: Unknownish[CommandTypes] = UNKNOWN


class CommandTypes(enum.Enum):
    #: Slash commands; a text-based command that shows up when a user types
    #: `/`
    CHAT_INPUT = 1
    #: A UI-based command that shows up when you right click or tap on a user
    USER = 2
    #: A UI-based command that shows up when you right click or tap on a
    #: message
    MESSAGE = 3


@attr.frozen(kw_only=True)
class ApplicationCommandOption:
    #: value of application command option type
    type: ApplicationCommandOptionType
    #: 1-32 lowercase character name matching ^[\w-]{1,32}$
    name: str
    #: 1-100 character description
    description: str
    #: if the parameter is required or optional–default false
    required: Unknownish[bool] = UNKNOWN
    #: choices for STRING, INTEGER, and NUMBER types for the user to pick from
    choices: Unknownish[typing.List[ApplicationCommandOptionChoice]] = UNKNOWN
    #: if autocomplete interactions are enabled for this `STRING`, `INTEGER`,
    #: or `NUMBER` type option. Note that this cannot be True if choices is
    #: present, and that options using autocomplete are not confined to only
    #: use choices given by the application.
    autocomplete: Unknownish[bool] = UNKNOWN
    #: if the option is a subcommand or subcommand group type, this nested
    #: options will be the parameters
    options: Unknownish[typing.List[ApplicationCommandOption]] = UNKNOWN
    #: if the option is a channel type, the channels shown will be restricted
    #: to these types
    channel_types: Unknownish[typing.List[ChannelTypes]] = UNKNOWN
    #: if the option is an `INTEGER` or `NUMBER` type, the minimum value
    #: permitted
    min_value: Unknownish[float] = UNKNOWN
    #: if the option is an `INTEGER` or `NUMBER` type, the maximum value
    #: permitted
    max_value: Unknownish[float] = UNKNOWN


class ApplicationCommandOptionType(enum.Enum):
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
    #: attachment object
    ATTACHMENT = 11


@attr.frozen(kw_only=True)
class ApplicationCommandOptionChoice:
    #: 1-100 character choice name
    name: str
    #: value of the choice, up to 100 characters if string
    value: typing.Union[str, int, float]


@attr.frozen(kw_only=True)
class GuildApplicationCommandPermissions:
    #: the id of the command
    id: Snowflake
    #: the id of the application the command belongs to
    application_id: Snowflake
    #: the id of the guild
    guild_id: Snowflake
    #: the permissions for the command in the guild
    permissions: typing.List[ApplicationCommandPermissions]


@attr.frozen(kw_only=True)
class ApplicationCommandPermissions:
    #: the id of the role or user
    id: Snowflake
    #: role or user
    type: ApplicationCommandPermissionType
    #: true to allow, false, to disallow
    permission: bool


class ApplicationCommandPermissionType(enum.Enum):
    ROLE = 1
    USER = 2


class InteractionType(enum.Enum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4


@attr.frozen(kw_only=True)
class ApplicationCommandInteractionData:
    # TODO: adt
    #: the ID of the invoked command
    id: Unknownish[Snowflake] = UNKNOWN
    #: the name of the invoked command
    name: Unknownish[str] = UNKNOWN
    #: the type of the invoked command
    # TODO: flag
    type: Unknownish[int] = UNKNOWN
    #: for components, the custom_id of the component
    custom_id: Unknownish[str] = UNKNOWN
    #: for components, the type of the component
    component_type: Unknownish[int] = UNKNOWN
    #: converted users + roles + channels + attachments
    resolved: Unknownish[ApplicationCommandInteractionDataResolved] = UNKNOWN
    #: the params + values from the user
    options: Unknownish[typing.List[ApplicationCommandInteractionDataOption]] = UNKNOWN
    #: the values the user selected
    values: Unknownish[typing.List[SelectOption]] = UNKNOWN
    #: id the of user or message targeted by a user or message command
    target_id: Unknownish[Snowflake] = UNKNOWN


@attr.frozen(kw_only=True)
class ApplicationCommandInteractionDataResolved:
    #: the ids and partial Member objects
    members: Unknownish[typing.Dict[str, typing.Any]]
    #: the ids and partial Channel objects
    channels: Unknownish[typing.Dict[str, typing.Any]]
    #: the ids and User objects
    users: Unknownish[typing.Dict[str, User]] = UNKNOWN
    #: the ids and Role objects
    roles: Unknownish[typing.Dict[str, Role]] = UNKNOWN
    #: the ids and partial Message objects
    messages: Unknownish[typing.Dict[str, typing.Any]] = UNKNOWN
    #: the ids and attachment objects
    attachments: Unknownish[typing.Dict[str, Attachment]]


@attr.frozen(kw_only=True)
class ApplicationCommandInteractionDataOption:
    #: the name of the parameter
    name: str
    #: value of application command option type
    type: ApplicationCommandOptionType
    #: the value of the option resulting from user input
    value: Unknownish[typing.Union[str, int, float]] = UNKNOWN
    #: present if this option is a group or subcommand
    options: Unknownish[typing.List[ApplicationCommandInteractionDataOption]] = UNKNOWN
    #: true if this option is the currently focused option for autocomplete
    focused: Unknownish[bool] = UNKNOWN


@attr.frozen(kw_only=True)
class InteractionResponse:
    #: the type of response
    type: InteractionCallbackType
    #: an optional response message
    data: Unknownish[InteractionApplicationCommandCallbackData] = UNKNOWN


class InteractionCallbackType(enum.Enum):
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
    #: respond to an autocomplete interaction with (up to 25) suggested
    #: choices
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8


@attr.frozen(kw_only=True)
class InteractionApplicationCommandCallbackData:
    #: is the response TTS
    tts: Unknownish[bool] = UNKNOWN
    #: message content
    content: Unknownish[str] = UNKNOWN
    #: supports up to 10 embeds
    embeds: Unknownish[typing.List[Embed]] = UNKNOWN
    #: allowed mentions object
    allowed_mentions: Unknownish[AllowedMentions] = UNKNOWN
    #: message flags combined as a bitfield (only SUPPRESS_EMBEDS and
    #: EPHEMERAL can be set)
    flags: Unknownish[int] = UNKNOWN
    #: message components
    components: Unknownish[typing.List[Component]] = UNKNOWN
    # TODO: partial attachments
    #: attachment objects with filename and description
    attachments: Unknownish[typing.List[typing.Dict[str, typing.Any]]] = UNKNOWN


class InteractionApplicationCommandCallbackDataFlags(enum.Enum):
    #: only the user receiving the message can see it
    EPHEMERAL = 64


@attr.frozen(kw_only=True)
class MessageInteraction:
    #: id of the interaction
    id: Snowflake
    #: the type of interaction
    type: InteractionType
    #: the name of the application command
    name: str
    #: the user who invoked the interaction
    user: User
    #: the member who invoked the interaction in the guild
    # TODO: partial member
    member: Unknownish[typing.Dict[str, typing.Any]] = UNKNOWN
