import sys
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from core import settings
from core.config import AppSettings


def test_settings():
    assert settings.app_title == 'tiny-service-core'

    assert settings.app_proj == 'tiny-service'
    assert settings.app_name == 'core'

    assert settings.app_env == 'test'
    assert settings.app_key == '42'

    assert settings.app_host == '127.0.0.1'
    assert settings.app_port == 8080

    assert settings.app_client_key_hashes == []

    assert settings.sentry_dsn is None
    assert type(settings.traces_sample_rate) is float

    assert settings.cache_url == 'redis://localhost:6379'
    assert settings.db_url == 'postgresql+asyncpg://foo:bar@127.0.0.1/dummy'
    assert settings.http_retries == 2


@pytest.mark.parametrize('key', ('APP_PROJ', 'APP_NAME'))
def test_slug_validation(key):
    with (
        patch.dict('os.environ', {key: 'Foo Bar'}),
        pytest.raises(ValidationError, match='string_pattern_mismatch'),
    ):
        AppSettings()


@patch.dict('os.environ', {'APP_CLIENT_KEY_HASHES': 'foo,bar'})
def test_settings_app_client_key_hashes():
    settings = AppSettings()
    assert settings.app_client_key_hashes == ['foo', 'bar']


@patch.dict(
    sys.modules,
    {
        'redis': None,
        'sqlmodel': None,
        'httpx': None,
    },
)
def test_config_init_no_optional():
    del sys.modules['core.config']
    del sys.modules['core']

    from core.config import (
        CacheSettings,
        CoreSettings,
        DBSettings,
        HTTPClientSettings,
    )

    assert not issubclass(CoreSettings, CacheSettings)
    assert not issubclass(CoreSettings, DBSettings)
    assert not issubclass(CoreSettings, HTTPClientSettings)

    settings = CoreSettings()
    assert not hasattr(settings, 'cache_url')
    assert not hasattr(settings, 'db_url')
    assert not hasattr(settings, 'http_retries')
