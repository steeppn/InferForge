from time import perf_counter

from fastapi import FastAPI
from pydantic import BaseModel, Field

from inferforge.cache import InMemorySemanticCache, SemanticCache
from inferforge.inference import InferenceBackend, MockInferenceBackend
from inferforge.metrics import MetricsCollector


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    use_cache: bool = True


class GenerateResponse(BaseModel):
    output: str
    cache_hit: bool
    latency_ms: float
    backend: str


def create_app(
    backend: InferenceBackend | None = None,
    cache: SemanticCache | None = None,
    metrics: MetricsCollector | None = None,
) -> FastAPI:
    app = FastAPI(title="InferForge", version="0.1.0")
    app.state.backend = backend or MockInferenceBackend()
    app.state.cache = cache or InMemorySemanticCache()
    app.state.metrics = metrics or MetricsCollector()

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/generate", response_model=GenerateResponse)
    async def generate(request: GenerateRequest) -> GenerateResponse:
        started = perf_counter()
        cache_hit = False

        if request.use_cache:
            cached = await app.state.cache.get(request.prompt)
            if cached.hit and cached.output is not None:
                cache_hit = True
                output = cached.output
            else:
                output = await app.state.backend.generate(request.prompt)
                await app.state.cache.set(request.prompt, output)
        else:
            output = await app.state.backend.generate(request.prompt)

        latency_ms = (perf_counter() - started) * 1000
        app.state.metrics.record_request(latency_ms=latency_ms, cache_hit=cache_hit)

        return GenerateResponse(
            output=output,
            cache_hit=cache_hit,
            latency_ms=latency_ms,
            backend=app.state.backend.name,
        )

    @app.get("/metrics")
    async def metrics_snapshot() -> dict[str, object]:
        return app.state.metrics.snapshot()

    return app


app = create_app()
