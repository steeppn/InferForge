from bisect import insort
from threading import Lock
from typing import Any


class MetricsCollector:
    def __init__(self) -> None:
        self._requests_total = 0
        self._cache_hits = 0
        self._cache_misses = 0
        self._latencies_ms: list[float] = []
        self._lock = Lock()

    def record_request(self, latency_ms: float, cache_hit: bool) -> None:
        with self._lock:
            self._requests_total += 1
            if cache_hit:
                self._cache_hits += 1
            else:
                self._cache_misses += 1
            insort(self._latencies_ms, latency_ms)

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            latencies = list(self._latencies_ms)
            requests_total = self._requests_total
            cache_hits = self._cache_hits
            cache_misses = self._cache_misses

        average_latency = sum(latencies) / len(latencies) if latencies else 0.0
        hit_rate = cache_hits / requests_total if requests_total else 0.0

        return {
            "requests_total": requests_total,
            "cache_hits": cache_hits,
            "cache_misses": cache_misses,
            "cache_hit_rate": hit_rate,
            "average_latency_ms": average_latency,
            "p50_latency_ms": self._percentile(latencies, 50),
            "p95_latency_ms": self._percentile(latencies, 95),
        }

    @staticmethod
    def _percentile(sorted_values: list[float], percentile: int) -> float:
        if not sorted_values:
            return 0.0
        if len(sorted_values) == 1:
            return sorted_values[0]

        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower = int(rank)
        upper = min(lower + 1, len(sorted_values) - 1)
        weight = rank - lower
        return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight
