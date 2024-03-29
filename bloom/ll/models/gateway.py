from __future__ import annotations

import datetime
import enum
import typing

import attr

from .application_commands import MessageInteraction
from .base import UNKNOWN, Snowflake, Unknownish
from .channel import (
    Attachment,
    Channel,
    ChannelMention,
    ChannelTypes,
    Embed,
    MessageActivity,
    MessageReference,
    Reaction,
    ThreadMember,
)
from .emoji import Emoji
from .guild import Guild, GuildMember, Integration
from .guild_scheduled_events import GuildScheduledEvent
from .interaction import Interaction
from .message import Message
from .message_components import Component
from .permissions import Role
from .stage_instance import StageInstance
from .sticker import Sticker, StickerItem
from .user import User
from .voice import VoiceState

# docs in this module are copied from the Discord Documentation


@attr.frozen(kw_only=True)
class GuildRequestMembers:
    #: id of the guild to get members for
    guild_id: Snowflake
    #: maximum number of members to send matching the query; a limit of 0 can
    #: be used with an empty string query to return all members
    limit: typing.Optional[int]
    #: string that username starts with, or an empty string to return all
    #: members
    query: Unknownish[typing.Optional[str]] = UNKNOWN
    #: used to specify if we want the presences of the matched members
    presences: Unknownish[typing.Optional[bool]] = UNKNOWN
    #: used to specify which users you wish to fetch
    user_ids: Unknownish[
        typing.Optional[typing.Union[Snowflake, typing.List[Snowflake]]]
    ] = UNKNOWN
    #: nonce to identify the Guild Members Chunk response
    nonce: Unknownish[typing.Optional[str]] = UNKNOWN


@attr.frozen(kw_only=True)
class GatewayVoiceStateUpdateEvent:
    #: id of the guild
    guild_id: Snowflake
    #: id of the voice channel client wants to join (null if disconnecting)
    channel_id: typing.Optional[Snowflake]
    #: is the client muted
    self_mute: bool
    #: is the client deafened
    self_deaf: bool


@attr.frozen(kw_only=True)
class Presence:
    #: unix time (in milliseconds) of when the client went idle, or null if
    #: the client is not idle
    since: typing.Optional[int]
    #: the user's activities
    activities: typing.List[Activity]
    #: the user's new status
    status: str
    #: whether or not the client is afk
    afk: bool


class StatusTypes(enum.Enum):
    ONLINE = 'Online'
    DND = 'Do Not Disturb'
    IDLE = 'AFK'
    INVISIBLE = 'Invisible and shown as offline'
    OFFLINE = 'Offline'


@attr.frozen(kw_only=True)
class Hello:
    #: the interval (in milliseconds) the client should heartbeat with
    heartbeat_interval: int


@attr.frozen(kw_only=True)
class ReadyEvent:
    #: gateway version
    v: int
    #: information about the user including email
    user: User
    #: the guilds the user is in
    guilds: typing.List[typing.Dict[str, typing.Any]]
    #: used for resuming connections
    session_id: str
    #: contains id and flags
    application: typing.Dict[str, typing.Any]
    #: the shard information associated with this session, if sent when
    #: identifying
    shard: Unknownish[typing.List[int]] = UNKNOWN


@attr.frozen(kw_only=True)
class ResumedEvent:
    pass


@attr.frozen(kw_only=True)
class ChannelCreateEvent(Channel):
    pass


@attr.frozen(kw_only=True)
class ChannelUpdateEvent(Channel):
    pass


@attr.frozen(kw_only=True)
class ChannelDeleteEvent(Channel):
    pass


@attr.frozen(kw_only=True)
class ThreadCreateEvent(Channel):
    newly_created: Unknownish[bool] = UNKNOWN


@attr.frozen(kw_only=True)
class ThreadUpdateEvent(Channel):
    pass


@attr.frozen(kw_only=True)
class ThreadDeleteEvent:
    # TODO: this is code duplication?
    #: the id of this channel
    id: Snowflake
    #: the id of the guild (may be missing for some channel objects received
    #: over gateway guild dispatches)
    guild_id: Unknownish[Snowflake] = UNKNOWN
    #: for guild channels: id of the parent category for a channel (each
    #: parent category can contain up to 50 channels), for threads: id of the
    #: text channel this thread was created
    parent_id: Unknownish[typing.Optional[Snowflake]] = UNKNOWN
    #: the type of channel
    type: ChannelTypes


