from __future__ import annotations

from typing import TYPE_CHECKING

from limits.errors import StorageError

from ._headers import make_headers
from ._utils import maybe_await
from .datastructures import RateLimitInfo
from .errors import RateLimitExceeded

if TYPE_CHECKING:
    from limits import RateLimitItem
    from starlette.requests import Request

    from .config import RateLimitConfig


async def check_limits(
    request: Request, config: RateLimitConfig, limit: RateLimitItem, bucket: str
):
    if await maybe_await(config.skip_func(request)):
        return None

    limiter = config.limiter
    key = await maybe_await(config.key_func(request, bucket))

    try:
        acquired = await limiter.hit(limit, key)
        reset, remaining = await limiter.get_window_stats(limit, key)
    except Exception as e:
        if config.pass_on_limiter_error and isinstance(
            e, (StorageError, limiter.storage.base_exceptions)
        ):
            return None

        raise

    info = RateLimitInfo(
        limiter,
        limit,
        config,
        key,
        remaining,
        reset,
    )
    headers = make_headers(config, limit, info)

    setattr(request.state, config.state_attr, info)

    if not acquired:
        detail = await maybe_await(config.error_detail_func(request))

        raise RateLimitExceeded(config, detail, headers)

    return headers
