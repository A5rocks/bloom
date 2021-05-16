""" connects to Discord's gateway """
from __future__ import annotations

import enum
import json
import logging
import random
import typing

import attr
import trio
import trio_websocket


@attr.define()
class _ShardData:
    seq: typing.Optional[int] = None
    have_acked: bool = True
    session_id: typing.Optional[str] = None


@attr.define()
class _ConnectionInfo:
    token: str
    intents: int
    shard_id: int
    shard_count: int


@attr.define()
class _Backoff:
    _base: float = 2.0
    _jitter: float = 0.2
    _repeats: int = 0
    _end: int = 6

    async def wait(self) -> None:
        if self._repeats < self._end:
            self._repeats += 1
        # 2, 4, 8, 16, 32, 64, 64, 64
        await trio.sleep(
            # exponential wait
            self._base ** self._repeats
            # random jitter (+- jitter)
            + random.random() * 2 * self._jitter - self._jitter
        )

    def reset(self) -> None:
        self._repeats = 0


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

async def _heartbeat(
        websocket: trio_websocket.WebSocketConnection,
        interval: float,
        data: _ShardData
) -> typing.NoReturn:
    while True:
        await trio.sleep(interval)

        if not data.have_acked:
            # want to reconnect.
            await websocket.aclose(1006)
            raise _MissedHeartbeat()

        data.have_acked = False
        await websocket.send_message(json.dumps({
            'op': 1,
            'd': data.seq
        }))


# TODO: this should probably return TypedDict-s
async def _stream(
        websocket: trio_websocket.WebSocketConnection
) -> typing.AsyncGenerator[typing.Dict[str, typing.Any], None]:
    while True:
        message = await websocket.get_message()
        yield json.loads(message)


# TODO: figure out how to decrease the number of arguments this takes?
async def _shared_logic(
        websocket: trio_websocket.WebSocketConnection,
        data: _ShardData,
        nursery: trio.Nursery,
        hello: typing.Dict[str, typing.Any]
) -> bool:
    # the return value is whether or not to resume next time.

    async for message in _stream(websocket):
        if message['op'] == 0:
            if message['t'] == 'READY':
                data.session_id = message['d']['session_id']

            seq = message['s']

            if data.seq and seq < data.seq:
                await websocket.aclose(1006)
                raise _NonMonotonicHeartbeat()

            data.seq = seq

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

        elif message['op'] == 11:
            data.have_acked = True

        else:
            logging.warning('UNIMPLEMENTED %r', message['op'])

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
    else:
        hello = {
            'op': 2,
            'd': {
                'token': info.token,
                'intents': info.intents,
                'properties': {
                    # TODO: this
                    '$os': 'linux',
                    '$browser': 'blinkenlights',
                    '$device': 'bloom'
                },
                'large_threshold': 250,  # TODO: customizable?
                'shard': [info.shard_id, info.shard_count],
                # TODO: presence?
            }
        }

    return await _shared_logic(websocket, shard_data, nursery, hello)


async def _run_shard(
        info: _ConnectionInfo,
        nursery: trio.Nursery
) -> typing.NoReturn:
    data = _ShardData()

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
            last_resume = trio.current_time()
            resumes += 1
        else:
            data = _ShardData()
            last_identify = trio.current_time()
            identifies += 1

        try:
            async with trio.open_nursery() as nursery:
                # TODO: dynamically get url
                url = "wss://gateway.discord.gg/?v=9&encoding=json"
                # set a max message size of 10mb since guilds are HUGE
                async with trio_websocket.open_websocket_url(url, max_message_size=10 * 1024 * 1024) as websocket:
                    should_resume = await _run_once(data, info, nursery, websocket, should_resume)

                    if should_resume:
                        await websocket.aclose(1006)
                    else:
                        await websocket.aclose(1000)

        except trio_websocket.ConnectionClosed as exc:
            logging.warning('[%r] websocket closed due to %r', exc.reason.code, exc.reason.reason)

            # TODO: have a more comprehensive set of close codes
            should_resume = exc.reason.code not in [1000, 1001]

        except _MissedHeartbeat as exc:
            logging.exception('missed a heartbeat', exc_info=exc)
            should_resume = True

        except _NonMonotonicHeartbeat as exc:
            logging.exception('heartbeat advanced non-monotonically', exc_info=exc)
            should_resume = True

        # resetting the counters:
        if trio.current_time() - last_identify > 60 * 60:
            identifies = 0
            identify_backoff.reset()

        if trio.current_time() - last_resume > 60 * 60:
            resumes = 0
            resume_backoff.reset()

        if not should_resume:
            resumes = 0
            resume_backoff.reset()

        # backing off:
        if should_resume and 0 < resumes < 10:
            await resume_backoff.wait()

        if resumes >= 10:
            # well. Discord has just been evil.
            # just re-identify I guess?
            should_resume = False

        if not should_resume and 0 < identifies < 4:
            await identify_backoff.wait()

        if identifies >= 4:
            # and Discord made the bot re-identify wayyy too much.
            # there's an identify ratelimit, which makes me antsy.
            raise TooManyIdentifies()


async def connect(
        token: str,
        intents: int,
        *,
        shard_ids: typing.Sequence[int] = (0,),
        shard_count: int = 1
) -> typing.NoReturn:
    """Connects to the gateway with a specified token."""
    async with trio.open_nursery() as nursery:
        for shard_id in shard_ids:
            info = _ConnectionInfo(token, intents, shard_id, shard_count)
            nursery.start_soon(_run_shard, info, nursery)

    raise RuntimeError("Should never get here.")

__all__ = ('connect', 'Intents', 'ShardException', 'TooManyIdentifies')
