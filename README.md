# InferForge

InferForge is an Arm-native AI inference optimization platform for cloud AI workloads.

Phase 1 provides the foundation:

- FastAPI inference proxy
- `POST /generate`
- `GET /health`
- `GET /metrics`
- mock inference backend
- in-memory semantic cache
- metrics collector
- Typer CLI
- pytest coverage
- Dockerfile

Advanced benchmarking, replay, optimization advising, model backends, and adaptive batching are planned after the foundation is stable.

## Requirements

- Python 3.12+
- Docker, optional

## Quickstart

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install InferForge with development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run the proxy:

```bash
inferforge serve
```

Call the inference endpoint:

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

Call the same prompt again with caching enabled to see a cache hit.

Check service health:

```bash
curl http://localhost:8000/health
```

View metrics:

```bash
curl http://localhost:8000/metrics
```

## Tests

```bash
pytest
```

## Docker

Build the image:

```bash
docker build -t inferforge .
```

Run the proxy:

```bash
docker run --rm -p 8000:8000 inferforge
```

## Project Scope

The Phase 1 MVP is intentionally limited to the lightweight proxy foundation. It does not include ONNX Runtime, llama.cpp, FAISS, Sentence Transformers, benchmark generation, replay mode, the optimization advisor, or adaptive batching yet.
