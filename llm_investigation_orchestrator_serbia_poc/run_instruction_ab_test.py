#!/usr/bin/env python3
"""Run paired inline-vs-persistent General-agent latency measurements."""

from __future__ import annotations

import argparse
import json
import statistics
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MODES = ("inline", "persistent")


def post_json(url: str, payload: dict[str, Any], timeout: float) -> tuple[dict[str, Any], float]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=timeout) as response:
        result = json.loads(response.read().decode("utf-8"))
    return result, round((time.perf_counter() - started) * 1000, 3)


def percentile(values: list[float], fraction: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int((len(ordered) - 1) * fraction)))
    return round(ordered[index], 3)


def summarize(rows: list[dict[str, Any]], warm_only: bool = True) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for mode in MODES:
        candidates = [row for row in rows if row["mode"] == mode and row.get("ok")]
        if warm_only:
            candidates = [row for row in candidates if not row.get("cold")]
        elapsed = [float(row["elapsed_ms"]) for row in candidates]
        tokens = [int(row["input_tokens"]) for row in candidates if row.get("input_tokens") is not None]
        summary[mode] = {
            "successful_runs": len(candidates),
            "median_elapsed_ms": round(statistics.median(elapsed), 3) if elapsed else None,
            "p90_elapsed_ms": percentile(elapsed, 0.90),
            "median_input_tokens": round(statistics.median(tokens), 3) if tokens else None,
        }
    a = summary["inline"]["median_elapsed_ms"]
    b = summary["persistent"]["median_elapsed_ms"]
    summary["persistent_latency_improvement_percent"] = round((a - b) / a * 100, 2) if a and b else None
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="Full /api/investigate URL")
    parser.add_argument("--question", required=True)
    parser.add_argument("--locale", choices=("he", "en"), default="he")
    parser.add_argument("--pairs", type=int, default=12)
    parser.add_argument("--timeout", type=float, default=360)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    if args.pairs < 2:
        parser.error("--pairs must be at least 2 so cold and warm results can be separated")

    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for pair in range(args.pairs):
        order = MODES if pair % 2 == 0 else tuple(reversed(MODES))
        for mode in order:
            row: dict[str, Any] = {"pair": pair + 1, "mode": mode, "cold": mode not in seen}
            seen.add(mode)
            payload = {
                "prompt": args.question,
                "routing_prompt": args.question,
                "locale": args.locale,
                "history": [],
                "investigation_id": f"instruction-ab-{mode}-{uuid.uuid4().hex[:20]}",
                "instruction_mode": mode,
            }
            try:
                result, elapsed_ms = post_json(args.url, payload, args.timeout)
                usage = result.get("usage") or {}
                row.update({
                    "ok": True,
                    "elapsed_ms": elapsed_ms,
                    "run_id": result.get("run_id"),
                    "performance_log": result.get("performance_log"),
                    "input_tokens": usage.get("input_tokens"),
                    "output_tokens": usage.get("output_tokens"),
                    "tool_sequence": [step.get("tool") for step in result.get("investigation_steps") or []],
                    "instruction_experiment": result.get("instruction_experiment"),
                    "answer": result.get("answer"),
                })
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                row.update({"ok": False, "error": str(exc)})
            rows.append(row)
            print(json.dumps({key: row.get(key) for key in ("pair", "mode", "cold", "ok", "elapsed_ms", "input_tokens")}, ensure_ascii=False), flush=True)

    report = {
        "schema_version": 1,
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "url": args.url,
        "question": args.question,
        "locale": args.locale,
        "pairs": args.pairs,
        "summary_warm": summarize(rows, warm_only=True),
        "summary_all": summarize(rows, warm_only=False),
        "runs": rows,
    }
    output = args.output or Path("test_runs") / f"instruction_ab_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(output.resolve()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
