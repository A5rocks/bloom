""" connects to Discord's gateway """
from __future__ import annotations

import enum
import json
import logging
import platform
import random
import typing

import attr
import trio
import trio_websocket
from cattr import Converter
from cattr.preconf.json import make_converter

import bloom._compat as compat
import bloom.models.base as base_models
import bloom.models.gateway as gateway_models
import bloom.models.permissions as permission_models
import bloom.substrate as subs

tags_to_model = {
    'READY': gateway_models.ReadyEvent,
    'CHANNEL_CREATE': gateway_models.ChannelCreateEvent,
    'CHANNEL_UPDATE': gateway_models.ChannelUpdateEvent,
    'CHANNEL_DELETE': gateway_models.ChannelDeleteEvent,
    'THREAD_CREATE': gateway_models.ThreadCreateEvent,
    'THREAD_UPDATE': gateway_models.ThreadUpdateEvent,
    'THREAD_DELETE': gateway_models.ThreadDeleteEvent,
    'THREAD_LIST_SYNC': gateway_models.ThreadListSyncEvent,
    'THREAD_MEMBER_UPDATE': gateway_models.ThreadMemberUpdateEvent,
    'THREAD_MEMBERS_UPDATE': gateway_models.ThreadMembersUpdateEvent,
    'CHANNEL_PINS_UPDATE': gateway_models.ChannelPinsUpdateEvent,
    'GUILD_CREATE': gateway_models.GuildCreateEvent,
    'GUILD_UPDATE': gateway_models.GuildUpdateEvent,
    'GUILD_DELETE': gateway_models.GuildDeleteEvent,
    'GUILD_BAN_ADD': gateway_models.GuildBanAddEvent,
    'GUILD_BAN_REMOVE': gateway_models.GuildBanRemoveEvent,
    'GUILD_EMOJIS_UPDATE': gateway_models.GuildEmojisUpdateEvent,
    'GUILD_STICKERS_UPDATE': gateway_models.GuildStickersUpdateEvent,
    'GUILD_INTEGRATIONS_UPDATE': gateway_models.GuildIntegrationsUpdateEvent,
    'GUILD_MEMBER_ADD': gateway_models.GuildMemberAddEvent,
    'GUILD_MEMBER_REMOVE': gateway_models.GuildMemberRemoveEvent,
    'GUILD_MEMBER_UPDATE': gateway_models.GuildMemberUpdateEvent,
    'GUILD_MEMBERS_CHUNK': gateway_models.GuildMembersChunkEvent,
    'GUILD_ROLE_CREATE': gateway_models.GuildRoleCreateEvent,
    'GUILD_ROLE_UPDATE': gateway_models.GuildRoleUpdateEvent,
    'GUILD_ROLE_DELETE': gateway_models.GuildRoleDeleteEvent,
    'INTEGRATION_CREATE': gateway_models.IntegrationCreateEvent,
    'INTEGRATION_UPDATE': gateway_models.IntegrationUpdateEvent,
    'INTEGRATION_DELETE': gateway_models.IntegrationDeleteEvent,
    'INVITE_CREATE': gateway_models.InviteCreateEvent,
    'INVITE_DELETE': gateway_models.InviteDeleteEvent,
    'MESSAGE_CREATE': gateway_models.MessageCreateEvent,
    'MESSAGE_UPDATE': gateway_models.MessageUpdateEvent,
    'MESSAGE_DELETE': gateway_models.MessageDeleteEvent,
    'MESSAGE_DELETE_BULK': gateway_models.MessageDeleteBulkEvent,
    'MESSAGE_REACTION_ADD': gateway_models.MessageReactionAddEvent,
    'MESSAGE_REACTION_REMOVE': gateway_models.MessageReactionRemoveEvent,
    'MESSAGE_REACTION_REMOVE_ALL': gateway_models.MessageReactionRemoveAllEvent,
    'MESSAGE_REACTION_REMOVE_EMOJI': gateway_models.MessageReactionRemoveEmojiEvent,
    'PRESENCE_UPDATE': gateway_models.PresenceUpdateEvent,
    'TYPING_START': gateway_models.TypingStartEvent,
    'USER_UPDATE': gateway_models.UserUpdateEvent,
    'VOICE_STATE_UPDATE': gateway_models.VoiceStateUpdateEvent,
    'VOICE_SERVER_UPDATE': gateway_models.VoiceServerUpdateEvent,
    'WEBHOOKS_UPDATE': gateway_models.WebhooksUpdateEvent,
    'INTERACTION_CREATE': gateway_models.InteractionCreateEvent,
    'STAGE_INSTANCE_CREATE': gateway_models.StageInstanceCreateEvent,
    'STAGE_INSTANCE_UPDATE': gateway_models.StageInstanceUpdateEvent,
    'STAGE_INSTANCE_DELETE': gateway_models.StageInstanceDeleteEvent,
    'RESUMED': gateway_models.ResumedEvent,
}

