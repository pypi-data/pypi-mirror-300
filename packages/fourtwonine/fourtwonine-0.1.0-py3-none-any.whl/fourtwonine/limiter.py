from typing import cast

from starlette.applications import Starlette

from .config import RateLimitConfig


def initialize_config(app: Starlette, config: RateLimitConfig):
    app.state.__fourtwonine_config = config  # noqa: SLF001


def get_config(app: Starlette):
    return cast(RateLimitConfig, app.state.__fourtwonine_config)  # noqa: SLF001
