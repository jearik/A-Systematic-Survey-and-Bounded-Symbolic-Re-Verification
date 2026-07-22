# Superseded Experimental-Evidence Note

This compatibility path replaces an earlier interpretation that is withdrawn.
It is not an authoritative result summary.

The authoritative model status is in
`MODEL_SCOPE_AND_CORRECTION_NOTICE.md` and
`supplement_S3_logs/S3_MODEL_VALIDITY_STATUS.csv`:

- M1 is **PARTIAL** after the transcript correction: honest completion,
  secrecy, and responder injective agreement pass; initiator injective
  agreement timed out at 120 seconds.
- M2-M6 ProVerif files and every Tamarin/Scyther family file are
  **ILLUSTRATIVE** tool-specific executions. They are not semantic cross-tool
  translations and support no family-wide or algorithm-level conclusion.
- AVISPA source files are retained as literature-context ports; no local
  backend result is counted.

Files under the legacy `ablation_models/` and `results_ablation/` paths inject
an explicit secret release and/or acceptance-without-run rule. They are
parser/runner sanity checks, not component-removal ablations. Their detection
labels and runtimes support no causal component claim, false-positive rate,
false-negative rate, protocol ranking, or security comparison.

Desktop primitive timings remain one-host measurements. Network values remain
analytical projections under assumed one-way latency and bandwidth profiles.
