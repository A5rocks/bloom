import typing

import attr
import httpx
import trio

import bloom._compat
import bloom.ratelimits
import bloom.rest.models


@attr.frozen()
class Response:
    headers: httpx.Headers = attr.ib(converter=httpx.Headers)
    json_body: typing.Any
    status_code: int = 200

    def raise_for_status(self) -> None:
        assert 200 <= self.status_code < 300

    def json(self) -> typing.Any:
        return {}


@attr.define()
class Client:
    responses: typing.List[Response]
    storage: typing.List[
        typing.Tuple[float, str, str, object, object, object, object, object]
    ] = attr.Factory(list)

    async def request(
            self,
            method: str,
            url: str,
            *,
            params: typing.Optional[
                typing.Mapping[
                    str,
                    typing.Union[
                        str,
                        int,
                        float,
                        bool,
                        None,
                        typing.Sequence[typing.Union[str, int, float, bool, None]]
                    ]
                ]
            ] = None,
            json: typing.Any = None,
            headers: typing.Optional[typing.Dict[str, str]] = None,
            data: typing.Optional[typing.Dict[str, str]] = None,
            files: typing.Optional[typing.Dict[str, typing.Any]] = None,
    ) -> Response:
        self.storage.append((trio.current_time(), method, url, params, json, headers, data, files))

        return self.responses.pop()


async def test_makes_a_request() -> None:
    client = Client([Response({'a': 'header'}, {})])
    state = bloom.ratelimits.RatelimitingState(client)

    req = bloom.rest.models.Request(method='GET', route='/blah', args={})

    await state.request(req)

    assert len(client.storage) == 1

    resp = client.storage[0]

    assert resp[1] == 'GET'
    assert resp[2] == '/blah'
    assert resp[3] is None
    assert resp[4] is None


async def test_ratelimits_once(autojump_clock: object) -> None:
    reset_in = 2

    client = Client([Response({
        'X-RateLimit-Bucket': 'a',
        'X-RateLimit-Remaining': '0',
        'X-RateLimit-Reset-After': str(reset_in)
    }, {})]*2)
    state = bloom.ratelimits.RatelimitingState(client)

    start = trio.current_time()

    req = bloom.rest.models.Request(method='GET', route='/blah', args={})

    await state.request(req)
    await state.request(req)

    end = trio.current_time()

    assert start + reset_in <= end


async def test_ratelimits_twice(autojump_clock: object) -> None:
    reset_in = 2

    client = Client([Response({
        'X-RateLimit-Bucket': 'a',
        'X-RateLimit-Remaining': '0',
        'X-RateLimit-Reset-After': str(reset_in)
    }, {})]*3)
    state = bloom.ratelimits.RatelimitingState(client)

    start = trio.current_time()

    req = bloom.rest.models.Request(method='GET', route='/blah', args={})

    await state.request(req)
    await state.request(req)
    await state.request(req)

    end = trio.current_time()

    assert start + reset_in * 2 <= end


async def test_respects_remaining(autojump_clock: object) -> None:
    reset_in = 2

    client = Client([
        Response({
            'X-RateLimit-Bucket': 'a',
            'X-RateLimit-Remaining': '1',
            'X-RateLimit-Reset-After': str(reset_in)
        }, {}),
        Response({
            'X-RateLimit-Bucket': 'a',
            'X-RateLimit-Remaining': '0',
            'X-RateLimit-Reset-After': str(reset_in)
        }, {}),
        Response({
            'X-RateLimit-Bucket': 'a',
            'X-RateLimit-Remaining': '1',
            'X-RateLimit-Reset-After': str(reset_in)
        }, {})
    ])
    state = bloom.ratelimits.RatelimitingState(client)

    start = trio.current_time()

    req = bloom.rest.models.Request(method='GET', route='/blah', args={})

    await state.request(req)
    await state.request(req)
    await state.request(req)

    end = trio.current_time()

    assert start + reset_in <= end < start + reset_in * 2


async def test_respects_endless_remaining(autojump_clock: object) -> None:
    reset_in = 2

    client = Client([Response({
        'X-RateLimit-Bucket': 'a',
        'X-RateLimit-Remaining': '1',
        'X-RateLimit-Reset-After': str(reset_in)
    }, {})]*10)
    state = bloom.ratelimits.RatelimitingState(client)

    start = trio.current_time()

    req = bloom.rest.models.Request(method='GET', route='/blah', args={})

    await state.request(req)
    await state.request(req)
    await state.request(req)

    end = trio.current_time()

    assert end < start + reset_in
