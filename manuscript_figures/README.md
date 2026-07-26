# Reproducible manuscript figures

Run the following commands from the supplementary-package root:

```bash
python manuscript_figures/generate_fig3_prisma.py
python manuscript_figures/generate_corrected_figures.py
```

The dedicated Fig. 3 generator validates the selection checkpoints in
`manuscript_figures/data/fig3_selection_counts.csv` and exports an exact-size
3.5 x 5.4 in SVG/PDF plus a 600-dpi PNG. The second generator builds the
remaining manuscript composites.

The scripts read only the CSV files in `manuscript_figures/data`, validate the
108-study totals, and write the manuscript PNGs to `figures/`. Editable PDF
and SVG companions are written to `manuscript_figures/exports/`. All rendering is
performed with Python and matplotlib. Every canvas is exactly 3.5 in wide so
the declared 7-8 pt labels retain that size when inserted at the manuscript's
single-column width.

Figure logic:

- `fig3_prisma_flow`: the documented identification, deduplication,
  eligibility, and exclusion checkpoints yield the 108-study primary corpus.
- `image1`: a conceptual audit-relevance path links context, the AKE audit
  target, protocol obligations, and operational relevance without asserting
  observed attack causality.
- `image4`: primary family, overlapping deployment facets, and orthogonal
  verification-evidence categories are three distinct classification axes;
  its third panel is conceptual, so it does not duplicate the counts in
  `image5`.
- `image5`: the final A-E distribution is 21, 30, 10, 20, and 27.
- `image6`: mechanism families have different verification-evidence profiles.
- `image8`: the declared P1 analytical latency projection is recomputed from
  three one-way flights, 1036 transmitted bytes, 247.993 microseconds of host
  time, and the assumed profiles in `data/latency_profiles.csv`; these inputs
  are analytical assumptions rather than field measurements.
- `image9`: methods create four distinguishable RQ-linked evidence streams,
  which converge into claim-boundary synthesis and research priorities. This
  is an evidence-logic workflow rather than a duplicate section directory.
