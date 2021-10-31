from __future__ import annotations

import datetime as dt
import typing as t
from enum import Enum, IntFlag

import attr

from .application_commands import MessageInteraction
from .base import UNKNOWN, Snowflake, Unknownish
from .channel import (Attachment, Channel, ChannelMention, ChannelTypes, Embed,
                      MessageActivity, MessageReference, Reaction,
                      ThreadMember)
from .emoji import Emoji
from .guild import Guild, GuildMember, Integration
from .interaction import Interaction
from .message import Message
from .message_components import Component
from .permissions import Role
from .stage_instance import StageInstance
from .sticker import Sticker, StickerItem
from .user import User
from .voice import VoiceState


@attr.frozen(kw_only=True)
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


@attr.frozen(kw_only=True)
class GatewayVoiceStateUpdateEvent:
    #: id of the guild
    guild_id: Snowflake
    #: id of the voice channel client wants to join (null if disconnecting)
    channel_id: t.Optional[Snowflake]
    #: is the client muted
    self_mute: bool
    #: is the client deafened
    self_deaf: bool


@attr.frozen(kw_only=True)
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
    guilds: t.List[t.Dict[str, t.Any]]
    #: used for resuming connections
    session_id: str
    #: contains id and flags
    application: t.Dict[str, t.Any]
    #: the shard information associated with this session, if sent when
    #: identifying
    shard: Unknownish[t.List[int]] = UNKNOWN


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
    pass


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
    parent_id: Unknownish[t.Optional[Snowflake]] = UNKNOWN
    #: the type of channel
    type: ChannelTypes


@attr.frozen(kw_only=True)
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


# TODO: blocked on https://github.com/python-attrs/attrs/issues/842
attr.resolve_types(ThreadMember)


@attr.frozen(kw_only=True)
class ThreadMemberUpdateEvent(ThreadMember):
    pass


@attr.frozen(kw_only=True)
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


@attr.frozen(kw_only=True)
class ChannelPinsUpdateEvent:
    #: the id of the channel
    channel_id: Snowflake
    #: the id of the guild
    guild_id: Unknownish[Snowflake] = UNKNOWN
    #: the time at which the most recent pinned message was pinned
    last_pin_timestamp: Unknownish[t.Optional[dt.datetime]] = UNKNOWN


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
    # TODO: A partial guild object. Represents an Offline Guild, or a Guild
    # whose information has not been provided through Guild Create events
    # during the Gateway connect.
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
    emojis: t.List[Emoji]


@attr.frozen(kw_only=True)
class GuildStickersUpdateEvent:
    #: id of the guild
    guild_id: Snowflake
    #: array of stickers
    stickers: t.List[Sticker]


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
    roles: t.List[Snowflake]
    #: the user
    user: User
    # TODO: does this get sent at all?
    #: the member's guild avatar hash
    avatar: Unknownish[t.Optional[str]] = UNKNOWN
    # TODO: when can this be null?
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


@attr.frozen(kw_only=True)
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
    target_application: Unknownish[t.Dict[str, t.Any]] = UNKNOWN


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
    timestamp: Unknownish[dt.datetime] = UNKNOWN
    #: when this message was edited (or null if never)
    edited_timestamp: Unknownish[t.Optional[dt.datetime]] = UNKNOWN
    #: whether this was a TTS message
    tts: Unknownish[bool] = UNKNOWN
    #: whether this message mentions everyone
    mention_everyone: Unknownish[bool] = UNKNOWN
    #: users specifically mentioned in the message
    mentions: Unknownish[t.List[User]] = UNKNOWN
    #: roles specifically mentioned in this message
    mention_roles: Unknownish[t.List[Snowflake]] = UNKNOWN
    #: channels specifically mentioned in this message
    mention_channels: Unknownish[t.List[ChannelMention]] = UNKNOWN
    #: any attached files
    attachments: Unknownish[t.List[Attachment]] = UNKNOWN
    #: any embedded content
    embeds: Unknownish[t.List[Embed]] = UNKNOWN
    #: whether this message is pinned
    pinned: Unknownish[bool] = UNKNOWN
    #: type of message
    type: Unknownish[int] = UNKNOWN
    #: the message associated with the message_reference
    referenced_message: Unknownish[t.Optional[Message]] = UNKNOWN
    #: id of the guild the message was sent in
    guild_id: Unknownish[Snowflake] = UNKNOWN
    #: reactions to the message
    reactions: Unknownish[t.List[Reaction]] = UNKNOWN
    #: used for validating a message was sent
    nonce: Unknownish[t.Union[int, str]] = UNKNOWN
    #: if the message is generated by a webhook, this is the webhook's id
    webhook_id: Unknownish[Snowflake] = UNKNOWN
    #: sent with Rich Presence-related chat embeds
    activity: Unknownish[MessageActivity] = UNKNOWN
    #: sent with Rich Presence-related chat embeds
    application: Unknownish[t.Dict[str, t.Any]] = UNKNOWN
    #: if the message is a response to an Interaction, this is the id of the
    #: interaction's application
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
    components: Unknownish[t.List[Component]] = UNKNOWN
    #: sent if the message contains stickers
    sticker_items: Unknownish[t.List[StickerItem]] = UNKNOWN
    #: Deprecated the stickers sent with the message
    stickers: Unknownish[t.List[Sticker]] = UNKNOWN


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
    ids: t.List[Snowflake]
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
    emoji: t.Dict[str, t.Any]
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
    emoji: t.Dict[str, t.Any]
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
    emoji: t.Dict[str, t.Any]
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
    # of fields and types within this event.
    user: Unknownish[PresenceUpdateUser] = UNKNOWN
    guild_id: Unknownish[Snowflake] = UNKNOWN
    status: Unknownish[str] = UNKNOWN
    activities: Unknownish[t.List[Activity]] = UNKNOWN
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
    emoji: Unknownish[t.Optional[ActivityEmoji]] = UNKNOWN
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
    buttons: Unknownish[t.List[t.Tuple[str, str]]] = UNKNOWN


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
    size: Unknownish[t.Tuple[int, int]] = UNKNOWN


@attr.frozen(kw_only=True)
class ActivityAssets:

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


class ActivityFlags(IntFlag):
    INSTANCE = 1
    JOIN = 2
    SPECTATE = 4
    JOIN_REQUEST = 8
    SYNC = 16
    PLAY = 32


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
    endpoint: t.Optional[str]


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
