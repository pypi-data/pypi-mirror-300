from limits.aio.storage import MemoryStorage
from limits.aio.strategies import MovingWindowRateLimiter
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route

import fourtwonine
from fourtwonine import RateLimitConfig, RateLimitMiddleware


async def rate_limited_endpoint(_request: Request):
    return PlainTextResponse("hit me 11 times in a minute!")


async def hello(_request: Request):
    return PlainTextResponse("hello world!")


app = Starlette(
    # Apply a global rate limit...
    middleware=[
        Middleware(RateLimitMiddleware, limit_value="20/minute", bucket="global"),
    ],
    routes=[
        Route(
            "/rate-limited",
            rate_limited_endpoint,
            # ...and then a specific rate limit for an endpoint.
            middleware=[
                Middleware(
                    RateLimitMiddleware, limit_value="10/minute", bucket="rate-limited"
                ),
            ],
        ),
        Route("/hello", hello),
    ],
)

# Attach a global configuration to the app, which will be used for
# all middlewares that don't specify their own configuration.
fourtwonine.initialize_config(
    app,
    RateLimitConfig(
        limiter=MovingWindowRateLimiter(MemoryStorage()),
    ),
)
