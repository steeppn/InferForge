from fastapi.testclient import TestClient

from apps.proxy.main import create_app


def test_health_endpoint() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_generate_endpoint_returns_mock_output_and_records_cache_miss() -> None:
    client = TestClient(create_app())

    response = client.post("/generate", json={"prompt": "Optimize inference on Arm"})

    assert response.status_code == 200
    body = response.json()
    assert body["output"] == "Mock response for: Optimize inference on Arm"
    assert body["cache_hit"] is False
    assert body["latency_ms"] >= 0
    assert body["backend"] == "mock"

    metrics = client.get("/metrics").json()
    assert metrics["requests_total"] == 1
    assert metrics["cache_hits"] == 0
    assert metrics["cache_misses"] == 1


def test_generate_endpoint_uses_cache_on_repeated_prompt() -> None:
    client = TestClient(create_app())

    first = client.post("/generate", json={"prompt": "Summarize Graviton inference"})
    second = client.post("/generate", json={"prompt": " summarize   graviton INFERENCE "})

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["cache_hit"] is False
    assert second.json()["cache_hit"] is True
    assert second.json()["output"] == "Mock response for: Summarize Graviton inference"

    metrics = client.get("/metrics").json()
    assert metrics["requests_total"] == 2
    assert metrics["cache_hits"] == 1
    assert metrics["cache_misses"] == 1
    assert metrics["cache_hit_rate"] == 0.5


def test_generate_endpoint_can_bypass_cache() -> None:
    client = TestClient(create_app())

    client.post("/generate", json={"prompt": "Bypass cache"})
    response = client.post(
        "/generate",
        json={"prompt": "Bypass cache", "use_cache": False},
    )

    assert response.status_code == 200
    assert response.json()["cache_hit"] is False

    metrics = client.get("/metrics").json()
    assert metrics["requests_total"] == 2
    assert metrics["cache_hits"] == 0
    assert metrics["cache_misses"] == 2
