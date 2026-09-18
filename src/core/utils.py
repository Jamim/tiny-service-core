from datetime import UTC, datetime


def now() -> datetime:
    """Return current UTC timestamp as a naive datetime."""

    return datetime.now(UTC).replace(tzinfo=None)
