"""Local semantic-style event retrieval backend.

This module intentionally has no mandatory third-party dependencies. For the
current POC scale, a persisted sparse lexical TF-IDF index is good enough to
provide a real shared retrieval backend and a stable extension point for a
future multilingual embedding model.
"""

from __future__ import annotations

import math
import pickle
import re
from collections import Counter
from pathlib import Path
from typing import Any


INDEX_VERSION = "semantic-event-index-v1"
TOKEN_RE = re.compile(r"[\w\u0590-\u05ff׳״'-]+", re.UNICODE)


def normalize_text(value: str | None) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip()).casefold()


def tokenize(text: str) -> list[str]:
    tokens = [token for token in TOKEN_RE.findall(normalize_text(text)) if len(token) > 1]
    bigrams = [f"{tokens[index]} {tokens[index + 1]}" for index in range(len(tokens) - 1)]
    return tokens + bigrams


def cosine_sparse(first: dict[str, float], second: dict[str, float], first_norm: float, second_norm: float) -> float:
    if not first or not second or first_norm <= 0 or second_norm <= 0:
        return 0.0
    if len(first) > len(second):
        first, second = second, first
    dot = sum(weight * second.get(term, 0.0) for term, weight in first.items())
    if dot <= 0:
        return 0.0
    return dot / (first_norm * second_norm)


class SemanticEventIndex:
    """Shared semantic retrieval backend over event records.

    The backend currently uses sparse TF-IDF over enriched event text. The API is
    intentionally named as a semantic index so callers do not depend on the
    implementation; an embedding model can replace the internals later.
    """

    def __init__(self, records: list[dict[str, Any]], cache_dir: Path | str | None = None, signature: dict[str, Any] | None = None):
        self.records = records
        self.cache_dir = Path(cache_dir) if cache_dir else None
        self.signature = signature or {}
        self.backend = "lexical_tfidf"
        self.idf: dict[str, float] = {}
        self.doc_vectors: list[dict[str, float]] = []
        self.doc_norms: list[float] = []
        self.manifest: dict[str, Any] = {}
        self._load_or_build()

    @staticmethod
    def event_text(record: dict[str, Any]) -> str:
        parts = [
            record.get("event_summary"),
            record.get("entity_id"),
            record.get("entity_name"),
            record.get("location_id"),
            record.get("location_name"),
            record.get("source_type"),
            record.get("timestamp_utc"),
            record.get("certainty_level"),
            record.get("source_reliability_label"),
        ]
        return " ".join(str(part) for part in parts if part)

    def _cache_path(self) -> Path | None:
        if not self.cache_dir:
            return None
        return self.cache_dir / "semantic_event_index.pkl"

    def _expected_manifest(self) -> dict[str, Any]:
        return {
            "version": INDEX_VERSION,
            "backend": self.backend,
            "record_count": len(self.records),
            **self.signature,
        }

    def _load_or_build(self) -> None:
        path = self._cache_path()
        expected = self._expected_manifest()
        if path and path.exists():
            try:
                with path.open("rb") as handle:
                    payload = pickle.load(handle)
                if payload.get("manifest") == expected:
                    self.idf = payload["idf"]
                    self.doc_vectors = payload["doc_vectors"]
                    self.doc_norms = payload["doc_norms"]
                    self.manifest = expected
                    return
            except Exception:
                pass
        self._build()
        self.manifest = expected
        if path:
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                temporary = path.with_suffix(".tmp")
                with temporary.open("wb") as handle:
                    pickle.dump(
                        {
                            "manifest": self.manifest,
                            "idf": self.idf,
                            "doc_vectors": self.doc_vectors,
                            "doc_norms": self.doc_norms,
                        },
                        handle,
                        protocol=pickle.HIGHEST_PROTOCOL,
                    )
                temporary.replace(path)
            except Exception:
                pass

    def _build(self) -> None:
        document_tokens = [tokenize(self.event_text(record)) for record in self.records]
        document_frequency = Counter()
        for tokens in document_tokens:
            document_frequency.update(set(tokens))
        document_count = max(len(document_tokens), 1)
        self.idf = {
            term: math.log((1 + document_count) / (1 + count)) + 1.0
            for term, count in document_frequency.items()
        }
        self.doc_vectors = []
        self.doc_norms = []
        for tokens in document_tokens:
            vector = self._vectorize_tokens(tokens)
            self.doc_vectors.append(vector)
            self.doc_norms.append(math.sqrt(sum(weight * weight for weight in vector.values())))

    def _vectorize_tokens(self, tokens: list[str]) -> dict[str, float]:
        counts = Counter(tokens)
        if not counts:
            return {}
        max_count = max(counts.values())
        return {
            term: (0.5 + 0.5 * (count / max_count)) * self.idf.get(term, 0.0)
            for term, count in counts.items()
            if term in self.idf
        }

    def _query_vector(self, query: str) -> tuple[dict[str, float], float]:
        vector = self._vectorize_tokens(tokenize(query))
        norm = math.sqrt(sum(weight * weight for weight in vector.values()))
        return vector, norm

    @staticmethod
    def _passes_filters(record: dict[str, Any], filters: dict[str, Any]) -> bool:
        start_time = filters.get("start_time")
        end_time = filters.get("end_time")
        timestamp = record.get("timestamp_utc") or ""
        if start_time and timestamp < str(start_time):
            return False
        if end_time and timestamp > str(end_time):
            return False
        for key, field in [
            ("location_ids", "location_id"),
            ("entity_ids", "entity_id"),
            ("source_types", "source_type"),
            ("reliabilities", "source_reliability"),
            ("certainty_levels", "certainty_level"),
        ]:
            values = set(filters.get(key) or [])
            if values and record.get(field) not in values:
                return False
        keywords = [normalize_text(keyword) for keyword in filters.get("keywords") or [] if normalize_text(keyword)]
        if keywords:
            haystack = normalize_text(SemanticEventIndex.event_text(record))
            matcher = all if filters.get("match_all_keywords") else any
            if not matcher(keyword in haystack for keyword in keywords):
                return False
        return True

    @staticmethod
    def _rationale(query_terms: set[str], record: dict[str, Any], score: float) -> str:
        record_terms = set(tokenize(SemanticEventIndex.event_text(record)))
        overlap = [term for term in query_terms if term in record_terms]
        if overlap:
            return f"shared weighted terms: {', '.join(overlap[:6])}; score={score:.3f}"
        return f"vector similarity score={score:.3f}"

    def search(self, query: str, filters: dict[str, Any] | None = None, limit: int = 50) -> list[dict[str, Any]]:
        filters = filters or {}
        limit = max(1, int(limit or 50))
        query_vector, query_norm = self._query_vector(query)
        query_terms = set(tokenize(query))
        scored = []
        for index, record in enumerate(self.records):
            if not self._passes_filters(record, filters):
                continue
            score = cosine_sparse(query_vector, self.doc_vectors[index], query_norm, self.doc_norms[index])
            if score <= 0:
                continue
            scored.append(
                {
                    "event_id": record.get("event_id"),
                    "semantic_score": round(score, 6),
                    "rationale": self._rationale(query_terms, record, score),
                    "record": record,
                }
            )
        scored.sort(key=lambda item: (-item["semantic_score"], item["record"].get("timestamp_utc", ""), item["event_id"] or ""))
        return scored[:limit]
