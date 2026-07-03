from collections.abc import Awaitable, Callable
from typing import Any

from starlette.datastructures import State

type CleanUpFunc = Callable[[], Awaitable[None]]
type CoreInitFunc = Callable[[State, Any], CleanUpFunc]
type AppInitFunc = Callable[[State], CleanUpFunc | None]
