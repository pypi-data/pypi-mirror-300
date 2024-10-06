from fastapi import Depends, FastAPI
from limits.aio.storage import MemoryStorage
from limits.aio.strategies import MovingWindowRateLimiter

import fourtwonine
from fourtwonine.config import RateLimitConfig
from fourtwonine.fastapi import RateLimitDep

app = FastAPI(
    # Apply a global rate limit...
    dependencies=[Depends(RateLimitDep("20/minute", "global"))]
)
fourtwonine.initialize_config(
    app,
    config=RateLimitConfig(
        limiter=MovingWindowRateLimiter(MemoryStorage()),
        skip_func=lambda r: r.url.path in {"/redoc", "/docs", "/openapi.json"},
    ),
)


@app.get(
    "/rate-limited",
    # ...and then a specific rate limit for an endpoint.
    dependencies=[Depends(RateLimitDep("10/minute", "rate-limited"))],
)
async def rate_limited():
    return {"challenge": "hit me 11 times in a minute!"}


# This endpoint will still be affected by the global rate limit.
@app.get("/hello")
async def hello_world():
    return {"message": "Hello World!"}
