from __future__ import annotations

import datetime as dt
import typing as t
from dataclasses import dataclass
from enum import Enum

from .base import UNKNOWN, Snowflake, Unknownish
from .channel import Channel, ThreadMember
from .emoji import Emoji
from .guild import GuildMember
from .permissions import Role
from .sticker import Sticker
from .user import User


@dataclass()
class GuildRequestMembers:
    #: id of the guild to get members for
    guild_id: Snowflake
    #: maximum number of members to send matching the query; a limit of 0 can
    #: be used with an empty string query to return all members
    limit: t.Optional[int]
    #: string that username starts with, or an empty string to return all
    #: members
    query: Unknownish[t.Optional[str]] = UNKNOWN
    #: used to specify if we want the presences of the matched members
    presences: Unknownish[t.Optional[bool]] = UNKNOWN
    #: used to specify which users you wish to fetch
    user_ids: Unknownish[t.Optional[t.Union[Snowflake, t.List[Snowflake]]]] = UNKNOWN
    #: nonce to identify the Guild Members Chunk response
    nonce: Unknownish[t.Optional[str]] = UNKNOWN


@dataclass()
class GatewayVoiceStateUpdate:
    #: id of the guild
    guild_id: Snowflake
    #: id of the voice channel client wants to join (null if disconnecting)
    channel_id: t.Optional[Snowflake]
    #: is the client muted
    self_mute: bool
    #: is the client deafened
    self_deaf: bool


@dataclass()
class Presence:
    #: unix time (in milliseconds) of when the client went idle, or null if
    #: the client is not idle
    since: t.Optional[int]
    #: the user's activities
    activities: t.List[Activity]
    #: the user's new status
    status: str
    #: whether or not the client is afk
    afk: bool


class StatusTypes(Enum):
    ONLINE = "Online"
    DND = "Do Not Disturb"
    IDLE = "AFK"
    INVISIBLE = "Invisible and shown as offline"
    OFFLINE = "Offline"


@dataclass()
class Hello:
    #: the interval (in milliseconds) the client should heartbeat with
    heartbeat_interval: int


@dataclass()
class ReadyEvent:
    #: gateway version
    v: int
    #: information about the user including email
    user: User
    #: the guilds the user is in
    guilds: t.List[t.Dict[str, object]]
    #: used for resuming connections
    session_id: str
    #: contains id and flags
    application: t.Dict[str, object]
    #: the shard information associated with this session, if sent when
    #: identifying
    shard: Unknownish[t.List[int]] = UNKNOWN


@dataclass()
class ThreadListSyncEvent:
    #: the id of the guild
    guild_id: Snowflake
    #: all active threads in the given channels that the current user can
    #: access
    threads: t.List[Channel]
    #: all thread member objects from the synced threads for the current user,
    #: indicating which threads the current user has been added to
    members: t.List[ThreadMember]
    #: the parent channel ids whose threads are being synced. If omitted, then
    #: threads were synced for the entire guild. This array may contain
    #: channel_ids that have no active threads as well, so you know to clear
    #: that data.
    channel_ids: Unknownish[t.List[Snowflake]] = UNKNOWN


@dataclass()
class ThreadMembersUpdateEvent:
    #: the id of the thread
    id: Snowflake
    #: the id of the guild
    guild_id: Snowflake
    #: the approximate number of members in the thread, capped at 50
    member_count: int
    #: the users who were added to the thread
    added_members: Unknownish[t.List[ThreadMember]] = UNKNOWN
    #: the id of the users who were removed from the thread
    removed_member_ids: Unknownish[t.List[Snowflake]] = UNKNOWN


@dataclass()
class ChannelPinsUpdateEvent:
    #: the id of the channel
    channel_id: Snowflake
    #: the id of the guild
    guild_id: Unknownish[Snowflake] = UNKNOWN
    #: the time at which the most recent pinned message was pinned
    last_pin_timestamp: Unknownish[t.Optional[dt.datetime]] = UNKNOWN


@dataclass()
class GuildBanAddEvent:
    #: id of the guild
    guild_id: Snowflake
    #: the banned user
    user: User


