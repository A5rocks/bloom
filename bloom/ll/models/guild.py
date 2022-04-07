from __future__ import annotations

import datetime
import enum
import typing

import attr

from bloom.ll.models.base import UNKNOWN, Snowflake, Unknownish
from bloom.ll.models.channel import Channel
from bloom.ll.models.emoji import Emoji
from bloom.ll.models.guild_scheduled_events import GuildScheduledEvent
from bloom.ll.models.permissions import Role
from bloom.ll.models.stage_instance import StageInstance
from bloom.ll.models.sticker import Sticker
from bloom.ll.models.user import User

# docs in this module are copied from the Discord Documentation


@attr.frozen(kw_only=True)
class Guild:
    #: guild id
    id: Snowflake
    #: guild name (2-100 characters, excluding trailing and leading
    #: whitespace)
    name: str
    #: icon hash
    icon: typing.Optional[str]
    #: splash hash
    splash: typing.Optional[str]
    #: discovery splash hash; only present for guilds with the "DISCOVERABLE"
    #: feature
    discovery_splash: typing.Optional[str]
    #: true if the user is the owner of the guild
    owner: Unknownish[bool] = UNKNOWN
    #: id of owner
    owner_id: Snowflake
    #: total permissions for the user in the guild (excludes overwrites)
    permissions: Unknownish[str] = UNKNOWN
    #: voice region id for the guild (deprecated)
    region: Unknownish[typing.Optional[str]] = UNKNOWN
    #: id of afk channel
    afk_channel_id: typing.Optional[Snowflake]
    #: afk timeout in seconds
    afk_timeout: int
    #: verification level required for the guild
    verification_level: int
    #: default message notifications level
    default_message_notifications: int
    #: explicit content filter level
    explicit_content_filter: int
    #: roles in the guild
    roles: typing.List[Role]
    #: custom guild emojis
    emojis: typing.List[Emoji]
    #: enabled guild features
    features: typing.List[str]
    #: required MFA level for the guild
    mfa_level: int
    #: application id of the guild creator if it is bot-created
    application_id: typing.Optional[Snowflake]
    #: the id of the channel where guild notices such as welcome messages and
    #: boost events are posted
    system_channel_id: typing.Optional[Snowflake]
    #: system channel flags
    system_channel_flags: int
    #: the id of the channel where Community guilds can display rules and/or
    #: guidelines
    rules_channel_id: typing.Optional[Snowflake]
    #: when this guild was joined at
    joined_at: Unknownish[datetime.datetime] = UNKNOWN
    #: true if this is considered a large guild
    large: Unknownish[bool] = UNKNOWN
    #: true if this guild is unavailable due to an outage
    unavailable: Unknownish[bool] = UNKNOWN
    #: total number of members in this guild
    member_count: Unknownish[int] = UNKNOWN
    #: states of members currently in voice channels; lacks the guild_id key
    voice_states: Unknownish[typing.List[typing.Dict[str, typing.Any]]] = UNKNOWN
    #: users in the guild
    members: Unknownish[typing.List[GuildMember]] = UNKNOWN
    #: channels in the guild
    channels: Unknownish[typing.List[Channel]] = UNKNOWN
    #: all active threads in the guild that current user has permission to
    #: view
    threads: Unknownish[typing.List[Channel]] = UNKNOWN
    #: presences of the members in the guild, will only include non-offline
    #: members if the size is greater than large threshold
    presences: Unknownish[typing.List[typing.Dict[str, typing.Any]]] = UNKNOWN
    #: the vanity url code for the guild
    vanity_url_code: typing.Optional[str]
    #: the description of a guild
    description: typing.Optional[str]
    #: banner hash
    banner: typing.Optional[str]
    #: premium tier (Server Boost level)
    premium_tier: int
    #: the preferred locale of a Community guild; used in server discovery and
    #: notices from Discord; defaults to "en-US"
    preferred_locale: str
    #: the id of the channel where admins and moderators of Community guilds
    #: receive notices from Discord
    public_updates_channel_id: typing.Optional[Snowflake]
    #: guild NSFW level
    nsfw_level: int
    #: Stage instances in the guild
    stage_instances: Unknownish[typing.List[StageInstance]] = UNKNOWN
    #: icon hash, returned when in the template object
    icon_hash: Unknownish[typing.Optional[str]] = UNKNOWN
    #: true if the server widget is enabled
    widget_enabled: Unknownish[bool] = UNKNOWN
    #: the channel id that the widget will generate an invite to, or null if
    #: set to no invite
    widget_channel_id: Unknownish[typing.Optional[Snowflake]] = UNKNOWN
    #: the maximum number of presences for the guild (null is always returned,
    #: apart from the largest of guilds)
    max_presences: Unknownish[typing.Optional[int]] = UNKNOWN
    #: the maximum number of members for the guild
    max_members: Unknownish[int] = UNKNOWN
    #: the number of boosts this guild currently has
    premium_subscription_count: Unknownish[int] = UNKNOWN
    #: the maximum amount of users in a video channel
    max_video_channel_users: Unknownish[int] = UNKNOWN
    #: approximate number of members in this guild, returned from the GET
    #: /guilds/<id> endpoint when with_counts is true
    approximate_member_count: Unknownish[int] = UNKNOWN
    #: approximate number of non-offline members in this guild, returned from
    #: the GET /guilds/<id> endpoint when with_counts is true
    approximate_presence_count: Unknownish[int] = UNKNOWN
    #: the welcome screen of a Community guild, shown to new members, returned
    #: in an Invite's guild object
    welcome_screen: Unknownish[WelcomeScreen] = UNKNOWN
    #: custom guild stickers
    stickers: Unknownish[typing.List[Sticker]] = UNKNOWN
    #: the scheduled events in the guild
    guild_scheduled_events: Unknownish[typing.List[GuildScheduledEvent]] = UNKNOWN
    #: whether the guild has the boost progress bar enabled
    premium_progress_bar_enabled: bool


