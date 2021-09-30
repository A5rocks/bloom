from __future__ import annotations

import datetime
import json
import typing

import attr
from cattr import Converter

from bloom._compat import Literal
from bloom.models.application import Application
from bloom.models.application_commands import (
    ApplicationCommand, ApplicationCommandOption,
    ApplicationCommandPermissions, CommandTypes,
    GuildApplicationCommandPermissions, InteractionResponse)
from bloom.models.audit_log import AuditLog, AuditLogEvents
from bloom.models.base import UNKNOWN, UNKNOWN_TYPE, Snowflake, Unknownish
from bloom.models.channel import (AllowedMentions, Attachment, Channel,
                                  ChannelTypes, Embed, FollowedChannel,
                                  MessageFlags, MessageReference, Overwrite,
                                  ThreadMember, VideoQualityModes)
from bloom.models.emoji import Emoji
from bloom.models.gateway import DetailedGatewayResponse, GatewayResponse
from bloom.models.guild import (Ban, DefaultMessageNotificationLevel,
                                ExplicitContentFilterLevel, Guild,
                                GuildFeatures, GuildMember, GuildPreview,
                                GuildWidget, Integration,
                                ModifyGuildChannelPositionsParameters,
                                ModifyGuildRolePositionsParameters, PruneCount,
                                SystemChannelFlags, UserConnection,
                                VerificationLevel, WelcomeScreen,
                                WelcomeScreenChannel, WidgetStyleOptions)
from bloom.models.guild_template import GuildTemplate
from bloom.models.invite import Invite, InviteMetadata, InviteTargetTypes
from bloom.models.message import Message
from bloom.models.message_components import Component
from bloom.models.oauth2 import AuthorizationInformation
from bloom.models.permissions import BitwisePermissionFlags, Role
from bloom.models.stage_instance import PrivacyLevel, StageInstance
from bloom.models.sticker import NitroStickerPacks, Sticker
from bloom.models.user import User
from bloom.models.voice import VoiceRegion
from bloom.models.webhook import Webhook
from bloom.rest.models import Request


def prepare(rest: RawRest, input_dict: typing.Dict[str, object]) -> typing.Dict[str, object]:
    res: typing.Dict[str, object] = rest.conv.unstructure({
        k: v for k, v in input_dict.items() if v is not UNKNOWN
    })

    return res


