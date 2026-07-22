# Supplement S3: Explicit-Fault Parser/Runner Sanity Checks

This folder preserves raw outputs from deliberately unsafe templates. Each
template directly releases a secret and/or permits acceptance without a prior
run. The templates therefore check only that the installed tool and runner
record an obvious seeded fault.

The legacy `ABLATION` tokens in filenames are retained solely for path
compatibility. These files are not one-factor ablations and do not isolate any
certificate, ledger, KGC, pseudonym, PUF, or proof-term component. They support
no causal component claim and no false-positive or false-negative-rate estimate.

## Current files

- `S3_MODEL_VALIDITY_STATUS.csv`: authoritative M1-M6 and bounded-case status.
- `S3_ABLATION_LOG_MANIFEST.csv`: compatibility filename containing seeded
  labels and `EXPLICIT_FAULT_DETECTED` runner outcomes.
- `S3_ABLATION_QUANTITATIVE_ANALYSIS.csv`: compatibility filename containing
  runner timing metadata only.
- `S3_ABLATION_FULL_LOGS.txt` and `.zip`: preserved raw legacy outputs; the ZIP
  includes this same boundary notice and corrected metadata tables.
- `S3_TOOL_METRIC_FRAMEWORK.csv`: current scope and tool-capability boundaries.
- `S3_HANDSHAKE_BYTE_ACCOUNTING.csv`: analytical byte accounting, not packet
  captures or component-removal measurements.
- `S3_SHA256SUMS.csv`: relative paths and current SHA-256 digests for every
  other top-level file in this folder.

The current runner can be invoked with `python3 run_ablation_and_timing.py`.
Its legacy directory names do not change the interpretation above.
