# Public data quality report

## Dataset and grain

- S1: 109 included primary studies, one row per `paper_id`.
- S2 and S7: 131 unique screened reports, one row per `paper_id`.
- Intended use: reproduce descriptive counts, inspect screening/coding decisions, trace bounded model evidence, and regenerate manuscript figures.

## Checks performed

- row counts and candidate-key uniqueness;
- exact-row, normalized DOI, and normalized-title duplication;
- required identifier coverage across S1, S2, and S7;
- accepted values and aggregate totals for evidence category, primary family, year, and venue type;
- cross-file agreement with the final statistical JSON and derived matrices;
- missing-value profiling;
- local-path, username, and obvious credential-pattern scanning;
- repository manifest path, byte-count, and SHA-256 verification.

## Findings

1. **Core denominators and aggregates: PASS.** S1 contains 109 unique IDs; S2 and S7 contain 131. Evidence totals are 21/31/10/20/27, family totals are 57/15/9/10/7/6/5, and venue totals are 54/37/18.
2. **Duplicates: PASS.** No exact duplicate rows, duplicate normalized DOI values, or duplicate normalized titles were found in S1 or S2.
3. **Bibliographic cleanup: corrected in the public derivative.** Three titles (`P122`, `P176`, and `P198`) were truncated or contained OCR spacing in the validated submission payload. They were normalized from the manuscript bibliography/DOI metadata without changing any coding or aggregate result.
4. **Expected missingness: documented.** Eight S1 rows have blank `properties`; these blanks mean the field has no retained coded value, not that the paper claims no properties. Sixty-three blank `correction_reason` values mean no final correction was applied. One excluded preprint-only S2 record has no DOI.
5. **Public-release hygiene: PASS.** Tool-installation logs and a nested duplicate raw-log ZIP were excluded. Remaining text logs were sanitized for absolute paths and local usernames. No obvious access token, API key, or password value was detected by the release check.

## Residual limitations

- The public deposit does not include the original Web of Science/Scopus exports or the full 304-record pre-deduplication candidate table. The earliest search/deduplication transformation cannot therefore be replayed from raw exports.
- Bibliographic metadata were not independently revalidated field by field for all 131 reports during public-release preparation.
- Single-reviewer screening/coding remains a methodological limitation; automated consistency checks are not an independent reassessment.
- Formal-model outcomes retain their query-specific and encoded-model boundaries.

## Automated check

Run `python scripts/validate_public_release.py`. A passing run validates structural integrity and reported invariants; it does not independently establish the substantive correctness of every study-level judgment.
