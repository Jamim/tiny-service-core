from typing import Annotated, cast

from fastapi import Depends, Request
from redis.asyncio.client import Redis


def get_cache(request: Request) -> Redis:
    return cast(Redis, request.app.state.cache)


Cache = Annotated[Redis, Depends(get_cache)]
