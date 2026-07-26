# Public data quality report

## Dataset and grain

- S1: 108 included primary studies, one row per `paper_id`.
- S2 and S7: 131 unique screened reports, one row per `paper_id`.
- Intended use: reproduce descriptive counts, inspect screening/coding
  decisions, trace bounded model evidence, and regenerate manuscript figures.

## Checks performed

- row counts and candidate-key uniqueness;
- exact-row, normalized DOI, and normalized-title duplication;
- required identifier coverage across S1, S2, and S7;
- accepted values and aggregate totals for evidence category, primary family,
  year, venue, facets, and reported security properties;
- cross-file agreement with the final statistical JSON and derived matrices;
- first-online publication-year agreement between S1 and the screening ledger,
  including correct derivation of the two analysis periods;
- explicit verification that P207 contributes zero to the primary denominator;
- missing-value profiling, local-path scanning, and release-manifest validation.

## Findings

1. **Core denominators and aggregates: PASS.** S1 contains 108 unique IDs; S2
   and S7 contain 131. Evidence totals are 21/30/10/20/27, family totals are
   56/15/9/10/7/6/5, and venue totals are 53/37/18.
2. **P207 scope correction: PASS.** P207 is retained in S2/S7 as
   `exclude_out_of_scope_full_text`, contributes zero to the primary
   denominator, and is absent from S1/S8/S10 and all derived aggregates.
3. **Screening-status cleanup: PASS.** P195, P158, P139, and P178 are confirmed
   as included, and obsolete borderline markers were removed.
4. **Bibliographic synchronization: PASS.** The P178 title is synchronized
   across the primary tables, screening ledger, manifest, mapping, and
   validation table.
5. **Publication-year synchronization: PASS.** Publication year is defined as
   the year of first peer-reviewed online publication, including early access.
   P190 is coded as 2025 and P198 as 2023; the resulting period denominators
   are 40 for 2021--2023 and 68 for 2024--2026.
6. **Duplicates and public-release hygiene: PASS.** No duplicate primary IDs,
   unsanitized absolute user paths, or manifest mismatches remain.

## Residual limitations

- The public deposit does not include the original Web of Science/Scopus
  exports or the full 304-record pre-deduplication candidate table.
- Single-reviewer screening/coding remains a methodological limitation;
  automated consistency checks are not an independent reassessment.
- Formal-model outcomes retain their query-specific and encoded-model
  boundaries.

The structural checks reported here were run before release. Their outputs are
retained in `validation/`, and `MANIFEST_SHA256.csv` allows every payload file
to be re-verified independently.
