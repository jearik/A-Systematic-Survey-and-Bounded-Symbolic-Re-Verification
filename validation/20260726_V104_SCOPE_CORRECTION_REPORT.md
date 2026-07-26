# v1.0.4 scope-correction and statistical validation report

Generated: 2026-07-26

## Scope decision

- P207 was retained in the 131-record screening ledger but excluded from the
  quantitative corpus at full-text review.
- Reason: Excluded at full-text review: peer-reviewed UAV mutual-authentication protocol, but no explicit cross-domain, inter-domain, or multi-domain trust transition or authentication mechanism was identified.
- Primary denominator: 109 -> 108.
- Excluded/contextual records: 22 -> 23.
- S2 and S7 remain identical at 131 unique records.
- P195, P158, P139, and P178 are confirmed as included; obsolete
  `borderline_review_needed` markers were removed.
- The P178 title was synchronized to the DOI-registered publisher title.

## Recomputed aggregates

- Verification A-E: 21/30/10/20/27.
- Families: 56/15/9/10/7/6/5 in the documented family order.
- Facets: ledger-present 100; privacy/anonymity-layer 64;
  edge/fog-mediated 35; multi-ledger 18; no-ledger 8.
- Venue totals: IEEE journal 53; other journal 37; conference/proceedings 18.
- Publication year is the year of first peer-reviewed online publication,
  including early-access publication; later issue assignment is bibliographic
  metadata only.
- Period totals: 2021-2023 = 40; 2024-2026 = 68.

## Recomputed tests

- Informal-only period comparison: Pearson chi-square =
  7.623529, p =
  0.005761; Yates-corrected chi-square =
  6.405882, p =
  0.011374; Fisher two-sided p =
  0.010448.
- Symbolic-tool period comparison: Pearson chi-square =
  1.955955, p =
  0.161947; Fisher two-sided p =
  0.211150.
- Venue exact tests: symbolic-tool Fisher-Freeman-Halton p =
  0.463050;
  informal-only p =
  0.036000.

All aggregates are generated from `data/S1_ROWLEVEL_CODING_INCLUDED_108.csv`.
