from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, NoReturn, cast

import limits
from limits import RateLimitItem
from starlette.applications import Starlette
from starlette.datastructures import Headers, MutableHeaders
from starlette.requests import Request
from typing_extensions import Doc

from ._core import check_limits
from ._utils import ensure_config_exists, maybe_await
from .errors import RateLimitExceeded

if TYPE_CHECKING:
    from starlette.types import ASGIApp, Message, Receive, Scope, Send

    from .config import RateLimitConfig

__all__ = ("RateLimitMiddleware",)


class RateLimitMiddleware:
    """ASGI rate limiting middleware for Starlette."""

    def __init__(
        self,
        app: ASGIApp,
        limit_value: Annotated[
            str | RateLimitItem,
            Doc(
                """
                A rate limit passed as a `limits.RateLimitItem` or a string
                (e.g. `10/second`).
                """
            ),
        ],
        bucket: Annotated[str, Doc("The rate limit bucket to use.")],
        config: Annotated[
            RateLimitConfig | None,
            Doc(
                """
                The rate limit configuration to use. Uses the global configuration
                attached to your app if not specified.
                """
            ),
        ] = None,
    ) -> None:
        self.app = app
        self.bucket = bucket
        self.config = config

        if isinstance(limit_value, str):
            self.limit_value = limits.parse(limit_value)
        else:
            self.limit_value = limit_value

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        self.config = ensure_config_exists(self.config, cast(Starlette, scope["app"]))
        request = Request(scope, receive, send)

        try:
            headers = await check_limits(
                request, self.config, self.limit_value, self.bucket
            )
        except RateLimitExceeded as e:
            response = await maybe_await(self.config.response_func(request, e))

            await response(scope, receive, send)
            return

        if headers is None:
            return

        await RateLimitResponder(self.app, headers)(scope, receive, send)


class RateLimitResponder:
    def __init__(self, app: ASGIApp, headers: dict[str, str]) -> None:
        self.app = app
        self.send: Send = unattached_send
        self.headers = headers

        self.started: bool = False
        self.rate_limit_headers_set: bool = False
        self.initial_message: Message = {}

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        self.send = send
        await self.app(scope, receive, self.send_wrapper)

    async def send_wrapper(self, message: Message):
        if message["type"] == "http.response.start":
            self.initial_message = message

            raw_headers: list[tuple[bytes, bytes]] = self.initial_message["headers"]  # pyright: ignore[reportRedeclaration]
            headers = Headers(raw=raw_headers)

            if "X-RateLimit-Limit" in headers or "RateLimit-Policy" in headers:
                self.rate_limit_headers_set = True

        # Middleware in Starlette goes from bottom to top. If there are already
        # rate-limit headers set (by a more local rate limiter), don't set
        # rate limit headers any more.
        elif message["type"] == "http.response.body" and self.rate_limit_headers_set:
            if not self.started:
                self.started = True
                await self.send(self.initial_message)

            await self.send(message)
        elif message["type"] == "http.response.body":
            if not self.started:
                self.started = True

                raw_headers: list[tuple[bytes, bytes]] = self.initial_message["headers"]
                headers = MutableHeaders(raw=raw_headers)
                headers.update(self.headers)

                await self.send(self.initial_message)

            await self.send(message)


async def unattached_send(_message: Message) -> NoReturn:
    raise RuntimeError("send awaitable not set")
