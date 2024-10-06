# pyright: reportImportCycles=false
from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from starlette.responses import JSONResponse
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

if TYPE_CHECKING:
    from limits.aio.strategies import RateLimiter
    from starlette.requests import Request
    from starlette.responses import Response

    from .errors import RateLimitExceeded

StandardHeaderType = Literal["draft-06", "draft-07"]
KeyFuncT = Callable[["Request", str], Awaitable[str] | str]
SkipFuncT = Callable[["Request"], Awaitable[bool] | bool]
DetailFuncT = Callable[["Request"], Awaitable[str | None] | str | None]
ResponseFuncT = Callable[
    ["Request", "RateLimitExceeded"], "Awaitable[Response] | Response"
]


@dataclass(kw_only=True)
class RateLimitConfig:
    """Rate limiting configuration."""

    limiter: RateLimiter
    """
    The :cls:`limits.aio.strategies.RateLimiter` instance used to throttle requests.
    """

    pass_on_limiter_error: bool = False
    """
    Whether to block or allow requests in the case of a limiter error. If this is
    set to `False` (default), all requests are blocked until the limiter no longer errors
    (fail closed). Set this to `True` to allow requests through without rate limiting.
    """

    status_code: int = HTTP_429_TOO_MANY_REQUESTS
    """The response code used for rate limited requests."""

    legacy_headers: bool = False
    """
    Whether to send legacy rate limit headers for the limit (`X-RateLimit-Limit`), current
    usage (`X-RateLimit-Remaining`) and reset time (`X-RateLimit-Reset`) on all responses.

    If a request is blocked, `Retry-After` will also be sent.
    """

    headers: None | StandardHeaderType = "draft-07"
    """
    Whether to send rate limit headers conforming to the
    [RateLimit header fields for HTTP standardization draft](https://github.com/ietf-wg-httpapi/ratelimit-headers)
    adopted by the IETF.

    If set to `draft-06`, the headers `RateLimit-Policy`, `RateLimit-Limit`,
    `RateLimit-Remaining` and `RateLimit-Reset` are sent on all responses, matching the
    [sixth draft](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-ratelimit-headers-06)
    of the specification.

    If set to `draft-07`, the headers `RateLimit` and `RateLimit-Policy` are sent,
    matching the [seventh draft](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-ratelimit-headers-07)
    of the specification.

    If ratelimit headers are sent and a request is blocked, `Retry-After` will also
    be sent.
    """

    key_func: KeyFuncT = lambda r, b: f"{r.client.host if r.client else 'anonymous'}:{b}"
    """
    Function to retrieve custom identifiers for clients. Should be a sync/async
    function that accepts :cls:`starlette.requests.Request` and the bucket name,
    and returns a string.

    By default, the IP address of the client is used:

    ```python
    lambda r, b: lambda r, b: f"{r.client.host if r.client else 'anonymous'}:{b}"
    ```
    """

    skip_func: SkipFuncT = lambda _: False
    """
    Function to determine whether this request counts towards a client's quota.
    Should be a sync/async function that accepts :cls:`starlette.requests.Request`
    and returns a boolean.

    By default, no requests are skipped:
    ```python
    lambda _: False
    ```
    """

    error_detail_func: DetailFuncT = lambda _: "Rate limit exceeded."
    """
    Function to determine the detail attached to the rate limit exception.
    Should be a sync/async function that accepts :cls:`starlette.requests.Request`
    and returns a string.
    """

    response_func: ResponseFuncT = lambda _, e: JSONResponse(
        {"detail": e.detail},
        e.status_code,
        e.headers,
    )
    """
    Function to make a response when the rate limit is hit. Only used on Starlette
    middleware; the FastAPI dependency raises :cls:`fourtwonine.errors.RateLimitExceeded`
    directly.
    """

    state_attr: str = "rate_limit"
    """
    The name of the attribute on the :attr:`starlette.requests.Request.state` object
    to store the rate limit information.
    """
