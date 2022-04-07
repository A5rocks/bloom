from __future__ import annotations

import datetime
import enum
import typing

import attr

from bloom.ll.models.base import UNKNOWN, Snowflake, Unknownish
from bloom.ll.models.permissions import BitwisePermissionFlags
from bloom.ll.models.user import User

# docs in this module are copied from the Discord Documentation


@attr.frozen(kw_only=True)
class Channel:
    #: the id of this channel
    id: Snowflake
    #: the type of channel
    type: ChannelTypes
    #: amount of seconds a user has to wait before sending another message
    #: (0-21600); bots, as well as users with the permission manage_messages
    #: or manage_channel, are unaffected
    rate_limit_per_user: Unknownish[int] = UNKNOWN
    #: the id of the guild (may be missing for some channel objects received
    #: over gateway guild dispatches)
    guild_id: Unknownish[Snowflake] = UNKNOWN
    #: sorting position of the channel
    position: Unknownish[int] = UNKNOWN
    #: explicit permission overwrites for members and roles
    permission_overwrites: Unknownish[typing.List[Overwrite]] = UNKNOWN
    #: the name of the channel (1-100 characters)
    name: Unknownish[typing.Optional[str]] = UNKNOWN
    #: the channel topic (0-1024 characters)
    topic: Unknownish[typing.Optional[str]] = UNKNOWN
    #: whether the channel is nsfw
    nsfw: Unknownish[bool] = UNKNOWN
    #: the id of the last message sent in this channel (may not point to an
    #: existing or valid message)
    last_message_id: Unknownish[typing.Optional[Snowflake]] = UNKNOWN
    #: the bitrate (in bits) of the voice channel
    bitrate: Unknownish[int] = UNKNOWN
    #: the user limit of the voice channel
    user_limit: Unknownish[int] = UNKNOWN
    #: the recipients of the DM
    recipients: Unknownish[typing.List[User]] = UNKNOWN
    #: icon hash of the group DM
    icon: Unknownish[typing.Optional[str]] = UNKNOWN
    #: id of the creator of the group DM or thread
    owner_id: Unknownish[Snowflake] = UNKNOWN
    #: application id of the group DM creator if it is bot-created
    application_id: Unknownish[Snowflake] = UNKNOWN
    #: for guild channels: id of the parent category for a channel (each
    #: parent category can contain up to 50 channels), for threads: id of the
    #: text channel this thread was created
    parent_id: Unknownish[typing.Optional[Snowflake]] = UNKNOWN
    #: when the last pinned message was pinned. This may be null in events
    #: such as GUILD_CREATE when a message is not pinned.
    last_pin_timestamp: Unknownish[typing.Optional[datetime.datetime]] = UNKNOWN
    #: voice region id for the voice channel, automatic when set to null
    rtc_region: Unknownish[typing.Optional[str]] = UNKNOWN
    #: the camera video quality mode of the voice channel, 1 when not present
    video_quality_mode: Unknownish[int] = UNKNOWN
    #: an approximate count of messages in a thread, stops counting at 50
    message_count: Unknownish[int] = UNKNOWN
    #: an approximate count of users in a thread, stops counting at 50
    member_count: Unknownish[int] = UNKNOWN
    #: thread-specific fields not needed by other channels
    thread_metadata: Unknownish[ThreadMetadata] = UNKNOWN
    #: thread member object for the current user, if they have joined the
    #: thread, only included on certain API endpoints
    member: Unknownish[ThreadMember] = UNKNOWN
    #: default duration that the clients (not the API) will use for newly
    #: created threads, in minutes, to automatically archive the thread after
    #: recent activity, can be set to: 60, 1440, 4320, 10080
    default_auto_archive_duration: Unknownish[int] = UNKNOWN
    #: computed permissions for the invoking user in the channel, including
    #: overwrites, only included when part of the resolved data received on an
    #: application command interaction
    permissions: Unknownish[BitwisePermissionFlags] = UNKNOWN


