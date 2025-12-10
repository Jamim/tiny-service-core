import sys
from importlib.metadata import version
from unittest.mock import patch

from pydantic_settings import BaseSettings

import core
from core import logger, run, settings
from core.config import CoreSettings


def test_logger():
    assert logger.name == 'tiny-service-core'


def test_settings_default():
    assert isinstance(settings, CoreSettings)
    assert type(settings) is CoreSettings


def _test_custom_settings(app_config, base_class):
    del sys.modules['core']

    class Settings(base_class):
        foo: str = 'bar'

    app_config.Settings = Settings

    from core import settings

    assert isinstance(settings, CoreSettings)
    assert isinstance(settings, Settings)

    assert settings.app_name == 'core'
    assert settings.foo == 'bar'

    return settings


@patch.dict(sys.modules)
def test_settings_subclass(app_config):
    settings = _test_custom_settings(app_config, CoreSettings)
    assert type(settings) is app_config.Settings


@patch.dict(sys.modules)
def test_settings_combined(app_config):
    settings = _test_custom_settings(app_config, BaseSettings)
    assert type(settings).__name__ == 'CombinedSettings'


@patch('uvicorn.run')
def test_run(uvicorn_run):
    app = object()

    run(app, access_log=False)

    uvicorn_run.assert_called_once_with(
        app, host=settings.app_host, port=settings.app_port, access_log=False
    )


@patch.dict(sys.modules, {'core.lock': None})
def test_init_no_lock():
    del sys.modules['core']

    import core

    assert not hasattr(core, 'Lock')


def test_module_name():
    assert core.__name__ == 'tiny-service-core'


def test_module_version():
    assert core.__version__ == version(core.__name__)