@attr.frozen(kw_only=True)
class ThreadListSyncEvent:
    #: the id of the guild
    guild_id: Snowflake
    #: all active threads in the given channels that the current user can
    #: access
    threads: typing.List[Channel]
    #: all thread member objects from the synced threads for the current user,
    #: indicating which threads the current user has been added to
    members: typing.List[ThreadMember]
    #: the parent channel ids whose threads are being synced. If omitted, then
    #: threads were synced for the entire guild. This array may contain
    #: channel_ids that have no active threads as well, so you know to clear
    #: that data.
    channel_ids: Unknownish[typing.List[Snowflake]] = UNKNOWN


# TODO: blocked on https://github.com/python-attrs/attrs/issues/842
attr.resolve_types(ThreadMember)


@attr.frozen(kw_only=True)
class ThreadMemberUpdateEvent(ThreadMember):
    guild_id: Snowflake


@attr.frozen(kw_only=True)
class ThreadMembersUpdateEvent:
    #: the id of the thread
    id: Snowflake
    #: the id of the guild
    guild_id: Snowflake
    #: the approximate number of members in the thread, capped at 50
    member_count: int
    #: the users who were added to the thread
    added_members: Unknownish[typing.List[ThreadMember]] = UNKNOWN
    #: the id of the users who were removed from the thread
    removed_member_ids: Unknownish[typing.List[Snowflake]] = UNKNOWN


@attr.frozen(kw_only=True)
class ChannelPinsUpdateEvent:
    #: the id of the channel
    channel_id: Snowflake
    #: the id of the guild
    guild_id: Unknownish[Snowflake] = UNKNOWN
    #: the time at which the most recent pinned message was pinned
    last_pin_timestamp: Unknownish[typing.Optional[datetime.datetime]] = UNKNOWN


@attr.frozen(kw_only=True)
class GuildCreateEvent(Guild):
    pass


@attr.frozen(kw_only=True)
class GuildUpdateEvent(Guild):
    pass


@attr.frozen(kw_only=True)
class GuildDeleteEvent:
    id: Snowflake
    unavailable: bool = False
    # TODO: A partial guild objectyping. Represents an Offline Guild, or a Guild
    # whose information has not been provided through Guild Create events
    # during the Gateway connectyping.
    pass


@attr.frozen(kw_only=True)
class GuildBanAddEvent:
    #: id of the guild
    guild_id: Snowflake
    #: the banned user
    user: User


@attr.frozen(kw_only=True)
class GuildBanRemoveEvent:
    #: id of the guild
    guild_id: Snowflake
    #: the unbanned user
    user: User


@attr.frozen(kw_only=True)
class GuildEmojisUpdateEvent:
    #: id of the guild
    guild_id: Snowflake
    #: array of emojis
    emojis: typing.List[Emoji]


@attr.frozen(kw_only=True)
class GuildStickersUpdateEvent:
    #: id of the guild
    guild_id: Snowflake
    #: array of stickers
    stickers: typing.List[Sticker]


@attr.frozen(kw_only=True)
class GuildIntegrationsUpdateEvent:
    #: id of the guild whose integrations were updated
    guild_id: Snowflake


@attr.frozen(kw_only=True)
class GuildMemberAddEvent(GuildMember):
    #: id of the guild
    guild_id: Snowflake


# TODO: blocked on https://github.com/python-attrs/attrs/issues/842
attr.resolve_types(GuildMemberAddEvent, globals(), locals())


@attr.frozen(kw_only=True)
class GuildMemberRemoveEvent:
    #: the id of the guild
    guild_id: Snowflake
    #: the user who was removed
    user: User


