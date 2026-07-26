# Data dictionary and missing-value semantics

## Authoritative row-level tables

### `data/S1_ROWLEVEL_CODING_INCLUDED_108.csv`

Grain: one included primary study per row. Candidate key: `paper_id`.

- `paper_id`: stable project identifier; it is not a publisher identifier.
- `ref_number`: numbered manuscript-reference entry.
- `title`, `doi`: bibliographic identifiers. DOI values are normalized for matching but should be checked against publisher metadata before external reuse.
- `mechanism_family`: one mutually exclusive primary trust-establishment family.
- `deployment_crosscutting_facets`: semicolon-separated, non-exclusive facets.
- `verification_level`: operational evidence category A-E.
- `properties`: semicolon-separated coded security-property claims. A blank value means no property value was retained in this field; it must not be interpreted as evidence that the source paper claimed no security properties.
- `year`, `year_group`: the year of first peer-reviewed online publication
  (including early-access publication) and its reported stratum. A later issue
  year is bibliographic metadata only and does not determine the stratum.
- `venue_tier`: descriptive publication type despite the historical field name; it is not a quality ranking.
- `scope_status`: inclusion status within the quantitative primary corpus.
- `mechanism_source`: provenance of the mechanism assignment.
- `correction_reason`: blank means no final evidence/venue correction was applied to that row.

### `data/S2_SCREENING_LEDGER_ALL_131.csv`

Grain: one unique screened report per row. Candidate key: `paper_id`. The single blank DOI belongs to an excluded preprint-only record and is expected.


Bibliographic fields shared by S2 and S7 are `title`, `doi`, `authors`, `venue`, `publication_year`, `volume`, `issue`, `pages_or_article_number`, `publisher`, and `publication_type`. The 13 rows marked `related_survey` were verified against DOI/publisher metadata on 2026-07-25. Blank fields mean that the value was not verified and must not be inferred.

### `data/S7_CORPUS_MANIFEST_ALL_131.csv`

Synchronized corpus-manifest view of the same 131 report identifiers. It should agree with S2 on identifiers and screening metadata.

## Derived tables

- `S4_*`: aggregate property, family, venue, and year-group tables derived from S1.
- `S6_THREE_DIMENSIONAL_MAPPING.csv`: definitions for the three coding dimensions.
- `S8_EVIDENCE_APPRAISAL_INCLUDED_108.csv`: evidence-appraisal details for included studies.
- `S9_PUBLISHED_PROTOCOL_CASE_SELECTION.csv`: the three bounded published-protocol cases.
- `S10_IIOT_CONTEXT_MATRIX_INCLUDED_108.csv`: IIoT relevance and context coding.

Empty fields in derived tables mean “not retained/not assigned under this field’s coding operation” unless the corresponding table states a stronger meaning. They are not automatically negative findings.

## Full bibliography enrichment (2026-07-25)

S2 and S7 synchronize complete local titles for the 108 included primary studies from S1 and DOI-registered bibliographic metadata from Crossref where available. `bibliographic_metadata_source` states the provenance. A blank field means that the value was unavailable from the verified source and was not inferred.
