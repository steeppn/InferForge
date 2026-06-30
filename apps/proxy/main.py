from fastapi import FastAPI
from pydantic import BaseModel, Field

from inferforge.cache import InMemorySemanticCache, SemanticCache
from inferforge.inference import InferenceBackend, MockInferenceBackend
from inferforge.metrics import MetricsCollector
from inferforge.services import InferenceService


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
    app.state.inference_service = InferenceService(
        backend=app.state.backend,
        cache=app.state.cache,
        metrics=app.state.metrics,
    )

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/generate", response_model=GenerateResponse)
    async def generate(request: GenerateRequest) -> GenerateResponse:
        result = await app.state.inference_service.generate(
            prompt=request.prompt,
            use_cache=request.use_cache,
        )
        return GenerateResponse(
            output=result.output,
            cache_hit=result.cache_hit,
            latency_ms=result.latency_ms,
            backend=result.backend,
        )

    @app.get("/metrics")
    async def metrics_snapshot() -> dict[str, object]:
        return app.state.metrics.snapshot()

    return app


app = create_app()
