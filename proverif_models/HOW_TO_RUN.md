# Symbolic-Artifact Runner Guide: Current Boundary

Before running any file, read `MODEL_SCOPE_AND_CORRECTION_NOTICE.md` and
`supplement_S3_logs/S3_MODEL_VALIDITY_STATUS.csv`.

The family sources can be executed with `bash run_all_tools.sh`, but generated
aggregate PASS tokens are runner-local outputs, not cross-tool validation. M1
has an authoritative query-specific PARTIAL status; M2-M6 and all
Tamarin/Scyther family files are illustrative. The M3 fresh-session-atom check
does not establish PFS.

For the paper-facing M1 status, use the sources and logs under
`reachability_checks/`. For the three bounded published-protocol diagnostics,
use `run_published_protocols.sh`, `PUBLISHED_PROTOCOL_REVERIFY_SUMMARY.csv`, and
`PUBLISHED_PROTOCOL_TRACEABILITY.md`. Their namespace is C1=CCAP, C2=CL-BASA,
and C3=BCAE.

`run_ablation_and_timing.py` retains legacy path names but generates deliberately
unsafe explicit-fault templates. Those outputs are parser/runner sanity checks,
not component-removal evidence. Do not infer FPR, FNR, causal contribution,
protocol security, or family security from them.
