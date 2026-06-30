from inferforge.cache import InMemorySemanticCache


async def test_in_memory_cache_matches_normalized_prompt() -> None:
    cache = InMemorySemanticCache()

    await cache.set("Summarize Arm inference", "cached output")
    result = await cache.get("  summarize   ARM inference  ")

    assert result.hit is True
    assert result.output == "cached output"
    assert result.similarity == 1.0


async def test_in_memory_cache_miss() -> None:
    cache = InMemorySemanticCache()

    result = await cache.get("missing")

    assert result.hit is False
    assert result.output is None
    assert result.similarity is None