@attr.frozen(kw_only=True)
class GuildMemberUpdateEvent:
    # TODO: code duplication with GuildMember?
    #: the id of the guild
    guild_id: Snowflake
    #: user role ids
    roles: typing.List[Snowflake]
    #: the user
    user: User
    # TODO: does this get sent at all?
    #: the member's guild avatar hash
    avatar: Unknownish[typing.Optional[str]] = UNKNOWN
    # TODO: when can this be null?
    #: when the user joined the guild
    joined_at: typing.Optional[datetime.datetime]
    #: nickname of the user in the guild
    nick: Unknownish[typing.Optional[str]] = UNKNOWN
    #: when the user starting boosting the guild
    premium_since: Unknownish[typing.Optional[datetime.datetime]] = UNKNOWN
    #: whether the user is deafened in voice channels
    deaf: Unknownish[bool] = UNKNOWN
    #: whether the user is muted in voice channels
    mute: Unknownish[bool] = UNKNOWN
    #: whether the user has not yet passed the guild's Membership Screening
    #: requirements
    pending: Unknownish[bool] = UNKNOWN
    #: when the user's timeout will expire and the user will be able to
    #: communicate in the guild again, null or a time in the past if the user
    #: is not timed out
    communication_disabled_until: Unknownish[typing.Optional[datetime.datetime]] = UNKNOWN


@attr.frozen(kw_only=True)
class GuildMembersChunkEvent:
    #: the id of the guild
    guild_id: Snowflake
    #: set of guild members
    members: typing.List[GuildMember]
    #: the chunk index in the expected chunks for this response (0 <=
    #: chunk_index < chunk_count)
    chunk_index: int
    #: the total number of expected chunks for this response
    chunk_count: int
    #: if passing an invalid id to REQUEST_GUILD_MEMBERS, it will be returned
    #: here
    not_found: Unknownish[typing.List[Snowflake]] = UNKNOWN
    #: if passing true to REQUEST_GUILD_MEMBERS, presences of the returned
    #: members will be here
    presences: Unknownish[typing.List[Presence]] = UNKNOWN
    #: the nonce used in the Guild Members Request
    nonce: Unknownish[str] = UNKNOWN


@attr.frozen(kw_only=True)
class GuildRoleCreateEvent:
    #: the id of the guild
    guild_id: Snowflake
    #: the role created
    role: Role


@attr.frozen(kw_only=True)
class GuildRoleUpdateEvent:
    #: the id of the guild
    guild_id: Snowflake
    #: the role updated
    role: Role


@attr.frozen(kw_only=True)
class GuildRoleDeleteEvent:
    #: id of the guild
    guild_id: Snowflake
    #: id of the role
    role_id: Snowflake


@attr.frozen(kw_only=True)
class GuildScheduledEventCreateEvent(GuildScheduledEvent):
    pass


@attr.frozen(kw_only=True)
class GuildScheduledEventUpdateEvent(GuildScheduledEvent):
    pass


@attr.frozen(kw_only=True)
class GuildScheduledEventDeleteEvent(GuildScheduledEvent):
    pass


@attr.frozen(kw_only=True)
class GuildScheduledEventUserAddEvent:
    guild_scheduled_event_id: Snowflake
    user_id: Snowflake
    guild_id: Snowflake


@attr.frozen(kw_only=True)
class GuildScheduledEventUserRemoveEvent:
    guild_scheduled_event_id: Snowflake
    user_id: Snowflake
    guild_id: Snowflake


@attr.frozen(kw_only=True)
class IntegrationCreateEvent(Integration):
    #: id of the guild
    guild_id: Snowflake


@attr.frozen(kw_only=True)
class IntegrationUpdateEvent(Integration):
    #: id of the guild
    guild_id: Snowflake


@attr.frozen(kw_only=True)
class IntegrationDeleteEvent:
    #: integration id
    id: Snowflake
    #: id of the guild
    guild_id: Snowflake
    #: id of the bot/OAuth2 application for this discord integration
    application_id: Unknownish[Snowflake] = UNKNOWN


@attr.frozen(kw_only=True)
class InviteCreateEvent:
    #: the channel the invite is for
    channel_id: Snowflake
    #: the unique invite code
    code: str
    #: the time at which the invite was created
    created_at: datetime.datetime
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
    target_application: Unknownish[typing.Dict[str, typing.Any]] = UNKNOWN


