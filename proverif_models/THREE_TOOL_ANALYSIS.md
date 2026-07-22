# Superseded Three-Tool Interpretation

The earlier cross-tool interpretation at this compatibility path is withdrawn.
Raw executions are retained for provenance, but the inputs and claims are not
semantically equivalent across ProVerif, Tamarin, and Scyther.

Current paper-facing status:

- M1 ProVerif is PARTIAL: completion, secrecy, and responder injective
  agreement pass; initiator injective agreement times out at 120 seconds.
- M2-M6 ProVerif files are illustrative encoded-claim skeletons.
- All M1-M6 Tamarin and Scyther files are illustrative tool-specific
  executions, not cross-tool replications.
- The M3 Tamarin lemma named `pfs_after_kgc_reveal` protects a fresh session
  atom independent of the revealed KGC material and is not a valid PFS test.
- AVISPA was not executed locally.

Use `MODEL_SCOPE_AND_CORRECTION_NOTICE.md` and
`supplement_S3_logs/S3_MODEL_VALIDITY_STATUS.csv` as the authoritative sources.
No solver-runtime ordering, family validation, or cross-tool vote is claimed.
