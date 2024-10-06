from __future__ import annotations

import time
from datetime import UTC, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from limits import RateLimitItem
    from starlette.datastructures import MutableHeaders

    from .config import RateLimitConfig
    from .datastructures import RateLimitInfo


def make_legacy_headers(info: RateLimitInfo) -> dict[str, str]:
    return {
        "X-RateLimit-Limit": str(info.limit),
        "X-RateLimit-Remaining": str(info.remaining),
        "X-RateLimit-Reset": str(info.reset_time),
        # Provide a Date header to deal with time desynchronization
        # between the client and server.
        "Date": datetime.now(UTC).strftime("%a, %d %b %Y %H:%M:%S %Z"),
    }


def make_draft_06_headers(
    info: RateLimitInfo, window: int, reset_secs: int
) -> dict[str, str]:
    return {
        "RateLimit-Policy": f"{info.limit};w={window}",
        "RateLimit-Limit": str(info.limit),
        "RateLimit-Remaining": str(info.remaining),
        "RateLimit-Reset": str(reset_secs),
    }


def make_draft_07_headers(
    info: RateLimitInfo, window: int, reset_secs: int
) -> dict[str, str]:
    return {
        "RateLimit-Policy": f"{info.limit};w={window}",
        "RateLimit": f"limit={info.limit}, remaining={info.remaining}, reset={reset_secs}",  # noqa: E501
    }


def make_headers(
    config: RateLimitConfig, limit: RateLimitItem, info: RateLimitInfo
) -> dict[str, str]:
    headers: dict[str, str] = {}
    reset_secs = info.reset_time - int(time.time())

    if config.legacy_headers:
        headers.update(make_legacy_headers(info))

    if config.headers == "draft-06":
        headers.update(make_draft_06_headers(info, limit.get_expiry(), reset_secs))
    elif config.headers == "draft-07":
        headers.update(make_draft_07_headers(info, limit.get_expiry(), reset_secs))

    if (config.legacy_headers or config.headers is not None) and info.remaining == 0:
        headers["Retry-After"] = str(reset_secs)

    return headers


def clear_headers(headers: MutableHeaders):
    del headers["X-RateLimit-Limit"]
    del headers["X-RateLimit-Remaining"]
    del headers["X-RateLimit-Reset"]
    del headers["Date"]
    del headers["RateLimit-Policy"]
    del headers["RateLimit"]
    del headers["RateLimit-Limit"]
    del headers["RateLimit-Remaining"]
    del headers["RateLimit-Reset"]