@attr.frozen(kw_only=True)
class InviteDeleteEvent:
    #: the channel of the invite
    channel_id: Snowflake
    #: the unique invite code
    code: str
    #: the guild of the invite
    guild_id: Unknownish[Snowflake] = UNKNOWN


@attr.frozen(kw_only=True)
class MessageCreateEvent(Message):
    pass


@attr.frozen(kw_only=True)
class MessageUpdateEvent:
    # TODO: this duplicates code...
    #: id of the message
    id: Snowflake
    #: id of the channel the message was sent in
    channel_id: Snowflake
    #: the author of this message (not guaranteed to be a valid user, see
    #: below)
    author: Unknownish[User] = UNKNOWN
    #: member properties for this message's author
    member: Unknownish[GuildMember] = UNKNOWN
    #: contents of the message
    content: Unknownish[str] = UNKNOWN
    #: when this message was sent
    timestamp: Unknownish[datetime.datetime] = UNKNOWN
    #: when this message was edited (or null if never)
    edited_timestamp: Unknownish[typing.Optional[datetime.datetime]] = UNKNOWN
    #: whether this was a TTS message
    tts: Unknownish[bool] = UNKNOWN
    #: whether this message mentions everyone
    mention_everyone: Unknownish[bool] = UNKNOWN
    #: users specifically mentioned in the message
    mentions: Unknownish[typing.List[User]] = UNKNOWN
    #: roles specifically mentioned in this message
    mention_roles: Unknownish[typing.List[Snowflake]] = UNKNOWN
    #: channels specifically mentioned in this message
    mention_channels: Unknownish[typing.List[ChannelMention]] = UNKNOWN
    #: any attached files
    attachments: Unknownish[typing.List[Attachment]] = UNKNOWN
    #: any embedded content
    embeds: Unknownish[typing.List[Embed]] = UNKNOWN
    #: whether this message is pinned
    pinned: Unknownish[bool] = UNKNOWN
    #: type of message
    type: Unknownish[int] = UNKNOWN
    #: the message associated with the message_reference
    referenced_message: Unknownish[typing.Optional[Message]] = UNKNOWN
    #: id of the guild the message was sent in
    guild_id: Unknownish[Snowflake] = UNKNOWN
    #: reactions to the message
    reactions: Unknownish[typing.List[Reaction]] = UNKNOWN
    #: used for validating a message was sent
    nonce: Unknownish[typing.Union[int, str]] = UNKNOWN
    #: if the message is generated by a webhook, this is the webhook's id
    webhook_id: Unknownish[Snowflake] = UNKNOWN
    #: sent with Rich Presence-related chat embeds
    activity: Unknownish[MessageActivity] = UNKNOWN
    #: sent with Rich Presence-related chat embeds
    application: Unknownish[typing.Dict[str, typing.Any]] = UNKNOWN
    #: if the message is a response to an Interaction or application-owned
    #: webhook, this is the id of the interaction's application
    application_id: Unknownish[Snowflake] = UNKNOWN
    #: data showing the source of a crosspost, channel follow add, pin, or
    #: reply message
    message_reference: Unknownish[MessageReference] = UNKNOWN
    #: message flags combined as a bitfield
    flags: Unknownish[int] = UNKNOWN
    #: sent if the message is a response to an Interaction
    interaction: Unknownish[MessageInteraction] = UNKNOWN
    #: the thread that was started from this message, includes thread member
    #: object
    thread: Unknownish[Channel] = UNKNOWN
    #: sent if the message contains components like buttons, action rows, or
    #: other interactive components
    components: Unknownish[typing.List[Component]] = UNKNOWN
    #: sent if the message contains stickers
    sticker_items: Unknownish[typing.List[StickerItem]] = UNKNOWN
    #: Deprecated the stickers sent with the message
    stickers: Unknownish[typing.List[Sticker]] = UNKNOWN


@attr.frozen(kw_only=True)
class MessageDeleteEvent:
    #: the id of the message
    id: Snowflake
    #: the id of the channel
    channel_id: Snowflake
    #: the id of the guild
    guild_id: Unknownish[Snowflake] = UNKNOWN


