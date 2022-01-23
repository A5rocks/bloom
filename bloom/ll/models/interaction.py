from __future__ import annotations

import attr

from bloom.ll.models.application_commands import ApplicationCommandInteractionData, InteractionType
from bloom.ll.models.base import UNKNOWN, Snowflake, Unknownish
from bloom.ll.models.guild import GuildMember
from bloom.ll.models.message import Message
from bloom.ll.models.user import User

# docs in this module are copied from the Discord Documentation


@attr.frozen(kw_only=True)
class Interaction:
    #: id of the interaction
    id: Snowflake
    #: id of the application this interaction is for
    application_id: Snowflake
    #: the type of interaction
    type: InteractionType
    #: the command data payload
    data: Unknownish[ApplicationCommandInteractionData] = UNKNOWN
    #: guild member data for the invoking user, including permissions
    member: Unknownish[GuildMember] = UNKNOWN
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
    #: the selected language of the invoking user (not available in PING),
    #: this is an IETF language tag composed of a 2 letter country code and
    #: occasionally a region code.
    locale: Unknownish[str] = UNKNOWN
    #: the guild's preferred locale, if invoked in a guild (defaults to en-US)
    guild_locale: Unknownish[str] = UNKNOWN
