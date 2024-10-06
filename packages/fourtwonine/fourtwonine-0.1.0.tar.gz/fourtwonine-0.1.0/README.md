# fourtwonine

Yet another rate limiter for Starlette and FastAPI.

This is simply a thin layer over the [limits](https://limits.readthedocs.io/en/stable/quickstart.html)
library, making it easy to define flexible rate limits.

## Features
- Fully async and typed
- Supports any data store the `limits` library supports: `redis`, `mongodb`, `memcached`, etc.
- Supports legacy rate limit headers, as well as IETF [draft 06](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-ratelimit-headers-06)
and [draft 07](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-ratelimit-headers-07) headers.
- Exposes rate limit state (under `request.state.rate_limit` by default)

## Examples
Check the [`examples`](examples) directory for how to integrate this into your app.
