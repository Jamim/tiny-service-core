from datetime import datetime

from freezegun import freeze_time

from core.utils import now


@freeze_time('2026-09-18 14:49:42')
def test_utils_now():
    timestamp = now()

    assert isinstance(timestamp, datetime)
    assert timestamp.tzinfo is None
    assert timestamp == datetime(2026, 9, 18, 14, 49, 42)
