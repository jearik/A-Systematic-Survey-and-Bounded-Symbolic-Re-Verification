# S3 Search Protocol and Provenance Boundary

Search date: 13 June 2026. Quantitative window: 2021-2026. Publication year is the year of first peer-reviewed online publication, including early-access publication; a later issue year is retained only as bibliographic metadata. Language: English. Document types: journal articles, proceedings papers, and review articles for contextual comparison.

## Web of Science Core Collection

`TS=(("cross-domain" OR "inter-domain" OR "multi-domain" OR "cross domain") AND ("authentication" OR "key agreement" OR "key exchange" OR "mutual authentication") AND ("IIoT" OR "industrial internet of things" OR "internet of things" OR "IoT") AND ("blockchain" OR "formal verification" OR "ProVerif" OR "security proof" OR "certificateless" OR "key management"))`

Refined hit count: 115.

## Scopus

`TITLE-ABS-KEY(("cross-domain" OR "inter-domain" OR "multi-domain" OR "cross domain") AND ("authentication" OR "key agreement" OR "key exchange" OR "mutual authentication") AND ("IIoT" OR "industrial internet of things" OR "internet of things" OR "IoT") AND ("blockchain" OR "formal verification" OR "ProVerif" OR "security proof" OR "certificateless" OR "key management")) AND PUBYEAR > 2020 AND PUBYEAR < 2027 AND (LIMIT-TO(LANGUAGE, "English"))`

Refined hit count: 156.

## Selection arithmetic

- Database hits: 271.
- Duplicates between the database exports: 101.
- Unique database records: 170.
- Reports added from a pre-existing author collection and backward snowballing: 134.
- Candidate reports before cross-source deduplication: 304.
- Cross-source duplicates removed by SHA-256, DOI, and normalized-title checks: 102.
- Reports remaining after cross-source deduplication: 202.
- Records excluded at title/abstract screening: 71.
- Unique reports in the corrected screening ledger: 131.

The 304-to-131 reduction combines two distinct PRISMA items and is reported as two
steps. Deduplication alone cannot reduce the candidate pool below the 170 unique
database records, so a single 173-record removal box (used in earlier drafts) was
internally inconsistent. The split was recovered by normalized-title matching of the
131-row manifest against the frozen 2026-06-13 exports using prisma_recount.py in the
private audit bundle. Outputs:
  - prisma_recount/S3a_db_records_excluded_at_screening_71.csv
  - prisma_recount/S3b_manifest_source_route_131.csv
The 71 screening exclusions are predominantly conference-volume container records
carrying no author or protocol content, plus topically unrelated hits returned by the
mechanism terms. Of the 131 assessed reports, 99 are traceable to the database exports
and 32 entered only through the supplementary route; within the 108 included primary
studies the split is 91 and 17.

Validation. The Web of Science export carries a DOI for all 115 records and every
manifest row carries a DOI, so the WoS side was matched exactly rather than by title:
86 WoS records entered the manifest and 29 were screened out. Normalized-title
matching returns the same 86/29 split for those records, with zero discrepancies.
The Scopus export carries no DOI column, so its 55 Scopus-only records were matched
by title; two variant-title pairs were identified and corrected manually. Repeating
the full count with those corrections reproduces 71, 102, 91, and 17 unchanged.
Residual uncertainty is confined to the Scopus-only records.
- Included primary studies: 108.
- Contextual or excluded records: 23.

## Provenance limitation

The surviving source exports do not preserve a reliable row-level distinction between the pre-existing author collection and backward-snowballing routes. These 134 reports are therefore reported as one supplementary source. They are not treated as an independent database denominator. Screening and coding were performed by the author; no dual-screening agreement statistic is claimed.
