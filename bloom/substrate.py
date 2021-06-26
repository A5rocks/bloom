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

    def register(
            self,
            typ: typing.Type[T],
            buffer_size: typing.Optional[int]
    ) -> trio.abc.ReceiveChannel[T]:
        buffer_size_ = math.inf if buffer_size is None else buffer_size

        send, recv = trio.open_memory_channel[T](buffer_size_)
        self._events[typ].append(send)
        self._recv_to_send[(typ, recv)] = send

        return recv

    def unregister(self, typ: typing.Type[T], chan: trio.abc.ReceiveChannel[T]) -> None:
        if (typ, chan) not in self._recv_to_send:
            return

        self._events[typ].remove(self._recv_to_send.pop((typ, chan)))

    async def broadcast(self, message: typing.Any) -> None:
        # TODO: should I broadcast to listeners listening to
        #   types up the mro?
        listeners = self._events[type(message)]

        if not listeners:
            await trio.lowlevel.checkpoint()
            return

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
