import asyncio
from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager
from typing import Any, cast

from fastapi import FastAPI
from starlette.datastructures import State

from . import settings

type CleanUpFunc = Callable[[], Awaitable[None]]


def init_cache(state: State, cache_url: str) -> CleanUpFunc:
    from redis.asyncio.client import Redis

    state.cache = Redis.from_url(cache_url)
    return cast(CleanUpFunc, state.cache.aclose)


def init_db(state: State, db_url: str) -> CleanUpFunc:
    from sqlalchemy.ext.asyncio import create_async_engine

    state.db = create_async_engine(db_url)
    return cast(CleanUpFunc, state.db.dispose)


def init_http_client(state: State, retries: int) -> CleanUpFunc:
    from httpx import AsyncClient, AsyncHTTPTransport

    state.http_client = AsyncClient(
        transport=AsyncHTTPTransport(retries=retries)
    )
    return cast(CleanUpFunc, state.http_client.aclose)


INIT_FUNCS: dict[str, Callable[[State, Any], CleanUpFunc]] = {
    'cache_url': init_cache,
    'db_url': init_db,
    'http_retries': init_http_client,
}


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    clean_up_funcs: list[CleanUpFunc] = []

    for attr, init_func in INIT_FUNCS.items():
        value = getattr(settings, attr, None)
        if value:
            clean_up_funcs.append(init_func(app.state, value))

    yield

    await asyncio.gather(*(func() for func in clean_up_funcs))
