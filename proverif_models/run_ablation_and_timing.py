#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
import os
import re
import shutil
import statistics
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ABL = ROOT / "ablation_models"
OUT = ROOT / "results_ablation"
TIMED = ROOT / "results_timing"

MODELS = [
    ("M1", "certificate_based_ECDHE", "certificate/transcript binding"),
    ("M2", "IBS_blockchain", "consortium-ledger trust anchor"),
    ("M3", "certificateless_AKA", "KGC partial-key binding"),
    ("M4", "blockchain_pseudonym", "pseudonym ledger / sealed identity"),
    ("M5", "PUF_keyestab", "PUF challenge-response"),
    ("M6", "anonymous_ZKP", "ZK credential proof"),
]

BASELINE = [
    ("M1", "ProVerif", ROOT / "M1_certificate_based_ECDHE.pv"),
    ("M2", "ProVerif", ROOT / "M2_IBS_blockchain.pv"),
    ("M3", "ProVerif", ROOT / "M3_certificateless_AKA.pv"),
    ("M4", "ProVerif", ROOT / "M4_blockchain_pseudonym.pv"),
    ("M5", "ProVerif", ROOT / "M5_PUF_keyestab.pv"),
    ("M6", "ProVerif", ROOT / "M6_anonymous_ZKP.pv"),
    ("M1", "Tamarin", ROOT / "tamarin_models" / "M1_certificate_based_ECDHE.spthy"),
    ("M2", "Tamarin", ROOT / "tamarin_models" / "M2_IBS_blockchain.spthy"),
    ("M3", "Tamarin", ROOT / "tamarin_models" / "M3_certificateless_AKA.spthy"),
    ("M4", "Tamarin", ROOT / "tamarin_models" / "M4_blockchain_pseudonym_abstract.spthy"),
    ("M5", "Tamarin", ROOT / "tamarin_models" / "M5_PUF_keyestab_abstract.spthy"),
    ("M6", "Tamarin", ROOT / "tamarin_models" / "M6_anonymous_ZKP_abstract.spthy"),
    ("M1", "Scyther", ROOT / "scyther_models" / "M1_certificate_based_ECDHE.spdl"),
    ("M2", "Scyther", ROOT / "scyther_models" / "M2_IBS_blockchain.spdl"),
    ("M3", "Scyther", ROOT / "scyther_models" / "M3_certificateless_AKA.spdl"),
    ("M4", "Scyther", ROOT / "scyther_models" / "M4_blockchain_pseudonym_abstract.spdl"),
    ("M5", "Scyther", ROOT / "scyther_models" / "M5_PUF_keyestab_abstract.spdl"),
    ("M6", "Scyther", ROOT / "scyther_models" / "M6_anonymous_ZKP_abstract.spdl"),
]


def which(*names: str) -> str | None:
    for n in names:
        p = shutil.which(n)
        if p:
            return p
    return None


def ensure_path() -> None:
    home = Path.home()
    for extra in [home / ".local" / "bin", home / ".opam" / "default" / "bin"]:
        if extra.exists():
            os.environ["PATH"] = str(extra) + os.pathsep + os.environ.get("PATH", "")


