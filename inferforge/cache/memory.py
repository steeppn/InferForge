import re

from inferforge.cache.base import CacheResult


class InMemorySemanticCache:
    """Small MVP cache using normalized exact prompt matches."""

    def __init__(self) -> None:
        self._items: dict[str, str] = {}

    async def get(self, prompt: str) -> CacheResult:
        key = self._normalize(prompt)
        output = self._items.get(key)
        if output is None:
            return CacheResult(hit=False)
        return CacheResult(hit=True, output=output, similarity=1.0)

    async def set(self, prompt: str, output: str) -> None:
        self._items[self._normalize(prompt)] = output

    @staticmethod
    def _normalize(prompt: str) -> str:
        return re.sub(r"\s+", " ", prompt.strip().casefold())
