import sys
from typing import get_args
from unittest.mock import patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import AsyncClient
from redis.asyncio.client import Redis
from sqlalchemy.engine.interfaces import IsolationLevel
from sqlmodel.ext.asyncio.session import AsyncSession

from core import make_app
from core.deps import Cache, HTTPClient, Session, Token, UserIP

AUTH_HEADERS = {'Authorization': 'Bearer 42'}


def _test_api(url, headers, status_code, json):
    app = make_app()
    with TestClient(app) as client:
        response = client.get(url, headers=headers)
        assert response.status_code == status_code
        assert response.json() == json


def get_status():
    return 'ok'


def add_api_factory(endpoint):
    def add_api(router):
        router.add_api_route('/status', endpoint, methods=['GET'])

    return add_api


@pytest.mark.parametrize(
    'headers,status_code,json',
    (
        (None, status.HTTP_401_UNAUTHORIZED, {'detail': 'Not authenticated'}),
        (
            {'Authorization': 'Bearer foo'},
            status.HTTP_401_UNAUTHORIZED,
            {'detail': 'App key is not valid'},
        ),
        (AUTH_HEADERS, status.HTTP_200_OK, 'ok'),
    ),
)
@patch('core.settings')
def test_verify_client(settings, api, headers, status_code, json):
    settings.app_client_key_hashes = [
        'cf01c9d9de8cf1433d212adb97be45ecfc0fd868599faf3ee4741a5e959d424e'
    ]
    api.add_internal_api = add_api_factory(get_status)
    _test_api('/internal/core/status', headers, status_code, json)


@patch.dict(
    sys.modules,
    {
        'core.deps.cache': None,
        'core.deps.db': None,
        'core.deps.http_client': None,
    },
)
def test_deps_init_no_optional():
    del sys.modules['core.deps']
    del sys.modules['core']

    import core

    # preventing ModuleNotFoundError: No module named 'tiny-service-core'
    core.__name__ = 'core'

    from core import deps

    assert deps.__all__ == [
        'Token',
        'VerifyClient',
        'UserIP',
    ]

    assert not hasattr(deps, 'Cache')
    assert not hasattr(deps, 'Session')
    assert not hasattr(deps, 'HTTPClient')


def get_token(token: Token):
    assert token == '42'
    return 'ok'


def get_cache(cache: Cache):
    assert isinstance(cache, Redis)
    return 'ok'


def get_session(session: Session):
    assert isinstance(session, AsyncSession)
    assert session.bind.dialect._on_connect_isolation_level is None
    return 'ok'


def get_http_client(http_client: HTTPClient):
    assert isinstance(http_client, AsyncClient)
    return 'ok'


def get_user_ip(user_ip: UserIP):
    assert user_ip == '1.1.1.1'
    return 'ok'


@pytest.mark.parametrize(
    'endpoint',
    (
        get_token,
        get_cache,
        get_session,
        get_http_client,
    ),
)
def test_get_dependency(api, endpoint):
    api.add_public_api = add_api_factory(endpoint)
    _test_api('/api/v1/core/status', AUTH_HEADERS, status.HTTP_200_OK, 'ok')


@pytest.mark.parametrize(
    'forwarded_for',
    (
        '1.1.1.1',
        '1.1.1.1,2.2.2.2',
        '1.1.1.1,2.2.2.2,3.3.3.3',
    ),
)
def test_user_id(api, forwarded_for):
    api.add_public_api = add_api_factory(get_user_ip)
    headers = {'X-Forwarded-For': forwarded_for, **AUTH_HEADERS}
    _test_api('/api/v1/core/status', headers, status.HTTP_200_OK, 'ok')


@pytest.mark.parametrize('isolation_level', get_args(IsolationLevel))
def test_db_isolation_level(api, isolation_level):
    def get_session(session: Session):
        assert isinstance(session, AsyncSession)
        assert (
            session.bind.dialect._on_connect_isolation_level == isolation_level
        )
        return 'ok'

    api.add_public_api = add_api_factory(get_session)

    from core import settings

    with patch.object(settings, 'db_isolation_level', isolation_level):
        _test_api(
            '/api/v1/core/status', AUTH_HEADERS, status.HTTP_200_OK, 'ok'
        )