if typing.TYPE_CHECKING:
    import typing_extensions


_LOGGER: typing_extensions.Final[logging.Logger] = logging.getLogger('bloom.shard')
ONE_HOUR = 60 * 60


@attr.define()
class _ShardData:
    converter: Converter
    substrate: subs.Substrate
    seq: typing.Optional[int] = None
    have_acked: bool = True
    session_id: typing.Optional[str] = None


@attr.define()
class _Bucket:
    pk: trio.lowlevel.ParkingLot
    _setter_queued: bool = False

    async def park(self) -> None:
        if not self._setter_queued:
            self._setter_queued = True
            await trio.lowlevel.checkpoint()
            return

        await self.pk.park()
        self._setter_queued = True

    async def set(self) -> None:
        await trio.sleep(5)
        self.pk.unpark()
        self._setter_queued = False


@attr.define()
class _ConnectionInfo:
    token: str
    intents: int
    shard_id: int
    shard_count: int
    bucket: _Bucket
    converter: Converter
    substrate: subs.Substrate


@attr.define()
class _Backoff:
    base: float = 2.0
    jitter: float = 0.2
    repeats: int = 0
    end: int = 6

    async def wait(self) -> None:
        if self.repeats < self.end:
            self.repeats += 1
        # 2, 4, 8, 16, 32, 64, 64, 64
        await trio.sleep(
            # exponential wait
            self.base ** self.repeats
            # random jitter (+- jitter)
            + random.random() * 2 * self.jitter - self.jitter
        )

    def reset(self) -> None:
        self.repeats = 0


@attr.define()
class ShardException(Exception):
    pass


@attr.define()
class _MissedHeartbeat(ShardException):
    pass


@attr.define()
class TooManyIdentifies(ShardException):
    pass


@attr.define()
class _NonMonotonicHeartbeat(ShardException):
    pass


# TODO: remove in non-debug version
@attr.define()
class _MissingKey(ShardException):
    tag: str
    data: typing.Dict[str, typing.Any]
    unexpected: object


class Intents(enum.IntFlag):
    GUILDS = 1 << 0
    GUILD_MEMBERS = 1 << 1
    GUILD_BANS = 1 << 2
    GUILD_EMOJIS = 1 << 3
    GUILD_INTEGRATIONS = 1 << 4
    GUILD_WEBHOOKS = 1 << 5
    GUILD_INVITES = 1 << 6
    GUILD_VOICE_STATES = 1 << 7
    GUILD_PRESENCES = 1 << 8
    GUILD_MESSAGES = 1 << 9
    GUILD_MESSAGE_REACTIONS = 1 << 10
    GUILD_MESSAGE_TYPING = 1 << 11
    DIRECT_MESSAGES = 1 << 12
    DIRECT_MESSAGE_REACTIONS = 1 << 13
    DIRECT_MESSAGE_TYPING = 1 << 14

    @classmethod
    def all(cls) -> Intents:
        return (cls.GUILDS
                | cls.GUILD_MEMBERS
                | cls.GUILD_BANS
                | cls.GUILD_EMOJIS
                | cls.GUILD_INTEGRATIONS
                | cls.GUILD_WEBHOOKS
                | cls.GUILD_INVITES
                | cls.GUILD_VOICE_STATES
                | cls.GUILD_PRESENCES
                | cls.GUILD_MESSAGES
                | cls.GUILD_MESSAGE_REACTIONS
                | cls.GUILD_MESSAGE_TYPING
                | cls.DIRECT_MESSAGES
                | cls.DIRECT_MESSAGE_REACTIONS
                | cls.DIRECT_MESSAGE_TYPING)

    @classmethod
    def unprivileged(cls) -> Intents:
        return cls.all() & ~(cls.GUILD_MEMBERS | cls.GUILD_PRESENCES)


