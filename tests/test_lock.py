from unittest.mock import Mock

from core import Lock


class DummyLock(Lock):
    template = 'dummy:{}'
    timeout = 42


def test_lock():
    cache = Mock()

    DummyLock(cache, 'foo')

    cache.lock.assert_called_once_with('core:lock:dummy:foo', timeout=42)
