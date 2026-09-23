#!/usr/bin/env python3
"""Build a scenario search cache offline, using the same Python/NumPy engine as the VM.

Run on a development machine with sufficient memory, never on the 1 GB demo VM.
Only install caches from a trusted build: Python pickle is executable content.
"""
import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", choices=["kosovo", "syria"])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--engine", choices=["python", "numpy"], default="python")
    args = parser.parse_args()
    os.environ["INTELLIGENCE_POC_SCENARIO"] = args.scenario
    # Importing stores must not create state in the working tree.
    with tempfile.TemporaryDirectory() as state:
        os.environ["INTELLIGENCE_POC_STATE_ROOT"] = state
        import mcp_server.server as server
        import semantic_index
        if args.engine == "python":
            semantic_index.np = None
        elif semantic_index.np is None:
            parser.error("NumPy is not installed for the requested engine")
        index = semantic_index.SemanticEventIndex(
            [server.public_event(event) for event in server.EVENTS],
            cache_dir=args.output, signature=server.semantic_index_signature(),
            backend=server.SEMANTIC_BACKEND,
        )
        path = index._cache_path()
        metadata = {"manifest": index.manifest, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        path.with_suffix(".json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        print(json.dumps({"cache": str(path), **metadata}, indent=2))


if __name__ == "__main__":
    main()
