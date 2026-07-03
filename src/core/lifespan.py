import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import cast

from fastapi import FastAPI
from starlette.datastructures import State

from . import settings
from .typing import CleanUpFunc, CoreInitFunc

try:
    from app.lifespan import INIT_FUNCS as APP_INIT_FUNCS
except ImportError:
    APP_INIT_FUNCS = []


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


INIT_FUNCS: dict[str, CoreInitFunc] = {
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

    for app_init_func in APP_INIT_FUNCS:
        clean_up = app_init_func(app.state)
        if clean_up:
            clean_up_funcs.append(clean_up)

    yield

    await asyncio.gather(*(func() for func in clean_up_funcs))
