#!/usr/bin/env python3
"""Rebuild MANIFEST_SHA256.csv from the exact public-release payload."""

from __future__ import annotations

import csv
import hashlib

from release_inventory import ROOT, payload_files


def main() -> None:
    destination = ROOT / "MANIFEST_SHA256.csv"
    temporary = destination.with_suffix(".csv.tmp")
    entries = []
    for path in payload_files():
        data = path.read_bytes()
        entries.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("path", "bytes", "sha256"),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(entries)
    temporary.replace(destination)
    print(f"WROTE: {destination}")


if __name__ == "__main__":
    main()
