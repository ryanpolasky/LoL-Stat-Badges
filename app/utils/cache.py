# Created by Ryan Polasky, 3/22/26
# All rights reserved

import time
import logging
from typing import Any

logger = logging.getLogger(__name__)


class TTLCache:
    """Simple in-memory cache with per-entry TTL expiration."""
    def __init__(self, ttl: int = 3600):
        self._cache: dict[str, tuple[float, Any]] = {}
        self._ttl = ttl

    def get(self, key: str) -> Any | None:
        entry = self._cache.get(key)
        if entry is None:
            return None
        timestamp, value = entry
        if time.monotonic() - timestamp < self._ttl:
            return value
        del self._cache[key]
        return None

    def set(self, key: str, value: Any) -> None:
        self._cache[key] = (time.monotonic(), value)
