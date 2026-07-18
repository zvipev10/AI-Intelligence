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
from functools import lru_cache
from pathlib import Path
from typing import Any

try:
    if os.environ.get("INTELLIGENCE_POC_DISABLE_NUMPY") == "1":
        raise ImportError("NumPy disabled for pure-Python semantic validation")
    import numpy as np
except ImportError:  # pragma: no cover - depends on deployment image
    np = None


INDEX_VERSION = "semantic-event-index-v8-v2-military-concepts"
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
    ("concept:uav_observation", 4.0, ("כטב״ם", "כטבם", "מל״ט", "מל״ט", "uav", "drone", "unmanned aerial", "aerial observation", "ניצול וידאו")),
    ("concept:convoy_or_vehicle_column", 5.0, ("שיירת כלי רכב", "שיירה", "טור כלי רכב", "טור צבאי", "convoy", "vehicle column", "military column", "колона возила")),
    ("concept:military_formation", 4.5, ("מבנה צבאי", "כוח גדודי", "כוח פלוגתי", "יחידה צבאית", "military formation", "unit formation", "troop formation", "војна формација")),
    ("concept:armored_vehicle", 5.0, ("רכב משוריין", "רכבים משוריינים", "נגמ״ש", "נגמש", "טנק", "armored vehicle", "armoured vehicle", "armored personnel carrier", "armoured personnel carrier", "apc", "ifv", "оклопно возило")),
    ("concept:air_defense", 5.0, ("הגנה אווירית", "נ״מ", "נמ", "סוללת טילים", "מערכת נ״מ", "מכ״ם", "air defense", "air-defence", "sam battery", "surface-to-air", "radar unit", "противваздушна одбрана")),
    ("concept:logistics_vehicle", 3.5, ("משאית לוגיסטית", "רכב לוגיסטי", "שיירת אספקה", "logistics truck", "supply vehicle", "logistics convoy")),
    ("concept:observation_post", 3.5, ("עמדת תצפית", "נקודת תצפית", "observation post", "lookout post", "осматрачница")),
    ("concept:engineering_activity", 3.5, ("עבודות הנדסיות", "כלי הנדסי", "הקמת ביצורים", "engineering works", "engineering vehicle", "fortification work")),
    ("concept:helicopter", 3.5, ("מסוק", "מסוקים", "helicopter", "rotary-wing", "хеликоптер")),
    ("concept:roadblock_position", 4.0, ("מחסום דרכים", "נקודת חסימה", "עמדת חסימה", "roadblock", "blocking position", "контролни пункт")),
    ("concept:movement", 4.5, ("בתנועה", "נע לעבר", "מתקדם", "התקדמות", "בנסיגה", "נסוג", "movement", "moving", "advancing", "withdrawing", "maneuvering", "у покрету", "повлачење")),
    ("concept:deployment_or_staging", 4.5, ("בפריסה", "נפרס", "פריסה", "בהיערכות", "שטח היערכות", "deployed", "deployment", "staging", "assembly area", "распоређивање")),
    ("concept:stationary_or_halted", 3.0, ("בעצירה", "ללא שינוי נראה", "חונה", "stationary", "halted", "parked", "заустављен")),
    ("concept:force_concentration", 5.0, ("ריכוז כוחות", "הצטברות כוחות", "תגבור כוחות", "כוח מתוגבר", "force concentration", "troop concentration", "force buildup", "massing forces", "груписање снага")),
    ("concept:object_count", 3.0, ("הוערכו", "פריטים", "ספירת עצמים", "מספר כלי רכב", "כמות", "estimated count", "object count", "vehicle count", "units observed")),
    ("concept:serbian_forces", 5.0, ("צבא סרביה", "הצבא הסרבי", "כוחות סרביים", "חיל האוויר הסרבי", "serbian army", "serbian armed forces", "vojska srbije", "војска србије")),
    ("concept:nato_kfor_forces", 5.0, ("kfor", "nato", "נאט״ו", "נאטו", "כוחות נאט״ו", "כוחות קפור", "nato forces", "kfor forces")),
    ("concept:kosovo_police", 5.0, ("משטרת קוסובו", "kosovo police", "kosovska policija", "косовска полиција")),
    ("concept:kosovo_security_force", 5.0, ("כוח הביטחון של קוסובו", "ksf", "kosovo security force", "kosovske bezbednosne snage")),
    ("concept:kosovo_forces", 3.5, ("כוחות קוסובו", "kosovo forces", "kosovske snage")),
)