class DefaultMessageNotificationLevel(enum.Enum):
    #: members will receive notifications for all messages by default
    ALL_MESSAGES = 0
    #: members will receive notifications only for messages that @mention them
    #: by default
    ONLY_MENTIONS = 1


class ExplicitContentFilterLevel(enum.Enum):
    #: media content will not be scanned
    DISABLED = 0
    #: media content sent by members without roles will be scanned
    MEMBERS_WITHOUT_ROLES = 1
    #: media content sent by all members will be scanned
    ALL_MEMBERS = 2


class MfaLevel(enum.Enum):
    #: guild has no MFA/2FA requirement for moderation actions
    NONE = 0
    #: guild has a 2FA requirement for moderation actions
    ELEVATED = 1


class VerificationLevel(enum.Enum):
    #: unrestricted
    NONE = 0
    #: must have verified email on account
    LOW = 1
    #: must be registered on Discord for longer than 5 minutes
    MEDIUM = 2
    #: must be a member of the server for longer than 10 minutes
    HIGH = 3
    #: must have a verified phone number
    VERY_HIGH = 4


class GuildNsfwLevel(enum.Enum):
    DEFAULT = 0
    EXPLICIT = 1
    SAFE = 2
    AGE_RESTRICTED = 3


class PremiumTier(enum.Enum):
    #: guild has not unlocked any Server Boost perks
    NONE = 0
    #: guild has unlocked Server Boost level 1 perks
    TIER_1 = 1
    #: guild has unlocked Server Boost level 2 perks
    TIER_2 = 2
    #: guild has unlocked Server Boost level 3 perks
    TIER_3 = 3


class SystemChannelFlags(enum.IntFlag):
    #: Suppress member join notifications
    SUPPRESS_JOIN_NOTIFICATIONS = 1 << 0
    #: Suppress server boost notifications
    SUPPRESS_PREMIUM_SUBSCRIPTIONS = 1 << 1
    #: Suppress server setup tips
    SUPPRESS_GUILD_REMINDER_NOTIFICATIONS = 1 << 2
    #: Hide member join sticker reply buttons
    SUPPRESS_JOIN_NOTIFICATION_REPLIES = 1 << 3


