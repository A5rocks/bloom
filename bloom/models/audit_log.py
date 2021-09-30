from __future__ import annotations

import typing as t
from enum import Enum

import attr

from .base import UNKNOWN, Snowflake, Unknownish
from .channel import Channel
from .user import User
from .webhook import Webhook


@attr.frozen(kw_only=True)
class AuditLog:
    #: list of webhooks found in the audit log
    webhooks: t.List[Webhook]
    #: list of users found in the audit log
    users: t.List[User]
    #: list of audit log entries
    audit_log_entries: t.List[AuditLogEntry]
    # TODO: investigate this partial
    #: list of partial integration objects
    integrations: t.List[t.Dict[str, t.Any]]
    #: list of threads in the audit log
    threads: t.List[Channel]


@attr.frozen(kw_only=True)
class AuditLogEntry:
    #: id of the affected entity (webhook, user, role, etc.)
    target_id: t.Optional[str]
    #: the user who made the changes
    user_id: t.Optional[Snowflake]
    #: id of the entry
    id: Snowflake
    #: type of action that occurred
    action_type: AuditLogEvents
    #: changes made to the target_id
    changes: Unknownish[t.List[AuditLogChange]] = UNKNOWN
    #: additional info for certain action types
    options: Unknownish[OptionalAuditEntryInfo] = UNKNOWN
    #: the reason for the change (0-512 characters)
    reason: Unknownish[str] = UNKNOWN


class AuditLogEvents(Enum):
    GUILD_UPDATE = 1
    CHANNEL_CREATE = 10
    CHANNEL_UPDATE = 11
    CHANNEL_DELETE = 12
    CHANNEL_OVERWRITE_CREATE = 13
    CHANNEL_OVERWRITE_UPDATE = 14
    CHANNEL_OVERWRITE_DELETE = 15
    MEMBER_KICK = 20
    MEMBER_PRUNE = 21
    MEMBER_BAN_ADD = 22
    MEMBER_BAN_REMOVE = 23
    MEMBER_UPDATE = 24
    MEMBER_ROLE_UPDATE = 25
    MEMBER_MOVE = 26
    MEMBER_DISCONNECT = 27
    BOT_ADD = 28
    ROLE_CREATE = 30
    ROLE_UPDATE = 31
    ROLE_DELETE = 32
    INVITE_CREATE = 40
    INVITE_UPDATE = 41
    INVITE_DELETE = 42
    WEBHOOK_CREATE = 50
    WEBHOOK_UPDATE = 51
    WEBHOOK_DELETE = 52
    EMOJI_CREATE = 60
    EMOJI_UPDATE = 61
    EMOJI_DELETE = 62
    MESSAGE_DELETE = 72
    MESSAGE_BULK_DELETE = 73
    MESSAGE_PIN = 74
    MESSAGE_UNPIN = 75
    INTEGRATION_CREATE = 80
    INTEGRATION_UPDATE = 81
    INTEGRATION_DELETE = 82
    STAGE_INSTANCE_CREATE = 83
    STAGE_INSTANCE_UPDATE = 84
    STAGE_INSTANCE_DELETE = 85
    STICKER_CREATE = 90
    STICKER_UPDATE = 91
    STICKER_DELETE = 92


@attr.frozen(kw_only=True)
class OptionalAuditEntryInfo:
    #: number of days after which inactive members were kicked
    delete_member_days: str
    #: number of members removed by the prune
    members_removed: str
    #: channel in which the entities were targeted
    channel_id: Snowflake
    #: id of the message that was targeted
    message_id: Snowflake
    #: number of entities that were targeted
    count: str
    #: id of the overwritten entity
    id: Snowflake
    #: type of overwritten entity - "0" for "role" or "1" for "member"
    type: str
    #: name of the role if type is "0" (not present if type is "1")
    role_name: str


@attr.frozen(kw_only=True)
class AuditLogChange:
    #: name of audit log change key
    key: AuditLogChangeKey
    #: new value of the key
    new_value: Unknownish[t.Any] = UNKNOWN
    #: old value of the key
    old_value: Unknownish[t.Any] = UNKNOWN


