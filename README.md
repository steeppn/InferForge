# InferForge

InferForge is an open-source inference optimization platform for cloud AI workloads on Arm-based infrastructure.

It sits in front of an inference backend as a lightweight proxy, records measurable performance data, and provides the foundation for optimization workflows such as semantic caching, reproducible benchmarking, traffic replay, and data-driven recommendations.

The long-term goal is to help developers answer a practical question:

> How much faster, cheaper, and more efficient can my inference workload become on Arm if I add intelligent optimization?

InferForge is being built for the Arm Create: AI Optimization Challenge, Cloud AI track.

## Why InferForge

Inference optimization is only useful when it can be measured. InferForge is designed around that idea:

- route generation requests through a simple proxy
- cache repeat or semantically similar prompts
- measure latency and cache behavior
- compare optimized and unoptimized workloads
- replay traffic for repeatable tests
- generate reports that support performance claims

The current implementation establishes the proxy, cache, metrics, CLI, tests, and Docker packaging. Future modules will build on this foundation rather than mixing benchmark logic directly into the hot request path.

## Current Capabilities

- FastAPI inference proxy
- `POST /generate` endpoint
- `GET /health` endpoint
- `GET /metrics` endpoint
- inference backend abstraction
- mock inference backend for local development and tests
- semantic cache abstraction
- in-memory normalized prompt cache
- metrics collector with request totals, cache hits, cache misses, hit rate, average latency, p50, and p95
- Typer CLI with `inferforge serve`
- placeholder CLI commands for future benchmark, replay, and report workflows
- pytest coverage for core behavior
- Docker image support

## Architecture

```text
Client
   |
   v
InferForge Inference Proxy
   |
   |-- Semantic Cache
   |-- Metrics Collector
   |-- Future Benchmark Engine
   |-- Future Replay Engine
   |-- Future Optimization Advisor
   |-- Future Adaptive Batch Scheduler
   |
   v
Inference Backend
   |
   |-- Mock backend today
   |-- ONNX Runtime in a future phase
   |-- llama.cpp in a future phase
```

The proxy is intentionally small. Backends, caches, metrics, benchmark runners, and advisors are separated so the project can grow without turning the request path into a pile of feature flags.

## Requirements

- Python 3.12+
- Docker, optional

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the project with development dependencies:

```bash
python -m pip install -e ".[dev]"
```

## Quickstart

Run the proxy:

```bash
inferforge serve
```

Call the generation endpoint:

```bash
curl -X POST http://localhost:8000/generate ^
  -H "Content-Type: application/json" ^
  -d "{\"prompt\": \"Summarize Arm-based cloud inference optimization.\"}"
```

Example response:

```json
{
  "output": "Mock response for: Summarize Arm-based cloud inference optimization.",
  "cache_hit": false,
  "latency_ms": 0.12,
  "backend": "mock"
}
```

Call the same prompt again with caching enabled to see a cache hit:

```bash
curl -X POST http://localhost:8000/generate ^
  -H "Content-Type: application/json" ^
  -d "{\"prompt\": \"summarize arm-based cloud inference optimization.\"}"
```

Check service health:

```bash
curl http://localhost:8000/health
```

View runtime metrics:

```bash
curl http://localhost:8000/metrics
```

Example metrics response:

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

## API

### `GET /health`

Returns the health status of the proxy.

```json
{
  "status": "ok"
}
```

### `POST /generate`

Generates output through the configured backend, optionally using the cache.

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

### `GET /metrics`

Returns an in-memory snapshot of proxy activity since process start.

```json
{
  "requests_total": 100,
  "cache_hits": 45,
  "cache_misses": 55,
  "cache_hit_rate": 0.45,
  "average_latency_ms": 120.5,
  "p50_latency_ms": 98.2,
  "p95_latency_ms": 210.8
}
```

## CLI

Run the proxy:

```bash
inferforge serve
```

Future commands are already reserved in the CLI as placeholders:

```bash
inferforge benchmark
inferforge replay examples/workload.json
inferforge report
```

Those commands do not implement benchmark, replay, or report generation yet. They exist to make the intended developer workflow visible while keeping the current release honest.

## Docker

Build the image:

```bash
docker build -t inferforge .
```

Run the proxy:

```bash
docker run --rm -p 8000:8000 inferforge
```

Then call:

```bash
curl http://localhost:8000/health
```

## Tests

Run the test suite:

```bash
python -m pytest
```

The current tests cover:

- normalized prompt cache hits and misses
- metrics aggregation and percentiles
- health, generation, cache, and metrics API behavior

## Repository Layout

```text
inferforge/
|-- apps/
|   `-- proxy/
|       `-- main.py
|-- inferforge/
|   |-- cache/
|   |-- inference/
|   |-- metrics/
|   |-- advisor/
|   |-- benchmark/
|   |-- replay/
|   |-- scheduler/
|   `-- cli.py
|-- tests/
|-- docs/
|-- examples/
|-- Dockerfile
|-- pyproject.toml
|-- README.md
`-- LICENSE
```

## Roadmap

### Foundation

Status: implemented.

- FastAPI proxy
- backend abstraction
- mock backend
- cache abstraction
- in-memory cache
- metrics collector
- CLI
- tests
- Docker support

### Benchmarking

Planned next.

- run repeated requests against the proxy
- compare cache-on and cache-off behavior
- emit JSON and Markdown reports
- make results reproducible enough for demos and judging

### Replay

Planned after benchmark basics.

- read a workload file
- replay production-like traffic patterns
- compare baseline and optimized runs
- measure cache hit rate, latency changes, and throughput changes

### Optimization Advisor

Planned after benchmark and replay data exist.

- inspect measured results
- recommend cache and runtime tuning changes
- avoid generic advice that is not backed by project metrics

### Advanced Backends And Caching

Future work.

- ONNX Runtime backend
- llama.cpp backend
- embedding-based semantic cache
- vector search
- cache TTL and eviction policies

## Project Principles

- Every optimization claim should be measurable.
- The hot inference path should stay lightweight.
- Interfaces should make backends and caches swappable.
- Tests should cover every core behavior.
- Documentation should stay accurate and runnable.
- Advanced modules should wait until the base system is stable.

## License

InferForge is released under the MIT License. See `LICENSE`.
