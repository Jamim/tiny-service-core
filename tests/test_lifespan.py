import asyncio
import sys
from unittest.mock import AsyncMock, Mock, patch

from core import settings


def run_lifespan():
    from core.lifespan import lifespan

    app = Mock()

    async def test():
        async with lifespan(app):
            pass

    asyncio.run(test())

    return app


@patch('httpx2.AsyncHTTPTransport')
@patch('httpx2.AsyncClient')
@patch('sqlalchemy.ext.asyncio.create_async_engine')
@patch('redis.asyncio.client.Redis')
def test_lifespan(
    redis,
    create_async_engine,
    httpx2_client,
    httpx2_transport,
):
    gather = AsyncMock()
    with patch('asyncio.gather', gather):
        run_lifespan()

    redis.from_url.assert_called_once_with(settings.cache_url)
    create_async_engine.assert_called_once_with(settings.db_url)
    httpx2_transport.assert_called_once_with(retries=2)
    httpx2_client.assert_called_once_with(transport=httpx2_transport())

    cache_aclose = redis.from_url.return_value.aclose
    cache_aclose.assert_called_once_with()

    dispose = create_async_engine.return_value.dispose
    dispose.assert_called_once_with()

    http_aclose = httpx2_client.return_value.aclose
    http_aclose.assert_called_once_with()

    gather.assert_called_once_with(
        cache_aclose.return_value,
        dispose.return_value,
        http_aclose.return_value,
    )


def test_lifespan_missing_setting():
    func = Mock()

    gather = AsyncMock()
    with (
        patch.dict(
            'core.lifespan.INIT_FUNCS',
            {'missing_url': func},
            clear=True,
        ),
        patch('asyncio.gather', gather),
    ):
        run_lifespan()

    func.assert_not_called()
    gather.assert_called_once_with()


def test_lifespan_app_init_func(app_lifespan):
    del sys.modules['core.lifespan']

    clean_up = AsyncMock()
    init_foo = Mock(return_value=clean_up)
    init_bar = Mock(return_value=None)

    app_lifespan.INIT_FUNCS = [init_foo, init_bar]
    app = run_lifespan()

    init_foo.assert_called_once_with(app.state)
    clean_up.assert_called_once_with()

    init_bar.assert_called_once_with(app.state)
