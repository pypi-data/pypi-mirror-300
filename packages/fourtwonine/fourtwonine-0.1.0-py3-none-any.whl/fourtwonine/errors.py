from __future__ import annotations

from typing import TYPE_CHECKING

from starlette.exceptions import HTTPException

if TYPE_CHECKING:
    from .config import RateLimitConfig


class RateLimitExceeded(HTTPException):
    """Exception thrown when the rate limit has exceeded."""

    def __init__(
        self,
        config: RateLimitConfig,
        detail: str | None = None,
        headers: dict[str, str] | None = None,
    ):
        super().__init__(config.status_code, detail, headers)
