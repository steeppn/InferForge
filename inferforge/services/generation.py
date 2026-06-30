from dataclasses import dataclass
from time import perf_counter

from inferforge.cache import SemanticCache
from inferforge.inference import InferenceBackend
from inferforge.metrics import MetricsCollector


@dataclass(frozen=True)
class GenerationResult:
    output: str
    cache_hit: bool
    latency_ms: float
    backend: str


class InferenceService:
    def __init__(
        self,
        backend: InferenceBackend,
        cache: SemanticCache,
        metrics: MetricsCollector,
    ) -> None:
        self._backend = backend
        self._cache = cache
        self._metrics = metrics

    async def generate(self, prompt: str, use_cache: bool = True) -> GenerationResult:
        started = perf_counter()
        cache_hit = False

        if use_cache:
            cached = await self._cache.get(prompt)
            if cached.hit and cached.output is not None:
                cache_hit = True
                output = cached.output
            else:
                output = await self._backend.generate(prompt)
                await self._cache.set(prompt, output)
        else:
            output = await self._backend.generate(prompt)

        latency_ms = (perf_counter() - started) * 1000
        self._metrics.record_request(latency_ms=latency_ms, cache_hit=cache_hit)

        return GenerationResult(
            output=output,
            cache_hit=cache_hit,
            latency_ms=latency_ms,
            backend=self._backend.name,
        )
