# Do not get tempted by nicer type annotations! Using `from __future__ import annotations`
# will break Pydantic!
from typing import Annotated, Optional, Union, cast

import limits
from limits import RateLimitItem
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from typing_extensions import Doc

from ._core import check_limits
from ._headers import clear_headers
from ._utils import ensure_config_exists
from .config import RateLimitConfig


class RateLimitDep:
    """A rate limiting dependency for FastAPI."""

    def __init__(
        self,
        limit_value: Annotated[
            Union[str, RateLimitItem],
            Doc(
                """
                A rate limit passed as a `limits.RateLimitItem` or a string
                (e.g. `10/second`).
                """
            ),
        ],
        bucket: Annotated[str, Doc("The rate limit bucket to use.")],
        config: Annotated[
            Optional[RateLimitConfig],
            Doc(
                """
                The rate limit configuration to use. Uses the global configuration
                attached to your app if not specified.
                """
            ),
        ] = None,
    ) -> None:
        if isinstance(limit_value, str):
            self.limit_value = limits.parse(limit_value)
        else:
            self.limit_value = limit_value

        self.bucket = bucket
        self.config = config

    async def __call__(self, request: Request, response: Response):
        self.config = ensure_config_exists(self.config, cast(Starlette, request.app))
        headers = await check_limits(request, self.config, self.limit_value, self.bucket)

        if headers is None:
            return

        # FastAPI dependencies are evaluated from top-to-bottom; clear all headers
        # so we can apply the innermost rate limit headers.
        clear_headers(response.headers)
        response.headers.update(headers)
