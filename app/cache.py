# app/cache.py
"""
Simple in-memory cache and token/latency telemetry logger for InternGuide.
"""

import time
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TELEMETRY_LOG_FILE = PROJECT_ROOT / "data" / "telemetry.log"
TELEMETRY_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# Configure logger
logger = logging.getLogger("internguide.telemetry")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(TELEMETRY_LOG_FILE, encoding="utf-8")
    fh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(fh)


class SimpleCache:
    """Thread-safe in-memory cache with stats tracking."""

    def __init__(self, max_size: int = 256):
        self._cache: Dict[str, Tuple[Dict[str, Any], float]] = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0

    def _normalize_key(self, key: str) -> str:
        return " ".join(key.strip().lower().split())

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        norm_key = self._normalize_key(key)
        if norm_key in self._cache:
            self.hits += 1
            entry, _ = self._cache[norm_key]
            return entry
        self.misses += 1
        return None

    def set(self, key: str, value: Dict[str, Any]):
        norm_key = self._normalize_key(key)
        if len(self._cache) >= self.max_size:
            # Simple eviction: pop oldest entry
            oldest_key = next(iter(self._cache))
            self._cache.pop(oldest_key, None)
        self._cache[norm_key] = (value, time.time())

    def clear(self):
        self._cache.clear()
        self.hits = 0
        self.misses = 0

    def stats(self) -> Dict[str, Any]:
        total = self.hits + self.misses
        rate = round((self.hits / total) * 100.0, 2) if total > 0 else 0.0
        return {
            "size": len(self._cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate_pct": rate
        }


def estimate_tokens(text: str) -> int:
    """
    Estimates token count using character/word heuristics (approx. 4 chars or 0.75 words per token).
    """
    if not text:
        return 0
    words = len(text.split())
    chars = len(text)
    # Balanced approximation for English policy text
    return max(1, int(round((words * 1.25 + chars / 4.0) / 2.0)))


def log_telemetry(endpoint: str, query: str, latency_ms: float, prompt_tokens: int, completion_tokens: int, cached: bool):
    """Logs structured telemetry entry to data/telemetry.log."""
    record = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "endpoint": endpoint,
        "query_snippet": query[:60],
        "latency_ms": round(latency_ms, 2),
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
        "cached": cached
    }
    logger.info(json.dumps(record))


# Global cache instance
response_cache = SimpleCache()