def write_generated_models() -> None:
    for d in [ABL / "proverif", ABL / "tamarin", ABL / "scyther"]:
        d.mkdir(parents=True, exist_ok=True)

    pv_template = """(* Seeded parser sanity check labelled {model}: {component}.
   This is intentionally unsafe and is NOT an ablation of the {model}
   baseline. It only checks that the runner/parser records an explicit
   secrecy and correspondence failure. *)
free net: channel.
type id.
const devA: id.
const devB: id.
free compromised_secret: bitstring [private].
event expectedRun(id,id).
event accept(id,id).

query attacker(compromised_secret).
query a:id,b:id; event(accept(a,b)) ==> event(expectedRun(a,b)).

process
  out(net, compromised_secret);
  event accept(devA, devB)
"""

    tamarin_template = """theory {theory}
begin

/* Seeded parser sanity check labelled {model}: {component}.
   This is NOT an ablation of the {model} baseline. The single rule releases
   the secret and accepts without a run event so that the runner/parser has
   an explicit failure to detect. */

rule Removed_Module_Attack:
  [ Fr(~k) ]
  --[ Accept('devA','devB',~k), Secret(~k) ]->
  [ Out(~k) ]

lemma secrecy_after_ablation:
  "All k #i. Secret(k) @ i ==> not (Ex #j. K(k) @ j)"

lemma agreement_after_ablation:
  "All k #i.
     Accept('devA','devB',k) @ i
     ==> (Ex #j. Run('devB','devA',k) @ j & j < i)"

end
"""

    scyther_template = """// Seeded parser sanity check labelled {model}: {component}.
// This is NOT an ablation of the {model} baseline. Public values intentionally
// make the claimed secret and synchronization goals fail.

hashfunction H;

protocol {proto}(A,B)
{{
  role A
  {{
    fresh na: Nonce;
    var nb: Nonce;
    send_1(A,B, na);
    recv_2(B,A, nb);
    claim(A, Secret, H(na,nb));
    claim(A, Niagree);
    claim(A, Nisynch);
  }}

  role B
  {{
    var na: Nonce;
    fresh nb: Nonce;
    recv_1(A,B, na);
    send_2(B,A, nb);
    claim(B, Secret, H(na,nb));
    claim(B, Niagree);
    claim(B, Nisynch);
  }}
}}
"""

    for model, family, component in MODELS:
        safe = f"{model}_{family}_remove_module"
        (ABL / "proverif" / f"{safe}.pv").write_text(
            pv_template.format(model=model, component=component),
            encoding="utf-8",
        )
        (ABL / "tamarin" / f"{safe}.spthy").write_text(
            tamarin_template.format(theory=safe, model=model, component=component),
            encoding="utf-8",
        )
        (ABL / "scyther" / f"{safe}.spdl").write_text(
            scyther_template.format(
                model=model,
                component=component,
                proto=f"{model}{family}RemoveModule".replace("_", ""),
            ),
            encoding="utf-8",
        )


def run_cmd(cmd: list[str], timeout: int = 180) -> tuple[int, float, str]:
    t0 = time.perf_counter()
    p = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )
    return p.returncode, time.perf_counter() - t0, p.stdout


def classify(tool: str, text: str, code: int) -> str:
    low = text.lower()
    if tool == "ProVerif":
        if "is false" in low or re.search(r"attacker\\([^\\n]+\\) is true", low):
            return "ATTACK"
        if "cannot be proved" in low:
            return "INCONCLUSIVE"
        if "is true" in low and code == 0:
            return "PASS"
    if tool == "Tamarin":
        if "falsified" in low:
            return "ATTACK"
        if "verified" in low and code == 0:
            return "PASS"
        if "analysis incomplete" in low:
            return "INCONCLUSIVE"
    if tool == "Scyther":
        if "\x1b[31mfail" in low or "fail" in low or "attack" in low:
            return "ATTACK"
        if "\x1b[32mok" in low or "proof of correctness" in low or "\tok\t" in low:
            return "PASS"
    if code != 0:
        return "ERROR"
    return "INCONCLUSIVE"


def extract_claims(tool: str, text: str) -> str:
    if tool == "ProVerif":
        lines = [ln.strip() for ln in text.splitlines() if "RESULT" in ln or "Query" in ln]
        return " | ".join(lines[:6])
    if tool == "Tamarin":
        lines = [
            ln.strip()
            for ln in text.splitlines()
            if any(k in ln.lower() for k in ["verified", "falsified", "lemma", "summary"])
        ]
        return " | ".join(lines[-8:])
    if tool == "Scyther":
        lines = [ln.strip() for ln in text.splitlines() if "claim" in ln.lower()]
        return " | ".join(lines[:8])
    return ""


