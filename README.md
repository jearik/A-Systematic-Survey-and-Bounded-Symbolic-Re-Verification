# Security Assurance for Cross-Domain Authentication in the IIoT

Public data, analysis artifacts, and bounded symbolic models accompanying the manuscript:

> Security Assurance for Cross-Domain Authentication in the Industrial Internet of Things: A Systematic Survey and Bounded Symbolic Re-Verification

## Contents

- `data/`: the 109-study row-level coding table, the 131-record screening ledger and corpus manifest, evidence-appraisal tables, and aggregate derivatives.
- `validation/`: correction records, final statistical summaries, and cross-file validation outputs.
- `proverif_models/`: bounded ProVerif models, illustrative Tamarin/Scyther skeletons, published-protocol abstractions, runner scripts, and sanitized result logs.
- `performance/`: desktop primitive timings and analytical network projections. These are not industrial-device or field-network measurements.
- `manuscript_figures/`: CSV inputs, generator, and PNG/PDF/SVG exports for the current manuscript figures.
- `MANIFEST_SHA256.csv`: size and SHA-256 digest for every repository payload file.

## Key denominators and invariants

- Unique screened reports: 131.
- Included primary studies: 109.
- Verification-evidence categories A/B/C/D/E: 21/31/10/20/27.
- Primary mechanism families: 57/15/9/10/7/6/5 in the order documented in `data/S1_ROWLEVEL_CODING_INCLUDED_109.csv`.
- Venue types: 54 IEEE journals, 37 other journals, and 18 conference/proceedings records.

The evidence categories record the strongest reported artifact under the study's operational coding rule. They are not a universal ranking of proof correctness.

## Quick validation

Python 3.10 or later is sufficient for the repository-level integrity checks:

```bash
python scripts/rebuild_manifest.py
python scripts/validate_public_release.py
```

The manifest generator and validator use the same payload-selection rules.
For release testing, run the validator again after extracting the tagged archive
into a clean directory.

Regenerate the current manuscript figures with NumPy and Matplotlib:

```bash
python -m pip install -r requirements-figures.txt
python manuscript_figures/generate_corrected_figures.py
```

Formal-tool execution requires the corresponding external tools. See `proverif_models/HOW_TO_RUN.md` and the model-scope notices before interpreting any result.

## Scope and provenance boundaries

- Screening and coding were performed by one reviewer; no independent dual-screening agreement statistic is claimed.
- The original Web of Science and Scopus exports and the full 304-record pre-deduplication candidate table are not deposited. Early database-stage counts are therefore reported provenance, not a fully replayable raw-export transformation.
- Published-protocol models are bounded abstractions. PASS, ATTACK (model-level), PARTIAL, TIMEOUT, and INCONCLUSIVE apply only to the named query and encoded model.
- M2-M6 and the cross-tool family files are illustrative and do not establish algorithm-level or family-wide security.
- Absolute local paths and usernames in retained text logs were replaced with placeholders for public release. Installation logs and a nested duplicate raw-log ZIP were excluded. Numerical outputs and model source files were not changed by that sanitization step.
- Bibliographic titles, authors, venues, years, and DOI values describe published records; users should verify them against the cited publisher records before reuse.

## Citation

Use `CITATION.cff`. Add the article DOI and repository archive DOI after they are assigned.

## License

This repository uses a dual license:

- data, documentation, tables, figures, figure inputs, and result summaries: CC BY 4.0;
- original scripts, software code, and formal-model source files: MIT.

See `LICENSE`, `LICENSE-DATA.md`, and `LICENSE-CODE.txt` for scope and terms.
