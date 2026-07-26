# Security Assurance for Cross-Domain Authentication in the IIoT

Public data, analysis artifacts, and bounded symbolic models accompanying the manuscript:

> Security Assurance for Cross-Domain Authentication in the Industrial Internet of Things: A Systematic Review and Bounded Symbolic Re-Verification

## Contents

- `data/`: the 108-study row-level coding table, the 131-record screening ledger and corpus manifest, evidence-appraisal tables, and aggregate derivatives.
- `validation/`: correction records, final statistical summaries, and cross-file validation outputs.
- `proverif_models/`: bounded ProVerif models, illustrative Tamarin/Scyther skeletons, published-protocol abstractions, runner scripts, and sanitized result logs.
- `performance/`: desktop primitive timings and analytical network projections. These are not industrial-device or field-network measurements.
- `manuscript_figures/`: CSV inputs, generator, and PNG/PDF/SVG exports for the current manuscript figures.
- `MANUSCRIPT_ARTIFACT_MAP.md`: mapping from Supplements S1--S10 and supporting files to manuscript sections, figures, tables, and research questions.
- `MANIFEST_SHA256.csv`: size and SHA-256 digest for every repository payload file.

## Key denominators and invariants

- Unique screened reports: 131.
- Included primary studies: 108.
- Verification-evidence categories A/B/C/D/E: 21/30/10/20/27.
- Primary mechanism families: 56/15/9/10/7/6/5 in the order documented in `data/S1_ROWLEVEL_CODING_INCLUDED_108.csv`.
- Venue types: 53 IEEE journals, 37 other journals, and 18 conference/proceedings records.

The evidence categories record the strongest reported artifact under the study's operational coding rule. They are not a universal ranking of proof correctness.

## Quick validation

Python 3.10 or later is sufficient for the repository-level integrity checks:

```bash
python scripts/validate_public_release.py
```

Regenerate the current manuscript figures with NumPy and Matplotlib. The
dedicated PRISMA generator validates the documented selection arithmetic and
writes Fig. 3 at its final IEEE single-column size. The other
`manuscript_figures` generator writes the remaining manuscript composites,
including Fig. 4; the row-level script writes the corresponding Fig. 4--6
audit exports:

```bash
python -m pip install -r requirements-figures.txt
python manuscript_figures/generate_fig3_prisma.py
python manuscript_figures/generate_corrected_figures.py
python scripts/generate_v15_figures.py
```

Formal-tool execution requires the corresponding external tools. See `proverif_models/HOW_TO_RUN.md` and the model-scope notices before interpreting any result.

## Scope and provenance boundaries

- Screening and coding were performed by one reviewer; no independent dual-screening agreement statistic is claimed.
- The database-identification stage was reproduced from frozen Web of Science and Scopus exports, yielding 271 database records and 170 unique records. The licensed source exports are retained in a separately marked private audit bundle rather than this public archive.
- The combined author-collection and backward-snowballing inputs were not retained as separate route-specific lists. The 304-to-131 cross-source deduplication checkpoint is therefore arithmetically auditable but not fully replayable row by row.
- Published-protocol models are bounded abstractions. PASS, ATTACK (model-level), PARTIAL, TIMEOUT, and INCONCLUSIVE apply only to the named query and encoded model.
- M2-M6 and the cross-tool family files are illustrative and do not establish algorithm-level or family-wide security.
- Absolute local paths and usernames in retained text logs were replaced with placeholders for public release. Installation logs and a nested duplicate raw-log ZIP were excluded. Numerical outputs and model source files were not changed by that sanitization step.
- Bibliographic titles, authors, venues, years, and DOI values describe published records; users should verify them against the cited publisher records before reuse.

## Citation

Use `CITATION.cff` and cite the tagged v1.0.5 repository state:

`https://github.com/jearik/A-Systematic-Survey-and-Bounded-Symbolic-Re-Verification/tree/v1.0.5`

The existing Zenodo DOI archives the earlier v1.0.2 release and should not be
used as the identifier for the scope-corrected v1.0.5 dataset.

## License

This repository uses a dual license:

- data, documentation, tables, figures, figure inputs, and result summaries: CC BY 4.0;
- original scripts, software code, and formal-model source files: MIT.

See `LICENSE`, `LICENSE-DATA.md`, and `LICENSE-CODE.txt` for scope and terms.