class _EveryPayload(compat.TypedDict):
    op: compat.Literal[1, 7, 9, 10, 11]
    d: typing.Any


class _DispatchPayload(compat.TypedDict):
    op: compat.Literal[0]
    t: str
    s: int
    d: typing.Any


_DiscordPayload = typing.Union[_EveryPayload, _DispatchPayload]


# exhaustive checks with mypy!
def _never(thing: typing.NoReturn) -> typing.NoReturn:
    raise RuntimeError(f'Unexpected input {thing}')


async def _heartbeat(
        websocket: trio_websocket.WebSocketConnection,
        interval: float,
        data: _ShardData
) -> typing.NoReturn:
    while True:
        await trio.sleep(interval)

        if not data.have_acked:
            raise _MissedHeartbeat()

        data.have_acked = False
        await websocket.send_message(json.dumps({
            'op': 1,
            'd': data.seq
        }))


async def _stream(
        websocket: trio_websocket.WebSocketConnection
) -> typing.AsyncGenerator[_DiscordPayload, None]:
    while True:
        message = await websocket.get_message()
        yield json.loads(message)


# TODO: figure out how to decrease the number of arguments this takes?
async def _shared_logic(
        websocket: trio_websocket.WebSocketConnection,
        data: _ShardData,
        nursery: trio.Nursery,
        hello: typing.Dict[str, typing.Any],
        after_start: typing.Callable[[], typing.Awaitable[None]]
) -> bool:
    # the return value is whether or not to resume next time.

    async for message in _stream(websocket):
        if message['op'] == 0:
            if message['t'] == 'READY':
                data.session_id = message['d']['session_id']

            seq = message['s']

            if data.seq and seq < data.seq:
                raise _NonMonotonicHeartbeat()

            data.seq = seq

            # https://discord.com/channels/613425648685547541/697489244649816084/870221091849793587
            if message['t'] == 'GUILD_APPLICATION_COMMAND_COUNTS_UPDATE':
                continue

            try:
                model: object = data.converter.structure(message['d'], tags_to_model[message['t']])
                reverse: typing.Dict[str, object] = data.converter.unstructure(model)

                if not _skip_differences(message['t']):
                    differences = (
                        _diff_differences(reverse, message['d'])
                        - _allowed_differences(message['t'])
                    )
                    # https://github.com/discord/discord-api-docs/issues/1789
                    differences = differences - {'guild_hashes'}
                    if differences:
                        raise _MissingKey(message['t'], message['d'], differences)
            except Exception as e:
                _LOGGER.exception('improper payload', exc_info=e)

            await data.substrate.broadcast(model)

        elif message['op'] == 1:
            await websocket.send_message(json.dumps({
                'op': 1,
                'd': data.seq
            }))

        elif message['op'] == 7:
            return True

        elif message['op'] == 9:
            return bool(message['d'])

        elif message['op'] == 10:
            nursery.start_soon(
                _heartbeat,
                websocket,
                message['d']['heartbeat_interval'] / 1000,
                data
            )
            await websocket.send_message(json.dumps(hello))
            nursery.start_soon(after_start)

        elif message['op'] == 11:
            data.have_acked = True

        else:
            _LOGGER.warning('UNIMPLEMENTED %r', message['op'])
            _never(message)

    # early return? the backoff will handle identifying eventually, so a RESUME is fine
    return True


