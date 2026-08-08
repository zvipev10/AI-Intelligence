#!/usr/bin/env python3
"""Administrator-only target-bank backup and reset commands."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from target_bank import DEFAULT_BACKUP_DIRS, DEFAULT_DB_PATHS, TargetBank


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=("initialize", "backup", "counts", "reset", "restore"))
    parser.add_argument("--locale", required=True, choices=("he", "en"))
    parser.add_argument("--db", type=Path)
    parser.add_argument("--backup-dir", type=Path)
    parser.add_argument("--confirm-reset", action="store_true")
    parser.add_argument("--source-backup", type=Path)
    parser.add_argument("--confirm-restore", action="store_true")
    args = parser.parse_args()

    db_path = (args.db or DEFAULT_DB_PATHS[args.locale]).resolve()
    backup_dir = (args.backup_dir or DEFAULT_BACKUP_DIRS[args.locale]).resolve()
    bank = TargetBank(db_path, backup_dir, locale=args.locale)
    if args.operation == "initialize":
        bank.initialize()
        result = {"database": str(bank.db_path), **bank.counts()}
    elif args.operation == "backup":
        result = {"backup": str(bank.backup()), **bank.counts()}
    elif args.operation == "counts":
        result = {"database": str(bank.db_path), **bank.counts()}
    elif args.operation == "reset":
        result = {"backup": str(bank.reset(confirm=args.confirm_reset)), **bank.counts()}
    else:
        if args.source_backup is None:
            parser.error("restore requires --source-backup")
        result = {
            "safety_backup": str(bank.restore(args.source_backup, confirm=args.confirm_restore)),
            "restored_from": str(args.source_backup.resolve()),
            **bank.counts(),
        }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
