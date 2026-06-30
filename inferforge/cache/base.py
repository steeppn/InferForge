from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class CacheResult:
    hit: bool
    output: str | None = None
    similarity: float | None = None


class SemanticCache(Protocol):
    async def get(self, prompt: str) -> CacheResult:
        """Return a cached output for a prompt when available."""

    async def set(self, prompt: str, output: str) -> None:
        """Store an output for a prompt."""
