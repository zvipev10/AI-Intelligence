#!/usr/bin/env python3
"""Run full quality questions against the deployed VM-local UI API.

This script is intended to run on the Hermes VM, where the UI gateway can call
Hermes through direct localhost transport. It avoids the local Codex -> SSH ->
Hermes path used by development scripts.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = ROOT / "docs" / "quality" / "question_catalog_v1.json"
DEFAULT_OUTPUT_DIR = ROOT / "docs" / "quality" / "vm_full_question_runs"
DEFAULT_ENDPOINT = "http://127.0.0.1:8769/api/investigate"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_catalog() -> dict[str, Any]:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def post_json(url: str, payload: dict[str, Any], timeout: int) -> dict[str, Any]:
    encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=encoded,
        headers={"Content-Type": "application/json; charset=utf-8", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8-sig"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc


def select_questions(catalog: dict[str, Any], ids: list[str], run_all: bool) -> list[dict[str, Any]]:
    questions = catalog["full_investigation_questions"]
    if run_all:
        return questions
    wanted = set(ids)
    selected = [question for question in questions if question["id"] in wanted]
    missing = wanted - {question["id"] for question in selected}
    if missing:
        raise ValueError(f"Unknown question IDs: {', '.join(sorted(missing))}")
    return selected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", nargs="*", default=[], help="Question IDs to run")
    parser.add_argument("--all", action="store_true", help="Run all full investigation questions")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--timeout", type=int, default=540)
    args = parser.parse_args()

    if not args.all and not args.ids:
        raise SystemExit("Provide --ids ... or --all")

    catalog = load_catalog()
    questions = select_questions(catalog, args.ids, args.all)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    summaries = []
    for question in questions:
        started = time.perf_counter()
        print(f"RUN_START {question['id']}: {question['question']}", flush=True)
        result = post_json(
            args.endpoint,
            {
                "prompt": question["question"],
                "history": [],
                "investigation_state": {
                    "quality_test_id": question["id"],
                    "quality_catalog_id": catalog["catalog_id"],
                    "runner": "vm_local_ui_api",
                },
                "investigation_id": f"quality-{question['id']}-{int(time.time())}",
            },
            timeout=args.timeout,
        )
        elapsed = round((time.perf_counter() - started) * 1000, 3)
        artifact = {
            "id": question["id"],
            "question": question["question"],
            "recorded_at_utc": utc_now(),
            "elapsed_ms": elapsed,
            "source": "vm_local_ui_api",
            "endpoint": args.endpoint,
            "result": result,
        }
        output_path = args.output_dir / f"{question['id']}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
        output_path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        event_ids = result.get("event_ids") or result.get("answer_event_ids") or []
        summary = {
            "id": question["id"],
            "elapsed_ms": elapsed,
            "run_id": result.get("run_id"),
            "recommended_view": result.get("recommended_view"),
            "event_id_count": len(event_ids),
            "step_count": len(result.get("investigation_steps") or []),
            "output_file": output_path.as_posix(),
        }
        summaries.append(summary)
        print(json.dumps({"RUN_DONE": summary}, ensure_ascii=False), flush=True)

    print(json.dumps({"summary": summaries}, ensure_ascii=False, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
