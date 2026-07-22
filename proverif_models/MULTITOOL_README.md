# Multi-Tool Symbolic Artifact: Current Interpretation

## Authoritative status

Use `MODEL_SCOPE_AND_CORRECTION_NOTICE.md` and
`supplement_S3_logs/S3_MODEL_VALIDITY_STATUS.csv` for every paper-facing
interpretation.

- **M1 / ProVerif: PARTIAL.** The corrected four-field transcript source has
  query-specific results: completion PASS, secrecy PASS, responder injective
  agreement PASS, and initiator injective agreement TIMEOUT at 120 seconds.
- **M2-M6 / ProVerif: ILLUSTRATIVE.** These are encoded-claim skeleton runs,
  not complete proofs of the named mechanism families.
- **M1-M6 / Tamarin and Scyther: ILLUSTRATIVE.** These files use tool-specific
  abstractions and are not translations of the ProVerif messages or claims.
- **AVISPA: NOT EXECUTED.** HLPSL sources are retained for context only.

Accordingly, agreement among runner outputs is not cross-tool security
evidence. In particular, the M3 Tamarin fresh-session-atom lemma is not PFS,
and opaque ledger, pseudonym, PUF, and proof terms do not establish finality,
unlinkability, physical unclonability, or zero knowledge.

## Running the artifacts

`bash run_all_tools.sh` records tool-local execution logs under
`results_multitool/`. The preserved aggregate logs are legacy runner records;
their local PASS tokens must not replace the authoritative status above.

`python3 run_ablation_and_timing.py` regenerates files under legacy path names.
Those generated files inject obvious faults to test parser/runner recording.
They are explicit-fault sanity checks, not one-factor ablations, and their
runtime differences are metadata only.

The bounded published-protocol cases use the separate C1-C3 namespace:
C1=CCAP, C2=CL-BASA, and C3=BCAE. The performance-only composition is
namespaced as Perf-P1 (manuscript short label P1).