@attr.frozen(kw_only=True)
class MessageDeleteBulkEvent:
    #: the ids of the messages
    ids: typing.List[Snowflake]
    #: the id of the channel
    channel_id: Snowflake
    #: the id of the guild
    guild_id: Unknownish[Snowflake] = UNKNOWN


@attr.frozen(kw_only=True)
class MessageReactionAddEvent:
    #: the id of the user
    user_id: Snowflake
    #: the id of the channel
    channel_id: Snowflake
    #: the id of the message
    message_id: Snowflake
    #: the emoji used to react - example
    emoji: typing.Dict[str, typing.Any]
    #: the id of the guild
    guild_id: Unknownish[Snowflake] = UNKNOWN
    #: the member who reacted if this happened in a guild
    member: Unknownish[GuildMember] = UNKNOWN


@attr.frozen(kw_only=True)
class MessageReactionRemoveEvent:
    #: the id of the user
    user_id: Snowflake
    #: the id of the channel
    channel_id: Snowflake
    #: the id of the message
    message_id: Snowflake
    #: the emoji used to react - example
    emoji: typing.Dict[str, typing.Any]
    #: the id of the guild
    guild_id: Unknownish[Snowflake] = UNKNOWN


@attr.frozen(kw_only=True)
class MessageReactionRemoveAllEvent:
    #: the id of the channel
    channel_id: Snowflake
    #: the id of the message
    message_id: Snowflake
    #: the id of the guild
    guild_id: Unknownish[Snowflake] = UNKNOWN


@attr.frozen(kw_only=True)
class MessageReactionRemoveEmojiEvent:
    #: the id of the channel
    channel_id: Snowflake
    #: the id of the message
    message_id: Snowflake
    #: the emoji that was removed
    emoji: typing.Dict[str, typing.Any]
    #: the id of the guild
    guild_id: Unknownish[Snowflake] = UNKNOWN


@attr.frozen(kw_only=True)
class PresenceUpdateUser:
    # TODO: see note below
    id: Snowflake


@attr.frozen(kw_only=True)
class PresenceUpdateEvent:
    # TODO: The user object within this event can be partial, the only
    # field which must be sent is the id field, everything else is optional.
    # Along with this limitation, no fields are required, and the types of
    # the fields are not validated. Your client should expect any combination
    # of fields and types within this eventyping.
    user: Unknownish[PresenceUpdateUser] = UNKNOWN
    guild_id: Unknownish[Snowflake] = UNKNOWN
    status: Unknownish[str] = UNKNOWN
    activities: Unknownish[typing.List[Activity]] = UNKNOWN
    client_status: Unknownish[ClientStatus] = UNKNOWN


@attr.frozen(kw_only=True)
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


@attr.frozen(kw_only=True)
class Activity:
    #: the activity's name
    name: str
    #: activity type
    type: ActivityTypes
    #: unix timestamp (in milliseconds) of when the activity was added to the
    #: user's session
    created_at: int
    #: stream url, is validated when type is 1
    url: Unknownish[typing.Optional[str]] = UNKNOWN
    #: unix timestamps for start and/or end of the game
    timestamps: Unknownish[ActivityTimestamps] = UNKNOWN
    #: application id for the game
    application_id: Unknownish[Snowflake] = UNKNOWN
    #: what the player is currently doing
    details: Unknownish[typing.Optional[str]] = UNKNOWN
    #: the user's current party status
    state: Unknownish[typing.Optional[str]] = UNKNOWN
    #: the emoji used for a custom status
    emoji: Unknownish[typing.Optional[ActivityEmoji]] = UNKNOWN
    #: information for the current party of the player
    party: Unknownish[ActivityParty] = UNKNOWN
    #: images for the presence and their hover texts
    assets: Unknownish[ActivityAssets] = UNKNOWN
    #: secrets for Rich Presence joining and spectating
    secrets: Unknownish[ActivitySecrets] = UNKNOWN
    #: whether or not the activity is an instanced game session
    instance: Unknownish[bool] = UNKNOWN
    #: activity flagsORd together, describes what the payload includes
    flags: Unknownish[ActivityFlags] = UNKNOWN
    #: the custom buttons shown in the Rich Presence (max 2)
    buttons: Unknownish[typing.List[typing.Tuple[str, str]]] = UNKNOWN


