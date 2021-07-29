from __future__ import annotations

import datetime as dt
import typing as t
from dataclasses import dataclass
from enum import Enum

from .base import UNKNOWN, Snowflake, Unknownish
from .user import User


class Oauth2Scopes(Enum):
    ACTIVITIES_READ = "allows your app to fetch data from a user’s “Now Playing/Recently Played” list - requires Discord approval"
    ACTIVITIES_WRITE = "allows your app to update a user’s activity - requires Discord approval (NOT REQUIRED FOR"
    APPLICATIONS_BUILDS_READ = (
        "allows your app to read build data for a user’s applications"
    )
    APPLICATIONS_BUILDS_UPLOAD = "allows your app to upload/update builds for a user’s applications - requires Discord approval"
    APPLICATIONS_COMMANDS = "allows your app to use"
    APPLICATIONS_COMMANDS_UPDATE = "allows your app to update its"
    APPLICATIONS_ENTITLEMENTS = (
        "allows your app to read entitlements for a user’s applications"
    )
    APPLICATIONS_STORE_UPDATE = "allows your app to read and update store data (SKUs, store listings, achievements, etc.) for a user’s applications"
    BOT = "for oauth2 bots, this puts the bot in the user’s selected guild by default"
    CONNECTIONS = "allows"
    EMAIL = "enables"
    GDM_JOIN = "allows your app to"
    GUILDS = "allows"
    GUILDS_JOIN = "allows"
    IDENTIFY = "allows"
    MESSAGES_READ = "for local rpc server api access, this allows you to read messages from all client channels (otherwise restricted to channels/guilds your app creates)"
    RELATIONSHIPS_READ = "allows your app to know a user’s friends and implicit relationships - requires Discord approval"
    RPC = "for local rpc server access, this allows you to control a user’s local Discord client - requires Discord approval"
    RPC_ACTIVITIES_WRITE = "for local rpc server access, this allows you to update a user’s activity - requires Discord approval"
    RPC_NOTIFICATIONS_READ = "for local rpc server access, this allows you to receive notifications pushed out to the user - requires Discord approval"
    RPC_VOICE_READ = "for local rpc server access, this allows you to read a user’s voice settings and listen for voice events - requires Discord approval"
    RPC_VOICE_WRITE = "for local rpc server access, this allows you to update a user’s voice settings - requires Discord approval"
    WEBHOOK_INCOMING = "this generates a webhook that is returned in the oauth token response for authorization code grants"


@dataclass()
class Response:
    #: the current application
    application: t.Dict[str, object]
    #: the scopes the user has authorized the application for
    scopes: t.List[str]
    #: when the access token expires
    expires: dt.datetime
    #: the user who has authorized, if the user has authorized with the identify scope
    user: Unknownish[User] = UNKNOWN
