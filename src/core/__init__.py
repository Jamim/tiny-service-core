import logging
from importlib.metadata import version
from typing import Any, cast

from fastapi import FastAPI

from .config import CoreSettings

settings_class: type[CoreSettings]
try:
    from app.config import Settings
except ImportError:
    settings_class = CoreSettings
else:
    if issubclass(Settings, CoreSettings):
        settings_class = cast(type[CoreSettings], Settings)
    else:
        settings_class = type('CombinedSettings', (Settings, CoreSettings), {})


settings = settings_class()
logger = logging.getLogger(settings.app_title)

from .app import make_app
from .crypto import get_key_hash


def run(app: FastAPI, **kwargs: Any) -> None:
    import uvicorn

    kwargs.setdefault('host', settings.app_host)
    kwargs.setdefault('port', settings.app_port)

    uvicorn.run(app, **kwargs)


__all__ = [
    'get_key_hash',
    'logger',
    'make_app',
    'run',
    'settings',
]

try:
    from .lock import Lock
except ImportError:
    pass
else:
    __all__.append('Lock')

__name__ = 'tiny-service-core'
__version__ = version(__name__)
