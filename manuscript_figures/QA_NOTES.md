# Figure QA record

## Figure contracts

| Figure | Core conclusion | Evidence chain | Archetype |
|---|---|---|---|
| `fig3_prisma_flow` | The documented selection checkpoints yield a 108-study primary corpus. | The central path is 271 to 170 to 304 to 131 to 108; side paths show the 101, 173, and 23 removals and the 134-report addition. | Schematic-led selection flow |
| `image4` | Primary family, overlapping deployment facets, and verification evidence are distinct classification axes. | Panel a gives one family per study; panel b permits overlapping facets; panel c gives the orthogonal A-E totals. | Quantitative grid |
| `image5` | The final A-E distribution is 21, 30, 10, 20, and 27 out of 108 studies. | Direct count and percentage labels on one bar per category. | Quantitative single panel |
| `image6` | Mechanism families have different verification-evidence profiles. | Annotated family-by-category cells, with row and column totals visible in axis labels. | Quantitative heatmap |
| `image8` | Assumed link latency dominates the illustrative P1 projection on slow links. | Totals are recomputed from three one-way flights, 1036 bytes, 247.993 microseconds of host time, and the six declared link profiles. | Analytical projection |
| `image9` | Search and coding methods feed four distinguishable RQ-linked evidence streams, which converge into boundary-aware synthesis. | Two methods nodes split into RQ1-RQ4 streams and rejoin at the synthesis node. | Schematic-led workflow |

## Reproducibility and integrity checks

- Backend: Python/matplotlib only for generation, export, preview, and QA.
- Source-data validation: Fig. 3 arithmetic closes at every checkpoint
  (`271-101=170`, `170+134=304`, `304-173=131`, and `131-23=108`);
  A-E totals sum to 108; family-matrix columns equal
  `21,30,10,20,27`; family-matrix rows equal `56,15,9,10,7,6,5`; the
  workflow source contains exactly the two methods nodes, RQ1-RQ4, and the
  synthesis node. The P1 projection reproduces `1.830873, 9.413753,
  30.330873, 308.535993, 4938.381326, 1651.076793` ms before display rounding.
- Final-size contract: every figure is designed directly at the IEEE single-
  column width of 3.5 in, so `width=\columnwidth` does not reduce its nominal
  text size. Fig. 3 is `3.50x5.40` in; PDF sizes are `3.50x8.25`,
  `3.50x3.15`, `3.50x4.25`, and `3.50x5.25` in for images 4, 5, 6, and 9,
  respectively.
- Typography at final size: image 4 uses 7.0-7.8 pt body/panel text and an
  8.6-pt figure title; image 5 uses 7.0-7.4 pt body text and an 8.7-pt title;
  image 6 uses 7.0-7.2 pt labels/cell values and an 8.2-pt title; image 9 uses
  7.0-7.2 pt workflow labels. Long family labels are line-wrapped rather than
  reduced below the final-size readability target.
- PNG resolution: Fig. 3 is exported at 600 dpi (`2100x3240`). The other four
  manuscript rasters are 300 dpi, with pixel dimensions `1050x2475`,
  `1050x945`, `1050x1275`, and `1050x1575` for images 4, 5, 6, and 9,
  respectively.
- Editable exports: each SVG contains live text elements. Each PDF contains
  extractable text and embedded Arial regular/bold font subsets.
- Visual inspection: all four regenerated PNGs were opened at high detail and
  again as 3.5-in-wide, 110-dpi single-column previews. Labels, count
  annotations, heatmap values, arrows, and section names remain legible at the
  latter size; no clipping or overlap remains.
- Color/accessibility: the charts use a restrained blue-led palette, outlined
  bars, numeric annotations, and a sequential heatmap. No result depends on a
  red-versus-green distinction.

The figures report descriptive counts, not inferential statistics; therefore
no uncertainty interval or hypothesis-test annotation is attached to these
panels.
