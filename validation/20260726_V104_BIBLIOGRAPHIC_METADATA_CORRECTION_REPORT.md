# v1.0.4 bibliographic metadata correction audit

Date: 2026-07-26

## Scope

This audit reconciles the included-study control table, screening ledger, corpus
manifest, evidence appraisal, IIoT context matrix, paper-to-reference mapping,
validated master table, and `references.tex`.

## Corrections

- P173: S1, the mapping table, and the validated master now use DOI
  `10.1109/JIOT.2021.3113321` and venue tier
  `IEEE transaction / flagship journal`, matching S2/S7 and Ref. 40.
- P137: S1, the mapping table, and the validated master now use DOI
  `10.1109/ICSP62122.2024.10743919` and venue tier
  `conference / proceedings`, matching S2/S7 and Ref. 85.
- P152: S2 and S7 now classify the record as `proceedings-article`, matching
  its conference venue and the S1 venue tier.
- P190: S1, S8, S10, the mapping table, and the validated master now use the
  publisher title containing “With a Cross-Domain,” matching S2/S7 and
  Ref. 81.

## Cross-file validation

All 108 included records were compared by paper ID across S1, S2, S7, S8,
S10, the paper-to-reference mapping, the validated master, and
`references.tex`. DOI, reference-number, title-identity, mechanism-family, and
venue-type checks pass after the correction. S1/S8/S10 retain 108 unique IDs;
S2/S7 retain 131 unique IDs; P207 remains excluded from the primary
denominator.

## Aggregate impact

The correction does not change the reported aggregates. Venue counts remain
53 IEEE journals, 37 other journals, and 18 conference/proceedings papers.
Verification-evidence counts remain A=21, B=30, C=10, D=20, and E=27.
P173 and P137 are both ledger-mediated, informal-only records and their
opposite venue corrections cancel in the venue-by-evidence matrix.

## Publication-year convention resolved

Publication year is coded as the year of first peer-reviewed online
publication, including early-access publication; later issue assignment is
retained only as bibliographic metadata. P190 is coded as 2025 rather than its
2026 issue year, and P198 is coded as 2023 rather than its 2024 issue year.
P198 therefore moves from the 2024--2026 stratum to the 2021--2023 stratum.
The period table and statistical tests were regenerated from S1.
