# Public release notes - v1.0.7

Source package: `Survey_FV_CrossDomain_IIoT_ACCESS_Supplementary_Artifacts_v17_1_20260720.zip`.

Preparation actions:

1. extracted the validated 387-file payload;
2. removed tool-installation logs containing user-specific environment paths;
3. removed the nested duplicate `S3_ABLATION_FULL_LOGS.zip` while retaining its text and CSV evidence;
4. replaced absolute Windows, WSL, and Linux home paths in text logs with placeholders;
5. added current reproducible vector-figure inputs and exports;
6. corrected three truncated/OCR-damaged bibliographic titles without changing coding fields;
7. added repository metadata, citation metadata, dependencies, and integrity records;
8. applied CC BY 4.0 to data/documentation and MIT to original code/model sources;
9. regenerated `MANIFEST_SHA256.csv` for the public directory.

These actions create a sanitized derivative for public distribution. The validated submission ZIP remains the immutable provenance package.

## v1.0.4 scope correction

- P207 was excluded at full-text review because the reported UAV mutual-authentication protocol does not specify a cross-domain trust transition.
- The quantitative denominator changed from 109 to 108; all dependent aggregates, tests, figure sources, and validators were regenerated.
- The 131-record screening ledger is unchanged in size.

## v1.0.6 release consolidation

- separated the PRISMA database-deduplication and screening counts and added the row-level recount audit under `data/prisma_recount/`;
- consolidated the seven manuscript figures, vector exports, previews, and mapping notes under `figures/`;
- removed redundant figure-generation copies, superseded validators, and package-construction scripts from the public payload;
- refreshed the affected row-level tables, statistical summaries, documentation, and `MANIFEST_SHA256.csv`;
- retained CC BY 4.0 for data and documentation and the MIT License for original code and formal-model source files.

## v1.0.7 public-artifact hygiene

- removed two duplicate or superseded family-model runners that are not used by
  the paper-facing execution workflow;
- retained only the performance, multi-tool, published-protocol, ablation/timing,
  and M1 query-specific runners referenced by the public documentation;
- replaced legacy internal-tool labels in two validation-table schema elements
  with the neutral field name `correction_reason`; row values and research
  coding were not changed;
- regenerated `MANIFEST_SHA256.csv` and rechecked the 108-study and 131-record
  invariants.
