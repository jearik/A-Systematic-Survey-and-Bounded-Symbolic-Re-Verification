#!/usr/bin/env python3
"""Regenerate the public package SHA-256 manifest deterministically."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST_SHA256.csv"


def main() -> None:
    files = sorted(
        (
            path
            for path in ROOT.rglob("*")
            if path.is_file()
            and path != MANIFEST
            and ".git" not in path.relative_to(ROOT).parts
            and "__pycache__" not in path.relative_to(ROOT).parts
        ),
        key=lambda path: path.relative_to(ROOT).as_posix(),
    )
    with MANIFEST.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["path", "bytes", "sha256"])
        writer.writeheader()
        for path in files:
            data = path.read_bytes()
            writer.writerow(
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                }
            )
    print(f"PASS: wrote {len(files)} manifest entries")


if __name__ == "__main__":
    main()