class AuditLogChangeKey(Enum):
    #: a "guild" just changed. the values are of type snowflake
    #: description: afk channel changed
    AFK_CHANNEL_ID = 'afk_channel_id'
    #: a "guild" just changed. the values are of type integer
    #: description: afk timeout duration changed
    AFK_TIMEOUT = 'afk_timeout'
    #: a "role" just changed. the values are of type string
    #: description: a permission on a text or voice channel was allowed for a
    #:    role
    ALLOW = 'allow'
    #: a "channel" just changed. the values are of type snowflake
    #: description: application id of the added or removed webhook or bot
    APPLICATION_ID = 'application_id'
    #: a "thread" just chaned. the values are of type bool
    #: description: thread is now archived/unarchived
    ARCHIVED = 'archived'
    #: a "sticker" just changed. the values are of type string
    #: description: empty string
    ASSET = 'asset'
    #: a "thread" just changed. the values are of type int
    #: description: auto archive duration changed
    AUTO_ARCHIVE_DURATION = 'auto_archive_duration'
    #: a "sticker" just changed. the values are of type boolean
    #: description: availability of sticker changed
    AVAILABLE = 'available'
    #: a "user" just changed. the values are of type string
    #: description: user avatar changed
    AVATAR_HASH = 'avatar_hash'
    #: a "guild" just changed. the values are of type string
    #: description: guild banner changed
    BANNER_HASH = 'banner_hash'
    #: a "channel" just changed. the values are of type integer
    #: description: voice channel bitrate changed
    BITRATE = 'bitrate'
    #: a "invite" just changed. the values are of type snowflake
    #: description: channel for invite code changed
    CHANNEL_ID = 'channel_id'
    #: a "invite" just changed. the values are of type string
    #: description: invite code changed
    CODE = 'code'
    #: a "role" just changed. the values are of type integer
    #: description: role color changed
    COLOR = 'color'
    #: a "user" just changed. the values are of type boolean
    #: description: user server deafened/undeafened
    DEAF = 'deaf'
    #: a "channel" just changed. the values are of type int
    #: description: default auto archive duration for newly created threads
    #:    changed
    DEFAULT_AUTO_ARCHIVE_DURATION = 'default_auto_archive_duration'
    #: a "guild" just changed. the values are of type integer
    #: description: default message notification level changed
    DEFAULT_MESSAGE_NOTIFICATIONS = 'default_message_notifications'
    #: a "role" just changed. the values are of type string
    #: description: a permission on a text or voice channel was denied for a
    #:    role
    DENY = 'deny'
    #: a "guild or sticker" just changed. the values are of type string
    #: description: description changed
    DESCRIPTION = 'description'
    #: a "guild" just changed. the values are of type string
    #: description: discovery splash changed
    DISCOVERY_SPLASH_HASH = 'discovery_splash_hash'
    #: a "integration" just changed. the values are of type boolean
    #: description: integration emoticons enabled/disabled
    ENABLE_EMOTICONS = 'enable_emoticons'
    #: a "integration" just changed. the values are of type integer
    #: description: integration expiring subscriber behavior changed
    EXPIRE_BEHAVIOR = 'expire_behavior'
    #: a "integration" just changed. the values are of type integer
    #: description: integration expire grace period changed
    EXPIRE_GRACE_PERIOD = 'expire_grace_period'
    #: a "guild" just changed. the values are of type integer
    #: description: change in whose messages are scanned and deleted for
    # explicit content in the server
    EXPLICIT_CONTENT_FILTER = 'explicit_content_filter'
    #: a "sticker" just changed. the values are of type integer (format type)
    #: description: format type of sticker changed
    FORMAT_TYPE = 'format_type'
    #: a "sticker" just changed. the values are of type snowflake
    #: description: guild sticker is in changed
    GUILD_ID = 'guild_id'
    #: a "role" just changed. the values are of type boolean
    #: description: role is now displayed/no longer displayed separate from
    #:    online users
    HOIST = 'hoist'
    #: a "guild" just changed. the values are of type string
    #: description: icon changed
    ICON_HASH = 'icon_hash'
    #: a "any" just changed. the values are of type snowflake
    #: description: the id of the changed entity - sometimes used in
    #:    conjunction with other keys
    ID = 'id'
    #: a "invite" just changed. the values are of type snowflake
    #: description: person who created invite code changed
    INVITER_ID = 'inviter_id'
    #: a "thread" just changed. the values are of type bool
    #: description: thread is now locked/unlocked
    LOCKED = 'locked'
    #: a "invite" just changed. the values are of type integer
    #: description: how long invite code lasts changed
    MAX_AGE = 'max_age'
    #: a "invite" just changed. the values are of type integer
    #: description: change to max number of times invite code can be used
    MAX_USES = 'max_uses'
    #: a "role" just changed. the values are of type boolean
    #: description: role is now mentionable/unmentionable
    MENTIONABLE = 'mentionable'
    #: a "guild" just changed. the values are of type integer
    #: description: two-factor auth requirement changed
    MFA_LEVEL = 'mfa_level'
    #: a "user" just changed. the values are of type boolean
    #: description: user server muted/unmuted
    MUTE = 'mute'
    #: a "any" just changed. the values are of type string
    #: description: name changed
    NAME = 'name'
    #: a "user" just changed. the values are of type string
    #: description: user nickname changed
    NICK = 'nick'
    #: a "channel" just changed. the values are of type boolean
    #: description: channel nsfw restriction changed
    NSFW = 'nsfw'
    #: a "guild" just changed. the values are of type snowflake
    #: description: owner changed
    OWNER_ID = 'owner_id'
    #: a "channel" just changed. the values are of type
    #:    array<channel_overwrite_structure>
    #: description: permissions on a channel changed
    PERMISSION_OVERWRITES = 'permission_overwrites'
    #: a "role" just changed. the values are of type string
    #: description: permissions for a role changed
    PERMISSIONS = 'permissions'
    #: a "channel" just changed. the values are of type integer
    #: description: text or voice channel position changed
    POSITION = 'position'
    #: a "guild" just changed. the values are of type string
    #: description: preferred locale changed
    PREFERRED_LOCALE = 'preferred_locale'
    #: a "stage instance" just changed. the values are of type integer
    #:    (privacy level)
    #: description: privacy level of the stage instance changed
    PRIVACY_LEVEL = 'privacy_level'
    #: a "guild" just changed. the values are of type integer
    #: description: change in number of days after which inactive and
    #:    role-unassigned members are kicked
    PRUNE_DELETE_DAYS = 'prune_delete_days'
    #: a "guild" just changed. the values are of type snowflake
    #: description: id of the public updates channel changed
    PUBLIC_UPDATES_CHANNEL_ID = 'public_updates_channel_id'
    #: a "channel" just changed. the values are of type integer
    #: description: amount of seconds a user has to wait before sending
    #:    another message changed
    RATE_LIMIT_PER_USER = 'rate_limit_per_user'
    #: a "guild" just changed. the values are of type string
    #: description: region changed
    REGION = 'region'
    #: a "guild" just changed. the values are of type snowflake
    #: description: id of the rules channel changed
    RULES_CHANNEL_ID = 'rules_channel_id'
    #: a "guild" just changed. the values are of type string
    #: description: invite splash page artwork changed
    SPLASH_HASH = 'splash_hash'
    #: a "guild" just changed. the values are of type snowflake
    #: description: id of the system channel changed
    SYSTEM_CHANNEL_ID = 'system_channel_id'
    #: a "sticker" just changed. the values are of type string
    #: description: related emoji of sticker changed
    TAGS = 'tags'
    #: a "invite" just changed. the values are of type boolean
    #: description: invite code is temporary/never expires
    TEMPORARY = 'temporary'
    #: a "channel or stage instance" just changed. the values are of type
    #:    string
    #: description: text channel topic or stage instance topic changed
    TOPIC = 'topic'
    #: a "any" just changed. the values are of type integer | string
    #: description: type of entity created
    TYPE = 'type'
    #: a "role" just changed. the values are of type string
    #: description: role unicode emoji changed
    UNICODE_EMOJI = 'unicode_emoji'
    #: a "voice channel" just changed. the values are of type integer
    #: description: new user limit in a voice channel
    USER_LIMIT = 'user_limit'
    #: a "invite" just changed. the values are of type integer
    #: description: number of times invite code used changed
    USES = 'uses'
    #: a "guild" just changed. the values are of type string
    #: description: guild invite vanity url changed
    VANITY_URL_CODE = 'vanity_url_code'
    #: a "guild" just changed. the values are of type integer
    #: description: required verification level changed
    VERIFICATION_LEVEL = 'verification_level'
    #: a "guild" just changed. the values are of type snowflake
    #: description: channel id of the server widget changed
    WIDGET_CHANNEL_ID = 'widget_channel_id'
    #: a "guild" just changed. the values are of type boolean
    #: description: server widget enabled/disable
    WIDGET_ENABLED = 'widget_enabled'
    #: a "guild" just changed. the values are of type
    #:   array<partial_role_structure>
    #: description: new role added
    ADD = '$add'
    #: a "guild" just changed. the values are of type
    #:   array<partial_role_structure>
    #: description: role removed
    REMOVE = '$remove'