class ChannelTypes(enum.Enum):
    #: a text channel within a server
    GUILD_TEXT = 0
    #: a direct message between users
    DM = 1
    #: a voice channel within a server
    GUILD_VOICE = 2
    #: a direct message between multiple users
    GROUP_DM = 3
    #: an organizational category that contains up to 50 channels
    GUILD_CATEGORY = 4
    #: a channel that users can follow and crosspost into their own server
    GUILD_NEWS = 5
    #: a temporary sub-channel within a GUILD_NEWS channel
    GUILD_NEWS_THREAD = 10
    #: a temporary sub-channel within a GUILD_TEXT channel
    GUILD_PUBLIC_THREAD = 11
    #: a temporary sub-channel within a GUILD_TEXT channel that is only
    #: viewable by those invited and those with the MANAGE_THREADS permission
    GUILD_PRIVATE_THREAD = 12
    #: a voice channel for hosting events with an audience
    GUILD_STAGE_VOICE = 13
    #: the channel in a hub containing the listed servers
    GUILD_DIRECTORY = 14


class VideoQualityModes(enum.Enum):
    #: Discord chooses the quality for optimal performance
    AUTO = 1
    #: 720p
    FULL = 2


class MessageTypes(enum.Enum):
    DEFAULT = 0
    RECIPIENT_ADD = 1
    RECIPIENT_REMOVE = 2
    CALL = 3
    CHANNEL_NAME_CHANGE = 4
    CHANNEL_ICON_CHANGE = 5
    CHANNEL_PINNED_MESSAGE = 6
    GUILD_MEMBER_JOIN = 7
    USER_PREMIUM_GUILD_SUBSCRIPTION = 8
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_1 = 9
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_2 = 10
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_3 = 11
    CHANNEL_FOLLOW_ADD = 12
    GUILD_DISCOVERY_DISQUALIFIED = 14
    GUILD_DISCOVERY_REQUALIFIED = 15
    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
    THREAD_CREATED = 18
    REPLY = 19
    CHAT_INPUT_COMMAND = 20
    THREAD_STARTER_MESSAGE = 21
    GUILD_INVITE_REMINDER = 22
    CONTEXT_MENU_COMMAND = 23


@attr.frozen(kw_only=True)
class MessageActivity:
    #: type of message activity
    type: int
    #: party_id from a Rich Presence event
    party_id: Unknownish[str] = UNKNOWN


class MessageActivityTypes(enum.Enum):
    JOIN = 1
    SPECTATE = 2
    LISTEN = 3
    JOIN_REQUEST = 5


class MessageFlags(enum.Enum):
    #: this message has been published to subscribed channels (via Channel
    #: Following)
    CROSSPOSTED = 1 << 0
    #: this message originated from a message in another channel (via Channel
    #: Following)
    IS_CROSSPOST = 1 << 1
    #: do not include any embeds when serializing this message
    SUPPRESS_EMBEDS = 1 << 2
    #: the source message for this crosspost has been deleted (via Channel
    #: Following)
    SOURCE_MESSAGE_DELETED = 1 << 3
    #: this message came from the urgent message system
    URGENT = 1 << 4
    #: this message has an associated thread, with the same id as the message
    HAS_THREAD = 1 << 5
    #: this message is only visible to the user who invoked the Interaction
    EPHEMERAL = 1 << 6
    #: this message is an Interaction Response and the bot is "thinking"
    LOADING = 1 << 7
    #: this message failed to mention some roles and add their members to the
    #: thread
    FAILED_TO_MENTION_SOME_ROLES_IN_THREAD = 1 << 8


@attr.frozen(kw_only=True)
class MessageReference:
    #: id of the originating message's channel
    channel_id: Unknownish[Snowflake] = UNKNOWN
    #: id of the originating message
    message_id: Unknownish[Snowflake] = UNKNOWN
    #: id of the originating message's guild
    guild_id: Unknownish[Snowflake] = UNKNOWN
    #: when sending, whether to error if the referenced message doesn't exist
    #: instead of sending as a normal (non-reply) message, default true
    fail_if_not_exists: Unknownish[bool] = UNKNOWN