def run_ablations() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ensure_path()
    pv = which("proverif")
    tam = which("tamarin-prover", "tamarin")
    scy = which("scyther", "scyther-linux")
    tools = {"ProVerif": pv, "Tamarin": tam, "Scyther": scy}

    rows = []
    for model, family, component in MODELS:
        safe = f"{model}_{family}_remove_module"
        specs = [
            ("ProVerif", ABL / "proverif" / f"{safe}.pv"),
            ("Tamarin", ABL / "tamarin" / f"{safe}.spthy"),
            ("Scyther", ABL / "scyther" / f"{safe}.spdl"),
        ]
        for tool, path in specs:
            exe = tools[tool]
            log_path = OUT / f"{tool.lower()}_{safe}.txt"
            if not exe:
                log_path.write_text("SKIP: tool not found\n", encoding="utf-8")
                rows.append([model, component, tool, "SKIP", "", "", str(log_path)])
                continue
            cmd = [exe, str(path)]
            if tool == "Tamarin":
                cmd.append("--prove")
            code, elapsed, text = run_cmd(cmd)
            log_path.write_text(text, encoding="utf-8", errors="replace")
            rows.append(
                [
                    model,
                    component,
                    tool,
                    classify(tool, text, code),
                    f"{elapsed:.4f}",
                    extract_claims(tool, text),
                    str(log_path),
                ]
            )

    csv_path = OUT / "ABLATION_SUMMARY.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["model", "seeded_label", "tool", "runner_detection", "elapsed_s", "evidence_excerpt", "log"])
        w.writerows(rows)

    md_path = OUT / "ABLATION_SUMMARY.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Explicit-Fault Parser/Runner Sanity-Check Summary (legacy path)\n\n")
        f.write("Each template directly injects an obvious fault. Detection checks parser/runner recording only; it is not component-removal evidence.\n\n")
        f.write("| Model | Seeded label | ProVerif | Tamarin | Scyther |\n")
        f.write("|---|---|---:|---:|---:|\n")
        for model, family, component in MODELS:
            sub = [r for r in rows if r[0] == model]
            by_tool = {r[2]: f"{r[3]} ({r[4]} s)" for r in sub}
            f.write(f"| {model} | {component} | {by_tool.get('ProVerif','SKIP')} | {by_tool.get('Tamarin','SKIP')} | {by_tool.get('Scyther','SKIP')} |\n")


def run_timing(repeats: int = 10) -> None:
    TIMED.mkdir(parents=True, exist_ok=True)
    ensure_path()
    pv = which("proverif")
    tam = which("tamarin-prover", "tamarin")
    scy = which("scyther", "scyther-linux")
    exe = {"ProVerif": pv, "Tamarin": tam, "Scyther": scy}
    props = {
        "ProVerif": "secrecy; injective correspondence; identity non-derivability where encoded",
        "Tamarin": "trace secrecy; agreement; explicit reveal/compromise lemmas where encoded",
        "Scyther": "Secret; Alive; Weakagree; Niagree; Nisynch",
    }
    rows = []
    raw = []
    for model, tool, path in BASELINE:
        if not exe[tool]:
            rows.append([model, tool, "SKIP", "", "", "", props[tool]])
            continue
        times = []
        statuses = []
        for rep in range(1, repeats + 1):
            cmd = [exe[tool], str(path)]
            if tool == "Tamarin":
                cmd.append("--prove")
            code, elapsed, text = run_cmd(cmd)
            status = classify(tool, text, code)
            times.append(elapsed)
            statuses.append(status)
            (TIMED / f"{tool.lower()}_{model}_rep{rep:02d}.txt").write_text(
                text,
                encoding="utf-8",
                errors="replace",
            )
            raw.append([model, tool, rep, status, f"{elapsed:.6f}"])
        rows.append(
            [
                model,
                tool,
                ";".join(sorted(set(statuses))),
                f"{statistics.mean(times):.4f}",
                f"{statistics.stdev(times):.4f}" if len(times) > 1 else "0.0000",
                repeats,
                props[tool],
            ]
        )

    with (TIMED / "THREE_TOOL_TIMING_RAW.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["model", "tool", "replicate", "status", "elapsed_s"])
        w.writerows(raw)

    with (TIMED / "THREE_TOOL_TIMING_SUMMARY.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["model", "tool", "status_set", "mean_elapsed_s", "std_elapsed_s", "repeats", "supported_properties"])
        w.writerows(rows)

    with (TIMED / "THREE_TOOL_TIMING_SUMMARY.md").open("w", encoding="utf-8") as f:
        f.write("# Three-Tool Timing Summary\n\n")
        f.write(f"Repeated runs per executable model/tool pair: {repeats}.\n\n")
        f.write("| Model | Tool | Status | Mean s | Std s | Supported properties |\n")
        f.write("|---|---|---:|---:|---:|---|\n")
        for r in rows:
            f.write(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[6]} |\n")


def main() -> None:
    write_generated_models()
    run_ablations()
    run_timing(repeats=10)
    print(f"explicit_fault_summary={OUT / 'ABLATION_SUMMARY.csv'}")
    print(f"timing_summary={TIMED / 'THREE_TOOL_TIMING_SUMMARY.csv'}")


if __name__ == "__main__":
    main()