@dataclass()
class GuildBanRemoveEvent:
    #: id of the guild
    guild_id: Snowflake
    #: the unbanned user
    user: User


@dataclass()
class GuildEmojisUpdateEvent:
    #: id of the guild
    guild_id: Snowflake
    #: array of emojis
    emojis: t.List[Emoji]


@dataclass()
class GuildStickersUpdateEvent:
    #: id of the guild
    guild_id: Snowflake
    #: array of stickers
    stickers: t.List[Sticker]


@dataclass()
class GuildIntegrationsUpdateEvent:
    #: id of the guild whose integrations were updated
    guild_id: Snowflake


@dataclass()
class GuildMemberAddExtra:
    #: id of the guild
    guild_id: Snowflake


@dataclass()
class GuildMemberRemoveEvent:
    #: the id of the guild
    guild_id: Snowflake
    #: the user who was removed
    user: User


@dataclass()
class GuildMemberUpdateEvent:
    #: the id of the guild
    guild_id: Snowflake
    #: user role ids
    roles: t.List[Snowflake]
    #: the user
    user: User
    #: when the user joined the guild
    joined_at: t.Optional[dt.datetime]
    #: nickname of the user in the guild
    nick: Unknownish[t.Optional[str]] = UNKNOWN
    #: when the user starting boosting the guild
    premium_since: Unknownish[t.Optional[dt.datetime]] = UNKNOWN
    #: whether the user is deafened in voice channels
    deaf: Unknownish[bool] = UNKNOWN
    #: whether the user is muted in voice channels
    mute: Unknownish[bool] = UNKNOWN
    #: whether the user has not yet passed the guild's Membership Screening
    #: requirements
    pending: Unknownish[bool] = UNKNOWN


@dataclass()
class GuildMembersChunkEvent:
    #: the id of the guild
    guild_id: Snowflake
    #: set of guild members
    members: t.List[GuildMember]
    #: the chunk index in the expected chunks for this response (0 <=
    #: chunk_index < chunk_count)
    chunk_index: int
    #: the total number of expected chunks for this response
    chunk_count: int
    #: if passing an invalid id to REQUEST_GUILD_MEMBERS, it will be returned
    #: here
    not_found: Unknownish[t.List[Snowflake]] = UNKNOWN
    #: if passing true to REQUEST_GUILD_MEMBERS, presences of the returned
    #: members will be here
    presences: Unknownish[t.List[Presence]] = UNKNOWN
    #: the nonce used in the Guild Members Request
    nonce: Unknownish[str] = UNKNOWN


@dataclass()
class GuildRoleCreateEvent:
    #: the id of the guild
    guild_id: Snowflake
    #: the role created
    role: Role


@dataclass()
class GuildRoleUpdateEvent:
    #: the id of the guild
    guild_id: Snowflake
    #: the role updated
    role: Role


@dataclass()
class GuildRoleDeleteEvent:
    #: id of the guild
    guild_id: Snowflake
    #: id of the role
    role_id: Snowflake


@dataclass()
class IntegrationCreateEventAdditional:
    #: id of the guild
    guild_id: Snowflake


@dataclass()
class IntegrationUpdateEventAdditional:
    #: id of the guild
    guild_id: Snowflake


@dataclass()
class IntegrationDeleteEvent:
    #: integration id
    id: Snowflake
    #: id of the guild
    guild_id: Snowflake
    #: id of the bot/OAuth2 application for this discord integration
    application_id: Unknownish[Snowflake] = UNKNOWN


@dataclass()
class InviteCreateEvent:
    #: the channel the invite is for
    channel_id: Snowflake
    #: the unique invite code
    code: str
    #: the time at which the invite was created
    created_at: dt.datetime
    #: how long the invite is valid for (in seconds)
    max_age: int
    #: the maximum number of times the invite can be used
    max_uses: int
    #: whether or not the invite is temporary (invited users will be kicked on
    #: disconnect unless they're assigned a role)
    temporary: bool
    #: how many times the invite has been used (always will be 0)
    uses: int
    #: the guild of the invite
    guild_id: Unknownish[Snowflake] = UNKNOWN
    #: the user that created the invite
    inviter: Unknownish[User] = UNKNOWN
    #: the type of target for this voice channel invite
    target_type: Unknownish[int] = UNKNOWN
    #: the user whose stream to display for this voice channel stream invite
    target_user: Unknownish[User] = UNKNOWN
    #: the embedded application to open for this voice channel embedded
    #: application invite
    target_application: Unknownish[t.Dict[str, object]] = UNKNOWN


