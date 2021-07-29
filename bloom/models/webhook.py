from __future__ import annotations

import typing as t
from dataclasses import dataclass
from enum import Enum

from .base import UNKNOWN, Snowflake, Unknownish
from .user import User


@dataclass()
class Webhook:
    #: the id of the webhook
    id: Snowflake
    #: the type of the webhook
    type: int
    #: the channel id this webhook is for, if any
    channel_id: t.Optional[Snowflake]
    #: the default name of the webhook
    name: t.Optional[str]
    #: the default user avatar hash of the webhook
    avatar: t.Optional[str]
    #: the bot/OAuth2 application that created this webhook
    application_id: t.Optional[Snowflake]
    #: the guild id this webhook is for, if any
    guild_id: Unknownish[t.Optional[Snowflake]] = UNKNOWN
    #: the user this webhook was created by (not returned when getting a webhook with its token)
    user: Unknownish[User] = UNKNOWN
    #: the secure token of the webhook (returned for Incoming Webhooks)
    token: Unknownish[str] = UNKNOWN
    #: the guild of the channel that this webhook is following (returned for Channel Follower Webhooks)
    source_guild: Unknownish[t.Dict[str, object]] = UNKNOWN
    #: the channel that this webhook is following (returned for Channel Follower Webhooks)
    source_channel: Unknownish[t.Dict[str, object]] = UNKNOWN
    #: the url used for executing the webhook (returned by the webhooks OAuth2 flow)
    url: Unknownish[str] = UNKNOWN


class WebhookTypes(Enum):
    #: Incoming Webhooks can post messages to channels with a generated token
    INCOMING = 1
    #: Channel Follower Webhooks are internal webhooks used with Channel Following to post new messages into channels
    CHANNEL_FOLLOWER = 2
    #: Application webhooks are webhooks used with Interactions
    APPLICATION = 3
