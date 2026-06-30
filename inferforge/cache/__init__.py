"""Cache implementations for InferForge."""

from inferforge.cache.base import CacheResult, SemanticCache
from inferforge.cache.memory import InMemorySemanticCache

__all__ = ["CacheResult", "InMemorySemanticCache", "SemanticCache"]
