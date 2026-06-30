# InferForge

An Arm-native AI Inference Optimization Platform for Cloud AI.

## 1. Project Goal

InferForge is an open-source inference optimization platform designed to improve AI inference performance on Arm-based cloud infrastructure.

The project provides an inference proxy, semantic caching, metrics collection, reproducible benchmarking, replay-based workload testing, and optimization recommendations.

The goal is not only to make inference faster, but to prove the improvement through measurable reports.

## 2. Hackathon Context

This project is intended for the Arm Create: AI Optimization Challenge.

Selected track:

* Track: Cloud AI
* Submission type: Optimization
* Target platform: Arm-based cloud infrastructure, such as AWS Graviton or another Arm64 environment

## 3. Core Value Proposition

InferForge helps developers answer this question:

> “How much faster, cheaper, and more efficient can my AI inference workload become on Arm if I add intelligent optimization?”

InferForge should make this answer measurable through:

* latency comparisons
* throughput comparisons
* cache hit rate
* CPU and memory usage
* replayed workload results
* benchmark reports
* estimated compute savings

## 4. System Overview

```text
Client
   |
   v
InferForge Inference Proxy
   |
   |-- Semantic Cache
   |-- Metrics Collector
   |-- Adaptive Batch Scheduler
   |-- Benchmark Engine
   |-- Replay Engine
   |-- Optimization Advisor
   |
   v
AI Inference Backend
   |
   |-- ONNX Runtime
   |-- llama.cpp
   |-- Mock backend for testing
```

## 5. Design Principles

* Every optimization must be measurable.
* The hot inference path should stay lightweight.
* Developer experience matters.
* The project must be easy to run, test, and validate.
* Benchmark results should be reproducible.
* InferForge should feel like a reusable infrastructure tool, not a one-off demo.
* Prefer clean architecture over rushed feature stacking.
* Build the MVP first before adding advanced modules.

## 6. MVP Scope

The Phase 1 MVP must include:

* Python 3.12 project structure
* FastAPI inference proxy
* `POST /generate` endpoint
* Basic inference backend abstraction
* Mock backend for local testing
* Semantic cache interface
* Basic in-memory semantic cache implementation
* Metrics collector
* `/metrics` endpoint
* Typer CLI skeleton
* pytest setup
* Dockerfile
* README quickstart

The Phase 1 MVP should not include:

* full benchmark engine
* replay mode
* optimization advisor
* adaptive batch scheduler
* cloud deployment automation
* advanced dashboard

Those will be added after the base system is stable.

## 7. Target Developer Workflow

The intended long-term developer experience is:

```bash
inferforge serve
inferforge benchmark
inferforge replay traffic.json
inferforge report
```

For the MVP, the required workflow is:

```bash
inferforge serve
```

Then call:

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Summarize Arm-based cloud inference optimization."}'
```

## 8. Proposed Repository Structure

```text
inferforge/
│
├── apps/
│   └── proxy/
│       └── main.py
│
├── inferforge/
│   ├── __init__.py
│   │
│   ├── cache/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── memory.py
│   │
│   ├── inference/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── mock.py
│   │
│   ├── metrics/
│   │   ├── __init__.py
│   │   └── collector.py
│   │
│   ├── scheduler/
│   │   └── __init__.py
│   │
│   ├── benchmark/
│   │   └── __init__.py
│   │
│   ├── replay/
│   │   └── __init__.py
│   │
│   ├── advisor/
│   │   └── __init__.py
│   │
│   └── cli.py
│
├── tests/
│   ├── test_proxy.py
│   ├── test_cache.py
│   └── test_metrics.py
│
├── docs/
│   └── PROJECT_SPEC.md
│
├── examples/
│   └── workload.json
│
├── reports/
│
├── Dockerfile
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
```

## 9. API Requirements

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
  "output": "Generated response text.",
  "cache_hit": false,
  "latency_ms": 123.45,
  "backend": "mock"
}
```

Rules:

* If cache is enabled and a matching prompt exists, return cached output.
* If cache miss, call the inference backend.
* Store the response in cache after successful generation.
* Always record latency.
* Always record whether the request was a cache hit or miss.

### `GET /health`

Response:

```json
{
  "status": "ok"
}
```

### `GET /metrics`

Response:

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

## 10. Core Modules

## 10.1 Inference Backend

The inference backend must be abstracted behind an interface.

Purpose:

* allow swapping between mock backend, ONNX Runtime, and future llama.cpp backend
* keep the proxy independent from backend implementation
* make testing easier

Required interface:

```python
class InferenceBackend:
    async def generate(self, prompt: str) -> str:
        ...
```

MVP backend:

```python
class MockInferenceBackend:
    async def generate(self, prompt: str) -> str:
        return f"Mock response for: {prompt}"
```

