from typing import Any, Literal

from fastapi import APIRouter, FastAPI, params

from . import settings
from .deps import VerifyClient
from .lifespan import lifespan
from .sentry import init_sentry


def make_app(**kwargs: Any) -> FastAPI:
    init_sentry()

    slug = settings.app_name

    app = FastAPI(
        lifespan=lifespan,
        docs_url=f'/{slug}/docs',
        redoc_url=f'/{slug}/redoc',
        openapi_url=(
            None
            if settings.app_env == 'production'
            else f'/{slug}/openapi.json'
        ),
        title=settings.app_title,
        **kwargs,
    )

    add_router(app, 'public', f'/api/v1/{slug}')
    add_router(app, 'internal', f'/internal/{slug}', [VerifyClient])

    return app


def add_router(
    app: FastAPI,
    router_type: Literal['public', 'internal'],
    prefix: str,
    dependencies: list[params.Depends] | None = None,
) -> None:
    from app import api

    func_name = f'add_{router_type}_api'
    if not hasattr(api, func_name):
        return

    router = APIRouter(prefix=prefix, dependencies=dependencies)
    getattr(api, func_name)(router)

    app.include_router(router)
