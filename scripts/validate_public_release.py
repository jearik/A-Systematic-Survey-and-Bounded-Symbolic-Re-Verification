#!/usr/bin/env python3
"""Validate public-release integrity and core study invariants."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import struct
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def rows(rel: str) -> list[dict[str, str]]:
    with (ROOT / rel).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def png_dimensions(rel: str) -> tuple[int, int]:
    data = (ROOT / rel).read_bytes()
    check(data[:8] == b"\x89PNG\r\n\x1a\n", f"Not a PNG file: {rel}")
    return struct.unpack(">II", data[16:24])


def normalized_title(value: str) -> str:
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "", ascii_value.casefold())


def title_similarity(left: str, right: str) -> float:
    return SequenceMatcher(None, normalized_title(left), normalized_title(right)).ratio()


def expected_venue_tier(ledger_row: dict[str, str]) -> str:
    publication_type = ledger_row["publication_type"]
    if publication_type == "proceedings-article":
        return "conference / proceedings"
    check(publication_type == "journal-article", f"Unexpected publication type: {publication_type}")
    is_ieee = (
        ledger_row["publisher"].casefold() == "ieee"
        or ledger_row["venue"].casefold().startswith("ieee ")
    )
    return "IEEE transaction / flagship journal" if is_ieee else "other journal"


def main() -> None:
    s1 = rows("data/S1_ROWLEVEL_CODING_INCLUDED_108.csv")
    s2 = rows("data/S2_SCREENING_LEDGER_ALL_131.csv")
    s7 = rows("data/S7_CORPUS_MANIFEST_ALL_131.csv")
    s8 = rows("data/S8_EVIDENCE_APPRAISAL_INCLUDED_108.csv")
    s10 = rows("data/S10_IIOT_CONTEXT_MATRIX_INCLUDED_108.csv")
    mapping = rows("scripts/paperid_ref_mapping_included_108.csv")
    master = rows("validation/20260726_V105_MASTER_INCLUDED_108_VALIDATED.csv")
    check(len(s1) == 108, f"S1 row count is {len(s1)}, expected 108")
    check(len(s2) == 131, f"S2 row count is {len(s2)}, expected 131")
    check(len(s7) == 131, f"S7 row count is {len(s7)}, expected 131")
    check(len(s8) == 108, f"S8 row count is {len(s8)}, expected 108")
    check(len(s10) == 108, f"S10 row count is {len(s10)}, expected 108")
    check(len(mapping) == 108, f"Mapping row count is {len(mapping)}, expected 108")
    check(len(master) == 108, f"Master row count is {len(master)}, expected 108")
    ids = [row["paper_id"] for row in s1]
    check(len(ids) == len(set(ids)), "S1 paper_id is not unique")
    id_set = set(ids)
    check(id_set.issubset({row["paper_id"] for row in s2}), "S1 contains IDs absent from S2")
    check(id_set.issubset({row["paper_id"] for row in s7}), "S1 contains IDs absent from S7")
    check(id_set == {row["paper_id"] for row in s8}, "S8 IDs do not exactly match S1")
    check(id_set == {row["paper_id"] for row in s10}, "S10 IDs do not exactly match S1")
    check(id_set == {row["paper_id"] for row in mapping}, "Mapping IDs do not exactly match S1")
    check(id_set == {row["paper_id"] for row in master}, "Master IDs do not exactly match S1")
    check("P207" not in set(ids), "P207 remains in the primary corpus")
    p207_s2 = next(row for row in s2 if row["paper_id"] == "P207")
    check(p207_s2["screening_decision_v15_3E"] == "exclude_out_of_scope_full_text", "P207 screening decision is incorrect")
    check(p207_s2["primary_denominator_contribution"] == "0", "P207 still contributes to the denominator")
    check(s2 == s7, "S2 and S7 are not identical")
    s2_by_id = {row["paper_id"]: row for row in s2}
    s8_by_id = {row["paper_id"]: row for row in s8}
    s10_by_id = {row["paper_id"]: row for row in s10}
    mapping_by_id = {row["paper_id"]: row for row in mapping}
    master_by_id = {row["paper_id"]: row for row in master}
    for row in s1:
        paper_id = row["paper_id"]
        ledger_row = s2_by_id[paper_id]
        check(
            row["doi"].casefold() == ledger_row["doi"].casefold(),
            f"{paper_id} DOI differs between S1 and S2/S7",
        )
        check(
            row["venue_tier"] == expected_venue_tier(ledger_row),
            f"{paper_id} venue tier differs between S1 and S2/S7 publication type",
        )
        check(
            row["year"] == ledger_row["publication_year"],
            f"{paper_id} first-online publication year differs between S1 and S2/S7",
        )
        expected_year_group = "2021-2023" if int(row["year"]) <= 2023 else "2024-2026"
        check(
            row["year_group"] == expected_year_group,
            f"{paper_id} year_group is inconsistent with the first-online year",
        )
        for dataset_name, other in (
            ("S2/S7", ledger_row),
            ("S8", s8_by_id[paper_id]),
            ("S10", s10_by_id[paper_id]),
            ("mapping", mapping_by_id[paper_id]),
            ("master", master_by_id[paper_id]),
        ):
            check(
                title_similarity(row["title"], other["title"]) >= 0.98,
                f"{paper_id} title identity differs between S1 and {dataset_name}",
            )
        for dataset_name, other in (
            ("S8", s8_by_id[paper_id]),
            ("S10", s10_by_id[paper_id]),
            ("mapping", mapping_by_id[paper_id]),
        ):
            check(
                row["ref_number"] == other["ref_number"],
                f"{paper_id} ref_number differs between S1 and {dataset_name}",
            )
        check(
            row["mechanism_family"] == s8_by_id[paper_id]["mechanism_family"]
            == s10_by_id[paper_id]["primary_family"]
            == mapping_by_id[paper_id]["mechanism_family"]
            == master_by_id[paper_id]["mechanism_family"],
            f"{paper_id} mechanism family is not synchronized",
        )
        check(
            row["doi"].casefold() == mapping_by_id[paper_id]["doi"].casefold()
            == master_by_id[paper_id]["doi"].casefold(),
            f"{paper_id} DOI is not synchronized with mapping/master",
        )
    expected_titles = {
        "P176": "Blockchain-Empowered Decentralized Horizontal Federated Learning for 5G-Enabled UAVs",
        "P122": "LCC-AKA: Lightweight Certificateless Cross-Domain Authentication Key Agreement Protocol for IoT Devices",
        "P178": "BP-AKAA: Blockchain-enforced Privacy-preserving Authentication and Key Agreement and Access Control for IIoT",
        "P190": "Dynamic Authentication and Granularized Authorization With a Cross-Domain Zero Trust Architecture in Large-Scale IoT Networks",
        "P198": "Endogenous Security Formal Definition, Innovation Mechanisms, and Experiment Research in Industrial Internet",
    }
    by_id = {row["paper_id"]: row for row in s1}
    check(all(by_id[key]["title"] == value for key, value in expected_titles.items()), "Public bibliographic title corrections are missing")
    for dataset_name, dataset in (("S2", s2), ("S7", s7), ("S8", s8), ("S10", s10)):
        dataset_by_id = {row["paper_id"]: row for row in dataset}
        check(
            dataset_by_id["P178"]["title"] == expected_titles["P178"],
            f"P178 title is not synchronized in {dataset_name}",
        )
    confirmed = {"P195", "P158", "P139", "P178"}
    check(
        all("borderline_review_needed" not in s8_by_id[key]["uncertain_reason"] for key in confirmed),
        "A confirmed inclusion still carries a borderline flag in S8",
    )
    check(
        all(s10_by_id[key]["relevance_status"] == "include_primary" for key in confirmed),
        "A confirmed inclusion is not marked include_primary in S10",
    )

    levels = Counter(row["verification_level"] for row in s1)
    expected_levels = {"A": 21, "B": 30, "C": 10, "D": 20, "E": 27}
    check(dict(levels) == expected_levels, f"Evidence totals differ: {dict(levels)}")
    families = Counter(row["mechanism_family"] for row in s1)
    check(sorted(families.values(), reverse=True) == [56, 15, 10, 9, 7, 6, 5], f"Family totals differ: {families}")
    venues = Counter(row["venue_tier"] for row in s1)
    check(sorted(venues.values(), reverse=True) == [53, 37, 18], f"Venue totals differ: {venues}")

    summary = json.loads((ROOT / "validation/20260726_V105_FINAL_STATISTICAL_SUMMARY.json").read_text(encoding="utf-8-sig"))
    check(summary["primary_n"] == 108 and summary["screening_n"] == 131, "Final JSON denominators are incorrect")
    check(
        summary["publication_year_convention"]
        == "year of first peer-reviewed online publication, including early-access publication",
        "Final JSON publication-year convention is missing or incorrect",
    )
    check(summary["verification_counts"] == expected_levels, "Final JSON evidence totals differ from S1")
    check(summary["family_counts"] == dict(families), "Final JSON family totals differ from S1")
    check(summary["property_counts"] == {
        "Anonymity": 91,
        "Replay resistance": 76,
        "Revocation": 75,
        "Mutual authentication": 68,
        "Session-key secrecy": 62,
        "MITM resistance": 60,
        "Impersonation resistance": 46,
        "Unlinkability": 41,
        "Perfect forward secrecy": 31,
        "Key-compromise impersonation": 1,
    }, "Final JSON property totals are incorrect")
    check(summary["facet_counts"] == {
        "ledger-present": 100,
        "privacy/anonymity-layer": 64,
        "edge/fog-mediated": 35,
        "multi-ledger": 18,
        "no-ledger": 8,
    }, "Final JSON facet totals are incorrect")
    expected_year_group_matrix = {
        "2021-2023": [5, 7, 3, 9, 16],
        "2024-2026": [16, 23, 7, 11, 11],
    }
    check(
        summary["year_group_matrix"] == expected_year_group_matrix,
        "Final JSON year-group matrix is incorrect",
    )
    year_table = rows("data/S4_VERIFICATION_BY_YEAR_GROUP_CORRECTED.csv")
    check(
        [
            [int(row[level]) for level in "ABCDE"]
            for row in year_table
            if row["year_group"] != "Total"
        ]
        == list(expected_year_group_matrix.values()),
        "S4 year-group table differs from the final year convention",
    )

    legacy_primary = list(ROOT.glob("data/*109*.csv")) + list(ROOT.glob("validation/*109*.csv"))
    check(not legacy_primary, f"Legacy 109-study primary files remain: {[p.name for p in legacy_primary]}")

    required_figures = [
        "figures/fig3_prisma_flow.pdf",
        "figures/fig3_prisma_flow.png",
        "figures/fig3_prisma_flow.svg",
        "figures/20260726_fig3_prisma_108_corrected.png",
        "figures/image4.png",
        "figures/20260726_fig4_taxonomy_3D_108_corrected.png",
        "figures/regenerated/figure3_prisma_108_corrected.pdf",
        "figures/regenerated/figure3_prisma_108_corrected.png",
        "figures/regenerated/figure3_prisma_108_corrected.svg",
        "figures/regenerated/figure3_prisma_108_corrected_source.csv",
        "figures/regenerated/figure4_taxonomy_3D_108_corrected.pdf",
        "figures/regenerated/figure4_taxonomy_3D_108_corrected.png",
        "figures/regenerated/figure4_taxonomy_3D_108_corrected.svg",
        "figures/source/figure4_taxonomy_3D_108_corrected_source.csv",
        "figures/source/figure3_prisma_108_corrected_source.csv",
        "manuscript_figures/exports/fig3_prisma_flow.pdf",
        "manuscript_figures/exports/fig3_prisma_flow.svg",
        "manuscript_figures/exports/image4.pdf",
        "manuscript_figures/exports/image4.svg",
    ]
    check(
        all((ROOT / rel).is_file() for rel in required_figures),
        "A current Fig. 3/Fig. 4 package artifact is missing",
    )
    stale_figure_names = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "figures").rglob("*")
        if path.is_file()
        and (
            "109" in path.name
            or "_sci" in path.name
            or path.name == "image3.png"
        )
    ]
    check(not stale_figure_names, f"Legacy figure artifacts remain: {stale_figure_names}")
    check(
        png_dimensions("figures/20260726_fig3_prisma_108_corrected.png") == (2014, 2565),
        "Canonical Fig. 3 PNG size is not 2014x2565",
    )
    check(png_dimensions("figures/image4.png") == (1050, 2475), "Restored Fig. 4 PNG size is not 1050x2475")
    identical_alias_groups = [
        [
            "figures/fig3_prisma_flow.png",
            "figures/20260726_fig3_prisma_108_corrected.png",
            "figures/regenerated/figure3_prisma_108_corrected.png",
        ],
        [
            "figures/fig3_prisma_flow.pdf",
            "figures/regenerated/figure3_prisma_108_corrected.pdf",
            "manuscript_figures/exports/fig3_prisma_flow.pdf",
        ],
        [
            "figures/fig3_prisma_flow.svg",
            "figures/regenerated/figure3_prisma_108_corrected.svg",
            "manuscript_figures/exports/fig3_prisma_flow.svg",
        ],
        [
            "figures/source/figure3_prisma_108_corrected_source.csv",
            "figures/regenerated/figure3_prisma_108_corrected_source.csv",
            "manuscript_figures/data/fig3_selection_counts.csv",
        ],
        [
            "figures/20260726_fig4_taxonomy_3D_108_corrected.png",
            "figures/regenerated/figure4_taxonomy_3D_108_corrected.png",
        ],
        [
            "figures/source/figure4_taxonomy_3D_108_corrected_source.csv",
            "figures/regenerated/figure4_taxonomy_3D_108_corrected_source.csv",
        ],
    ]
    for group in identical_alias_groups:
        hashes = {hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() for rel in group}
        check(len(hashes) == 1, f"Figure aliases are not synchronized: {group}")

    manifest_rows = rows("MANIFEST_SHA256.csv")
    manifest = {row["path"]: row for row in manifest_rows}
    actual = {
        p.relative_to(ROOT).as_posix()
        for p in ROOT.rglob("*")
        if p.is_file()
        and p.name != "MANIFEST_SHA256.csv"
        and ".git" not in p.relative_to(ROOT).parts
        and "__pycache__" not in p.relative_to(ROOT).parts
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
            or "__pycache__" in path.relative_to(ROOT).parts
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
