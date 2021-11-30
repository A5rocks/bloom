"""Basic ratelimiting implementation. WARNING: bugs ahead.

Okay, so when coming to Discord's API, the ratelimiting may seem downright
strange. I'll ignore the documentation for this bit, as the documentation is
wrong. Here's the general process of ratelimiting that is used here.

#. Lock the route (sharded by the major parameters of course). This is
    important because Discord has many limits that it does not tell API
    consumers -- take for example, editing a channel name. A channel can be
    edited quite a bit, but bots can only edit a channel *name* 2 times every
    10 minutes. This is not information that is accessible, so the two possible
    implementations are hardcoding all this information, or locking the route
    to serialize requests and only getting a 429 once -- bloom does the latter.

#. Find all buckets connected to the route. Unlike the lie the documentation
    gives about every route only having a single bucket, Discord actually has
    multiple buckets per route: `Discord documentation #1295
    https://github.com/discord/discord-api-docs/issues/1295`_

#. Wait until all buckets allow the request.

#. Make the request.

#. Get the bucket hash from the response, and update that bucket.

It might be noted that this ignores things like global ratelimits, simply
because those are impossible. The only correct implementation without using
the exact formulas Discord uses is this -- while someone may be tempted to
hardcode a 50 req/s bucket in, this does not work for bots on large bot
sharding.

Additionally, continuing the theme of trying to not run into ratelimits (like
how requests to the route are serialized), bloom uses the Reset-After header.
Hopefully you have good enough latency! If this ever becomes a problem though,
Reset-At is a thing, though it is risky. It would be locked behind a boolean
flag.
"""
from __future__ import annotations

import collections
import contextlib
import typing

import attr
import cattr
import httpx
import trio

from bloom._compat import get_args
from bloom.rest.models import Request

API_BASE_URL = 'https://discord.com/api/v9'
ReturnT = typing.TypeVar('ReturnT')


class HttpResponseProto(typing.Protocol):
    @property
    def headers(self) -> httpx.Headers:
        ...

    @property
    def status_code(self) -> int:
        ...

    def json(self) -> typing.Any:
        ...

    def raise_for_status(self) -> None:
        ...


class HttpClientProto(typing.Protocol):
    async def request(
        self,
        method: str,
        url: str,
        *,
        params: typing.Mapping[
            str,
            typing.Union[
                str,
                int,
                float,
                bool,
                None,
                typing.Sequence[typing.Union[str, int, float, bool, None]],
            ],
        ] = ...,
        json: typing.Any = ...,
        headers: typing.Dict[str, str] = ...,
        data: typing.Dict[str, str] = ...,
        # TODO: narrow file type?
        files: typing.Dict[str, typing.Any] = ...,
    ) -> HttpResponseProto:
        ...


@attr.define()
class Bucket:
    remaining: int
    reset_at: float

    async def wait_for(self) -> None:
        if self.remaining == 0:
            await trio.sleep_until(self.reset_at)


@attr.frozen()
class RatelimitingState:
    http: HttpClientProto
    converter: cattr.Converter

    # XXX: *technically* this is a leak but... who cares.
    locks: typing.Dict[
        str, typing.Dict[typing.Optional[typing.Union[int, str]], trio.Lock]
    ] = attr.Factory(
        lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: trio.Lock()))
    )

    buckets: typing.Dict[
        str, typing.Dict[typing.Optional[typing.Union[int, str]], typing.List[Bucket]]
    ] = attr.Factory(lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: [])))

    buckets_by_hash: typing.Dict[
        str, typing.Dict[typing.Optional[typing.Union[int, str]], Bucket]
    ] = attr.Factory(lambda: collections.defaultdict(lambda: {}))

    async def request(self, req: Request[ReturnT]) -> ReturnT:
        # this code makes the assumption of only a single major param.
        major_parameter = req.args.get('channel_id') or req.args.get('guild_id')

        # the routes with only webhook_id and not webhook_token are not
        # ratelimited, so this is perfectly fine.
        if 'webhook_id' in req.args and 'webhook_token' in req.args:
            # str key (cause interaction's webhook id is the app id...)
            major_parameter = str(req.args['webhook_id']) + str(req.args['webhook_token'])

        async with self.locks[req.route][major_parameter]:
            async with trio.open_nursery() as nursery:
                for bucket in self.buckets[req.route][major_parameter]:
                    nursery.start_soon(bucket.wait_for)

            # make the request
            kw_args = {}

            if req.params is not None:
                kw_args['params'] = req.params

            if req.json is not None:
                kw_args['json'] = req.json

            if req.headers is not None:
                kw_args['headers'] = req.headers

            if req.data is not None:
                kw_args['data'] = req.data

            if req.files is not None:
                kw_args['files'] = req.files

            result = await self.http.request(req.method, req.url, **kw_args)
            headers = result.headers

            # TODO: handle errors (429, ...) correctly (including decoding of error type)
            result.raise_for_status()

            # process the result

            bucket_hash = headers.get('X-RateLimit-Bucket')

            if bucket_hash is not None and major_parameter in self.buckets_by_hash[bucket_hash]:
                bucket = self.buckets_by_hash[bucket_hash][major_parameter]
                bucket.remaining = int(headers['X-RateLimit-Remaining'])
                # TODO: should this have a configuration option to use `X-Ratelimit-Reset` instead?
                bucket.reset_at = trio.current_time() + float(headers['X-RateLimit-Reset-After'])

            elif bucket_hash is not None:
                bucket = Bucket(
                    int(headers['X-RateLimit-Remaining']),
                    trio.current_time() + float(headers['X-RateLimit-Reset-After']),
                )

                self.buckets[req.route][major_parameter].append(bucket)
                self.buckets_by_hash[bucket_hash][major_parameter] = bucket

            else:
                # ?? no ratelimit?
                pass

            # runtime-only attribute :S
            result_type = req.type_args.inner  # type: ignore[attr-defined]

            # None == 204 == no body
            if result_type is None or None in get_args(result_type):
                if result.status_code == 204:
                    return None  # type: ignore[return-value]  # trust me mypy :-)
                else:
                    # TODO: specialize error (?)
                    raise Exception("Expected no body, got a body.")
            else:
                return_val: ReturnT = self.converter.structure(result.json(), result_type)
                return return_val

    @classmethod
    @contextlib.asynccontextmanager
    async def with_httpx(
        cls, token: str, converter: cattr.Converter
    ) -> typing.AsyncIterator[RatelimitingState]:
        async with httpx.AsyncClient(
            base_url=API_BASE_URL,
            headers={'Authorization': f'Bot {token}'},
        ) as client:
            yield RatelimitingState(client, converter)