class GuildFeatures(enum.Enum):
    #: guild has access to set an animated guild banner image
    ANIMATED_BANNER = 'ANIMATED_BANNER'
    #: guild has access to set an animated guild icon
    ANIMATED_ICON = 'ANIMATED_ICON'
    #: guild has access to set a guild banner image
    BANNER = 'BANNER'
    #: guild has access to use commerce features (i.e. create store channels)
    COMMERCE = 'COMMERCE'
    #: guild can enable welcome screen, Membership Screening, stage channels
    #: and discovery, and receives community updates
    COMMUNITY = 'COMMUNITY'
    #: guild is able to be discovered in the directory
    DISCOVERABLE = 'DISCOVERABLE'
    #: guild is able to be featured in the directory
    FEATURABLE = 'FEATURABLE'
    #: guild has access to set an invite splash background
    INVITE_SPLASH = 'INVITE_SPLASH'
    #: guild has enabled
    MEMBER_VERIFICATION_GATE_ENABLED = 'MEMBER_VERIFICATION_GATE_ENABLED'
    #: guild has access to create news channels
    NEWS = 'NEWS'
    #: guild is partnered
    PARTNERED = 'PARTNERED'
    #: guild can be previewed before joining via Membership Screening or the
    #: directory
    PREVIEW_ENABLED = 'PREVIEW_ENABLED'
    #: guild has access to set a vanity URL
    VANITY_URL = 'VANITY_URL'
    #: guild is verified
    VERIFIED = 'VERIFIED'
    #: guild has access to set 384kbps bitrate in voice (previously VIP voice
    #: servers)
    VIP_REGIONS = 'VIP_REGIONS'
    #: guild has enabled the welcome screen
    WELCOME_SCREEN_ENABLED = 'WELCOME_SCREEN_ENABLED'
    #: guild has enabled ticketed events
    TICKETED_EVENTS_ENABLED = 'TICKETED_EVENTS_ENABLED'
    #: guild has enabled monetization
    MONETIZATION_ENABLED = 'MONETIZATION_ENABLED'
    #: guild has increased custom sticker slots
    MORE_STICKERS = 'MORE_STICKERS'
    #: guild has access to the three day archive time for threads
    THREE_DAY_THREAD_ARCHIVE = 'THREE_DAY_THREAD_ARCHIVE'
    #: guild has access to the seven day archive time for threads
    SEVEN_DAY_THREAD_ARCHIVE = 'SEVEN_DAY_THREAD_ARCHIVE'
    #: guild has access to create private threads
    PRIVATE_THREADS = 'PRIVATE_THREADS'
    #: guild is able to set role icons
    ROLE_ICONS = 'ROLE_ICONS'


@attr.frozen(kw_only=True)
class GuildPreview:
    #: guild id
    id: Snowflake
    #: guild name (2-100 characters)
    name: str
    #: icon hash
    icon: typing.Optional[str]
    #: splash hash
    splash: typing.Optional[str]
    #: discovery splash hash
    discovery_splash: typing.Optional[str]
    #: custom guild emojis
    emojis: typing.List[Emoji]
    #: enabled guild features
    features: typing.List[str]
    #: approximate number of members in this guild
    approximate_member_count: int
    #: approximate number of online members in this guild
    approximate_presence_count: int
    #: the description for the guild, if the guild is discoverable
    description: typing.Optional[str]
    #: custom guild stickers
    stickers: typing.List[Sticker]


@attr.frozen(kw_only=True)
class GuildWidgetSettings:
    #: whether the widget is enabled
    enabled: bool
    #: the widget channel id
    channel_id: typing.Optional[Snowflake]


@attr.frozen(kw_only=True)
class GuildMember:
    #: array of role object ids
    roles: typing.List[Snowflake]
    #: when the user joined the guild
    joined_at: datetime.datetime
    #: whether the user is deafened in voice channels
    deaf: bool
    #: whether the user is muted in voice channels
    mute: bool
    #: the user this guild member represents
    user: Unknownish[User] = UNKNOWN
    #: this user's guild nickname
    nick: Unknownish[typing.Optional[str]] = UNKNOWN
    #: the member's guild avatar hash
    avatar: Unknownish[typing.Optional[str]] = UNKNOWN
    #: when the user started boosting the guild
    premium_since: Unknownish[typing.Optional[datetime.datetime]] = UNKNOWN
    #: whether the user has not yet passed the guild's Membership Screening
    #: requirements
    pending: Unknownish[bool] = UNKNOWN
    #: total permissions of the member in the channel, including overwrites,
    #: returned when in the interaction object
    permissions: Unknownish[str] = UNKNOWN

    #: timestamp of when the time out will be removed; until then, they cannot
    #: interact with the guild
    communication_disabled_until: Unknownish[typing.Optional[datetime.datetime]] = UNKNOWN


@attr.frozen(kw_only=True)
class Integration:
    #: integration id
    id: Snowflake
    #: integration name
    name: str
    #: integration type (twitch, youtube, or discord)
    type: str
    #: is this integration enabled
    enabled: bool
    #: is this integration syncing
    syncing: Unknownish[bool] = UNKNOWN
    #: id that this integration uses for "subscribers"
    role_id: Unknownish[Snowflake] = UNKNOWN
    #: whether emoticons should be synced for this integration (twitch only
    #: currently)
    enable_emoticons: Unknownish[bool] = UNKNOWN
    #: the behavior of expiring subscribers
    expire_behavior: Unknownish[IntegrationExpireBehaviors] = UNKNOWN
    #: the grace period (in days) before expiring subscribers
    expire_grace_period: Unknownish[int] = UNKNOWN
    #: user for this integration
    user: Unknownish[User] = UNKNOWN
    #: integration account information
    account: IntegrationAccount
    #: when this integration was last synced
    synced_at: Unknownish[datetime.datetime] = UNKNOWN
    #: how many subscribers this integration has
    subscriber_count: Unknownish[int] = UNKNOWN
    #: has this integration been revoked
    revoked: Unknownish[bool] = UNKNOWN
    #: The bot/OAuth2 application for discord integrations
    application: Unknownish[IntegrationApplication] = UNKNOWN