async def _run_once(
        shard_data: _ShardData,
        info: _ConnectionInfo,
        nursery: trio.Nursery,
        websocket: trio_websocket.WebSocketConnection,
        resume: bool = False
) -> bool:
    # the return value is whether or not to resume next time.

    # don't want to immediately exit due to "no heartbeat recv-ed"
    shard_data.have_acked = True

    if resume:
        hello = {
            'op': 6,
            'd': {
                'token': info.token,
                'session_id': shard_data.session_id,
                'seq': shard_data.seq
            }
        }

        async def setter() -> None:
            await trio.lowlevel.checkpoint()

    else:
        hello = {
            'op': 2,
            'd': {
                'token': info.token,
                'intents': info.intents,
                'properties': {
                    '$os': platform.system().lower(),
                    '$browser': 'blinkenlights',
                    '$device': 'bloom'
                },
                'large_threshold': 250,  # TODO: customizable?
                'shard': [info.shard_id, info.shard_count],
                # TODO: presence?
            }
        }
        setter = info.bucket.set

    return await _shared_logic(websocket, shard_data, nursery, hello, setter)


async def _run_shard(
        info: _ConnectionInfo,
) -> typing.NoReturn:
    data = _ShardData(info.converter, info.substrate)

    # variables for not uselessly resuming
    should_resume = False
    resumes = 0
    resume_backoff = _Backoff()
    last_resume = trio.current_time()

    # variables for not uselessly identifying
    identifies = 0
    last_identify = trio.current_time()
    identify_backoff = _Backoff(base=5.0, end=3)

    while True:
        if should_resume:
            _LOGGER.info('resuming')
            last_resume = trio.current_time()
            resumes += 1
        else:
            await info.bucket.park()
            _LOGGER.info('identifying')
            data = _ShardData(info.converter, info.substrate)
            last_identify = trio.current_time()
            identifies += 1

        # TODO: dynamically get url
        url = 'wss://gateway.discord.gg/?v=9&encoding=json'

        # set a max message size of 10mb since guilds are HUGE
        async with trio_websocket.open_websocket_url(
            url,
            max_message_size=10 * 1024 * 1024
        ) as websocket:
            try:
                async with trio.open_nursery() as nursery:
                    should_resume = await _run_once(data, info, nursery, websocket, should_resume)

                    if should_resume:
                        await websocket.aclose(3000)
                    else:
                        await websocket.aclose(1000)

                    nursery.cancel_scope.cancel()
            except trio_websocket.ConnectionClosed as exc:
                _LOGGER.warning('[%r] websocket closed due to %r',
                                exc.reason.code, exc.reason.reason)

                # TODO: have a more comprehensive set of close codes
                should_resume = exc.reason.code not in [1000, 1001]

            except _MissedHeartbeat as exc:
                await websocket.aclose(3000)

                _LOGGER.exception('missed a heartbeat', exc_info=exc)
                should_resume = True

            except _NonMonotonicHeartbeat as exc:
                await websocket.aclose(3000)

                _LOGGER.exception('heartbeat advanced non-monotonically', exc_info=exc)
                should_resume = True

            except trio.MultiError as exc:
                await websocket.aclose(1000)

                _LOGGER.exception('multiple exceptions thrown', exc_info=exc)
                should_resume = False

        # temporary variable to make logic clearer
        should_identify = not should_resume

        if should_identify:
            # identifying implies not resuming, so reset that backoff.
            resumes = 0
            resume_backoff.reset()

        if resumes >= 10:
            # well. Discord has just been evil.
            # just re-identify I guess?
            should_resume = False
            should_identify = True

        if identifies >= 4:
            # and Discord made the bot re-identify wayyy too much.
            # there's an identify ratelimit, which makes me antsy.
            raise TooManyIdentifies()

        if trio.current_time() - last_identify > ONE_HOUR:
            identifies = 0
            identify_backoff.reset()
        elif should_identify and identifies < 4:
            await identify_backoff.wait()

        if trio.current_time() - last_resume > ONE_HOUR:
            resumes = 0
            resume_backoff.reset()
        elif should_resume and resumes < 10:
            await resume_backoff.wait()


