# Reproducible manuscript figures

Run `python figure_sources/generate_corrected_figures.py` from the project root.

The script reads only the CSV files in `figure_sources/data`, validates the
109-study totals, and writes the manuscript PNGs to `figures/`. Editable PDF
and SVG companions are written to `figure_sources/exports/`. All rendering is
performed with Python and matplotlib. Every canvas is exactly 3.5 in wide so
the declared 7-8 pt labels retain that size when inserted at the manuscript's
single-column width.

Figure logic:

- `image1`: a conceptual audit-relevance path links context, the AKE audit
  target, protocol obligations, and operational relevance without asserting
  observed attack causality.
- `image4`: primary family, overlapping deployment facets, and orthogonal
  verification-evidence categories are three distinct classification axes;
  its third panel is conceptual, so it does not duplicate the counts in
  `image5`.
- `image5`: the final A-E distribution is 21, 31, 10, 20, and 27.
- `image6`: mechanism families have different verification-evidence profiles.
- `image8`: the declared P1 analytical latency projection is recomputed from
  three one-way flights, 1036 transmitted bytes, 247.993 microseconds of host
  time, and the assumed profiles in `data/latency_profiles.csv`; these inputs
  are analytical assumptions rather than field measurements.
- `image9`: methods create four distinguishable RQ-linked evidence streams,
  which converge into claim-boundary synthesis and research priorities. This
  is an evidence-logic workflow rather than a duplicate section directory.
