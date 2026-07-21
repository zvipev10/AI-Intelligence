#!/usr/bin/env python3
"""Post-run scorer; this is the only process allowed to read evaluator artifacts."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


THRESHOLDS = {"chain_recall": 0.90, "evidence_precision": 0.90, "evidence_recall": 0.90, "hard_negative_rejection": 0.95, "false_merge_rate_max": 0.05, "duplicate_target_rate_max": 0.02, "source_independence": 1.0}


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ratio(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-output", type=Path, required=True)
    parser.add_argument("--truth", type=Path, required=True)
    parser.add_argument("--labels", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    runtime = json.loads(args.runtime_output.read_text(encoding="utf-8"))
    truth = load_jsonl(args.truth)
    with args.labels.open(encoding="utf-8-sig", newline="") as handle:
        labels = list(csv.DictReader(handle))

    truth_by_anchor = {item["evidence_record_ids"][0]: item for item in truth}
    evidence_owner = {event_id: item["fusion_truth_id"] for item in truth for event_id in item["evidence_record_ids"]}
    expected_evidence = set(evidence_owner)
    hard_negatives = {row["record_id"] for row in labels if row.get("fusion_truth_role") == "hard_negative"}
    predicted = runtime.get("candidates") or []
    predicted_evidence, correct_evidence, matches = set(), set(), []
    false_merges = independent = 0
    failures = []
    for candidate in predicted:
        evidence = set(candidate.get("evidence_record_ids") or [])
        predicted_evidence |= evidence
        correct_evidence |= evidence & expected_evidence
        owners = {evidence_owner[item] for item in evidence if item in evidence_owner}
        if len(owners) > 1:
            false_merges += 1
            failures.append({"category": "false_merge", "candidate_key": candidate.get("candidate_key"), "owners": sorted(owners)})
        expected = truth_by_anchor.get(candidate.get("candidate_key"))
        if expected and set(expected["evidence_record_ids"]).issubset(evidence):
            matches.append(expected["fusion_truth_id"])
        if int(candidate.get("source_group_count") or 0) >= 2:
            independent += 1

    match_counts = Counter(matches)
    metrics = {
        "positive_chains": len(truth), "hard_negatives": len(hard_negatives), "predicted_candidates": len(predicted), "matched_chains": len(set(matches)),
        "chain_recall": ratio(len(set(matches)), len(truth)),
        "evidence_precision": ratio(len(correct_evidence), len(predicted_evidence)),
        "evidence_recall": ratio(len(correct_evidence), len(expected_evidence)),
        "hard_negative_rejection": ratio(len(hard_negatives - predicted_evidence), len(hard_negatives)),
        "false_merge_rate": ratio(false_merges, len(predicted)),
        "duplicate_target_rate": ratio(sum(count > 1 for count in match_counts.values()), len(truth)),
        "source_independence": ratio(independent, len(predicted)),
    }
    gates = {
        "chain_recall": metrics["chain_recall"] >= THRESHOLDS["chain_recall"],
        "evidence_precision": metrics["evidence_precision"] >= THRESHOLDS["evidence_precision"],
        "evidence_recall": metrics["evidence_recall"] >= THRESHOLDS["evidence_recall"],
        "hard_negative_rejection": metrics["hard_negative_rejection"] >= THRESHOLDS["hard_negative_rejection"],
        "false_merge_rate": metrics["false_merge_rate"] <= THRESHOLDS["false_merge_rate_max"],
        "duplicate_target_rate": metrics["duplicate_target_rate"] <= THRESHOLDS["duplicate_target_rate_max"],
        "source_independence": metrics["source_independence"] >= THRESHOLDS["source_independence"],
    }
    report = {"status": "pass" if all(gates.values()) else "fail", "thresholds": THRESHOLDS, "metrics": metrics, "gates": gates, "failure_categories": dict(Counter(item["category"] for item in failures)), "failures": failures[:200]}
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