def _register_converter(converter: Converter) -> Converter:
    converter.register_structure_hook(
        base_models.Snowflake,
        lambda d, _: base_models.Snowflake(int(d))
    )
    converter.register_structure_hook(
        permission_models.BitwisePermissionFlags,
        lambda d, _: permission_models.BitwisePermissionFlags(int(d))
    )

    def unstruct_permissions(d: permission_models.BitwisePermissionFlags) -> str:
        return str(d.value)

    converter.register_unstructure_hook(
        permission_models.BitwisePermissionFlags,
        unstruct_permissions
    )

    def struct_int_or_str(d: typing.Any, _: object) -> typing.Union[int, str]:
        try:
            return int(d)
        except ValueError:
            return str(d)

    converter.register_structure_hook(typing.Union[int, str], struct_int_or_str)

    UNKNOWN_TYPE = base_models.UNKNOWN_TYPE

    # TODO: use the new methods in `typing`
    def is_unknown(cls: type) -> bool:
        if getattr(
            cls, '__origin__'
        ) is typing.Union and UNKNOWN_TYPE in getattr(cls, '__args__'):
            return True
        return False

    def unknown_function(data: object, cls: typing.Type[typing.Any]) -> object:
        args = getattr(cls, '__args__', tuple())
        if len(args) == 2:
            return converter.structure(data, [n for n in args if n != UNKNOWN_TYPE][0])
        else:
            type: typing.Any = typing.Union[tuple(n for n in args if n != UNKNOWN_TYPE)]
            return converter.structure(data, type)

    converter.register_structure_hook_func(is_unknown, unknown_function)

    return converter


def _allowed_differences(tag: str) -> typing.Set[str]:
    # TODO: remove in non-debug version
    if tag == 'READY':
        return {
            # https://github.com/discord/discord-api-docs/issues/1239#issuecomment-563396658
            'user_settings',
            'relationships',
            'presences',
            # https://github.com/discord/discord-api-docs/commit/ab5d49ae7
            '_trace',
            # https://github.com/discord/discord-api-docs/commit/f36156dbb
            'private_channels',
            # in discord api
            # https://discord.com/channels/81384788765712384/381887113391505410/835382981681348668
            'guild_join_requests',
            # supposedly, for client voice region ordering
            # in discord bots
            # https://discord.com/channels/110373943822540800/110373943822540800/870570058424913930
            'geo_ordered_rtc_regions',
        }
    elif tag == 'GUILD_MEMBER_UPDATE':
        return {
            # https://github.com/discord/discord-api-docs/pull/1610#issuecomment-626846583
            'hoisted_role',
            # https://github.com/discord/discord-api-docs/pull/2299#issuecomment-742773209
            'is_pending',
        }
    elif tag == 'GUILD_MEMBER_ADD':
        return {
            # https://github.com/discord/discord-api-docs/pull/2299#issuecomment-742773209
            'is_pending',
        }
    elif tag == 'GUILD_CREATE':
        return {
            # https://github.com/discord/discord-api-docs/pull/2976#issuecomment-846251199
            'nsfw',
            # https://github.com/discord/discord-api-docs/pull/1074#issuecomment-522193546
            'lazy',
            # https://github.com/discord/discord-api-docs/pull/3063#issuecomment-855013415
            'application_command_count',
            # in discord developers
            # https://discord.com/channels/613425648685547541/697489244649816084/870221091849793587
            'application_command_counts',
            # I asked in DDevs, no answer yet.
            'guild_scheduled_events',
            # TODO: ??
            'embedded_activities',
            # https://github.com/discord/discord-api-docs/pull/4001
            'premium_progress_bar_enabled',
        }
    elif tag == 'GUILD_UPDATE':
        return {
            # https://github.com/discord/discord-api-docs/pull/2976#issuecomment-846251199
            'nsfw',
            # https://github.com/discord/discord-api-docs/issues/582
            'guild_id',
            # TODO: this seems to be guild hubs related but is nullable and undoc-ed
            'hub_type',
        }
    elif tag == 'THREAD_UPDATE':
        return {
            # will be removed soon-ish...
            # in discord developers
            # https://discord.com/channels/613425648685547541/859161948184379403/860543147817697300
            'audience',
        }
    elif tag == 'THREAD_DELETE':
        return {
            # will be removed soon-ish...
            # in discord developers
            # https://discord.com/channels/613425648685547541/859161948184379403/860543147817697300
            'audience',
        }
    elif tag == 'RESUMED':
        return {
            # https://github.com/discord/discord-api-docs/commit/ab5d49ae7
            '_trace',
        }
    elif tag == 'PRESENCE_UPDATE':
        # TODO: a custom user type for presences with these?
        return {
            'user.username',
            'user.discriminator',
            'user.avatar',
            'user.public_flags',
            'user.bot',
        }
    elif tag == 'MESSAGE_CREATE':
        return {
            # https://github.com/discord/discord-api-docs/pull/1610
            'member.hoisted_role',
            # https://github.com/discord/discord-api-docs/pull/2299#issuecomment-742773209
            'member.is_pending',
            # TODO: seems to be a partial member object? (same partial as on message)
            'interaction.member',
        }
    elif tag == 'MESSAGE_UPDATE':
        return {
            # https://github.com/discord/discord-api-docs/pull/1610
            'member.hoisted_role',
            # https://github.com/discord/discord-api-docs/pull/2299#issuecomment-742773209
            'member.is_pending',
            # TODO: seems to be a partial member object? (same partial as on message)
            'interaction.member',
        }
    elif tag == 'MESSAGE_REACTION_ADD':
        return {
            # https://github.com/discord/discord-api-docs/pull/1610
            'member.hoisted_role',
            # https://github.com/discord/discord-api-docs/pull/2299#issuecomment-742773209
            'member.is_pending',
        }
    elif tag == 'TYPING_START':
        return {
            # https://github.com/discord/discord-api-docs/pull/1610
            'member.hoisted_role',
            # https://github.com/discord/discord-api-docs/pull/2299#issuecomment-742773209
            'member.is_pending',
        }
    elif tag == 'VOICE_STATE_UPDATE':
        return {
            # https://github.com/discord/discord-api-docs/pull/1610
            'member.hoisted_role',
            # https://github.com/discord/discord-api-docs/pull/2299#issuecomment-742773209
            'member.is_pending',
        }
    elif tag == 'THREAD_MEMBERS_UPDATE':
        return {
            # SHOULD be removed soon.
            'audience'
        }
    elif tag == 'THREAD_MEMBER_UPDATE':
        return {
            # only meaningful for users
            'mute_config',
            'muted',
            # TODO: document this on the documentation.
            'guild_id'
        }

    return set()


