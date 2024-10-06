from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, TypeVar, cast

from .config import RateLimitConfig

if TYPE_CHECKING:
    from collections.abc import Awaitable

    from starlette.applications import Starlette


T = TypeVar("T")


async def maybe_await(value: Awaitable[T] | T) -> T:
    if inspect.isawaitable(value):
        return await value

    return value


def ensure_config_exists(config: RateLimitConfig | None, app: Starlette):
    if config is not None:
        return config

    try:
        config = cast(RateLimitConfig, app.state.__fourtwonine_config)  # noqa: SLF001
    except AttributeError as e:
        msg = (
            "This dependency does not specify a config, but a global config was "
            "not initialized. Use `fourtwonine.initialize` to attach a global "
            "rate limit configuration to your app, or specify a config."
        )
        raise RuntimeError(msg) from e

    return config