@attr.define()
class RawRest:
    # every single API method.
    conv: Converter

    def get_guild_audit_log(
            self,
            guild_id: Snowflake,
            *,
            user_id: Snowflake,
            action_type: AuditLogEvents,
            before: Snowflake,
            limit: int
    ) -> Request[AuditLog]:
        return Request[AuditLog](
            'GET',
            '/guilds/{guild_id}/audit-logs',
            {'guild_id': guild_id},
            params=prepare(self, {
                'user_id': user_id,
                'action_type': action_type,
                'before': before,
                'limit': limit,
            })
        )

    def get_channel(self, channel_id: Snowflake) -> Request[Channel]:
        return Request[Channel]('GET', '/channels/{channel_id}', {'channel_id': channel_id})

    def modify_channel(
            self,
            channel_id: Snowflake,
            *,
            # TODO: mypy_extensions.Expand[TypedDict] might help.
            name: Unknownish[str] = UNKNOWN,
            # base64 encoded icon
            icon: Unknownish[str] = UNKNOWN,
            type: Unknownish[ChannelTypes] = UNKNOWN,
            position: Unknownish[typing.Optional[int]] = UNKNOWN,
            topic: Unknownish[typing.Optional[str]] = UNKNOWN,
            nsfw: Unknownish[typing.Optional[bool]] = UNKNOWN,
            rate_limit_per_user: Unknownish[typing.Optional[int]] = UNKNOWN,
            bitrate: Unknownish[typing.Optional[int]] = UNKNOWN,
            user_limit: Unknownish[typing.Optional[int]] = UNKNOWN,
            permission_overwrites: Unknownish[typing.Optional[typing.List[Overwrite]]] = UNKNOWN,
            parent_id: Unknownish[typing.Optional[Snowflake]] = UNKNOWN,
            rtc_region: Unknownish[typing.Optional[str]] = UNKNOWN,
            video_quality_mode: Unknownish[typing.Optional[VideoQualityModes]] = UNKNOWN,
            default_auto_archive_duration: Unknownish[typing.Optional[int]] = UNKNOWN,
            # thread options (TODO: an ADT method?)
            archived: Unknownish[bool] = UNKNOWN,
            auto_archive_duration: Unknownish[int] = UNKNOWN,
            locked: Unknownish[bool] = UNKNOWN,
            # audit log
            reason: Unknownish[str] = UNKNOWN,
    ) -> Request[Channel]:
        return Request[Channel](
            'PATCH',
            '/channels/{channel_id}',
            {'channel_id': channel_id},
            json=prepare(self, {
                'name': name,
                'icon': icon,
                'type': type,
                'position': position,
                'topic': topic,
                'nsfw': nsfw,
                'rate_limit_per_user': rate_limit_per_user,
                'bitrate': bitrate,
                'user_limit': user_limit,
                'permission_overwrites': permission_overwrites,
                'parent_id': parent_id,
                'rtc_region': rtc_region,
                'video_quality_mode': video_quality_mode,
                'default_auto_archive_duration': default_auto_archive_duration,
                'archived': archived,
                'auto_archive_duration': auto_archive_duration,
                'locked': locked,
                'rate_limit_per_user': rate_limit_per_user,
            }),
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def delete_channel(
            self,
            channel_id: Snowflake,
            *,
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[Channel]:
        return Request[Channel](
            'DELETE',
            '/channels/{channel_id}',
            {'channel_id': channel_id},
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def get_channel_messages(
            self,
            channel_id: Snowflake,
            *,
            around: Unknownish[Snowflake] = UNKNOWN,
            before: Unknownish[Snowflake] = UNKNOWN,
            after: Unknownish[Snowflake] = UNKNOWN,
            limit: Unknownish[int] = UNKNOWN,
    ) -> Request[typing.List[Message]]:
        return Request[typing.List[Message]](
            'GET',
            '/channels/{channel_id}/messages',
            {'channel_id': channel_id},
            params=prepare(self, {
                'around': around,
                'before': before,
                'after': after,
                'limit': limit,
            })
        )

    def get_channel_message(
            self,
            channel_id: Snowflake,
            message_id: Snowflake
    ) -> Request[Message]:
        return Request[Message]('GET', '/channels/{channel.id}/messages/{message.id}', {
            'channel_id': channel_id,
            'message_id': message_id
        })

    def create_message(
            self,
            channel_id: Snowflake,
            *,
            # one of these is required:
            content: Unknownish[str] = UNKNOWN,
            file: Unknownish[object] = UNKNOWN,  # TODO: better file type?
            embeds: Unknownish[typing.List[Embed]] = UNKNOWN,
            sticker_ids: Unknownish[typing.List[Snowflake]] = UNKNOWN,
            # optional
            tts: Unknownish[bool] = UNKNOWN,
            allowed_mentions: Unknownish[AllowedMentions] = UNKNOWN,
            message_reference: Unknownish[MessageReference] = UNKNOWN,
            components: Unknownish[typing.List[Component]] = UNKNOWN,
    ) -> Request[Message]:
        json_payload = prepare(self, {
            'content': content,
            'embeds': embeds,
            'sticker_ids': sticker_ids,
            'tts': tts,
            'allowed_mentions': allowed_mentions,
            'message_reference': message_reference,
            'components': components,
        })

        return Request[Message](
            'POST',
            '/channels/{channel_id}/messages',
            {'channel_id': channel_id},
            data={'payload_json': json.dumps(json_payload)} if json_payload else None,
            files={'file': file} if file != UNKNOWN else None
        )

    def crosspost_message(self, channel_id: Snowflake, message_id: Snowflake) -> Request[Message]:
        return Request[Message](
            'POST',
            '/channels/{channel_id}/messages/{message_id}/crosspost',
            {'channel_id': channel_id, 'message_id': message_id}
        )

    # TODO: better emoji type?
    # TODO: don't forget to make None == 204 No Content.
    def create_reaction(
            self,
            channel_id: Snowflake,
            message_id: Snowflake,
            *,
            emoji: str
    ) -> Request[None]:
        return Request[None](
            'PUT',
            '/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me',
            {'channel_id': channel_id, 'message_id': message_id, 'emoji': emoji}
        )

    def delete_own_reaction(
            self,
            channel_id: Snowflake,
            message_id: Snowflake,
            *,
            emoji: str
    ) -> Request[None]:
        return Request[None](
            'DELETE',
            '/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me',
            {'channel_id': channel_id, 'message_id': message_id, 'emoji': emoji}
        )

    def delete_user_reaction(
            self,
            channel_id: Snowflake,
            message_id: Snowflake,
            *,
            emoji: str,
            user_id: Snowflake
    ) -> Request[None]:
        return Request[None](
            'DELETE',
            '/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/{user_id}',
            {
                'channel_id': channel_id,
                'message_id': message_id,
                'emoji': emoji,
                'user_id': user_id
            }
        )

    def get_reactions(
            self,
            channel_id: Snowflake,
            message_id: Snowflake,
            *,
            emoji: str,
            after: Unknownish[Snowflake] = UNKNOWN,
            limit: Unknownish[int] = UNKNOWN
    ) -> Request[typing.List[User]]:
        return Request[typing.List[User]](
            'GET',
            '/channels/{channel_id}/messages/{message_id}/reactions/{emoji}',
            {'channel_id': channel_id, 'message_id': message_id, 'emoji': emoji},
            params=prepare(self, {'after': after, 'limit': limit})
        )

    # TODO: what does this actually return??
    def delete_all_reactions(self, channel_id: Snowflake, message_id: Snowflake) -> Request[None]:
        return Request[None](
            'DELETE',
            '/channels/{channel_id}/messages/{message_id}/reactions',
            {'channel_id': channel_id, 'message_id': message_id}
        )

    # TODO: what does this actually return??
    def delete_all_reactions_for_emoji(
            self,
            channel_id: Snowflake,
            message_id: Snowflake,
            *,
            emoji: str
    ) -> Request[None]:
        return Request[None](
            'DELETE',
            '/channels/{channel_id}/messages/{message_id}/reactions/{emoji}',
            {'channel_id': channel_id, 'message_id': message_id, 'emoji': emoji}
        )

    def edit_message(
            self,
            channel_id: Snowflake,
            message_id: Snowflake,
            *,
            content: Unknownish[typing.Optional[str]] = UNKNOWN,
            embeds: Unknownish[typing.Optional[typing.List[Embed]]] = UNKNOWN,
            flags: Unknownish[typing.Optional[MessageFlags]] = UNKNOWN,
            # TODO: better file type
            file: Unknownish[typing.Optional[object]] = UNKNOWN,
            allowed_mentions: Unknownish[typing.Optional[AllowedMentions]] = UNKNOWN,
            attachments: Unknownish[typing.Optional[typing.List[Attachment]]] = UNKNOWN,
            components: Unknownish[typing.Optional[typing.List[Component]]] = UNKNOWN
    ) -> Request[Message]:
        json_payload = prepare(self, {
            'content': content,
            'embeds': embeds,
            'flags': flags,
            'allowed_mentions': allowed_mentions,
            'attachments': attachments,
            'components': components,
        })

        return Request[Message](
            'POST',
            '/channels/{channel_id}/messages',
            {'channel_id': channel_id},
            data={'payload_json': json.dumps(json_payload)} if json_payload else None,
            files={'file': file} if file != UNKNOWN else None
        )

    def delete_message(self, channel_id: Snowflake, message_id: Snowflake) -> Request[None]:
        return Request[None](
            'DELETE',
            '/channels/{channel_id}/messages/{message_id}',
            {'channel_id': channel_id, 'message_id': message_id}
        )

    def bulk_delete_messages(
            self,
            channel_id: Snowflake,
            *,
            messages: typing.List[Snowflake],
            reason: Unknownish[str] = UNKNOWN,
    ) -> Request[None]:
        return Request[None](
            'POST',
            '/channels/{channel_id}/messages/bulk-delete',
            {'channel_id': channel_id},
            json=prepare(self, {'messages': messages}),
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def edit_channel_permissions(
            self,
            channel_id: Snowflake,
            overwrite_id: Snowflake,
            *,
            allow: BitwisePermissionFlags,
            deny: BitwisePermissionFlags,
            type: Literal[0, 1],
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[None]:
        return Request[None](
            'PUT',
            '/channels/{channel_id}/permissions/{overwrite_id}',
            {'channel_id': channel_id, 'overwrite_id': overwrite_id},
            json=prepare(self, {'allow': allow, 'deny': deny, 'type': type}),
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def get_channel_invites(self, channel_id: Snowflake) -> Request[typing.List[InviteMetadata]]:
        return Request[typing.List[InviteMetadata]](
            'GET',
            '/channels/{channel_id}/invites',
            {'channel_id': channel_id}
        )

    def create_channel_invite(
            self,
            channel_id: Snowflake,
            *,
            max_age: Unknownish[int] = UNKNOWN,
            max_uses: Unknownish[int] = UNKNOWN,
            temporary: Unknownish[bool] = UNKNOWN,
            unique: Unknownish[bool] = UNKNOWN,
            target_type: Unknownish[InviteTargetTypes] = UNKNOWN,
            target_user_id: Unknownish[Snowflake] = UNKNOWN,
            target_application_id: Unknownish[Snowflake] = UNKNOWN,
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[Invite]:
        return Request[Invite](
            'POST',
            '/channels/{channel_id}/invites',
            {'channel_id': channel_id},
            json=prepare(self, {
                'max_age': max_age,
                'max_uses': max_uses,
                'temporary': temporary,
                'unique': unique,
                'target_type': target_type,
                'target_user_id': target_user_id,
                'target_application_id': target_application_id
            }),
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def delete_channel_permission(
            self,
            channel_id: Snowflake,
            overwrite_id: Snowflake,
            *,
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[None]:
        return Request[None](
            'DELETE',
            '/channels/{channel_id}/permissions/{overwrite_id}',
            {'channel_id': channel_id, 'overwrite_id': overwrite_id},
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def follow_news_channel(
            self,
            channel_id: Snowflake,
            *,
            webhook_channel_id: Snowflake
    ) -> Request[FollowedChannel]:
        return Request[FollowedChannel](
            'POST',
            '/channels/{channel_id}/followers',
            {'channel_id': channel_id},
            json=prepare(self, {'webhook_channel_id': webhook_channel_id})
        )

    def trigger_typing_indicator(self, channel_id: Snowflake) -> Request[None]:
        return Request[None]('POST', '/channels/{channel_id}/typing', {'channel_id': channel_id})

    def get_pinned_messages(self, channel_id: Snowflake) -> Request[typing.List[Message]]:
        return Request[typing.List[Message]](
            'GET',
            '/channels/{channel_id}/pins',
            {'channel_id': channel_id}
        )

    def pin_message(
            self,
            channel_id: Snowflake,
            message_id: Snowflake,
            *,
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[None]:
        return Request[None](
            'PUT',
            '/channels/{channel_id}/pins/{message_id}',
            {'channel_id': channel_id, 'message_id': message_id},
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def unpin_message(
            self,
            channel_id: Snowflake,
            message_id: Snowflake,
            *,
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[None]:
        return Request[None](
            'DELETE',
            '/channels/{channel_id}/pins/{message_id}',
            {'channel_id': channel_id, 'message_id': message_id},
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    # TODO: what does this return?
    def group_dm_add_recipient(
        self,
        channel_id: Snowflake,
        user_id: Snowflake,
        *,
        access_token: str,
        # ????????? I think this is optional (Unknownish)
        # TODO: test.
        nick: str
    ) -> Request[None]:
        return Request[None](
            'PUT',
            '/channels/{channel_id}/recipients/{user_id}',
            {'channel_id': channel_id, 'user_id': user_id},
            json=prepare(self, {'access_token': access_token, 'nick': nick})
        )

    # TODO: what does this return?
    def group_dm_remove_recipient(
            self,
            channel_id: Snowflake,
            user_id: Snowflake
    ) -> Request[None]:
        return Request[None](
            'DELETE',
            '/channels/{channel_id}/recipients/{user_id}',
            {'channel_id': channel_id, 'user_id': user_id},
        )

    def start_thread_with_message(
            self,
            channel_id: Snowflake,
            message_id: Snowflake,
            *,
            name: str,
            # TODO: is `auto_archive_duration` really required?
            auto_archive_duration: int,
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[Channel]:
        return Request[Channel](
            'POST',
            '/channels/{channel_id}/messages/{message_id}/threads',
            {'channel_id': channel_id, 'message_id': message_id},
            json=prepare(self, {'name': name, 'auto_archive_duration': auto_archive_duration}),
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def start_thread_without_message(
            self,
            channel_id: Snowflake,
            *,
            name: str,
            # TODO: is `auto_archive_duration` really required?
            auto_archive_duration: int,
            type: ChannelTypes,
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[Channel]:
        return Request[Channel](
            'POST',
            '/channels/{channel_id}/threads',
            {'channel_id': channel_id},
            json=prepare(self, {
                'name': name,
                'auto_archive_duration': auto_archive_duration,
                'type': type
            }),
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def join_thread(self, channel_id: Snowflake) -> Request[None]:
        return Request[None](
            'PUT',
            '/channels/{channel_id}/thread-members/@me',
            {'channel_id': channel_id}
        )

    def add_thread_member(self, channel_id: Snowflake, user_id: Snowflake) -> Request[None]:
        return Request[None](
            'PUT',
            '/channels/{channel_id}/thread-members/{user_id}',
            {'channel_id': channel_id, 'user_id': user_id}
        )

    def leave_thread(self, channel_id: Snowflake) -> Request[None]:
        return Request[None](
            'DELETE',
            '/channels/{channel_id}/thread-members/@me',
            {'channel_id': channel_id}
        )

    def remove_thread_member(self, channel_id: Snowflake, user_id: Snowflake) -> Request[None]:
        return Request[None](
            'DELETE',
            '/channels/{channel_id}/thread-members/{user_id}',
            {'channel_id': channel_id, 'user_id': user_id}
        )

    def list_thread_members(self, channel_id: Snowflake) -> Request[typing.List[ThreadMember]]:
        return Request[typing.List[ThreadMember]](
            'GET',
            '/channels/{channel_id}/thread-members',
            {'channel_id': channel_id}
        )

    # TODO: this doesn't return a channel, this returns a thread...
    #  ADT?
    def list_public_archived_threads(
            self,
            channel_id: Snowflake,
            *,
            before: Unknownish[datetime.datetime] = UNKNOWN,
            limit: Unknownish[int] = UNKNOWN
    ) -> Request[typing.List[Channel]]:
        return Request[typing.List[Channel]](
            'GET',
            '/channels/{channel.id}/threads/archived/public',
            {'channel_id': channel_id},
            params=prepare(self, {'before': before, 'limit': limit})
        )

    # TODO: this doesn't return a channel, this returns a thread...
    #  ADT?
    def list_private_archived_threads(
            self,
            channel_id: Snowflake,
            *,
            before: Unknownish[datetime.datetime] = UNKNOWN,
            limit: Unknownish[int] = UNKNOWN
    ) -> Request[typing.List[Channel]]:
        return Request[typing.List[Channel]](
            'GET',
            '/channels/{channel.id}/threads/archived/private',
            {'channel_id': channel_id},
            params=prepare(self, {'before': before, 'limit': limit})
        )

    # TODO: this doesn't return a channel, this returns a thread...
    #  ADT?
    def list_joined_private_archived_threads(
            self,
            channel_id: Snowflake,
            *,
            # TODO: why is this a snowflake???
            before: Unknownish[Snowflake] = UNKNOWN,
            limit: Unknownish[int] = UNKNOWN
    ) -> Request[typing.List[Channel]]:
        return Request[typing.List[Channel]](
            'GET',
            '/channels/{channel_id}/users/@me/threads/archived/private',
            {'channel_id': channel_id},
            params=prepare(self, {'before': before, 'limit': limit})
        )

    def list_guild_emojis(self, guild_id: Snowflake) -> Request[typing.List[Emoji]]:
        return Request[typing.List[Emoji]](
            'GET',
            '/guilds/{guild_id}/emojis',
            {'guild_id': guild_id}
        )

    def get_guild_emoji(self, guild_id: Snowflake, emoji_id: Snowflake) -> Request[Emoji]:
        return Request[Emoji](
            'GET',
            '/guilds/{guild_id}/emojis/{emoji_id}',
            {'guild_id': guild_id, 'emoji_id': emoji_id}
        )

    def create_guild_emoji(
            self,
            guild_id: Snowflake,
            *,
            name: str,
            # https://discord.com/developers/docs/reference#image-data
            image: str,
            # TODO: is `roles` optional?
            roles: typing.List[Snowflake],
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[Emoji]:
        return Request[Emoji](
            'POST',
            '/guilds/{guild_id}/emojis',
            {'guild_id': guild_id},
            json=prepare(self, {'name': name, 'image': image, 'roles': roles}),
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def modify_guild_emoji(
            self,
            guild_id: Snowflake,
            emoji_id: Snowflake,
            *,
            name: Unknownish[str] = UNKNOWN,
            roles: Unknownish[typing.Optional[typing.List[Snowflake]]] = UNKNOWN,
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[Emoji]:
        return Request[Emoji](
            'PATCH',
            '/guilds/{guild_id}/emojis/{emoji_id}',
            {'guild_id': guild_id, 'emoji_id': emoji_id},
            json=prepare(self, {'name': name, 'roles': roles}),
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def delete_guild_emoji(
            self,
            guild_id: Snowflake,
            emoji_id: Snowflake,
            *,
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[None]:
        return Request[None](
            'DELETE',
            '/guilds/{guild_id}/emojis/{emoji_id}',
            {'guild_id': guild_id, 'emoji_id': emoji_id},
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def create_guild(
            self,
            *,
            name: str,
            # todo: this is deprecated?
            region: Unknownish[typing.Optional[str]] = UNKNOWN,
            # https://discord.com/developers/docs/reference#image-data
            icon: Unknownish[str] = UNKNOWN,
            verification_level: Unknownish[VerificationLevel] = UNKNOWN,
            default_message_notifications: Unknownish[DefaultMessageNotificationLevel] = UNKNOWN,
            explicit_content_filter: Unknownish[ExplicitContentFilterLevel] = UNKNOWN,
            roles: Unknownish[typing.List[Role]] = UNKNOWN,
            # TODO: partial channel objects
            channels: Unknownish[typing.List[object]] = UNKNOWN,
            afk_channel_id: Unknownish[Snowflake] = UNKNOWN,
            afk_timeout: Unknownish[int] = UNKNOWN,
            system_channel_id: Unknownish[Snowflake] = UNKNOWN,
            system_channel_flags: Unknownish[int] = UNKNOWN
    ) -> Request[Guild]:
        return Request[Guild](
            'POST',
            '/guilds',
            {},
            json=prepare(self, {
                'name': name,
                'region': region,
                'icon': icon,
                'verification_level': verification_level,
                'default_message_notifications': default_message_notifications,
                'explicit_content_filter': explicit_content_filter,
                'roles': roles,
                'channels': channels,
                'afk_channel_id': afk_channel_id,
                'afk_timeout': afk_timeout,
                'system_channel_id': system_channel_id,
                'system_channel_flags': system_channel_flags
            })
        )

    def get_guild(self, guild_id: Snowflake, *, with_counts: bool) -> Request[Guild]:
        return Request[Guild](
            'GET',
            '/guilds/{guild_id}',
            {'guild_id': guild_id},
            params={'with_counts': with_counts}
        )

    def get_guild_preview(self, guild_id: Snowflake) -> Request[GuildPreview]:
        return Request[GuildPreview]('GET', '/guilds/{guild_id}/preview', {'guild_id': guild_id})

    def modify_guild(
            self,
            guild_id: Snowflake,
            *,
            name: Unknownish[str] = UNKNOWN,
            region: Unknownish[typing.Optional[str]] = UNKNOWN,
            verification_level: Unknownish[typing.Optional[VerificationLevel]] = UNKNOWN,
            default_message_notifications: Unknownish[
                typing.Optional[DefaultMessageNotificationLevel]
            ] = UNKNOWN,
            explicit_content_filter: Unknownish[
                typing.Optional[ExplicitContentFilterLevel]
            ] = UNKNOWN,
            afk_channel_id: Unknownish[typing.Optional[Snowflake]] = UNKNOWN,
            afk_timeout: Unknownish[int] = UNKNOWN,
            # https://discord.com/developers/docs/reference#image-data
            icon: Unknownish[typing.Optional[str]] = UNKNOWN,
            owner_id: Unknownish[Snowflake] = UNKNOWN,
            # https://discord.com/developers/docs/reference#image-data
            splash: Unknownish[typing.Optional[str]] = UNKNOWN,
            discovery_splash: Unknownish[typing.Optional[str]] = UNKNOWN,
            banner: Unknownish[typing.Optional[str]] = UNKNOWN,
            system_channel_id: Unknownish[typing.Optional[Snowflake]] = UNKNOWN,
            system_channel_flags: Unknownish[SystemChannelFlags] = UNKNOWN,
            rules_channel_id: Unknownish[typing.Optional[Snowflake]] = UNKNOWN,
            public_updates_channel_id: Unknownish[typing.Optional[Snowflake]] = UNKNOWN,
            preferred_locale: Unknownish[typing.Optional[str]] = UNKNOWN,
            features: Unknownish[typing.List[GuildFeatures]] = UNKNOWN,
            description: Unknownish[typing.Optional[str]] = UNKNOWN,
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[Guild]:
        return Request[Guild](
            'PATCH',
            '/guilds/{guild_id}',
            {'guild_id': guild_id},
            json=prepare(self, {
                'name': name,
                'region': region,
                'verification_level': verification_level,
                'default_message_notifications': default_message_notifications,
                'explicit_content_filter': explicit_content_filter,
                'afk_channel_id': afk_channel_id,
                'afk_timeout': afk_timeout,
                'icon': icon,
                'owner_id': owner_id,
                'splash': splash,
                'discovery_splash': discovery_splash,
                'banner': banner,
                'system_channel_id': system_channel_id,
                'system_channel_flags': system_channel_flags,
                'rules_channel_id': rules_channel_id,
                'public_updates_channel_id': public_updates_channel_id,
                'preferred_locale': preferred_locale,
                'features': features,
                'description': description,
            }),
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def delete_guild(self, guild_id: Snowflake) -> Request[None]:
        return Request[None]('DELETE', '/guilds/{guild_id}', {'guild_id': guild_id})

    def get_guild_channels(self, guild_id: Snowflake) -> Request[typing.List[Channel]]:
        return Request[typing.List[Channel]](
            'GET',
            '/guilds/{guild_id}/channels',
            {'guild_id': guild_id}
        )

    def create_guild_channel(
            self,
            guild_id: Snowflake,
            *,
            name: str,
            type: Unknownish[ChannelTypes] = UNKNOWN,
            topic: Unknownish[str] = UNKNOWN,
            rate_limit_per_user: Unknownish[int] = UNKNOWN,
            position: Unknownish[int] = UNKNOWN,
            permission_overwrites: Unknownish[typing.List[Overwrite]] = UNKNOWN,
            parent_id: Unknownish[Snowflake] = UNKNOWN,
            nsfw: Unknownish[bool] = UNKNOWN,
            # voice only (TODO: typing override)
            bitrate: Unknownish[int] = UNKNOWN,
            user_limit: Unknownish[int] = UNKNOWN,
            reason: Unknownish[str] = UNKNOWN,
    ) -> Request[Channel]:
        return Request[Channel](
            'POST',
            '/guilds/{guild_id}/channels',
            {'guild_id': guild_id},
            json=prepare(self, {
                'name': name,
                'type': type,
                'topic': topic,
                'bitrate': bitrate,
                'user_limit': user_limit,
                'rate_limit_per_user': rate_limit_per_user,
                'position': position,
                'permission_overwrites': permission_overwrites,
                'parent_id': parent_id,
            }),
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def modify_guild_channel_permissions(
        self,
        guild_id: Snowflake,
        *,
        params: typing.List[ModifyGuildChannelPositionsParameters],
        reason: Unknownish[str] = UNKNOWN
    ) -> Request[None]:
        return Request[None](
            'PATCH',
            '/guilds/{guild_id}/channels',
            {'guild_id': guild_id},
            json=self.conv.unstructure(params),
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    # TODO: this returns threads not channels... ADT?
    def list_active_threads(self, guild_id: Snowflake) -> Request[typing.List[Channel]]:
        return Request[typing.List[Channel]](
            'GET',
            '/guilds/{guild_id}/threads/active',
            {'guild_id': guild_id}
        )

    def get_guild_member(self, guild_id: Snowflake, user_id: Snowflake) -> Request[GuildMember]:
        return Request[GuildMember](
            'GET',
            '/guilds/{guild_id}/members/{user_id}',
            {'guild_id': guild_id, 'user_id': user_id}
        )

    def list_guild_members(self, guild_id: Snowflake) -> Request[typing.List[GuildMember]]:
        return Request[typing.List[GuildMember]](
            'GET',
            '/guilds/{guild_id}/members',
            {'guild_id': guild_id}
        )

    def search_guild_members(
            self,
            guild_id: Snowflake,
            *,
            query: str,
            limit: Unknownish[int] = UNKNOWN
    ) -> Request[typing.List[GuildMember]]:
        return Request[typing.List[GuildMember]](
            'GET',
            '/guilds/{guild_id}/members/search',
            {'guild_id': guild_id},
            params=prepare(self, {'query': query, 'limit': limit})
        )

    # TODO: make sure to support unions/optionals!
    def add_guild_member(
            self,
            guild_id: Snowflake,
            user_id: Snowflake,
            *,
            access_token: str,
            # requires `MANAGE_NICKNAMES`
            nick: Unknownish[str] = UNKNOWN,
            # requires `MANAGE_ROLES`
            roles: Unknownish[typing.List[Snowflake]] = UNKNOWN,
            # requires `MUTE_MEMBERS`
            mute: Unknownish[bool] = UNKNOWN,
            # requires `DEAFEN_MEMBERS`
            deaf: Unknownish[bool] = UNKNOWN
    ) -> Request[typing.Optional[GuildMember]]:
        return Request[typing.Optional[GuildMember]](
            'PUT',
            '/guilds/{guild_id}/members/{user_id}',
            {'guild_id': guild_id, 'user_id': user_id},
            json=prepare(self, {
                'access_token': access_token,
                'nick': nick,
                'roles': roles,
                'mute': mute,
                'deaf': deaf
            })
        )

    def modify_guild_member(
            self,
            guild_id: Snowflake,
            user_id: Snowflake,
            *,
            nick: Unknownish[typing.Optional[str]] = UNKNOWN,
            roles: Unknownish[typing.Optional[typing.List[Snowflake]]] = UNKNOWN,
            mute: Unknownish[typing.Optional[bool]] = UNKNOWN,
            deaf: Unknownish[typing.Optional[bool]] = UNKNOWN,
            channel_id: Unknownish[typing.Optional[Snowflake]] = UNKNOWN,
            reason: Unknownish[str] = UNKNOWN,
    ) -> Request[GuildMember]:
        return Request[GuildMember](
            'PATCH',
            '/guilds/{guild_id}/members/{user_id}',
            {'guild_id': guild_id, 'user_id': user_id},
            json=prepare(self, {
                'nick': nick,
                'roles': roles,
                'mute': mute,
                'deaf': deaf,
                'channel_id': channel_id
            }),
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def modify_current_member(
        self,
        guild_id: Snowflake,
        *,
        nick: Unknownish[typing.Optional[str]] = UNKNOWN
    ) -> Request[GuildMember]:
        return Request[str](
            'PATCH',
            '/guilds/{guild_id}/members/@me',
            {'guild_id': guild_id},
            json=prepare(self, {'nick': nick}),
            # TODO: this probably supports audit log
            # headers=prepare(self, {
            #     'X-Audit-Log-Reason': reason
            # })
        )

    # TODO: does this actually return a str of the nickname?
    def modify_current_user_nick(
            self,
            guild_id: Snowflake,
            *,
            # TODO: why ON EARTH is this not required in the api???
            nick: Unknownish[typing.Optional[str]] = UNKNOWN,
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[str]:
        # deprecated for modify current member
        return Request[str](
            'PATCH',
            '/guilds/{guild_id}/members/@me/nick',
            {'guild_id': guild_id},
            json=prepare(self, {'nick': nick}),
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def add_guild_member_role(
            self,
            guild_id: Snowflake,
            user_id: Snowflake,
            role_id: Snowflake,
            *,
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[None]:
        return Request[None](
            'PUT',
            '/guilds/{guild_id}/members/{user_id}/roles/{role_id}',
            {'guild_id': guild_id, 'user_id': user_id, 'role_id': role_id},
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def remove_guild_member_role(
            self,
            guild_id: Snowflake,
            user_id: Snowflake,
            role_id: Snowflake,
            *,
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[None]:
        return Request[None](
            'DELETE',
            '/guilds/{guild_id}/members/{user_id}/roles/{role_id}',
            {'guild_id': guild_id, 'user_id': user_id, 'role_id': role_id},
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def remove_guild_member(
            self,
            guild_id: Snowflake,
            user_id: Snowflake,
            *,
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[None]:
        return Request[None](
            'DELETE',
            '/guilds/{guild_id}/members/{user_id}',
            {'guild_id': guild_id, 'user_id': user_id},
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def get_guild_bans(self, guild_id: Snowflake) -> Request[typing.List[Ban]]:
        return Request[typing.List[Ban]]('GET', '/guilds/{guild_id}/bans', {'guild_id': guild_id})

    def get_guild_ban(self, guild_id: Snowflake, user_id: Snowflake) -> Request[Ban]:
        return Request[Ban](
            'GET',
            '/guilds/{guild_id}/bans/{user_id}',
            {'guild_id': guild_id, 'user_id': user_id}
        )

    def create_guild_ban(
            self,
            guild_id: Snowflake,
            user_id: Snowflake,
            *,
            delete_message_days: Unknownish[int] = UNKNOWN,
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[None]:
        return Request[None](
            'PUT',
            '/guilds/{guild_id}/bans/{user_id}',
            {'guild_id': guild_id, 'user_id': user_id},
            json=prepare(self, {'delete_message_days': delete_message_days}),
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def remove_guild_ban(
        self,
        guild_id: Snowflake,
        user_id: Snowflake,
        *,
        reason: Unknownish[str] = UNKNOWN
    ) -> Request[None]:
        return Request[None](
            'DELETE',
            '/guilds/{guild_id}/bans/{user_id}',
            {'guild_id': guild_id, 'user_id': user_id},
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def get_guild_roles(self, guild_id: Snowflake) -> Request[typing.List[Role]]:
        return Request[typing.List[Role]](
            'GET',
            '/guilds/{guild_id}/roles',
            {'guild_id': guild_id}
        )

    def create_guild_role(
            self,
            guild_id: Snowflake,
            *,
            name: Unknownish[str] = UNKNOWN,
            permissions: Unknownish[BitwisePermissionFlags] = UNKNOWN,
            color: Unknownish[int] = UNKNOWN,
            hoist: Unknownish[bool] = UNKNOWN,
            # https://discord.com/developers/docs/reference#image-data
            # TODO: are these nullable
            icon: Unknownish[str] = UNKNOWN,
            unicode_emoji: Unknownish[str] = UNKNOWN,
            mentionable: Unknownish[bool] = UNKNOWN,
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[Role]:
        return Request[Role](
            'POST',
            '/guilds/{guild_id}/roles',
            {'guild_id': guild_id},
            json=prepare(self, {
                'name': name,
                'permissions': permissions,
                'color': color,
                'hoist': hoist,
                'mentionable': mentionable
            }),
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def modify_guild_role_positions(
            self,
            guild_id: Snowflake,
            *,
            parameters: typing.List[ModifyGuildRolePositionsParameters],
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[typing.List[Role]]:
        return Request[typing.List[Role]](
            'PATCH',
            '/guilds/{guild_id}/roles',
            {'guild_id': guild_id},
            json=self.conv.unstructure(parameters),
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def modify_guild_role(
            self,
            guild_id: Snowflake,
            role_id: Snowflake,
            *,
            name: Unknownish[typing.Optional[str]] = UNKNOWN,
            permissions: Unknownish[typing.Optional[BitwisePermissionFlags]] = UNKNOWN,
            color: Unknownish[typing.Optional[int]] = UNKNOWN,
            hoist: Unknownish[typing.Optional[bool]] = UNKNOWN,
            # https://discord.com/developers/docs/reference#image-data
            icon: Unknownish[typing.Optional[str]] = UNKNOWN,
            unicode_emoji: Unknownish[typing.Optional[str]] = UNKNOWN,
            mentionable: Unknownish[typing.Optional[bool]] = UNKNOWN,
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[Role]:
        return Request[Role](
            'PATCH',
            '/guilds/{guild_role}/roles/{role_id}',
            {'guild_id': guild_id, 'role_id': role_id},
            json=prepare(self, {
                'name': name,
                'permissions': permissions,
                'color': color,
                'hoist': hoist,
                'mentionable': mentionable
            }),
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def delete_guild_role(
            self,
            guild_id: Snowflake,
            role_id: Snowflake,
            *,
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[None]:
        return Request[None](
            'DELETE',
            '/guilds/{guild_id}/roles/{role_id}',
            {'guild_id': guild_id, 'role_id': role_id},
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    # TODO: should this get a seperate object since thing inside cannot be None?
    def get_guild_prune_count(
            self,
            guild_id: Snowflake,
            *,
            days: Unknownish[int] = UNKNOWN,
            include_roles: Unknownish[typing.List[Snowflake]] = UNKNOWN
    ) -> Request[PruneCount]:
        return Request[PruneCount](
            'GET',
            '/guilds/{guild_id}/prune',
            {'guild_id': guild_id},
            json=prepare(self, {
                'days': days,
                'include_roles': (
                    ','.join(map(str, include_roles))
                    if not isinstance(include_roles, UNKNOWN_TYPE) else include_roles
                )
            })
        )

    def begin_guild_prune(
            self,
            guild_id: Snowflake,
            *,
            days: Unknownish[int] = UNKNOWN,
            compute_prune_count: Unknownish[bool] = UNKNOWN,
            include_roles: Unknownish[typing.List[Snowflake]] = UNKNOWN,
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[PruneCount]:
        return Request[PruneCount](
            'POST',
            '/guilds/{guild_id}/prune',
            {'guild_id': guild_id},
            json=prepare(self, {
                'days': days,
                'compute_prune_count': compute_prune_count,
                'include_roles': (
                    ','.join(map(str, include_roles))
                    if not isinstance(include_roles, UNKNOWN_TYPE) else include_roles
                )
            }),
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def get_guild_voice_regions(self, guild_id: Snowflake) -> Request[typing.List[VoiceRegion]]:
        return Request[typing.List[VoiceRegion]](
            'GET',
            '/guilds/{guild_id}/regions',
            {'guild_id': guild_id}
        )

    def get_guild_invites(self, guild_id: Snowflake) -> Request[typing.List[InviteMetadata]]:
        return Request[typing.List[InviteMetadata]](
            'GET',
            '/guilds/{guild_id}/invites',
            {'guild_id': guild_id}
        )

    def get_guild_integrations(self, guild_id: Snowflake) -> Request[typing.List[Integration]]:
        return Request[typing.List[Integration]](
            'GET',
            '/guilds/{guild_id}/integrations',
            {'guild_id': guild_id}
        )

    def delete_guild_integration(
        self,
        guild_id: Snowflake,
        integration_id: Snowflake,
        *,
        reason: Unknownish[str] = UNKNOWN
    ) -> Request[None]:
        return Request[None](
            'DELETE',
            '/guilds/{guild_id}/integrations/{integration_id}',
            {'guild_id': guild_id, 'integration_id': integration_id},
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def get_guild_widget_settings(self, guild_id: Snowflake) -> Request[GuildWidget]:
        return Request[GuildWidget]('GET', '/guilds/{guild_id}/widget', {'guild_id': guild_id})

    def modify_guild_widget(
        self,
        guild_id: Snowflake,
        *,
        # TODO: this is not DRY...
        enabled: Unknownish[bool] = UNKNOWN,
        channel_id: Unknownish[typing.Optional[Snowflake]] = UNKNOWN,
        reason: Unknownish[str] = UNKNOWN
    ) -> Request[GuildWidget]:
        return Request[GuildWidget](
            'PATCH',
            '/guilds/{guild_id}/widget',
            {'guild_id': guild_id},
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    # TODO: is it even worth making a model for this one route?
    def get_guild_widget(self, guild_id: Snowflake) -> Request[typing.Dict[str, typing.Any]]:
        return Request[typing.Dict[str, typing.Any]](
            'GET',
            '/guilds/{guild_id}/widget.json',
            {'guild_id': guild_id}
        )

    # TODO: check this partial out.
    def get_guild_vanity_url(self, guild_id: Snowflake) -> Request[typing.Dict[str, typing.Any]]:
        return Request[typing.Dict[str, typing.Any]](
            'GET',
            '/guilds/{guild_id}/vanity-url',
            {'guild_id': guild_id}
        )

    # ... I guess it's a string? it's an image though :thinking:
    # TODO: is there a better way to type this?
    def get_guild_widget_image(
            self,
            guild_id: Snowflake,
            *,
            style: Unknownish[WidgetStyleOptions] = UNKNOWN
    ) -> Request[str]:
        return Request[str](
            'GET',
            '/guilds/{guild_id}/widget.png',
            {'guild_id': guild_id},
            params=prepare(self, {'style': style})
        )

    def get_guild_welcome_screen(self, guild_id: Snowflake) -> Request[WelcomeScreen]:
        return Request[WelcomeScreen](
            'GET',
            '/guilds/{guild_id}/welcome-screen',
            {'guild_id': guild_id}
        )

    def modify_guild_welcome_screen(
        self,
        guild_id: Snowflake,
        *,
        enabled: Unknownish[typing.Optional[bool]] = UNKNOWN,
        welcome_channels: Unknownish[typing.Optional[typing.List[WelcomeScreenChannel]]] = UNKNOWN,
        description: Unknownish[typing.Optional[str]] = UNKNOWN,
        reason: Unknownish[str] = UNKNOWN
    ) -> Request[WelcomeScreen]:
        return Request[WelcomeScreen](
            'PATCH',
            '/guilds/{guild_id}/welcome-screen',
            {'guild_id': guild_id},
            json=prepare(self, {
                'enabled': enabled,
                'welcome_channels': welcome_channels,
                'description': description
            }),
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    # TODO: what does this return?
    def modify_current_user_voice_state(
        self,
        guild_id: Snowflake,
        *,
        channel_id: Snowflake,
        suppress: Unknownish[bool] = UNKNOWN,
        request_to_speak_timestamp: Unknownish[typing.Optional[datetime.datetime]] = UNKNOWN
    ) -> Request[None]:
        return Request[None](
            'PATCH',
            '/guilds/{guild_id}/voice-states/@me',
            {'guild_id': guild_id},
            json=prepare(self, {
                'channel_id': channel_id,
                'suppress': suppress,
                'request_to_speak_timestamp': request_to_speak_timestamp
            })
        )

    # TODO: what does this return?
    def modify_user_voice_state(
        self,
        guild_id: Snowflake,
        user_id: Snowflake,
        *,
        channel_id: Snowflake,
        suppress: Unknownish[bool] = UNKNOWN
    ) -> Request[None]:
        return Request[None](
            'PATCH',
            '/guilds/{guild_id}/voice-states/{user_id}',
            {'guild_id': guild_id, 'user_id': user_id},
            json=prepare(self, {'channel_id': channel_id, 'suppress': suppress})
        )

    def get_guild_template(self, template_code: str) -> Request[GuildTemplate]:
        return Request[GuildTemplate](
            'GET',
            '/guilds/template/{template_code}',
            {'template_code': template_code}
        )

    def create_guild_from_guild_template(
            self,
            template_code: str,
            *,
            name: str,
            # https://discord.com/developers/docs/reference#image-data
            icon: Unknownish[str] = UNKNOWN
    ) -> Request[Guild]:
        return Request[Guild](
            'POST',
            '/guilds/templates/{template_code}',
            {'template_code': template_code},
            json=prepare(self, {'name': name, 'icon': icon})
        )

    def get_guild_templates(self, guild_id: Snowflake) -> Request[typing.List[GuildTemplate]]:
        return Request[typing.List[GuildTemplate]](
            'GET',
            '/guilds/{guild_id}/templates',
            {'guild_id': guild_id}
        )

    def create_guild_template(
            self,
            guild_id: Snowflake,
            *,
            name: str,
            description: Unknownish[typing.Optional[str]] = UNKNOWN
    ) -> Request[GuildTemplate]:
        return Request[GuildTemplate](
            'POST',
            '/guilds/{guild_id}/templates',
            {'guild_id': guild_id},
            json=prepare(self, {'name': name, 'description': description})
        )

    def sync_guild_template(
            self,
            guild_id: Snowflake,
            template_code: str
    ) -> Request[GuildTemplate]:
        return Request[GuildTemplate](
            'PUT',
            '/guilds/{guild_id}/templates/{template_code}',
            {'guild_id': guild_id, 'template_code': template_code}
        )

    def modify_guild_template(
            self,
            guild_id: Snowflake,
            template_code: str,
            *,
            name: Unknownish[str] = UNKNOWN,
            description: Unknownish[typing.Optional[str]] = UNKNOWN
    ) -> Request[GuildTemplate]:
        return Request[GuildTemplate](
            'PUT',
            '/guilds/{guild_id}/templates/{template_code}',
            {'guild_id': guild_id, 'template_code': template_code},
            json=prepare(self, {'name': name, 'description': description})
        )

    def delete_guild_template(
            self,
            guild_id: Snowflake,
            template_code: str
    ) -> Request[GuildTemplate]:
        return Request[GuildTemplate](
            'DELETE',
            '/guilds/{guild_id}/templates/{template_code}',
            {'guild_id': guild_id, 'template_code': template_code}
        )

    def get_invite(self, invite_code: str) -> Request[Invite]:
        return Request[Invite]('GET', '/invites/{invite_code}', {'invite_code': invite_code})

    def delete_invite(
            self,
            invite_code: str,
            *,
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[Invite]:
        return Request[Invite](
            'DELETE',
            '/invites/{invite_code}',
            {'invite_code': invite_code},
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    # TODO: what does this return?
    def create_stage_instance(
        self,
        *,
        channel_id: Snowflake,
        topic: str,
        privacy_level: Unknownish[PrivacyLevel] = UNKNOWN,
        reason: Unknownish[str] = UNKNOWN
    ) -> Request[None]:
        return Request[None](
            'POST',
            '/stage-instances',
            {},
            json=prepare(self, {
                'channel_id': channel_id,
                'topic': topic,
                'privacy_level': privacy_level
            }),
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def get_stage_instance(self, channel_id: Snowflake) -> Request[StageInstance]:
        return Request[StageInstance](
            'GET',
            '/stage-instances/{channel_id}',
            {'channel_id': channel_id}
        )

    # TODO: what does this return?
    def modify_stage_instance(
            self,
            channel_id: Snowflake,
            *,
            topic: Unknownish[str] = UNKNOWN,
            privacy_level: Unknownish[PrivacyLevel] = UNKNOWN,
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[None]:
        return Request[None](
            'PATCH',
            '/stage-instances/{channel_id}',
            {'channel_id': channel_id},
            json=prepare(self, {'topic': topic, 'privacy_level': privacy_level}),
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    # TODO: what does this return?
    def delete_stage_instance(
            self,
            channel_id: Snowflake,
            *,
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[None]:
        return Request[None](
            'DELETE',
            '/stage-instances/{channel_id}',
            {'channel_id': channel_id},
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def get_sticker(self, sticker_id: Snowflake) -> Request[Sticker]:
        return Request[Sticker]('GET', '/stickers/{sticker_id}', {'sticker_id': sticker_id})

    def list_nitro_sticker_packs(self) -> Request[NitroStickerPacks]:
        return Request[NitroStickerPacks]('GET', '/sticker-packs', {})

    def list_guild_sickers(self, guild_id: Snowflake) -> Request[typing.List[Sticker]]:
        return Request[typing.List[Sticker]](
            'GET',
            '/guilds/{guild_id}/stickers',
            {'guild_id': guild_id}
        )

    def get_guild_sticker(self, guild_id: Snowflake, sticker_id: Snowflake) -> Request[Sticker]:
        return Request[Sticker](
            'GET',
            '/guilds/{guild_id}/stickers/{sticker_id}',
            {'guild_id': guild_id, 'sticker_id': sticker_id}
        )

    def create_guild_sticker(
            self,
            guild_id: Snowflake,
            *,
            name: str,
            # TODO: this is probably `typing.Optional`?
            description: str,
            tags: str,
            # TODO: better file type
            file: object,
            reason: Unknownish[str] = UNKNOWN,
    ) -> Request[Sticker]:
        return Request[Sticker](
            'POST',
            '/guilds/{guild_id}/stickers',
            {'guild_id': guild_id},
            data=prepare(self, {'name': name, 'description': description, 'tags': tags}),
            files={'file': file},
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def modify_guild_sticker(
            self,
            guild_id: Snowflake,
            sticker_id: Snowflake,
            *,
            name: Unknownish[str] = UNKNOWN,
            description: Unknownish[typing.Optional[str]] = UNKNOWN,
            tags: Unknownish[str] = UNKNOWN,
            reason: Unknownish[str] = UNKNOWN,
    ) -> Request[Sticker]:
        return Request[Sticker](
            'PATCH',
            '/guilds/{guild_id}/stickers/{sticker_id}',
            {'guild_id': guild_id, 'sticker_id': sticker_id},
            json=prepare(self, {'name': name, 'description': description, 'tags': tags}),
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def delete_guild_sticker(
            self,
            guild_id: Snowflake,
            sticker_id: Snowflake,
            *,
            reason: Unknownish[str] = UNKNOWN
    ) -> Request[None]:
        return Request[None](
            'DELETE',
            '/guilds/{guild_id}/stickers/{sticker_id}',
            {'guild_id': guild_id, 'sticker_id': sticker_id},
            headers=prepare(self, {
                'X-Audit-Log-Reason': reason
            })
        )

    def get_current_user(self) -> Request[User]:
        return Request[User]('GET', '/users/@me', {})

    def get_user(self, user_id: Snowflake) -> Request[User]:
        return Request[User]('GET', '/users/{user_id}', {'user_id': user_id})

    def modify_current_user(
            self,
            *,
            username: Unknownish[str] = UNKNOWN,
            # https://discord.com/developers/docs/reference#image-data
            avatar: Unknownish[typing.Optional[str]] = UNKNOWN,
    ) -> Request[User]:
        return Request[User](
            'PATCH',
            '/users/@me',
            {},
            json=prepare(self, {'username': username, 'avatar': avatar})
        )

    # TODO: partial guild object?
    def get_current_user_guilds(self) -> Request[typing.List[typing.Dict[str, typing.Any]]]:
        return Request[typing.List[typing.Dict[str, typing.Any]]]('GET', '/users/@me/guilds', {})

    def leave_guild(self, guild_id: Snowflake) -> Request[None]:
        return Request[None]('DELETE', '/users/@me/guilds/{guild_id}', {'guild_id': guild_id})

    def create_dm(self, *, recipient_id: Snowflake) -> Request[Channel]:
        return Request[Channel](
            'POST',
            '/users/@me/channels',
            {},
            json=prepare(self, {'recipient_id': recipient_id})
        )

    # TODO: do DMs created with this really not show up in client?
    def create_group_dm(
            self,
            *,
            access_tokens: typing.List[str],
            nicks: typing.Dict[Snowflake, str]
    ) -> Request[Channel]:
        return Request[Channel](
            'POST',
            '/users/@me/channels',
            {},
            json=prepare(self, {'access_tokens': access_tokens, 'nicks': nicks})
        )

    def get_user_connections(self) -> Request[typing.List[UserConnection]]:
        return Request[typing.List[UserConnection]]('GET', '/users/@me/connections', {})

    def list_voice_regions(self) -> Request[typing.List[VoiceRegion]]:
        return Request[typing.List[VoiceRegion]]('GET', '/voice/regions', {})

    # TODO: does this really not support audit log reason?
    def create_webhook(
            self,
            channel_id: Snowflake,
            *,
            name: str,
            # https://discord.com/developers/docs/reference#image-data
            avatar: Unknownish[typing.Optional[str]] = UNKNOWN
    ) -> Request[Webhook]:
        return Request[Webhook](
            'POST',
            '/channels/{channel_id}/webhooks',
            {'channel_id': channel_id},
            json=prepare(self, {'name': name, 'avatar': avatar})
        )

    def get_channel_webhooks(self, channel_id: Snowflake) -> Request[typing.List[Webhook]]:
        return Request[typing.List[Webhook]](
            'GET',
            '/channels/{channel_id}/webhooks',
            {'channel_id': channel_id}
        )

    def get_guild_webhooks(self, guild_id: Snowflake) -> Request[typing.List[Webhook]]:
        return Request[typing.List[Webhook]](
            'GET',
            '/guilds/{guild_id}/webhooks',
            {'guild_id': guild_id}
        )

    def get_webhook(self, webhook_id: Snowflake) -> Request[Webhook]:
        return Request[Webhook]('GET', '/webhooks/{webhook_id}', {'webhook_id': webhook_id})

    def get_webhook_with_token(
            self,
            webhook_id: Snowflake,
            webhook_token: str
    ) -> Request[Webhook]:
        return Request[Webhook](
            'GET',
            '/webhooks/{webhook_id}/{webhook_token}',
            {'webhook_id': webhook_id, 'webhook_token': webhook_token}
        )

    def modify_webhook(
            self,
            webhook_id: Snowflake,
            *,
            name: Unknownish[str] = UNKNOWN,
            avatar: Unknownish[typing.Optional[str]] = UNKNOWN,
            # https://discord.com/developers/docs/reference#image-data
            channel_id: Unknownish[Snowflake] = UNKNOWN,
    ) -> Request[Webhook]:
        return Request[Webhook](
            'PATCH',
            '/webhooks/{webhook_id}',
            {'webhook_id': webhook_id},
            json=prepare(self, {'name': name, 'avatar': avatar, 'channel_id': channel_id})
        )

    def modify_webhook_with_token(
            self,
            webhook_id: Snowflake,
            webhook_token: str,
            *,
            name: Unknownish[str] = UNKNOWN,
            avatar: Unknownish[typing.Optional[str]] = UNKNOWN,
            # https://discord.com/developers/docs/reference#image-data
            channel_id: Unknownish[Snowflake] = UNKNOWN,
    ) -> Request[Webhook]:
        return Request[Webhook](
            'PATCH',
            '/webhooks/{webhook_id}/{webhook_token}',
            {'webhook_id': webhook_id, 'webhook_token': webhook_token},
            json=prepare(self, {'name': name, 'avatar': avatar, 'channel_id': channel_id})
        )

    def delete_webhook(self, webhook_id: Snowflake) -> Request[None]:
        return Request[None]('DELETE', '/webhooks/{webhook_id}', {'webhook_id': webhook_id})

    def delete_webhook_with_token(
            self,
            webhook_id: Snowflake,
            webhook_token: str
    ) -> Request[None]:
        return Request[None](
            'DELETE',
            '/webhooks/{webhook_id}/{webhook_token}',
            {'webhook_id': webhook_id, 'webhook_token': webhook_token}
        )

    # TODO: webhooks can't send stickers?
    # TODO: what does this return?
    def execute_webhook(
            self,
            webhook_id: Snowflake,
            webhook_token: str,
            *,
            # one of these is required:
            content: Unknownish[str] = UNKNOWN,
            file: Unknownish[object] = UNKNOWN,  # TODO: better file type?
            embeds: Unknownish[typing.List[Embed]] = UNKNOWN,
            # optional
            wait: Unknownish[bool] = UNKNOWN,
            thread_id: Unknownish[Snowflake] = UNKNOWN,
            username: Unknownish[str] = UNKNOWN,
            avatar_url: Unknownish[str] = UNKNOWN,
            tts: Unknownish[bool] = UNKNOWN,
            allowed_mentions: Unknownish[AllowedMentions] = UNKNOWN,
            message_reference: Unknownish[MessageReference] = UNKNOWN,
            components: Unknownish[typing.List[Component]] = UNKNOWN,
    ) -> Request[None]:
        json_payload = prepare(self, {
            'content': content,
            'embeds': embeds,
            'username': username,
            'avatar_url': avatar_url,
            'tts': tts,
            'allowed_mentions': allowed_mentions,
            'message_reference': message_reference,
            'components': components,
        })

        return Request[None](
            'POST',
            '/webhooks/{webhook_id}/{webhook_token}',
            {'webhook_id': webhook_id, 'webhook_token': webhook_token},
            params=prepare(self, {'wait': wait, 'thread_id': thread_id}),
            data={'payload_json': json.dumps(json_payload)} if json_payload else None,
            files={'file': file} if file != UNKNOWN else None
        )

    def get_webhook_message(
            self,
            webhook_id: Snowflake,
            webhook_token: str,
            message_id: Snowflake
    ) -> Request[Message]:
        return Request[Message](
            'GET',
            '/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}',
            {'webhook_id': webhook_id, 'webhook_token': webhook_token, 'message_id': message_id}
        )

    def edit_webhook_message(
            self,
            webhook_id: Snowflake,
            webhook_token: str,
            message_id: Snowflake,
            *,
            content: Unknownish[typing.Optional[str]] = UNKNOWN,
            embeds: Unknownish[typing.Optional[typing.List[Embed]]] = UNKNOWN,
            # TODO: better file type
            file: Unknownish[typing.Optional[object]] = UNKNOWN,
            allowed_mentions: Unknownish[typing.Optional[AllowedMentions]] = UNKNOWN,
            attachments: Unknownish[typing.Optional[typing.List[Attachment]]] = UNKNOWN,
            components: Unknownish[typing.Optional[typing.List[Component]]] = UNKNOWN,
    ) -> Request[Message]:
        json_payload = prepare(self, {
            'content': content,
            'embeds': embeds,
            'allowed_mentions': allowed_mentions,
            'components': components,
            'attachments': attachments
        })

        return Request[Message](
            'PATCH',
            '/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}',
            {'webhook_id': webhook_id, 'webhook_token': webhook_token, 'message_id': message_id},
            data={'payload_json': json.dumps(json_payload)} if json_payload else None,
            files={'file': file} if file != UNKNOWN else None
        )

    def delete_webhook_message(
            self,
            webhook_id: Snowflake,
            webhook_token: str,
            message_id: Snowflake
    ) -> Request[None]:
        return Request[None](
            'DELETE',
            '/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}',
            {'webhook_id': webhook_id, 'webhook_token': webhook_token, 'message_id': message_id}
        )

    def get_gateway(self) -> Request[GatewayResponse]:
        return Request[GatewayResponse]('GET', '/gateway', {})

    def get_gateway_bot(self) -> Request[DetailedGatewayResponse]:
        return Request[DetailedGatewayResponse]('GET', '/gateway/bot', {})

    def get_current_bot_application_information(self) -> Request[Application]:
        return Request[Application]('GET', '/oauth2/applications/@me', {})

    def get_current_authorization_information(self) -> Request[AuthorizationInformation]:
        return Request[AuthorizationInformation]('GET', '/oauth2/@me', {})

    def get_global_application_commands(
            self,
            application_id: Snowflake
    ) -> Request[typing.List[ApplicationCommand]]:
        return Request[typing.List[ApplicationCommand]](
            'GET',
            '/applications/{application_id}',
            {'application_id': application_id}
        )

    def create_global_application_command(
            self,
            application_id: Snowflake,
            *,
            name: str,
            description: str,
            options: Unknownish[typing.List[ApplicationCommandOption]] = UNKNOWN,
            default: Unknownish[bool] = UNKNOWN,
            type: Unknownish[CommandTypes] = UNKNOWN
    ) -> Request[ApplicationCommand]:
        return Request[ApplicationCommand](
            'POST',
            '/applications/{application_id}/commands',
            {'application_id': application_id},
            json=prepare(self, {
                'name': name,
                'description': description,
                'options': options,
                'default': default,
                'type': type
            })
        )

    def get_global_application_command(
            self,
            application_id: Snowflake,
            command_id: Snowflake
    ) -> Request[ApplicationCommand]:
        return Request[ApplicationCommand](
            'GET',
            '/applications/{application_id}/{command_id}',
            {'application_id': application_id, 'command_id': command_id}
        )

    def edit_global_application_command(
            self,
            application_id: Snowflake,
            command_id: Snowflake,
            *,
            name: Unknownish[str] = UNKNOWN,
            description: Unknownish[str] = UNKNOWN,
            options: Unknownish[typing.List[ApplicationCommandOption]] = UNKNOWN,
            default_permission: Unknownish[bool] = UNKNOWN
    ) -> Request[ApplicationCommand]:
        return Request[ApplicationCommand](
            'PATCH',
            '/applications/{application_id}/commands/{command_id}',
            {'application_id': application_id, 'command_id': command_id},
            json=prepare(self, {
                'name': name,
                'description': description,
                'options': options,
                'default_permission': default_permission
            })
        )

    def delete_global_application_command(
            self,
            application_id: Snowflake,
            command_id: Snowflake
    ) -> Request[None]:
        return Request[None](
            'DELETE',
            '/applications/{application_id}/commands/{command_id}',
            {'application_id': application_id, 'command_id': command_id}
        )

    def bulk_overwrite_global_application_commands(
            self,
            application_id: Snowflake,
            *,
            commands: typing.List[ApplicationCommand]
    ) -> Request[typing.List[ApplicationCommand]]:
        return Request[typing.List[ApplicationCommand]](
            'PUT',
            '/applications/{application_id}/commands',
            {'application_id': application_id},
            json=self.conv.unstructure(commands)
        )

    def get_guild_application_commands(
            self,
            application_id: Snowflake,
            guild_id: Snowflake
    ) -> Request[typing.List[ApplicationCommand]]:
        return Request(
            'GET',
            '/applications/{application_id}/guilds/{guild_id}/commands',
            {'application_id': application_id, 'guild_id': guild_id}
        )

    def create_guild_application_command(
            self,
            application_id: Snowflake,
            guild_id: Snowflake,
            *,
            name: str,
            description: str,
            options: Unknownish[typing.List[ApplicationCommandOption]] = UNKNOWN,
            default: Unknownish[bool] = UNKNOWN,
            type: Unknownish[CommandTypes] = UNKNOWN
    ) -> Request[ApplicationCommand]:
        return Request[ApplicationCommand](
            'POST',
            '/applications/{application_id}/commands',
            {'application_id': application_id},
            json=prepare(self, {
                'name': name,
                'description': description,
                'options': options,
                'default': default,
                'type': type
            })
        )

    def get_guild_application_command(
            self,
            application_id: Snowflake,
            guild_id: Snowflake,
            command_id: Snowflake
    ) -> Request[ApplicationCommand]:
        return Request[ApplicationCommand](
            'GET',
            '/applications/{application_id}/guilds/{guild_id}/commands/{command_id}',
            {'application_id': application_id, 'guild_id': guild_id, 'command_id': command_id}
        )

    def edit_guild_application_command(
            self,
            application_id: Snowflake,
            guild_id: Snowflake,
            command_id: Snowflake,
            *,
            name: Unknownish[str] = UNKNOWN,
            description: Unknownish[str] = UNKNOWN,
            options: Unknownish[typing.List[ApplicationCommandOption]] = UNKNOWN,
            default_permission: Unknownish[bool] = UNKNOWN
    ) -> Request[ApplicationCommand]:
        return Request[ApplicationCommand](
            'PATCH',
            '/applications/{application_id}/guilds/{guild_id}/commands/{command_id}',
            {'application_id': application_id, 'guild_id': guild_id, 'command_id': command_id},
            json=prepare(self, {
                'name': name,
                'description': description,
                'options': options,
                'default_permission': default_permission
            })
        )

    def delete_guild_application_command(
            self,
            application_id: Snowflake,
            guild_id: Snowflake,
            command_id: Snowflake
    ) -> Request[None]:
        return Request[None](
            'DELETE',
            '/applications/{application_id}/guilds/{guild_id}/commands/{command_id}',
            {'application_id': application_id, 'guild_id': guild_id, 'command_id': command_id}
        )

    def bulk_overwrite_guild_application_commands(
            self,
            application_id: Snowflake,
            guild_id: Snowflake,
            *,
            commands: typing.List[ApplicationCommand]
    ) -> Request[typing.List[ApplicationCommand]]:
        return Request[typing.List[ApplicationCommand]](
            'PUT',
            '/applications/{application_id}/guilds/{guild_id}/commands',
            {'application_id': application_id, 'guild_id': guild_id},
            json=self.conv.unstructure(commands)
        )

    def get_guild_application_command_permissions(
            self,
            application_id: Snowflake,
            guild_id: Snowflake,
    ) -> Request[typing.List[GuildApplicationCommandPermissions]]:
        return Request[typing.List[GuildApplicationCommandPermissions]](
            'GET',
            '/applications/{application_id}/guilds/{guild_id}/commands/permissions',
            {'application_id': application_id, 'guild_id': guild_id}
        )

    def get_application_command_permissions(
            self,
            application_id: Snowflake,
            guild_id: Snowflake,
            command_id: Snowflake
    ) -> Request[typing.List[ApplicationCommandPermissions]]:
        return Request[typing.List[ApplicationCommandPermissions]](
            'GET',
            '/applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions',
            {'application_id': application_id, 'guild_id': guild_id, 'command_id': command_id}
        )

    def edit_application_command_permissions(
            self,
            application_id: Snowflake,
            guild_id: Snowflake,
            command_id: Snowflake,
            *,
            permissions: typing.List[ApplicationCommandPermissions]
    ) -> Request[GuildApplicationCommandPermissions]:
        return Request[GuildApplicationCommandPermissions](
            'PUT',
            '/applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions',
            {'application_id': application_id, 'guild_id': guild_id, 'command_id': command_id},
            json=prepare(self, {'permissions': permissions})
        )

    def batch_edit_application_command_permissions(
            self,
            application_id: Snowflake,
            guild_id: Snowflake,
            *,
            # TODO: partial GuildApplicationCommandPermissions
            new_permissions: typing.Dict[typing.Any, typing.Any]
    ) -> Request[typing.List[GuildApplicationCommandPermissions]]:
        return Request[typing.List[GuildApplicationCommandPermissions]](
            'PUT',
            '/applications/{application_id}/guilds/{guild_id}/commands/permissions',
            {'application_id': application_id, 'guild_id': guild_id},
            json=self.conv.unstructure(new_permissions)
        )

    # TODO: what does this return?
    def create_interaction_response(
            self,
            application_id: Snowflake,
            interaction_token: str,
            *,
            response: InteractionResponse
    ) -> Request[None]:
        return Request[None](
            'POST',
            # this ratelimits on webhook
            '/interactions/{webhook_id}/{webhook_token}/callback',
            {'webhook_id': application_id, 'webhook_token': interaction_token},
            json=self.conv.unstructure(response)
        )

    def get_original_interaction_response(
            self,
            application_id: Snowflake,
            interaction_token: str,
    ) -> Request[Message]:
        return Request[Message](
            'GET',
            # this ratelimits on webhook
            '/webhooks/{webhook_id}/{webhook_token}/messages/@original',
            {'webhook_id': application_id, 'webhook_token': interaction_token}
        )

    def edit_original_interaction_response(
            self,
            application_id: Snowflake,
            interaction_token: str,
            *,
            content: Unknownish[typing.Optional[str]] = UNKNOWN,
            embeds: Unknownish[typing.Optional[typing.List[Embed]]] = UNKNOWN,
            # TODO: better file type
            file: Unknownish[typing.Optional[object]] = UNKNOWN,
            allowed_mentions: Unknownish[typing.Optional[AllowedMentions]] = UNKNOWN,
            attachments: Unknownish[typing.Optional[typing.List[Attachment]]] = UNKNOWN,
            components: Unknownish[typing.Optional[typing.List[Component]]] = UNKNOWN,
    ) -> Request[Message]:
        json_payload = prepare(self, {
            'content': content,
            'embeds': embeds,
            'allowed_mentions': allowed_mentions,
            'components': components,
            'attachments': attachments
        })

        return Request[Message](
            'PATCH',
            # this ratelimits on webhook
            '/webhooks/{webhook_id}/{webhook_token}/messages/@original',
            {'webhook_id': application_id, 'webhook_token': interaction_token},
            data={'payload_json': json.dumps(json_payload)} if json_payload else None,
            files={'file': file} if file != UNKNOWN else None
        )

    def delete_original_interaction_response(
            self,
            application_id: Snowflake,
            interaction_token: str
    ) -> Request[None]:
        return Request[None](
            'DELETE',
            # this ratelimits on webhook
            '/webhooks/{webhook_id}/{webhook_token}/messages/@original',
            {'webhook_id': application_id, 'webhook_token': interaction_token}
        )

    # TODO: interaction followups can't send stickers?
    # TODO: what does this return?
    def create_followup_message(
            self,
            application_id: Snowflake,
            interaction_token: str,
            *,
            # one of these is required:
            content: Unknownish[str] = UNKNOWN,
            file: Unknownish[object] = UNKNOWN,  # TODO: better file type?
            embeds: Unknownish[typing.List[Embed]] = UNKNOWN,
            # optional
            flags: Unknownish[MessageFlags] = UNKNOWN,
            # TODO: interaction followups probably can't do these?
            username: Unknownish[str] = UNKNOWN,
            avatar_url: Unknownish[str] = UNKNOWN,
            tts: Unknownish[bool] = UNKNOWN,
            allowed_mentions: Unknownish[AllowedMentions] = UNKNOWN,
            message_reference: Unknownish[MessageReference] = UNKNOWN,
            components: Unknownish[typing.List[Component]] = UNKNOWN,
    ) -> Request[None]:
        json_payload = prepare(self, {
            'content': content,
            'embeds': embeds,
            'username': username,
            'avatar_url': avatar_url,
            'tts': tts,
            'allowed_mentions': allowed_mentions,
            'message_reference': message_reference,
            'components': components,
        })

        return Request[None](
            'POST',
            # this ratelimits on webhook
            '/webhooks/{webhook_id}/{webhook_token}',
            {'webhook_id': application_id, 'webhook_token': interaction_token},
            data={'payload_json': json.dumps(json_payload)} if json_payload else None,
            files={'file': file} if file != UNKNOWN else None
        )

    def get_followup_message(
            self,
            application_id: Snowflake,
            interaction_token: str,
            message_id: Snowflake
    ) -> Request[Message]:
        return Request[Message](
            'GET',
            # this ratelimits on webhook
            '/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}',
            {
                'webhook_id': application_id,
                'webhook_token': interaction_token,
                'message_id': message_id
            }
        )

    def edit_followup_message(
            self,
            application_id: Snowflake,
            interaction_token: str,
            message_id: Snowflake,
            *,
            content: Unknownish[typing.Optional[str]] = UNKNOWN,
            embeds: Unknownish[typing.Optional[typing.List[Embed]]] = UNKNOWN,
            # TODO: better file type
            file: Unknownish[typing.Optional[object]] = UNKNOWN,
            allowed_mentions: Unknownish[typing.Optional[AllowedMentions]] = UNKNOWN,
            attachments: Unknownish[typing.Optional[typing.List[Attachment]]] = UNKNOWN,
            components: Unknownish[typing.Optional[typing.List[Component]]] = UNKNOWN,
    ) -> Request[Message]:
        json_payload = prepare(self, {
            'content': content,
            'embeds': embeds,
            'allowed_mentions': allowed_mentions,
            'components': components,
            'attachments': attachments
        })

        return Request[Message](
            'PATCH',
            '/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}',
            {
                'webhook_id': application_id,
                'webhook_token': interaction_token,
                'message_id': message_id
            },
            data={'payload_json': json.dumps(json_payload)} if json_payload else None,
            files={'file': file} if file != UNKNOWN else None
        )

    def delete_followup_message(
            self,
            application_id: Snowflake,
            interaction_token: str,
            message_id: Snowflake
    ) -> Request[None]:
        return Request[None](
            'DELETE',
            '/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}',
            {
                'webhook_id': application_id,
                'webhook_token': interaction_token,
                'message_id': message_id
            }
        )
