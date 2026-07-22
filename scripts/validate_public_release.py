#!/usr/bin/env python3
"""Validate public-release integrity and core study invariants."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def rows(rel: str) -> list[dict[str, str]]:
    with (ROOT / rel).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    s1 = rows("data/S1_ROWLEVEL_CODING_INCLUDED_109.csv")
    s2 = rows("data/S2_SCREENING_LEDGER_ALL_131.csv")
    s7 = rows("data/S7_CORPUS_MANIFEST_ALL_131.csv")
    check(len(s1) == 109, f"S1 row count is {len(s1)}, expected 109")
    check(len(s2) == 131, f"S2 row count is {len(s2)}, expected 131")
    check(len(s7) == 131, f"S7 row count is {len(s7)}, expected 131")
    ids = [row["paper_id"] for row in s1]
    check(len(ids) == len(set(ids)), "S1 paper_id is not unique")
    check(set(ids).issubset({row["paper_id"] for row in s2}), "S1 contains IDs absent from S2")
    check(set(ids).issubset({row["paper_id"] for row in s7}), "S1 contains IDs absent from S7")
    expected_titles = {
        "P176": "Blockchain-Empowered Decentralized Horizontal Federated Learning for 5G-Enabled UAVs",
        "P122": "LCC-AKA: Lightweight Certificateless Cross-Domain Authentication Key Agreement Protocol for IoT Devices",
        "P198": "Endogenous Security Formal Definition, Innovation Mechanisms, and Experiment Research in Industrial Internet",
    }
    by_id = {row["paper_id"]: row for row in s1}
    check(all(by_id[key]["title"] == value for key, value in expected_titles.items()), "Public bibliographic title corrections are missing")

    levels = Counter(row["verification_level"] for row in s1)
    expected_levels = {"A": 21, "B": 31, "C": 10, "D": 20, "E": 27}
    check(dict(levels) == expected_levels, f"Evidence totals differ: {dict(levels)}")
    families = Counter(row["mechanism_family"] for row in s1)
    check(sorted(families.values(), reverse=True) == [57, 15, 10, 9, 7, 6, 5], f"Family totals differ: {families}")
    venues = Counter(row["venue_tier"] for row in s1)
    check(sorted(venues.values(), reverse=True) == [54, 37, 18], f"Venue totals differ: {venues}")

    summary = json.loads((ROOT / "validation/20260720_FINAL_STATISTICAL_SUMMARY.json").read_text(encoding="utf-8-sig"))
    check(summary["verification_counts"] == expected_levels, "Final JSON evidence totals differ from S1")

    manifest_rows = rows("MANIFEST_SHA256.csv")
    manifest = {row["path"]: row for row in manifest_rows}
    actual = {
        p.relative_to(ROOT).as_posix()
        for p in ROOT.rglob("*")
        if p.is_file()
        and p.name != "MANIFEST_SHA256.csv"
        and ".git" not in p.relative_to(ROOT).parts
    }
    check(set(manifest) == actual, "Manifest path set does not match repository files")
    for rel, row in manifest.items():
        data = (ROOT / rel).read_bytes()
        check(int(row["bytes"]) == len(data), f"Byte-count mismatch: {rel}")
        check(row["sha256"] == hashlib.sha256(data).hexdigest(), f"SHA-256 mismatch: {rel}")

    forbidden = re.compile(r"(?:[A-Za-z]:\\|/mnt/[a-zA-Z]/|/home/(?:jeari|jearik)/|\buser=(?:jeari|jearik)\b)", re.I)
    findings = []
    for path in ROOT.rglob("*"):
        if (
            not path.is_file()
            or path.name == "MANIFEST_SHA256.csv"
            or ".git" in path.relative_to(ROOT).parts
        ):
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            continue
        if forbidden.search(text):
            findings.append(path.relative_to(ROOT).as_posix())
    check(not findings, f"Unsanitized local paths/usernames remain: {findings[:10]}")
    check(not (ROOT / "proverif_models/install_logs").exists(), "Installation logs must not be public")
    check(not (ROOT / "proverif_models/supplement_S3_logs/S3_ABLATION_FULL_LOGS.zip").exists(), "Nested raw-log ZIP must not be public")
    print("PASS: public-release integrity, denominators, aggregates, and path sanitization")


if __name__ == "__main__":
    main()