COUNT_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"(?:estimated_object_count|object_count|estimated count|object count|count|הוערכו|זוהו|נספרו)\s*[:=]?\s*(\d{1,3})", re.IGNORECASE),
    re.compile(r"(\d{1,3})\s+(?:פריטים|כלי רכב|רכבים|עצמים|vehicles|objects|units)\b", re.IGNORECASE),
)


@lru_cache(maxsize=65_536)
def concept_weights(text: str) -> dict[str, float]:
    normalized = normalize_text(text)
    return {
        feature_name: weight
        for feature_name, weight, markers in CONCEPT_FEATURES
        if any(normalize_text(marker) in normalized for marker in markers)
    }


@lru_cache(maxsize=65_536)
def object_counts(text: str) -> frozenset[int]:
    normalized = normalize_text(text)
    return frozenset(
        int(match.group(1))
        for pattern in COUNT_PATTERNS
        for match in pattern.finditer(normalized)
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
    features.extend(concept_weights(normalized).items())
    features.extend((f"object_count:{count}", 4.0) for count in object_counts(normalized))
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
        self.record_texts = [self.event_text(record) for record in records]
        self.record_concept_weights = [concept_weights(text) for text in self.record_texts]
        self.record_object_counts = [object_counts(text) for text in self.record_texts]
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
            f"collection_family {record.get('collection_family')}" if record.get("collection_family") else None,
            f"observation_id {record.get('observation_id')}" if record.get("observation_id") else None,
            f"mission_id {record.get('mission_id')}" if record.get("mission_id") else None,
            f"object_class {record.get('object_class')}" if record.get("object_class") else None,
            f"estimated_object_count {record.get('estimated_object_count')}" if record.get("estimated_object_count") not in {None, ""} else None,
            f"mobility_status {record.get('movement_status')}" if record.get("movement_status") else None,
            f"travel_direction {record.get('movement_direction')}" if record.get("movement_direction") else None,
            f"geolocation_confidence {record.get('geolocation_confidence')}" if record.get("geolocation_confidence") else None,
            f"identification_confidence {record.get('identification_confidence')}" if record.get("identification_confidence") else None,
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
            "dense_engine": ("numpy" if np is not None else "python") if self.backend in {"dense_hash_embedding", "hybrid_embedding"} else None,
            "fallback_mode": "dense_only" if self.backend == "hybrid_embedding" and np is None else None,
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
        if self.backend == "hybrid_embedding" and np is None:
            # On constrained deployments without NumPy, retaining both sparse
            # lexical vectors and sparse dense vectors causes excessive memory
            # pressure. Dense-only fallback preserves cross-language concepts.
            self._build_dense()
            return
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
                dense_score = self._sparse_embedding_similarity(query_vector, self.embedding_matrix[index])
            else:
                dense_score = float(scores[index])
            concept_score = min(self._concept_overlap_score(query, record) / 8.0, 1.0)
            count_score = self._count_overlap_score(query, record)
            score = (0.58 * max(dense_score, 0.0)) + (0.30 * concept_score) + (0.12 * count_score)
            if score <= 0:
                continue
            scored.append(
                {
                    "event_id": record.get("event_id"),
                    "semantic_score": round(score, 6),
                    "record": record,
                }
            )
        scored.sort(key=lambda item: (-item["semantic_score"], item["record"].get("timestamp_utc", ""), item["event_id"] or ""))
        selected = scored[:limit]
        for item in selected:
            item["rationale"] = self._dense_rationale(query, item["record"], item["semantic_score"])
        return selected

    @staticmethod
    def _sparse_embedding_similarity(first: dict[int, float], second: dict[int, float]) -> float:
        if not first or not second:
            return 0.0
        if len(first) > len(second):
            first, second = second, first
        return sum(weight * second.get(bucket, 0.0) for bucket, weight in first.items())

    def _record_index(self, record: dict[str, Any]) -> int | None:
        return self.record_index_by_id.get(record.get("event_id"))

    def _concept_overlap_score(self, query: str, record: dict[str, Any]) -> float:
        query_features = concept_weights(query)
        record_index = self._record_index(record)
        record_features = (
            self.record_concept_weights[record_index]
            if record_index is not None
            else concept_weights(self.event_text(record))
        )
        return sum(weight for name, weight in query_features.items() if name in record_features)

    def _count_overlap_score(self, query: str, record: dict[str, Any]) -> float:
        query_values = object_counts(query)
        if not query_values:
            return 0.0
        record_index = self._record_index(record)
        record_values = (
            self.record_object_counts[record_index]
            if record_index is not None
            else object_counts(self.event_text(record))
        )
        return 1.0 if query_values & record_values else 0.0

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
        if np is None:
            return self._search_dense(query, filters, limit)
        lexical_backend = self.backend
        self.backend = "lexical_tfidf"
        try:
            lexical_matches = SemanticEventIndex.search(self, query, filters, max(limit, 2000))
        finally:
            self.backend = lexical_backend
        if not lexical_matches:
            return self._search_dense(query, filters, limit)
        pure_python_rerank = np is None and self.embedding_matrix is None
        if self.embedding_matrix is None and not pure_python_rerank:
            return lexical_matches[:limit]
        query_embedding = self._query_embedding(query)
        sparse_dense_scores = False
        if np is not None:
            dense_scores = self.embedding_matrix @ query_embedding if np.any(query_embedding) else None
        elif self.embedding_matrix is not None:
            sparse_dense_scores = bool(query_embedding)
            dense_scores = None
        else:
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
            if pure_python_rerank and query_embedding:
                record_embedding = self._sparse_embedding_from_features(dense_features(self.event_text(record)))
                record_norm = math.sqrt(sum(weight * weight for weight in record_embedding.values()))
                if record_norm > 0:
                    record_embedding = {bucket: weight / record_norm for bucket, weight in record_embedding.items()}
                dense_score = self._sparse_embedding_similarity(query_embedding, record_embedding)
            elif sparse_dense_scores:
                dense_score = self._sparse_embedding_similarity(query_embedding, self.embedding_matrix[record_index])
            else:
                dense_score = float(dense_scores[record_index]) if dense_scores is not None else 0.0
            concept_score = min(self._concept_overlap_score(query, record) / 8.0, 1.0)
            count_score = self._count_overlap_score(query, record)
            specificity_penalty = self._specificity_penalty(query, record)
            final_score = max(0.0, (0.48 * lexical_score) + (0.20 * max(dense_score, 0.0)) + (0.20 * concept_score) + (0.12 * count_score) - specificity_penalty)
            reranked.append(
                {
                    "event_id": event_id,
                    "semantic_score": round(final_score, 6),
                    "rationale": (
                        f"hybrid lexical={lexical_score:.3f}; dense={dense_score:.3f}; "
                        f"concept={concept_score:.3f}; count={count_score:.3f}; penalty={specificity_penalty:.3f}; source={item.get('rationale')}"
                    ),
                    "record": record,
                }
            )
        reranked.sort(key=lambda row: (-row["semantic_score"], row["record"].get("timestamp_utc", ""), row["event_id"] or ""))
        return reranked[:limit]