@dataclass()
class InviteDeleteEvent:
    #: the channel of the invite
    channel_id: Snowflake
    #: the unique invite code
    code: str
    #: the guild of the invite
    guild_id: Unknownish[Snowflake] = UNKNOWN


@dataclass()
class MessageDeleteEvent:
    #: the id of the message
    id: Snowflake
    #: the id of the channel
    channel_id: Snowflake
    #: the id of the guild
    guild_id: Unknownish[Snowflake] = UNKNOWN


@dataclass()
class MessageDeleteBulkEvent:
    #: the ids of the messages
    ids: t.List[Snowflake]
    #: the id of the channel
    channel_id: Snowflake
    #: the id of the guild
    guild_id: Unknownish[Snowflake] = UNKNOWN


@dataclass()
class MessageReactionAddEvent:
    #: the id of the user
    user_id: Snowflake
    #: the id of the channel
    channel_id: Snowflake
    #: the id of the message
    message_id: Snowflake
    #: the emoji used to react - example
    emoji: t.Dict[str, object]
    #: the id of the guild
    guild_id: Unknownish[Snowflake] = UNKNOWN
    #: the member who reacted if this happened in a guild
    member: Unknownish[GuildMember] = UNKNOWN


@dataclass()
class MessageReactionRemoveEvent:
    #: the id of the user
    user_id: Snowflake
    #: the id of the channel
    channel_id: Snowflake
    #: the id of the message
    message_id: Snowflake
    #: the emoji used to react - example
    emoji: t.Dict[str, object]
    #: the id of the guild
    guild_id: Unknownish[Snowflake] = UNKNOWN


@dataclass()
class MessageReactionRemoveAllEvent:
    #: the id of the channel
    channel_id: Snowflake
    #: the id of the message
    message_id: Snowflake
    #: the id of the guild
    guild_id: Unknownish[Snowflake] = UNKNOWN


@dataclass()
class MessageReactionRemoveEmoji:
    #: the id of the channel
    channel_id: Snowflake
    #: the id of the message
    message_id: Snowflake
    #: the emoji that was removed
    emoji: t.Dict[str, object]
    #: the id of the guild
    guild_id: Unknownish[Snowflake] = UNKNOWN


@dataclass()
class ClientStatus:

    #: the user's status set for an active desktop (Windows, Linux, Mac)
    #: application session
    desktop: Unknownish[str] = UNKNOWN
    #: the user's status set for an active mobile (iOS, Android) application
    #: session
    mobile: Unknownish[str] = UNKNOWN
    #: the user's status set for an active web (browser, bot account)
    #: application session
    web: Unknownish[str] = UNKNOWN


@dataclass()
class Activity:
    #: the activity's name
    name: str
    #: activity type
    type: int
    #: unix timestamp (in milliseconds) of when the activity was added to the
    #: user's session
    created_at: int
    #: stream url, is validated when type is 1
    url: Unknownish[t.Optional[str]] = UNKNOWN
    #: unix timestamps for start and/or end of the game
    timestamps: Unknownish[ActivityTimestamps] = UNKNOWN
    #: application id for the game
    application_id: Unknownish[Snowflake] = UNKNOWN
    #: what the player is currently doing
    details: Unknownish[t.Optional[str]] = UNKNOWN
    #: the user's current party status
    state: Unknownish[t.Optional[str]] = UNKNOWN
    #: the emoji used for a custom status
    emoji: Unknownish[t.Optional[Emoji]] = UNKNOWN
    #: information for the current party of the player
    party: Unknownish[ActivityParty] = UNKNOWN
    #: images for the presence and their hover texts
    assets: Unknownish[ActivityAssets] = UNKNOWN
    #: secrets for Rich Presence joining and spectating
    secrets: Unknownish[ActivitySecrets] = UNKNOWN
    #: whether or not the activity is an instanced game session
    instance: Unknownish[bool] = UNKNOWN
    #: activity flagsORd together, describes what the payload includes
    flags: Unknownish[int] = UNKNOWN
    #: the custom buttons shown in the Rich Presence (max 2)
    buttons: Unknownish[t.List[ActivityButtons]] = UNKNOWN


