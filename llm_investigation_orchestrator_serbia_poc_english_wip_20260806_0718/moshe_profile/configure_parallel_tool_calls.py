#!/usr/bin/env python3
"""Teach the shared Hermes Codex transport to honor a per-profile environment flag."""

from __future__ import annotations

import argparse
from pathlib import Path


OLD_IMPORT = "from typing import Any, Dict, List, Optional"
NEW_IMPORT = "import os\n\nfrom typing import Any, Dict, List, Optional"
OLD_ASSIGNMENT = 'kwargs["parallel_tool_calls"] = True'
NEW_ASSIGNMENT = (
    'kwargs["parallel_tool_calls"] = '
    'os.environ.get("HERMES_PARALLEL_TOOL_CALLS", "true").strip().lower() '
    'not in {"0", "false", "no", "off"}'
)


def configure(path: Path) -> bool:
    source = path.read_text(encoding="utf-8")
    if NEW_ASSIGNMENT in source:
        return False
    if OLD_ASSIGNMENT not in source:
        raise ValueError("Hermes Codex transport assignment was not found")
    if "import os" not in source:
        if OLD_IMPORT not in source:
            raise ValueError("Hermes Codex transport import anchor was not found")
        source = source.replace(OLD_IMPORT, NEW_IMPORT, 1)
    source = source.replace(OLD_ASSIGNMENT, NEW_ASSIGNMENT, 1)
    path.write_text(source, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("transport", type=Path)
    args = parser.parse_args()
    configure(args.transport.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