class IntegrationExpireBehaviors(enum.Enum):
    REMOVE_ROLE = 0
    KICK = 1


@attr.frozen(kw_only=True)
class IntegrationAccount:
    #: id of the account
    id: str
    #: name of the account
    name: str


@attr.frozen(kw_only=True)
class IntegrationApplication:
    #: the id of the app
    id: Snowflake
    #: the name of the app
    name: str
    #: the icon hash of the app
    icon: typing.Optional[str]
    #: the description of the app
    description: str
    #: the bot associated with this application
    bot: Unknownish[User] = UNKNOWN


@attr.frozen(kw_only=True)
class Ban:
    #: the reason for the ban
    reason: typing.Optional[str]
    #: the banned user
    user: User


@attr.frozen(kw_only=True)
class WelcomeScreen:
    #: the server description shown in the welcome screen
    description: typing.Optional[str]
    #: the channels shown in the welcome screen, up to 5
    welcome_channels: typing.List[WelcomeScreenChannel]


@attr.frozen(kw_only=True)
class WelcomeScreenChannel:
    #: the channel's id
    channel_id: Snowflake
    #: the description shown for the channel
    description: str
    #: the emoji id, if the emoji is custom
    emoji_id: typing.Optional[Snowflake]
    #: the emoji name if custom, the unicode character if standard, or null
    #: if no emoji is set
    emoji_name: typing.Optional[str]


@attr.frozen(kw_only=True)
class ModifyGuildChannelPositionsParameters:
    #: channel id
    id: Snowflake
    # TODO: some of these are optional (in the Unknownish kind of way)
    #      figure this out then update the documentation
    #: sorting position of the channel
    position: typing.Optional[int]
    #: syncs the permission overwrites with the new parent, if moving to a new
    #: category
    lock_permissions: typing.Optional[bool]
    #: the new parent ID for the channel that is moved
    parent_id: typing.Optional[Snowflake]


@attr.frozen(kw_only=True)
class ModifyGuildRolePositionsParameters:
    #: role
    id: Snowflake
    #: sorting position of the role
    position: Unknownish[typing.Optional[int]] = UNKNOWN


class WidgetStyleOptions(enum.Enum):
    #: shield style widget with Discord icon and guild members online count
    SHIELD = 'shield'
    #: large image with guild icon, name and online countyping. "POWERED BY
    #: DISCORD" as the footer of the widget
    BANNER1 = 'banner1'
    #: smaller widget style with guild icon, name and online countyping. Split on
    #: the right with Discord logo
    BANNER2 = 'banner2'
    #: large image with guild icon, name and online countyping. In the footer,
    #: Discord logo on the left and "Chat Now" on the right
    BANNER3 = 'banner3'
    #: large Discord logo at the top of the widgetyping. Guild icon, name and
    #: online count in the middle portion of the widget and a "JOIN MY SERVER"
    #: button at the bottom
    BANNER4 = 'banner4'


@attr.frozen(kw_only=True)
class PruneCount:
    #: the number of members that would be removed in a prune operation. Will
    #: be ``None`` if ``compute_prune_count`` is ``False`` when beginning a
    #: prune.
    pruned: typing.Optional[int]


# this is in here because otherwise circular imports.
@attr.frozen(kw_only=True)
class UserConnection:
    #: id of the connection account
    id: str
    #: the username of the connection account
    name: str
    #: the service of the connection (twitch, youtube)
    type: str
    #: whether the connection is revoked
    revoked: Unknownish[bool] = UNKNOWN
    #: an array of partial server integrations
    integrations: Unknownish[typing.List[Integration]] = UNKNOWN
    #: whether the connection is verified
    verified: bool
    #: whether friend sync is enabled for this connection
    friend_sync: bool
    #: whether activities related to this connection will be shown in presence
    #: updates
    show_activity: bool
    #: visibility of this connection
    visibility: UserConnectionVisibility


class UserConnectionVisibility(enum.Enum):
    #: invisible to everyone except the user themselves
    NONE = 0
    #: visible to everyone
    EVERYONE = 1


@attr.frozen(kw_only=True)
class GuildScheduledEventUser:
    #: the scheduled event id which the user subscribed to
    guild_scheduled_event_id: Snowflake
    #: user which subscribed to an event
    user: User
    #: guild member data for this user for the guild which this event belongs
    #: to, if any
    member: Unknownish[GuildMember] = UNKNOWN
