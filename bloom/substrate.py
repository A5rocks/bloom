# this backpressures based on the slowest consumer.
# if you mess this up, then uh, raise an issue.
# until then I do not want to think about design.
from __future__ import annotations

import collections
import math
import typing

import attr
import trio

T = typing.TypeVar('T')


@attr.define()
class Substrate:
    _events: typing.Dict[
        typing.Type[typing.Any],
        typing.List[trio.abc.SendChannel[typing.Any]]
    ] = attr.Factory(lambda: collections.defaultdict(lambda: []))

    _recv_to_send: typing.Dict[
        typing.Tuple[typing.Type[typing.Any], trio.abc.ReceiveChannel[typing.Any]],
        trio.abc.SendChannel[typing.Any]
    ] = attr.Factory(dict)

    # this cache makes event -> channels amortized O(1)
    _cache: typing.Dict[
        typing.Type[typing.Any],
        typing.List[typing.Any]
    ] = attr.Factory(dict)

    def register(
            self,
            typ: typing.Type[T],
            buffer_size: typing.Optional[int]
    ) -> trio.abc.ReceiveChannel[T]:
        buffer_size_ = math.inf if buffer_size is None else buffer_size

        if typ not in self._events:
            # cache invalidation is hard, just flush it every time there's a
            # possibility of change.
            self._cache = {}

        send, recv = trio.open_memory_channel[T](buffer_size_)
        self._events[typ].append(send)
        self._recv_to_send[(typ, recv)] = send

        return recv

    def unregister(self, typ: typing.Type[T], chan: trio.abc.ReceiveChannel[T]) -> None:
        if (typ, chan) not in self._recv_to_send:
            return

        self._events[typ].remove(self._recv_to_send.pop((typ, chan)))

    async def broadcast(self, message: typing.Any) -> None:
        listener_types = self._cache.get(type(message))

        if not listener_types:
            listener_types = [typ for typ in self._events.keys() if isinstance(message, typ)]
            self._cache[type(message)] = listener_types

        listeners = [
            listener
            for listener_type in listener_types
            for listener in self._events[listener_type]
        ]

        async with trio.open_nursery() as nursery:
            for listener in listeners:
                nursery.start_soon(listener.send, message)

    async def aclose(self) -> None:
        self._recv_to_send.clear()

        for k, chans in self._events.items():
            for chan in chans:
                await chan.aclose()

            self._events[k].clear()

        # just in case, trio-nic
        await trio.lowlevel.checkpoint()
