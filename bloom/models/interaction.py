from __future__ import annotations

from dataclasses import dataclass

from .base import UNKNOWN, Snowflake, Unknownish
from .guild import GuildMember
from .message import Message
from .slash_commands import (ApplicationCommandInteractionData,
                             InteractionRequestType)
from .user import User


@dataclass()
class Interaction:
    #: id of the interaction
    id: Snowflake
    #: id of the application this interaction is for
    application_id: Snowflake
    #: the type of interaction
    type: InteractionRequestType
    #: the command data payload
    data: ApplicationCommandInteractionData
    #: guild member data for the invoking user, including permissions
    member: GuildMember
    #: a continuation token for responding to the interaction
    token: str
    #: read-only property, always 1
    version: int
    #: the guild it was sent from
    guild_id: Unknownish[Snowflake] = UNKNOWN
    #: the channel it was sent from
    channel_id: Unknownish[Snowflake] = UNKNOWN
    #: user object for the invoking user, if invoked in a DM
    user: Unknownish[User] = UNKNOWN
    #: for components, the message they were attached to
    message: Unknownish[Message] = UNKNOWN
