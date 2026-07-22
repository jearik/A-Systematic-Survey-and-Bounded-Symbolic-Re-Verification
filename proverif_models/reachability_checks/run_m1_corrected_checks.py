#!/usr/bin/env python3
"""Run separable M1 v15.3F checks with ProVerif 2.05.

The original combined query can spend most of its time on one correspondence.
This runner creates query-specific copies from the corrected authoritative M1
source, records raw stdout/stderr, and reports timeout separately from PASS.
"""

from __future__ import annotations

import csv
import os
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = ROOT / "M1_certificate_based_ECDHE.pv"
PROVERIF = Path(os.path.expanduser("~/.opam/default/bin/proverif"))

QUERY_BLOCK = re.compile(
    r"query attacker\(secretA\);\s*attacker\(secretB\)\.\s*"
    r"query a: pkey, b: pkey, k: bitstring;\s*"
    r"inj-event\(respAccept\(a, b, k\)\) ==> inj-event\(initRunning\(a, b, k\)\)\.\s*"
    r"query a: pkey, b: pkey, k: bitstring;\s*"
    r"inj-event\(initAccept\(a, b, k\)\) ==> inj-event\(respRunning\(a, b, k\)\)\.",
    re.MULTILINE,
)

VARIANTS = {
    "secrecy": (
        "query attacker(secretA);\n      attacker(secretB).",
        60,
        [
            "RESULT not attacker(secretA[]) is true.",
            "RESULT not attacker(secretB[]) is true.",
        ],
    ),
    "responder_injective_agreement": (
        "query a: pkey, b: pkey, k: bitstring;\n"
        "      inj-event(respAccept(a, b, k)) ==> inj-event(initRunning(a, b, k)).",
        90,
        ["RESULT inj-event(respAccept(a,b,k_2)) ==> inj-event(initRunning(a,b,k_2)) is true."],
    ),
    "initiator_injective_agreement": (
        "query a: pkey, b: pkey, k: bitstring;\n"
        "      inj-event(initAccept(a, b, k)) ==> inj-event(respRunning(a, b, k)).",
        120,
        ["RESULT inj-event(initAccept(a,b,k_2)) ==> inj-event(respRunning(a,b,k_2)) is true."],
    ),
}


def run_one(name: str, source: Path, timeout_s: int, expected: list[str]) -> dict[str, str | int]:
    log = HERE / f"M1_corrected_{name}_proverif205.log"
    try:
        completed = subprocess.run(
            [str(PROVERIF), str(source)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout_s,
            check=False,
        )
        output = completed.stdout
        exit_code: int | str = completed.returncode
        status = "PASS" if all(line in output for line in expected) else "COMPLETED_WITHOUT_EXPECTED_RESULT"
    except subprocess.TimeoutExpired as exc:
        partial = exc.stdout or b""
        if isinstance(partial, bytes):
            partial = partial.decode("utf-8", errors="replace")
        output = partial + "\nTIMEOUT\n"
        exit_code = "TIMEOUT"
        status = "TIMEOUT"
    log.write_text(output, encoding="utf-8")
    return {
        "check": name,
        "status": status,
        "timeout_s": timeout_s,
        "exit_code": exit_code,
        "source": source.name,
        "log": log.name,
    }


def main() -> None:
    if not PROVERIF.exists():
        raise FileNotFoundError(PROVERIF)
    base = BASE.read_text(encoding="utf-8")
    if len(QUERY_BLOCK.findall(base)) != 1:
        raise RuntimeError("Could not identify exactly one M1 query block")

    rows: list[dict[str, str | int]] = []
    witness = HERE / "M1_honest_completion_witness.pv"
    rows.append(
        run_one(
            "honest_completion_witness",
            witness,
            30,
            ["RESULT not attacker(m1_completed[]) is false."],
        )
    )
    for name, (query, timeout_s, expected) in VARIANTS.items():
        variant = HERE / f"M1_corrected_{name}.pv"
        variant.write_text(QUERY_BLOCK.sub(query, base), encoding="utf-8")
        rows.append(run_one(name, variant, timeout_s, expected))

    with (HERE / "M1_CORRECTED_CHECK_STATUS.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
