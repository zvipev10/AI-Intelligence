"""Local semantic-style event retrieval backend.

This module intentionally has no mandatory third-party dependencies. It supports
two local retrieval backends:

* lexical_tfidf: sparse TF-IDF baseline.
* dense_hash_embedding: persisted dense hashed n-gram/concept vectors.
* hybrid_embedding: lexical recall with dense/concept reranking.

The dense backend is not tied to an external model. Its contract mirrors an
embedding index so a later multilingual model can replace only the encoder while
keeping the MCP tool shape and scoring harness stable.
"""

from __future__ import annotations

import math
import hashlib
import os
import pickle
import re
from collections import Counter
from pathlib import Path
from typing import Any

try:
    import numpy as np
except ImportError:  # pragma: no cover - depends on deployment image
    np = None


INDEX_VERSION = "semantic-event-index-v2"
TOKEN_RE = re.compile(r"[\w\u0590-\u05ff׳״'-]+", re.UNICODE)
DEFAULT_DENSE_DIMENSIONS = 768

CONCEPT_FEATURES: tuple[tuple[str, float, tuple[str, ...]], ...] = (
    ("concept:shooting_or_shots", 4.0, ("ירי", "יריות", "קולות שנשמעו כמו ירי", "נשמעו קולות")),
    ("concept:explosion_or_fireworks", 4.0, ("פיצוץ", "פיצוצים", "זיקוקים", "תקלה אזרחית", "רעש אזרחי")),
    ("concept:unverified_or_rumor", 2.5, ("לא מאומת", "לא אומת", "אין אישור", "שמועה", "אין תיעוד חזותי")),
    ("concept:old_or_misattributed_media", 4.0, ("סרטון", "תמונה", "ישן", "לא נראה מהיום", "אינו קשור", "אירוע קודם", "צולם באזור")),
    ("concept:repeated_claims", 3.0, ("ניסוח כמעט זהה", "כמה חשבונות", "מופיע בכמה", "מופץ")),
    ("concept:presence_or_patrol", 3.5, ("נוכחות מוגברת", "הגבירו סיורים", "הגביר את הנוכחות", "סיורים")),
    ("concept:buffer_or_friction_prevention", 4.0, ("למנוע חיכוך", "חיכוך ישיר", "חיץ", "להימנע מהגעה", "מוקדי חיכוך")),
    ("concept:blockade_or_road", 2.5, ("מחסום", "חסימה", "הכביש נחסם", "סגירת כבישים", "ציר")),
    ("concept:misidentification", 3.0, ("מייחסים", "מוצגת כ", "טוענים שמדובר", "לא ברור אם")),
)


def normalize_text(value: str | None) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip()).casefold()


def tokenize(text: str) -> list[str]:
    tokens = [token for token in TOKEN_RE.findall(normalize_text(text)) if len(token) > 1]
    bigrams = [f"{tokens[index]} {tokens[index + 1]}" for index in range(len(tokens) - 1)]
    return tokens + bigrams


def dense_features(text: str) -> list[tuple[str, float]]:
    normalized = normalize_text(text)
    tokens = [token for token in TOKEN_RE.findall(normalized) if len(token) > 1]
    features: list[tuple[str, float]] = []
    features.extend((f"tok:{token}", 1.0) for token in tokens)
    features.extend((f"bigram:{tokens[index]} {tokens[index + 1]}", 1.8) for index in range(len(tokens) - 1))
    compact = re.sub(r"\s+", " ", normalized)
    for size, weight in ((3, 0.35), (4, 0.45), (5, 0.55)):
        if len(compact) >= size:
            features.extend((f"char{size}:{compact[index:index + size]}", weight) for index in range(len(compact) - size + 1))
    for feature_name, weight, markers in CONCEPT_FEATURES:
        if any(normalize_text(marker) in normalized for marker in markers):
            features.append((feature_name, weight))
    return features


