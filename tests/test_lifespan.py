import asyncio
from unittest.mock import AsyncMock, Mock, patch

from core import settings
from core.lifespan import lifespan


def run_lifespan():
    app = Mock()

    async def test():
        async with lifespan(app):
            pass

    asyncio.run(test())


@patch('httpx.AsyncHTTPTransport')
@patch('httpx.AsyncClient')
@patch('sqlalchemy.ext.asyncio.create_async_engine')
@patch('redis.asyncio.client.Redis')
def test_lifespan(
    redis,
    create_async_engine,
    httpx_client,
    httpx_transport,
):
    gather = AsyncMock()
    with patch('asyncio.gather', gather):
        run_lifespan()

    redis.from_url.assert_called_once_with(settings.cache_url)
    create_async_engine.assert_called_once_with(settings.db_url)
    httpx_transport.assert_called_once_with(retries=2)
    httpx_client.assert_called_once_with(transport=httpx_transport())

    cache_aclose = redis.from_url.return_value.aclose
    cache_aclose.assert_called_once_with()

    dispose = create_async_engine.return_value.dispose
    dispose.assert_called_once_with()

    http_aclose = httpx_client.return_value.aclose
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
