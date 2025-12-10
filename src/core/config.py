from typing import TYPE_CHECKING, Annotated, Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode

SLUG_PATTERN = r'^[a-z0-9-]+$'


class AppSettings(BaseSettings):
    @property
    def app_title(self) -> str:
        return f'{self.app_proj}-{self.app_name}'

    app_proj: str = Field(pattern=SLUG_PATTERN)
    app_name: str = Field(pattern=SLUG_PATTERN)

    app_env: Literal['production', 'staging', 'local', 'test']
    app_key: str

    app_host: str = '127.0.0.1'
    app_port: int = 8080

    app_client_key_hashes: Annotated[list[str], NoDecode] = []

    @field_validator('app_client_key_hashes', mode='before')
    @classmethod
    def split_hashes(cls, hashes: str | list[str]) -> list[str]:
        if isinstance(hashes, str):
            hashes = hashes.split(',')
        return hashes


class SentrySettings(BaseSettings):
    sentry_dsn: str | None = None
    traces_sample_rate: float = 1.0


class CacheSettings(BaseSettings):
    cache_url: str = 'redis://localhost:6379'


class DBSettings(BaseSettings):
    db_url: str


class HTTPClientSettings(BaseSettings):
    http_retries: int = 2


OPTIONAL_SETTINGS: dict[str, type[BaseSettings]] = {
    'redis': CacheSettings,
    'sqlmodel': DBSettings,
    'httpx': HTTPClientSettings,
}

settings_bases = [AppSettings, SentrySettings]

for module, base in OPTIONAL_SETTINGS.items():
    try:
        __import__(module)
    except ImportError:
        pass
    else:
        settings_bases.append(base)


if TYPE_CHECKING:

    class CoreSettings(
        AppSettings,
        SentrySettings,
        CacheSettings,
        DBSettings,
        HTTPClientSettings,
    ): ...
else:

    class CoreSettings(*settings_bases): ...