@attr.frozen(kw_only=True)
class FollowedChannel:
    #: source channel id
    channel_id: Snowflake
    #: created target webhook id
    webhook_id: Snowflake


@attr.frozen(kw_only=True)
class Reaction:
    #: times this emoji has been used to react
    count: int
    #: whether the current user reacted using this emoji
    me: bool
    #: emoji information
    emoji: typing.Dict[str, typing.Any]


@attr.frozen(kw_only=True)
class Overwrite:
    #: role or user id
    id: Snowflake
    #: either 0 (role) or 1 (member)
    type: int
    #: permission bit set
    allow: BitwisePermissionFlags
    #: permission bit set
    deny: BitwisePermissionFlags


@attr.frozen(kw_only=True)
class ThreadMetadata:
    #: whether the thread is archived
    archived: bool
    #: duration in minutes to automatically archive the thread after recent
    #: activity, can be set to: 60, 1440, 4320, 10080
    auto_archive_duration: int
    #: timestamp when the thread's archive status was last changed, used for
    #: calculating recent activity
    archive_timestamp: datetime.datetime
    #: whether the thread is locked; when a thread is locked, only users with
    #: MANAGE_THREADS can unarchive it
    locked: bool
    #: whether non-moderators can add other non-moderators to a thread; only
    #: available on private threads
    invitable: Unknownish[bool] = UNKNOWN
    #: timestamp when the thread was created; only populated for threads
    #: created after 2022-01-09
    create_timestamp: Unknownish[typing.Optional[datetime.datetime]] = UNKNOWN


@attr.frozen(kw_only=True)
class ThreadMember:
    #: the id of the thread
    id: Unknownish[Snowflake] = UNKNOWN
    #: the id of the user
    user_id: Unknownish[Snowflake] = UNKNOWN
    #: the time the current user last joined the thread
    join_timestamp: datetime.datetime
    #: any user-thread settings, currently only used for notifications
    flags: int


@attr.frozen(kw_only=True)
class Embed:
    #: title of embed
    title: Unknownish[str] = UNKNOWN
    #: type of embed (always "rich" for webhook embeds)
    type: Unknownish[str] = UNKNOWN
    #: description of embed
    description: Unknownish[str] = UNKNOWN
    #: url of embed
    url: Unknownish[str] = UNKNOWN
    #: timestamp of embed content
    timestamp: Unknownish[datetime.datetime] = UNKNOWN
    #: color code of the embed
    color: Unknownish[int] = UNKNOWN
    #: footer information
    footer: Unknownish[EmbedFooter] = UNKNOWN
    #: image information
    image: Unknownish[EmbedImage] = UNKNOWN
    #: thumbnail information
    thumbnail: Unknownish[EmbedThumbnail] = UNKNOWN
    #: video information
    video: Unknownish[EmbedVideo] = UNKNOWN
    #: provider information
    provider: Unknownish[EmbedProvider] = UNKNOWN
    #: author information
    author: Unknownish[EmbedAuthor] = UNKNOWN
    #: fields information
    fields: Unknownish[typing.List[EmbedField]] = UNKNOWN


class EmbedTypes(enum.Enum):
    #: generic embed rendered from embed attributes
    RICH = 'rich'
    #: image embed
    IMAGE = 'image'
    #: video embed
    VIDEO = 'video'
    #: animated gif image embed rendered as a video embed
    GIFV = 'gifv'
    #: article embed
    ARTICLE = 'article'
    #: link embed
    LINK = 'link'


@attr.frozen(kw_only=True)
class EmbedThumbnail:
    #: source url of thumbnail (only supports http(s) and attachments)
    url: str
    #: a proxied url of the thumbnail
    proxy_url: Unknownish[str] = UNKNOWN
    #: height of thumbnail
    height: Unknownish[int] = UNKNOWN
    #: width of thumbnail
    width: Unknownish[int] = UNKNOWN


