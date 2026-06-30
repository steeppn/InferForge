import pytest

from inferforge.metrics import MetricsCollector


def test_metrics_collector_tracks_requests_and_percentiles() -> None:
    metrics = MetricsCollector()

    metrics.record_request(latency_ms=100.0, cache_hit=False)
    metrics.record_request(latency_ms=50.0, cache_hit=True)
    metrics.record_request(latency_ms=200.0, cache_hit=False)

    snapshot = metrics.snapshot()

    assert snapshot["requests_total"] == 3
    assert snapshot["cache_hits"] == 1
    assert snapshot["cache_misses"] == 2
    assert snapshot["cache_hit_rate"] == 1 / 3
    assert snapshot["average_latency_ms"] == 350 / 3
    assert snapshot["p50_latency_ms"] == 100.0
    assert snapshot["p95_latency_ms"] == pytest.approx(190.0)


def test_metrics_collector_empty_snapshot() -> None:
    snapshot = MetricsCollector().snapshot()

    assert snapshot == {
        "requests_total": 0,
        "cache_hits": 0,
        "cache_misses": 0,
        "cache_hit_rate": 0.0,
        "average_latency_ms": 0.0,
        "p50_latency_ms": 0.0,
        "p95_latency_ms": 0.0,
    }
