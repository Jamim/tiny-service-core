from redis.asyncio.client import Redis
from redis.asyncio.lock import Lock as RedisLock

from . import settings


class Lock:
    prefix: str = f'{settings.app_name}:lock'  # type: ignore[has-type]
    template: str = ''
    timeout: float | None = None

    # https://github.com/python/mypy/issues/15182
    def __new__(  # type: ignore[misc]
        cls,
        cache: Redis,
        *args: str,
    ) -> RedisLock:
        name = f'{cls.prefix}:{cls.template.format(*args)}'
        return cache.lock(name, timeout=cls.timeout)