@attr.frozen(kw_only=True)
class EmbedVideo:
    #: source url of video
    url: Unknownish[str] = UNKNOWN
    #: a proxied url of the video
    proxy_url: Unknownish[str] = UNKNOWN
    #: height of video
    height: Unknownish[int] = UNKNOWN
    #: width of video
    width: Unknownish[int] = UNKNOWN


@attr.frozen(kw_only=True)
class EmbedImage:
    #: source url of image (only supports http(s) and attachments)
    url: str
    #: a proxied url of the image
    proxy_url: Unknownish[str] = UNKNOWN
    #: height of image
    height: Unknownish[int] = UNKNOWN
    #: width of image
    width: Unknownish[int] = UNKNOWN


@attr.frozen(kw_only=True)
class EmbedProvider:
    #: name of provider
    name: Unknownish[str] = UNKNOWN
    #: url of provider
    url: Unknownish[str] = UNKNOWN


@attr.frozen(kw_only=True)
class EmbedAuthor:
    #: name of author
    name: str
    #: url of author
    url: Unknownish[str] = UNKNOWN
    #: url of author icon (only supports http(s) and attachments)
    icon_url: Unknownish[str] = UNKNOWN
    #: a proxied url of author icon
    proxy_icon_url: Unknownish[str] = UNKNOWN


@attr.frozen(kw_only=True)
class EmbedFooter:
    #: footer text
    text: str
    #: url of footer icon (only supports http(s) and attachments)
    icon_url: Unknownish[str] = UNKNOWN
    #: a proxied url of footer icon
    proxy_icon_url: Unknownish[str] = UNKNOWN


@attr.frozen(kw_only=True)
class EmbedField:
    #: name of the field
    name: str
    #: value of the field
    value: str
    #: whether or not this field should display inline
    inline: Unknownish[bool] = UNKNOWN


@attr.frozen(kw_only=True)
class Attachment:
    #: attachment id
    id: Snowflake
    #: name of file attached
    filename: str
    #: description for the file
    description: Unknownish[str] = UNKNOWN
    #: size of file in bytes
    size: int
    #: source url of file
    url: str
    #: a proxied url of file
    proxy_url: str
    #: the attachment's media type
    content_type: Unknownish[str] = UNKNOWN
    #: height of file (if image)
    height: Unknownish[typing.Optional[int]] = UNKNOWN
    #: width of file (if image)
    width: Unknownish[typing.Optional[int]] = UNKNOWN
    #: whether this attachment is ephemeral. Ephemeral attachments will
    #: automatically be removed after a set period of time. Ephemeral
    #: attachments on messages are guaranteed to be available as long as the
    #: message itself exists.
    ephemeral: Unknownish[bool] = UNKNOWN


@attr.frozen(kw_only=True)
class ChannelMention:
    #: id of the channel
    id: Snowflake
    #: id of the guild containing the channel
    guild_id: Snowflake
    #: the type of channel
    type: int
    #: the name of the channel
    name: str


class AllowedMentionTypes(enum.Enum):
    #: Controls role mentions
    ROLE_MENTIONS = 'roles'
    #: Controls user mentions
    USER_MENTIONS = 'users'
    #: Controls @everyone and @here mentions
    EVERYONE_MENTIONS = 'everyone'


@attr.frozen(kw_only=True)
class AllowedMentions:
    #: An array of allowed mention types to parse from the contentyping.
    parse: typing.List[AllowedMentionTypes]
    #: Array of role_ids to mention (Max size of 100)
    roles: typing.List[Snowflake]
    #: Array of user_ids to mention (Max size of 100)
    users: typing.List[Snowflake]
    #: For replies, whether to mention the author of the message being replied
    #: to (default false)
    replied_user: bool


@attr.frozen(kw_only=True)
class ResponseBody:
    #: the private, archived threads the current user has joined
    threads: typing.List[Channel]
    #: a thread member object for each returned thread the current user has
    #: joined
    members: typing.List[ThreadMember]
    #: whether there are potentially additional threads that could be returned
    #: on a subsequent call
    has_more: bool


# TODO: blocked on https://github.com/python-attrs/attrs/issues/842
attr.resolve_types(Channel, globals(), locals())
