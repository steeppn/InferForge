# InferForge Project Scope

InferForge is an open-source, Arm-native AI inference optimization platform for cloud AI workloads.

The project is being built for the Arm Create: AI Optimization Challenge, Cloud AI track, as an optimization-focused developer tool. The core promise is simple: make inference optimization measurable through a lightweight proxy, caching, metrics, repeatable tests, and later benchmark reports.

## Current Phase

Phase 1 foundation is implemented.

Phase 1 focuses on a clean, runnable MVP rather than advanced optimization features. The goal is to prove that the proxy path, backend abstraction, cache behavior, metrics collection, packaging, tests, and Docker workflow all work before adding benchmark, replay, or advisor modules.

## Phase 1 Delivered

- Python package setup with `pyproject.toml`
- FastAPI inference proxy in `apps/proxy/main.py`
- `GET /health`
- `POST /generate`
- `GET /metrics`
- inference backend protocol
- mock inference backend
- semantic cache protocol
- in-memory normalized prompt cache
- metrics collector for request totals, cache hits, cache misses, average latency, p50, and p95
- Typer CLI with `inferforge serve`
- placeholders for future `benchmark`, `replay`, and `report` commands
- pytest coverage for cache, metrics, and proxy behavior
- Dockerfile
- README quickstart
- example workload file

## Verified

- `python -m pytest` passes with 8 tests.
- `docker build -t inferforge .` succeeds.
- Docker container smoke test passes on `GET /health`.
- Docker container smoke test passes on `POST /generate`.
- The package build now includes both `apps` and `inferforge`, so the container can import `apps.proxy.main`.

## Phase 1 API

### `GET /health`

Returns:

```json
{
  "status": "ok"
}
```

### `POST /generate`

Request:

```json
{
  "prompt": "Summarize Arm-based inference optimization.",
  "use_cache": true
}
```

Response:

```json
{
  "output": "Mock response for: Summarize Arm-based inference optimization.",
  "cache_hit": false,
  "latency_ms": 0.12,
  "backend": "mock"
}
```

Rules:

- If cache is enabled and a normalized prompt match exists, return the cached output.
- If cache is enabled and no match exists, call the backend and store the generated output.
- If cache is disabled, always call the backend.
- Every request records latency and cache hit/miss status.

### `GET /metrics`

Returns:

```json
{
  "requests_total": 2,
  "cache_hits": 1,
  "cache_misses": 1,
  "cache_hit_rate": 0.5,
  "average_latency_ms": 0.2,
  "p50_latency_ms": 0.2,
  "p95_latency_ms": 0.3
}
```

## Current Repository Shape

```text
inferforge/
|-- apps/
|   `-- proxy/
|       `-- main.py
|-- inferforge/
|   |-- cache/
|   |   |-- base.py
|   |   `-- memory.py
|   |-- inference/
|   |   |-- base.py
|   |   `-- mock.py
|   |-- metrics/
|   |   `-- collector.py
|   |-- advisor/
|   |-- benchmark/
|   |-- replay/
|   |-- scheduler/
|   `-- cli.py
|-- tests/
|   |-- test_cache.py
|   |-- test_metrics.py
|   `-- test_proxy.py
|-- docs/
|   |-- PROJECT_SCOPE.md
|   |-- PROJECT_SPEC.md
|   `-- Hackathon-Rules.txt
|-- examples/
|   `-- workload.json
|-- Dockerfile
|-- pyproject.toml
|-- README.md
|-- LICENSE
`-- .gitignore
```

## Phase 1 Definition of Done

Phase 1 is considered complete when:

- the FastAPI app runs locally
- `/health` works
- `/generate` works
- `/metrics` works
- cache hits and misses are tracked
- latency is measured
- tests pass with pytest
- Docker image builds
- Docker container runs successfully
- README has a working quickstart
- project structure is clean and modular

Current status: complete.

## Not In Phase 1

The following are intentionally out of scope until the foundation remains stable:

- real ONNX Runtime backend
- llama.cpp backend
- Sentence Transformers
- FAISS or vector search
- full semantic similarity
- benchmark engine
- replay engine
- optimization advisor
- adaptive batch scheduler
- cloud deployment automation
- dashboard

## Phase 2 Candidates

The next practical foundation step is to add reproducible benchmarking without jumping straight to advanced model infrastructure.

Recommended Phase 2 order:

1. Add a simple benchmark runner that can call the local proxy repeatedly.
2. Produce JSON and Markdown benchmark reports.
3. Measure cache-on versus cache-off latency.
4. Add a replay input format based on `examples/workload.json`.
5. Keep optimization recommendations manual or rule-based only after benchmark data exists.

## Engineering Rules

- Keep changes small and reviewable.
- Use type hints.
- Prefer interfaces and dependency injection.
- Keep the hot inference path lightweight.
- Add tests for every core behavior.
- Keep README commands accurate and runnable.
- Do not implement future modules until their prerequisite metrics are measurable.
- Optimization claims must be backed by measured results.