class ActivityTypes(enum.Enum):
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


@attr.frozen(kw_only=True)
class ActivityTimestamps:

    #: unix time (in milliseconds) of when the activity started
    start: Unknownish[int] = UNKNOWN
    #: unix time (in milliseconds) of when the activity ends
    end: Unknownish[int] = UNKNOWN


@attr.frozen(kw_only=True)
class ActivityEmoji:
    #: the name of the emoji
    name: str
    #: the id of the emoji
    id: Unknownish[Snowflake] = UNKNOWN
    #: whether this emoji is animated
    animated: Unknownish[bool] = UNKNOWN


@attr.frozen(kw_only=True)
class ActivityParty:
    #: the id of the party
    id: Unknownish[str] = UNKNOWN
    #: used to show the party's current and maximum size
    size: Unknownish[typing.Tuple[int, int]] = UNKNOWN


@attr.frozen(kw_only=True)
class ActivityAssets:
    # TODO:
    # https://github.com/discord/discord-api-docs/commit/0a91423248b7de682515021de03d29d56f36b4f0
    #: the id for a large asset of the activity, usually a snowflake
    large_image: Unknownish[str] = UNKNOWN
    #: text displayed when hovering over the large image of the activity
    large_text: Unknownish[str] = UNKNOWN
    #: the id for a small asset of the activity, usually a snowflake
    small_image: Unknownish[str] = UNKNOWN
    #: text displayed when hovering over the small image of the activity
    small_text: Unknownish[str] = UNKNOWN


@attr.frozen(kw_only=True)
class ActivitySecrets:

    #: the secret for joining a party
    join: Unknownish[str] = UNKNOWN
    #: the secret for spectating a game
    spectate: Unknownish[str] = UNKNOWN
    #: the secret for a specific instanced match
    match: Unknownish[str] = UNKNOWN


class ActivityFlags(enum.IntFlag):
    INSTANCE = 1 << 0
    JOIN = 1 << 1
    SPECTATE = 1 << 2
    JOIN_REQUEST = 1 << 3
    SYNC = 1 << 4
    PLAY = 1 << 5
    PARTY_PRIVACY_FRIENDS = 1 << 6
    PARTY_PRIVACY_VOICE_CHANNEL = 1 << 7
    EMBEDDED = 1 << 8


# TODO: this gets sent when setting activity, but is not recved
@attr.frozen(kw_only=True)
class ActivityButtons:
    #: the text shown on the button (1-32 characters)
    label: str
    #: the url opened when clicking the button (1-512 characters)
    url: str


@attr.frozen(kw_only=True)
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


@attr.frozen(kw_only=True)
class UserUpdateEvent(User):
    pass


@attr.frozen(kw_only=True)
class VoiceStateUpdateEvent(VoiceState):
    pass


@attr.frozen(kw_only=True)
class VoiceServerUpdateEvent:
    #: voice connection token
    token: str
    #: the guild this voice server update is for
    guild_id: Snowflake
    #: the voice server host
    endpoint: typing.Optional[str]


@attr.frozen(kw_only=True)
class WebhooksUpdateEvent:
    #: id of the guild
    guild_id: Snowflake
    #: id of the channel
    channel_id: Snowflake


@attr.frozen(kw_only=True)
class InteractionCreateEvent(Interaction):
    pass


@attr.frozen(kw_only=True)
class StageInstanceCreateEvent(StageInstance):
    pass


@attr.frozen(kw_only=True)
class StageInstanceUpdateEvent(StageInstance):
    pass


@attr.frozen(kw_only=True)
class StageInstanceDeleteEvent(StageInstance):
    pass


@attr.frozen(kw_only=True)
class SessionStartLimit:
    #: The total number of session starts the current user is allowed
    total: int
    #: The remaining number of session starts the current user is allowed
    remaining: int
    #: The number of milliseconds after which the limit resets
    reset_after: int
    #: The number of identify requests allowed per 5 seconds
    max_concurrency: int


@attr.frozen(kw_only=True)
class GatewayResponse:
    url: str


@attr.frozen(kw_only=True)
class DetailedGatewayResponse:
    url: str
    shards: int
    session_start_limit: SessionStartLimit
