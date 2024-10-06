from dataclasses import dataclass

from limits import RateLimitItem
from limits.aio.strategies import RateLimiter

from .config import RateLimitConfig


@dataclass
class RateLimitInfo:
    """
    The rate limit information for each client, attached in the
    :cls:`starlette.requests.Request.state` object.
    """

    limiter: RateLimiter
    item: RateLimitItem
    config: RateLimitConfig
    key: str

    remaining: int
    reset_time: int

    @property
    def limit(self):
        return self.item.amount

    @property
    def used(self):
        return self.item.amount - self.remaining