def stable_bucket(feature: str, dimensions: int) -> tuple[int, float]:
    digest = hashlib.blake2b(feature.encode("utf-8"), digest_size=8).digest()
    value = int.from_bytes(digest, "big", signed=False)
    return value % dimensions, 1.0 if (value >> 63) == 0 else -1.0


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

    def __init__(
        self,
        records: list[dict[str, Any]],
        cache_dir: Path | str | None = None,
        signature: dict[str, Any] | None = None,
        backend: str | None = None,
        dense_dimensions: int | None = None,
    ):
        self.records = records
        self.record_index_by_id = {record.get("event_id"): index for index, record in enumerate(records) if record.get("event_id")}
        self.cache_dir = Path(cache_dir) if cache_dir else None
        self.signature = signature or {}
        requested_backend = normalize_text(backend or os.environ.get("INTELLIGENCE_POC_SEMANTIC_BACKEND") or "lexical_tfidf")
        self.backend = requested_backend if requested_backend in {"lexical_tfidf", "dense_hash_embedding", "hybrid_embedding"} else "lexical_tfidf"
        self.dense_dimensions = int(dense_dimensions or os.environ.get("INTELLIGENCE_POC_EMBEDDING_DIMENSIONS") or DEFAULT_DENSE_DIMENSIONS)
        self.idf: dict[str, float] = {}
        self.doc_vectors: list[dict[str, float]] = []
        self.doc_norms: list[float] = []
        self.feature_idf: dict[str, float] = {}
        self.embedding_matrix: Any | None = None
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
        return self.cache_dir / f"semantic_event_index_{self.backend}.pkl"

    def _expected_manifest(self) -> dict[str, Any]:
        return {
            "version": INDEX_VERSION,
            "backend": self.backend,
            "dense_dimensions": self.dense_dimensions if self.backend in {"dense_hash_embedding", "hybrid_embedding"} else None,
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
                    self.doc_vectors = payload.get("doc_vectors", [])
                    self.doc_norms = payload.get("doc_norms", [])
                    self.feature_idf = payload.get("feature_idf", {})
                    self.embedding_matrix = payload.get("embedding_matrix")
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
                            "feature_idf": self.feature_idf,
                            "embedding_matrix": self.embedding_matrix,
                        },
                        handle,
                        protocol=pickle.HIGHEST_PROTOCOL,
                    )
                temporary.replace(path)
            except Exception:
                pass

    def _build(self) -> None:
        if self.backend in {"dense_hash_embedding", "hybrid_embedding"}:
            self._build_dense()
            if self.backend == "hybrid_embedding":
                self._build_lexical()
            return
        self._build_lexical()

    def _build_lexical(self) -> None:
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

    def _build_dense(self) -> None:
        document_features = [dense_features(self.event_text(record)) for record in self.records]
        document_frequency = Counter()
        for features in document_features:
            document_frequency.update({feature for feature, _ in features})
        document_count = max(len(document_features), 1)
        self.feature_idf = {
            feature: math.log((1 + document_count) / (1 + count)) + 1.0
            for feature, count in document_frequency.items()
        }
        if np is None:
            vectors = []
            for features in document_features:
                vector = self._sparse_embedding_from_features(features)
                norm = math.sqrt(sum(weight * weight for weight in vector.values()))
                if norm > 0:
                    vector = {bucket: weight / norm for bucket, weight in vector.items()}
                vectors.append(vector)
            self.embedding_matrix = vectors
            self.idf = {}
            self.doc_vectors = []
            self.doc_norms = []
            return
        matrix = np.zeros((len(self.records), self.dense_dimensions), dtype=np.float32)
        for row_index, features in enumerate(document_features):
            vector = self._dense_vector_from_features(features)
            norm = float(np.linalg.norm(vector))
            if norm > 0:
                vector /= norm
            matrix[row_index] = vector
        self.embedding_matrix = matrix
        self.idf = {}
        self.doc_vectors = []
        self.doc_norms = []

    def _sparse_embedding_from_features(self, features: list[tuple[str, float]]) -> dict[int, float]:
        if not features:
            return {}
        vector: dict[int, float] = {}
        counts = Counter(feature for feature, _ in features)
        max_count = max(counts.values())
        for feature, base_weight in features:
            bucket, sign = stable_bucket(feature, self.dense_dimensions)
            tf = 0.5 + 0.5 * (counts[feature] / max_count)
            vector[bucket] = vector.get(bucket, 0.0) + (sign * base_weight * tf * self.feature_idf.get(feature, 1.0))
        return vector

    def _dense_vector_from_features(self, features: list[tuple[str, float]]) -> Any:
        if np is None:
            raise RuntimeError("NumPy is required for dense semantic embeddings")
        vector = np.zeros(self.dense_dimensions, dtype=np.float32)
        if not features:
            return vector
        counts = Counter(feature for feature, _ in features)
        max_count = max(counts.values())
        for feature, base_weight in features:
            bucket, sign = stable_bucket(feature, self.dense_dimensions)
            tf = 0.5 + 0.5 * (counts[feature] / max_count)
            vector[bucket] += np.float32(sign * base_weight * tf * self.feature_idf.get(feature, 1.0))
        return vector

    def _query_embedding(self, query: str) -> Any:
        if np is None:
            vector = self._sparse_embedding_from_features(dense_features(query))
            norm = math.sqrt(sum(weight * weight for weight in vector.values()))
            if norm > 0:
                return {bucket: weight / norm for bucket, weight in vector.items()}
            return {}
        vector = self._dense_vector_from_features(dense_features(query))
        norm = float(np.linalg.norm(vector))
        if norm > 0:
            vector /= norm
        return vector

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

    @staticmethod
    def _dense_rationale(query: str, record: dict[str, Any], score: float) -> str:
        query_concepts = [
            name.replace("concept:", "")
            for name, _, markers in CONCEPT_FEATURES
            if any(normalize_text(marker) in normalize_text(query) for marker in markers)
        ]
        record_text = SemanticEventIndex.event_text(record)
        record_concepts = [
            name.replace("concept:", "")
            for name, _, markers in CONCEPT_FEATURES
            if any(normalize_text(marker) in normalize_text(record_text) for marker in markers)
        ]
        shared = [concept for concept in query_concepts if concept in record_concepts]
        if shared:
            return f"shared embedding concepts: {', '.join(shared[:5])}; score={score:.3f}"
        return f"dense hashed embedding similarity score={score:.3f}"

    def search(self, query: str, filters: dict[str, Any] | None = None, limit: int = 50) -> list[dict[str, Any]]:
        filters = filters or {}
        limit = max(1, int(limit or 50))
        if self.backend == "dense_hash_embedding":
            return self._search_dense(query, filters, limit)
        if self.backend == "hybrid_embedding":
            return self._search_hybrid(query, filters, limit)
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

    def _search_dense(self, query: str, filters: dict[str, Any], limit: int) -> list[dict[str, Any]]:
        if self.embedding_matrix is None:
            return []
        query_vector = self._query_embedding(query)
        if np is not None:
            if not np.any(query_vector):
                return []
            scores = self.embedding_matrix @ query_vector
        elif not query_vector:
            return []
        else:
            scores = None
        scored = []
        for index, record in enumerate(self.records):
            if not self._passes_filters(record, filters):
                continue
            if scores is None:
                score = self._sparse_embedding_similarity(query_vector, self.embedding_matrix[index])
            else:
                score = float(scores[index])
            if score <= 0:
                continue
            scored.append(
                {
                    "event_id": record.get("event_id"),
                    "semantic_score": round(score, 6),
                    "rationale": self._dense_rationale(query, record, score),
                    "record": record,
                }
            )
        scored.sort(key=lambda item: (-item["semantic_score"], item["record"].get("timestamp_utc", ""), item["event_id"] or ""))
        return scored[:limit]

    @staticmethod
    def _sparse_embedding_similarity(first: dict[int, float], second: dict[int, float]) -> float:
        if not first or not second:
            return 0.0
        if len(first) > len(second):
            first, second = second, first
        return sum(weight * second.get(bucket, 0.0) for bucket, weight in first.items())

    @staticmethod
    def _concept_overlap_score(query: str, record: dict[str, Any]) -> float:
        query_text = normalize_text(query)
        record_text = normalize_text(SemanticEventIndex.event_text(record))
        score = 0.0
        for _, weight, markers in CONCEPT_FEATURES:
            query_has = any(normalize_text(marker) in query_text for marker in markers)
            record_has = any(normalize_text(marker) in record_text for marker in markers)
            if query_has and record_has:
                score += weight
        return score

    @staticmethod
    def _specificity_penalty(query: str, record: dict[str, Any]) -> float:
        query_text = normalize_text(query)
        record_text = normalize_text(SemanticEventIndex.event_text(record))
        violence_query = any(marker in query_text for marker in ("ירי", "יריות", "פיצוץ", "פיצוצים", "רעש"))
        if not violence_query:
            return 0.0
        direct_violence_or_noise = any(
            marker in record_text
            for marker in ("ירי", "יריות", "פיצוץ", "פיצוצים", "זיקוקים", "רעש אזרחי", "נשמעו קולות", "רעש חזק")
        )
        if direct_violence_or_noise:
            return 0.0
        generic_traffic_or_closure = any(marker in record_text for marker in ("סגירת כבישים", "סגירת כביש", "מחסום", "חסימה", "כביש"))
        if generic_traffic_or_closure:
            return 0.18
        return 0.08

    def _search_hybrid(self, query: str, filters: dict[str, Any], limit: int) -> list[dict[str, Any]]:
        lexical_backend = self.backend
        self.backend = "lexical_tfidf"
        try:
            lexical_matches = SemanticEventIndex.search(self, query, filters, max(limit, 2000))
        finally:
            self.backend = lexical_backend
        if not lexical_matches:
            return self._search_dense(query, filters, limit)
        if self.embedding_matrix is None:
            return lexical_matches[:limit]
        query_embedding = self._query_embedding(query)
        sparse_dense_scores = False
        if np is not None:
            dense_scores = self.embedding_matrix @ query_embedding if np.any(query_embedding) else None
        else:
            sparse_dense_scores = bool(query_embedding)
            dense_scores = None
        lexical_max = max((item["semantic_score"] for item in lexical_matches), default=1.0) or 1.0
        reranked = []
        for item in lexical_matches:
            event_id = item.get("event_id")
            record_index = self.record_index_by_id.get(event_id)
            if record_index is None:
                continue
            record = self.records[record_index]
            lexical_score = float(item["semantic_score"]) / lexical_max
            if sparse_dense_scores:
                dense_score = self._sparse_embedding_similarity(query_embedding, self.embedding_matrix[record_index])
            else:
                dense_score = float(dense_scores[record_index]) if dense_scores is not None else 0.0
            concept_score = min(self._concept_overlap_score(query, record) / 8.0, 1.0)
            specificity_penalty = self._specificity_penalty(query, record)
            final_score = max(0.0, (0.58 * lexical_score) + (0.22 * max(dense_score, 0.0)) + (0.20 * concept_score) - specificity_penalty)
            reranked.append(
                {
                    "event_id": event_id,
                    "semantic_score": round(final_score, 6),
                    "rationale": (
                        f"hybrid lexical={lexical_score:.3f}; dense={dense_score:.3f}; "
                        f"concept={concept_score:.3f}; penalty={specificity_penalty:.3f}; source={item.get('rationale')}"
                    ),
                    "record": record,
                }
            )
        reranked.sort(key=lambda row: (-row["semantic_score"], row["record"].get("timestamp_utc", ""), row["event_id"] or ""))
        return reranked[:limit]
