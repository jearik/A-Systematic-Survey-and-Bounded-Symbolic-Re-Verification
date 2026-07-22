#!/usr/bin/env python3
"""Validate final v17.1 supplementary evidence, family, year, and venue counts."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S1 = ROOT / "data" / "S1_ROWLEVEL_CODING_INCLUDED_109.csv"
LEVELS = "ABCDE"
EXPECTED_LEVELS = {"A": 21, "B": 31, "C": 10, "D": 20, "E": 27}
EXPECTED_FAMILIES = {
    "Ledger-mediated trust": [12, 11, 8, 8, 18],
    "Certificateless split-key": [2, 6, 1, 3, 3],
    "Zero-knowledge/privacy credential": [1, 3, 0, 4, 1],
    "Other/classical-general": [1, 4, 0, 3, 2],
    "Hardware-/device-rooted": [5, 0, 0, 1, 1],
    "Group-/ring-signature": [0, 4, 0, 0, 2],
    "Post-quantum": [0, 3, 1, 1, 0],
}
EXPECTED_YEAR_GROUP = {
    "2021-2023": [5, 8, 3, 8, 16],
    "2024-2026": [16, 23, 7, 12, 11],
}
EXPECTED_VENUE = {
    "IEEE transaction / flagship journal": [13, 15, 6, 10, 10],
    "other journal": [6, 13, 2, 8, 8],
    "conference / proceedings": [2, 3, 2, 2, 9],
}


def matrix(rows, field, keys):
    return {
        key: [sum(row[field] == key and row["verification_level"] == level for row in rows) for level in LEVELS]
        for key in keys
    }


def main():
    with S1.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 109
    assert len({row["paper_id"] for row in rows}) == 109
    assert dict(Counter(row["verification_level"] for row in rows)) == EXPECTED_LEVELS
    assert matrix(rows, "mechanism_family", EXPECTED_FAMILIES) == EXPECTED_FAMILIES
    assert matrix(rows, "year_group", EXPECTED_YEAR_GROUP) == EXPECTED_YEAR_GROUP
    assert matrix(rows, "venue_tier", EXPECTED_VENUE) == EXPECTED_VENUE
    print("PASS: final v17.1 row-level and aggregate invariants")


if __name__ == "__main__":
    main()
