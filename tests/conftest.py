import sys
from types import ModuleType
from unittest.mock import patch

import pytest


@pytest.fixture
def api():
    with patch.dict(sys.modules):
        sys.modules['app'] = ModuleType('app')
        sys.modules['app.api'] = api_module = ModuleType('api')

        yield api_module


@pytest.fixture
def app_config():
    with patch.dict(sys.modules):
        sys.modules['app'] = ModuleType('app')
        sys.modules['app.config'] = config_module = ModuleType('config')

        yield config_module


@pytest.fixture
def app_lifespan():
    with patch.dict(sys.modules):
        sys.modules['app'] = ModuleType('app')
        sys.modules['app.lifespan'] = config_module = ModuleType('lifespan')

        yield config_module