class ActivityTypes(Enum):
    #: Playing {name} - "Playing Rocket League"
    GAME = 0
    #: Streaming {details} - "Streaming Rocket League"
    STREAMING = 1
    #: Listening to {name} - "Listening to Spotify"
    LISTENING = 2
    #: Watching {name} - "Watching YouTube Together"
    WATCHING = 3
    #: {emoji} {name} - ":smiley: I am cool"
    CUSTOM = 4
    #: Competing in {name} - "Competing in Arena World Champions"
    COMPETING = 5


@dataclass()
class ActivityTimestamps:

    #: unix time (in milliseconds) of when the activity started
    start: Unknownish[int] = UNKNOWN
    #: unix time (in milliseconds) of when the activity ends
    end: Unknownish[int] = UNKNOWN


@dataclass()
class ActivityEmoji:
    #: the name of the emoji
    name: str
    #: the id of the emoji
    id: Unknownish[Snowflake] = UNKNOWN
    #: whether this emoji is animated
    animated: Unknownish[bool] = UNKNOWN


@dataclass()
class ActivityParty:

    #: the id of the party
    id: Unknownish[str] = UNKNOWN
    #: used to show the party's current and maximum size
    size: Unknownish[t.List[t.Tuple[int, int]]] = UNKNOWN


@dataclass()
class ActivityAssets:

    #: the id for a large asset of the activity, usually a snowflake
    large_image: Unknownish[str] = UNKNOWN
    #: text displayed when hovering over the large image of the activity
    large_text: Unknownish[str] = UNKNOWN
    #: the id for a small asset of the activity, usually a snowflake
    small_image: Unknownish[str] = UNKNOWN
    #: text displayed when hovering over the small image of the activity
    small_text: Unknownish[str] = UNKNOWN


@dataclass()
class ActivitySecrets:

    #: the secret for joining a party
    join: Unknownish[str] = UNKNOWN
    #: the secret for spectating a game
    spectate: Unknownish[str] = UNKNOWN
    #: the secret for a specific instanced match
    match: Unknownish[str] = UNKNOWN


class ActivityFlags(Enum):
    INSTANCE = 1
    JOIN = 2
    SPECTATE = 4
    JOIN_REQUEST = 8
    SYNC = 16
    PLAY = 32


@dataclass()
class ActivityButtons:
    #: the text shown on the button (1-32 characters)
    label: str
    #: the url opened when clicking the button (1-512 characters)
    url: str


@dataclass()
class TypingStartEvent:
    #: id of the channel
    channel_id: Snowflake
    #: id of the user
    user_id: Snowflake
    #: unix time (in seconds) of when the user started typing
    timestamp: int
    #: id of the guild
    guild_id: Unknownish[Snowflake] = UNKNOWN
    #: the member who started typing if this happened in a guild
    member: Unknownish[GuildMember] = UNKNOWN


@dataclass()
class VoiceServerUpdateEvent:
    #: voice connection token
    token: str
    #: the guild this voice server update is for
    guild_id: Snowflake
    #: the voice server host
    endpoint: t.Optional[str]


@dataclass()
class WebhookUpdateEvent:
    #: id of the guild
    guild_id: Snowflake
    #: id of the channel
    channel_id: Snowflake


@dataclass()
class ApplicationCommandExtra:

    #: id of the guild the command is in
    guild_id: Unknownish[Snowflake] = UNKNOWN


@dataclass()
class SessionStartLimit:
    #: The total number of session starts the current user is allowed
    total: int
    #: The remaining number of session starts the current user is allowed
    remaining: int
    #: The number of milliseconds after which the limit resets
    reset_after: int
    #: The number of identify requests allowed per 5 seconds
    max_concurrency: int
