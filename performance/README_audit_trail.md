# Performance evidence boundary

## Identifier namespace

The manuscript's performance P1 is canonically identified in this archive as
**Perf-P1**. This namespace is separate from the bounded published-protocol
cases C1=CCAP, C2=CL-BASA, and C3=BCAE.

## Paper-facing measured data

The authoritative desktop benchmark is:

- results/bench_30_rounds_raw.csv: 750 raw outer-round rows.
- results/bench_30_rounds_summary.csv, .json, and .md: 30-round summaries.
- scripts/bench_30_rounds.py: rerun script.

The archived metadata records Windows 11 and Python 3.12.13. A validated OpenSSL version and embedded hardware platform were not captured. Values are therefore one-host comparisons only.

The hash-path rows repeat SHA-256 operations along a Merkle-style path. They do not execute a blockchain, database, consensus protocol, smart contract, or finality mechanism.

## Analytical inputs

- results/bench_sizes.json contains byte-size inputs used for analytical accounting.
- results/bench_patterns.json contains abstract handshake compositions.
- results/e4_matrix.json contains latency projections over assumed one-way latency and bandwidth profiles.

The network profiles are illustrative assumptions and were not measured in this study. The analytical projections must not be reported as field performance.
