from __future__ import annotations

from ipaddress import IPv4Address, IPv6Address
from ssl import SSLContext
from typing import (Any, AsyncContextManager, Iterator, List, Optional, Tuple,
                    Union)

from trio import Nursery
from trio.abc import Stream

def open_websocket_url(
    url: str,
    ssl_context: Optional[SSLContext] = ...,
    *,
    subprotocols: Optional[Iterator[str]] = ...,
    extra_headers: Optional[List[Tuple[bytes, bytes]]] = ...,
    message_queue_size: int = ...,
    max_message_size: int = ...,
    connect_timeout: float = ...,
    disconnect_timeout: float = ...
) -> AsyncContextManager[WebSocketConnection]: ...


async def wrap_client_stream(
    nursery: Nursery,
    stream: Stream,
    host: str,
    resource: str,
    *,
    subprotocols: Optional[Iterator[str]] = ...,
    extra_headers: Optional[List[Tuple[bytes, bytes]]] = ...,
    message_queue_size: int = ...,
    max_message_size: int = ...
) -> WebSocketConnection: ...


class HandshakeError(Exception):
    ...


class ConnectionTimeout(HandshakeError):
    ...


class DisconnectionTimeout(HandshakeError):
    ...


class ConnectionClosed(Exception):
    reason: CloseReason = ...
    def __init__(self, reason: Any) -> None: ...


class ConnectionRejected(HandshakeError):
    status_code: int = ...
    headers: Optional[Tuple[Tuple[bytes, bytes], ...]] = ...
    body: Optional[bytes] = ...


class CloseReason:
    @property
    def code(self) -> int: ...
    @property
    def name(self) -> str: ...
    @property
    def reason(self) -> str: ...


class WebSocketConnection:
    # TODO: re-inherit from `trio.abc.AsyncResource`
    #   blocked on https://github.com/python/mypy/issues/10400
    CONNECTION_ID: Iterator[int] = ...
    @property
    def closed(self) -> Optional[CloseReason]: ...
    @property
    def is_client(self) -> bool: ...
    @property
    def is_server(self) -> bool: ...
    @property
    def local(self) -> Union[Endpoint, str]: ...
    @property
    def remote(self) -> Union[Endpoint, str]: ...
    @property
    def path(self) -> str: ...
    @property
    def subprotocol(self) -> Optional[str]: ...
    @property
    def handshake_headers(self) -> Tuple[Tuple[str, str], ...]: ...

    async def aclose(
        self,
        code: int = ...,
        reason: Optional[str] = ...
    ) -> None: ...
    async def get_message(self) -> Union[str, bytes]: ...
    async def ping(self, payload: Optional[bytes] = ...) -> None: ...
    async def pong(self, payload: Optional[bytes] = ...) -> None: ...
    async def send_message(self, message: Union[str, bytes]) -> None: ...


class Endpoint:
    address: Union[IPv4Address, IPv6Address] = ...
    port: int = ...
    is_ssl: bool = ...
    @property
    def url(self) -> str: ...