## 10.2 Semantic Cache

The cache must be abstracted behind an interface.

Required behavior:

* `get(prompt: str) -> CacheResult`
* `set(prompt: str, output: str) -> None`
* return whether a cache hit occurred
* include similarity score when available

MVP implementation:

* in-memory storage
* simple normalized text matching or lightweight similarity
* no FAISS yet
* no Sentence Transformers yet

Future implementation:

* Sentence Transformers
* ONNX Runtime embeddings
* FAISS vector search
* cosine similarity
* TTL cache

## 10.3 Metrics Collector

The metrics collector must track:

* total requests
* cache hits
* cache misses
* latency samples
* average latency
* p50 latency
* p95 latency

The collector should expose:

```python
record_request(latency_ms: float, cache_hit: bool) -> None
snapshot() -> dict
```

## 10.4 CLI

Use Typer.

MVP command:

```bash
inferforge serve
```

Future commands:

```bash
inferforge benchmark
inferforge replay workload.json
inferforge report
```

The CLI must not implement future features yet, but it can include placeholder messages.

## 11. Future Modules

## 11.1 Benchmark Engine

Future command:

```bash
inferforge benchmark
```

Outputs:

```text
benchmark.html
benchmark.md
benchmark.json
```

Benchmark scenarios:

* cold inference
* warm inference
* cache on/off
* scheduler on/off
* replay mode

## 11.2 Replay Engine

Future command:

```bash
inferforge replay requests.json
```

Purpose:

* replay recorded or synthetic workloads
* compare baseline vs optimized inference
* show latency improvement
* show throughput improvement
* show cache hit rate
* estimate compute savings

Example output:

```json
{
  "baseline_p95_ms": 850,
  "optimized_p95_ms": 310,
  "latency_reduction_percent": 63.5,
  "cache_hit_rate": 0.48,
  "estimated_monthly_savings_usd": 247.32
}
```

## 11.3 Optimization Advisor

Purpose:

Analyze benchmark results and generate actionable recommendations.

Example recommendations:

* increase similarity threshold if false-positive cache hits are likely
* decrease similarity threshold if cache hit rate is too low
* increase batch size if p95 latency is below target
* decrease batch size if p95 latency exceeds target
* increase worker count if throughput is bottlenecked
* improve request normalization if cache misses are too high

Important rule:

Recommendations must be based on measured benchmark data, not static generic advice.

## 11.4 Adaptive Batch Scheduler

Purpose:

Dynamically adjust batch size based on queue depth and latency.

Basic strategy:

* monitor queue depth
* monitor p95 latency
* increase batch size if latency is within target
* decrease batch size if latency exceeds target
* clamp batch size within safe minimum and maximum values

This is a stretch goal and should not be implemented in Phase 1.

## 12. Benchmarking Goals

InferForge should eventually measure:

* p50 latency
* p95 latency
* average latency
* requests per second
* throughput
* cache hit rate
* cache miss rate
* CPU usage
* memory usage
* queue depth
* batch size
* estimated compute savings

## 13. Demo Flow

The final hackathon demo should show:

1. Baseline inference without optimization
2. InferForge proxy enabled
3. Semantic cache hits
4. Benchmark report generation
5. Replay production-like traffic
6. Before vs after latency and throughput
7. Optimization Advisor recommendations
8. Estimated compute savings

## 14. Definition of Done for Phase 1

Phase 1 is complete when:

* the FastAPI app runs locally
* `/health` works
* `/generate` works
* `/metrics` works
* cache hits and misses are tracked
* latency is measured
* tests pass with pytest
* Docker image builds
* README has a working quickstart
* project structure is clean and modular

## 15. Engineering Style

Codex or any coding agent working on this project should follow these rules:

* Keep changes small and reviewable.
* Use type hints.
* Use clear class and function names.
* Avoid unnecessary complexity.
* Prefer interfaces and dependency injection.
* Do not hardcode advanced features into the proxy.
* Do not implement Phase 2 or Phase 3 until Phase 1 is stable.
* Add tests for every core behavior.
* Keep README instructions accurate and runnable.
* Make the project feel professional enough for judges and reusable enough for developers.

## 16. First Codex Task

Implement Phase 1 MVP only.

Required deliverables:

* Python 3.12 package setup
* FastAPI proxy
* `/health`
* `/generate`
* `/metrics`
* mock inference backend
* cache interface
* in-memory cache
* metrics collector
* Typer CLI with `serve`
* pytest tests
* Dockerfile
* README quickstart

Do not implement:

* real ONNX model loading
* FAISS
* Sentence Transformers
* benchmark engine
* replay engine
* optimization advisor
* adaptive batch scheduler

Focus on the foundation first.