def _skip_differences(tag: str) -> bool:
    # TODO: remove in non-debug version
    # these are payloads that aren't fully implemented
    return False


def _diff_differences(
    one: typing.Dict[str, object],
    two: typing.Dict[str, object]
) -> typing.Set[str]:
    # TODO: remove in non-debug version
    keys = {k for k in two if k not in one}
    keys.update(
        {
            k + '.' + v
            for k in set(one) if isinstance(one.get(k), dict) and isinstance(two.get(k), dict)
            # this type ignore shouldn't be necessary due to narrowing, but oh well.
            for v in _diff_differences(one[k], two[k])  # type: ignore[arg-type]
        }
    )

    return keys


async def connect(
        token: str,
        intents: Intents,
        substrate: subs.Substrate,
        *,
        shard_ids: typing.Sequence[int] = (0,),
        shard_count: int = 1,
        max_concurrency: int = 1
) -> typing.NoReturn:
    """Connects to the gateway with a specified token."""
    converter = _register_converter(make_converter())
    buckets = [_Bucket(trio.lowlevel.ParkingLot()) for _ in range(max_concurrency)]

    async with trio.open_nursery() as nursery:
        for shard_id in shard_ids:
            bucket = buckets[shard_id % max_concurrency]
            info = _ConnectionInfo(
                token,
                intents,
                shard_id,
                shard_count,
                bucket,
                converter,
                substrate
            )
            nursery.start_soon(_run_shard, info)

    raise RuntimeError('Should never get here.')

__all__ = ('connect', 'Intents', 'ShardException', 'TooManyIdentifies')
