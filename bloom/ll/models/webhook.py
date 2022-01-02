from __future__ import annotations

import enum
import typing

import attr

from bloom.ll.models.base import UNKNOWN, Snowflake, Unknownish
from bloom.ll.models.user import User

# docs in this module are copied from the Discord Documentation


@attr.frozen(kw_only=True)
class Webhook:
    #: the id of the webhook
    id: Snowflake
    #: the type of the webhook
    type: int
    #: the channel id this webhook is for, if any
    channel_id: typing.Optional[Snowflake]
    #: the default name of the webhook
    name: typing.Optional[str]
    #: the default user avatar hash of the webhook
    avatar: typing.Optional[str]
    #: the bot/OAuth2 application that created this webhook
    application_id: typing.Optional[Snowflake]
    #: the guild id this webhook is for, if any
    guild_id: Unknownish[typing.Optional[Snowflake]] = UNKNOWN
    #: the user this webhook was created by (not returned when getting a
    #: webhook with its token)
    user: Unknownish[User] = UNKNOWN
    #: the secure token of the webhook (returned for Incoming Webhooks)
    token: Unknownish[str] = UNKNOWN
    #: the guild of the channel that this webhook is following (returned for
    #: Channel Follower Webhooks)
    source_guild: Unknownish[typing.Dict[str, typing.Any]] = UNKNOWN
    #: the channel that this webhook is following (returned for Channel
    #: Follower Webhooks)
    source_channel: Unknownish[typing.Dict[str, typing.Any]] = UNKNOWN
    #: the url used for executing the webhook (returned by the webhooks OAuth2
    #: flow)
    url: Unknownish[str] = UNKNOWN


class WebhookTypes(enum.Enum):
    #: Incoming Webhooks can post messages to channels with a generated token
    INCOMING = 1
    #: Channel Follower Webhooks are internal webhooks used with Channel
    #: Following to post new messages into channels
    CHANNEL_FOLLOWER = 2
    #: Application webhooks are webhooks used with Interactions
    APPLICATION = 3
