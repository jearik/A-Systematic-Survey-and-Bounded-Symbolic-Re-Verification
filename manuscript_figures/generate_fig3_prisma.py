#!/usr/bin/env python3
"""Generate the single-column PRISMA-guided study-selection figure.

Figure contract
---------------
Core conclusion: the documented selection checkpoints reduce 271 database
records plus 134 reports from other methods to a 108-study primary corpus.
Evidence chain: the central path reports 271 -> 170 -> 304 -> 131 -> 108;
side paths report the 101, 173, and 23 removals and the 134-report addition.
Archetype: schematic-led selection flow.
Target/output: IEEE Access single-column figure whose canvas width equals the
class column width (242.67 pt = 3.358 in), so \\includegraphics[width=
\\columnwidth] places it at scale 1.0 and the drawn point sizes survive
unchanged. Python/matplotlib only; editable SVG and PDF plus a 600-dpi PNG.
Reviewer risks: denominator drift, ambiguous stage boundaries, arithmetic
that does not close, illegible single-column text, and clipped labels.

Typographic rules enforced here
-------------------------------
1. One typeface everywhere. Bold counts are drawn as real Arial Bold text
   runs, never as mathtext (`$\\bf{...}$` silently falls back to DejaVu Sans
   and mixes two typefaces inside one line).
2. Two type sizes only - one for the main flow column, one for the side
   notes - and both are auto-fitted to the widest measured line so no label
   is clipped and no size is chosen by hand.
3. All geometry is expressed in inches: one data unit == one inch, so line
   pitch, padding, box heights, and stroke gaps are exact and repeatable.
4. Every connector is orthogonal (pure vertical or pure horizontal runs);
   no diagonal or free-form segments.
"""

from __future__ import annotations

import csv
import shutil
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.path import Path as MplPath
from matplotlib.textpath import TextToPath


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "fig3_selection_counts.csv"
EXPORTS = HERE / "exports"
FIGURES = ROOT / "figures"

BLUE = "#245B7A"
EDGE = "#2E6DA4"
ARROW = "#4F708C"
GRAY = "#8A969E"
GRAY_EDGE = "#9AA5AD"
PALE_BLUE = "#EAF1F8"
PALE_GREEN = "#E6F4E6"
GREEN = "#2E7D32"
INK = "#111111"

FONT = "Arial"

# --- canvas geometry, inches -------------------------------------------------
FIG_W = 3.358          # IEEE Access \columnwidth = 242.67355 pt
MARGIN_TOP = 0.045
MARGIN_BOTTOM = 0.045
BAR_X, BAR_W = 0.032, 0.200
MAIN_X, MAIN_W = 0.310, 1.600
COL_GAP = 0.150
SIDE_X = MAIN_X + MAIN_W + COL_GAP
SIDE_W = FIG_W - 0.036 - SIDE_X
ROW_GAP = 0.400        # vertical clearance between consecutive main boxes

PAD_X = 0.062          # horizontal text inset inside every box
PAD_Y = 0.062          # vertical text inset inside every box
LINE_PITCH = 1.34      # line advance, in em
CAP_HEIGHT = 0.716     # Arial cap height, in em

BOX_LW = 0.85
ARROW_LW = 0.95
ARROW_SCALE = 7.0

MAIN_SIZES = [7.6, 7.5, 7.4, 7.3, 7.2, 7.1, 7.0, 6.9, 6.8, 6.7, 6.6, 6.5, 6.4]
SIDE_SIZES = [7.0, 6.9, 6.8, 6.7, 6.6, 6.5, 6.4, 6.3, 6.2, 6.1, 6.0, 5.9, 5.8]
BAR_SIZES = [6.6, 6.4, 6.2, 6.0, 5.8]

mpl.use("Agg")
mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": [FONT, "Helvetica", "DejaVu Sans", "sans-serif"],
        "svg.fonttype": "none",
        "svg.hashsalt": "fig3-prisma-v1.0.4",
        "pdf.fonttype": 42,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
    }
)

_TEXT_TO_PATH = TextToPath()


# --- text metrics ------------------------------------------------------------
# A "line" is a list of (string, bold) runs; a "block" is a list of lines.
Run = tuple[str, bool]
Line = list[Run]
Block = list[Line]


def run_width(text: str, size: float, bold: bool) -> float:
    """Advance width of one run, in inches."""
    prop = FontProperties(family=FONT, size=size, weight="bold" if bold else "normal")
    width, _, _ = _TEXT_TO_PATH.get_text_width_height_descent(text, prop, ismath=False)
    return width / 72.0


def line_width(line: Line, size: float) -> float:
    return sum(run_width(text, size, bold) for text, bold in line)


def fit_size(blocks: list[Block], usable_width: float, candidates: list[float]) -> float:
    """Largest candidate size at which every line of every block still fits."""
    for size in candidates:
        if all(line_width(line, size) <= usable_width for block in blocks for line in block):
            return size
    raise ValueError("No candidate font size keeps the labels inside the box width")


def fit_bar_size(bars: list[tuple[float, float, str]]) -> float:
    """Largest size at which every rotated stage label clears its own bar."""
    for size in BAR_SIZES:
        if all(
            run_width(label, size, True) <= (top - bottom) - 0.10
            for top, bottom, label in bars
        ):
            return size
    raise ValueError("No candidate font size keeps the stage labels inside their bars")


def block_height(block: Block, size: float) -> float:
    """Box height that holds the block with equal padding above and below."""
    pitch = LINE_PITCH * size / 72.0
    return (len(block) - 1) * pitch + CAP_HEIGHT * size / 72.0 + 2 * PAD_Y


def draw_block(
    ax: plt.Axes,
    x: float,
    y_center: float,
    width: float,
    block: Block,
    size: float,
    align: str,
) -> None:
    """Draw a text block on exact, evenly pitched baselines."""
    pitch = LINE_PITCH * size / 72.0
    cap = CAP_HEIGHT * size / 72.0
    # Optically centre the block: midpoint of (top of first caps, last baseline).
    first_baseline = y_center - cap / 2.0 + (len(block) - 1) * pitch / 2.0
    for index, line in enumerate(block):
        baseline = first_baseline - index * pitch
        if align == "center":
            pen = x + width / 2.0 - line_width(line, size) / 2.0
        else:
            pen = x + PAD_X
        for text, bold in line:
            ax.text(
                pen,
                baseline,
                text,
                ha="left",
                va="baseline",
                fontsize=size,
                fontweight="bold" if bold else "normal",
                color=INK,
                zorder=3,
            )
            pen += run_width(text, size, bold)


def add_box(
    ax: plt.Axes,
    x: float,
    y_center: float,
    width: float,
    height: float,
    block: Block,
    size: float,
    *,
    facecolor: str,
    edgecolor: str,
    align: str = "center",
) -> None:
    ax.add_patch(
        FancyBboxPatch(
            (x, y_center - height / 2.0),
            width,
            height,
            boxstyle="round,pad=0,rounding_size=0.035",
            linewidth=BOX_LW,
            edgecolor=edgecolor,
            facecolor=facecolor,
            joinstyle="miter",
            zorder=2,
        )
    )
    draw_block(ax, x, y_center, width, block, size, align)


def connector(ax: plt.Axes, points: list[tuple[float, float]], color: str) -> None:
    """Orthogonal connector with a single arrowhead at the last point."""
    codes = [MplPath.MOVETO] + [MplPath.LINETO] * (len(points) - 1)
    ax.add_patch(
        FancyArrowPatch(
            path=MplPath(points, codes),
            arrowstyle="-|>",
            mutation_scale=ARROW_SCALE,
            linewidth=ARROW_LW,
            color=color,
            joinstyle="miter",
            capstyle="butt",
            shrinkA=0.0,
            shrinkB=0.0,
            zorder=4,
        )
    )


def stage_bar(ax: plt.Axes, y_top: float, y_bottom: float, label: str, size: float) -> None:
    height = y_top - y_bottom
    ax.add_patch(
        FancyBboxPatch(
            (BAR_X, y_bottom),
            BAR_W,
            height,
            boxstyle="round,pad=0,rounding_size=0.030",
            linewidth=0,
            facecolor=BLUE,
            zorder=1,
        )
    )
    ax.text(
        BAR_X + BAR_W / 2.0,
        y_bottom + height / 2.0,
        label,
        rotation=90,
        ha="center",
        va="center",
        fontsize=size,
        fontweight="bold",
        color="white",
        zorder=3,
    )


def read_counts() -> dict[str, int]:
    with DATA.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    values = {row["source_or_action"]: int(row["count"]) for row in rows}
    required = {
        "Database records",
        "Cross-database duplicates removed",
        "Unique database records",
        "Other methods",
        "Candidate records / reports",
        "Cross-source duplicates removed",
        "Reports assessed for eligibility",
        "Reports excluded",
        "Studies included in the quantitative corpus",
    }
    if set(values) != required:
        raise ValueError(f"Unexpected Fig. 3 source rows: {sorted(values)}")
    if values["Database records"] - values["Cross-database duplicates removed"] != values["Unique database records"]:
        raise ValueError("Database-stage arithmetic does not close")
    if values["Unique database records"] + values["Other methods"] != values["Candidate records / reports"]:
        raise ValueError("Candidate-pool arithmetic does not close")
    if values["Candidate records / reports"] - values["Cross-source duplicates removed"] != values["Reports assessed for eligibility"]:
        raise ValueError("Cross-source deduplication arithmetic does not close")
    if values["Reports assessed for eligibility"] - values["Reports excluded"] != values["Studies included in the quantitative corpus"]:
        raise ValueError("Eligibility arithmetic does not close")
    if values["Studies included in the quantitative corpus"] != 108:
        raise ValueError("Fig. 3 must use the validated 108-study denominator")
    return values


def plain(text: str) -> Line:
    return [(text, False)]


def build_figure() -> tuple[plt.Figure, float, float, float]:
    c = read_counts()

    main_blocks: list[Block] = [
        [
            plain("Records identified through"),
            plain("database searching"),
            [(f"n = {c['Database records']}", True)],
            plain("Web of Science 115; Scopus 156"),
        ],
        [
            plain("Unique database records"),
            plain("after duplicate removal"),
            [(f"n = {c['Unique database records']}", True)],
        ],
        [
            plain("Candidate records / reports"),
            plain("(databases + other methods)"),
            [(f"n = {c['Candidate records / reports']}", True)],
        ],
        [
            plain("Reports assessed"),
            plain("for eligibility"),
            [(f"n = {c['Reports assessed for eligibility']}", True)],
        ],
        [
            plain("Studies included"),
            plain("in the quantitative corpus"),
            [(f"n = {c['Studies included in the quantitative corpus']}", True)],
            plain("peer-reviewed; 2021-2026"),
        ],
    ]

    # Side blocks are keyed by the main row they sit beside; row 1 is an input.
    side_blocks: dict[int, Block] = {
        0: [
            plain("Duplicate records removed"),
            plain("before screening"),
            [("(cross-database): ", False), (f"n = {c['Cross-database duplicates removed']}", True)],
        ],
        1: [
            plain("Reports identified through"),
            plain("other methods"),
            plain("(prior set + snowballing)"),
            [(f"n = {c['Other methods']}", True)],
        ],
        2: [
            plain("Duplicate reports removed"),
            plain("(hash / DOI / title)"),
            [(f"n = {c['Cross-source duplicates removed']}", True)],
        ],
        3: [
            [("Reports excluded: ", False), (f"n = {c['Reports excluded']}", True)],
            plain("Surveys / methodology: 13"),
            plain("Pre-2021 anchors: 3"),
            plain("arXiv-only record: 1"),
            plain("Out of scope: 6"),
        ],
    }

    main_size = fit_size(main_blocks, MAIN_W - 2 * PAD_X, MAIN_SIZES)
    side_size = fit_size(list(side_blocks.values()), SIDE_W - 2 * PAD_X, SIDE_SIZES)

    main_h = [block_height(block, main_size) for block in main_blocks]
    side_h = {row: block_height(block, side_size) for row, block in side_blocks.items()}

    fig_h = MARGIN_TOP + MARGIN_BOTTOM + sum(main_h) + ROW_GAP * (len(main_h) - 1)

    # Stack the main column from the top; every gap is identical.
    centers: list[float] = []
    cursor = fig_h - MARGIN_TOP
    for height in main_h:
        centers.append(cursor - height / 2.0)
        cursor -= height + ROW_GAP

    tops = [centers[i] + main_h[i] / 2.0 for i in range(len(main_h))]
    bottoms = [centers[i] - main_h[i] / 2.0 for i in range(len(main_h))]

    # Stage bars: each rotated label must clear its own bar span.
    bars = [
        (tops[0], bottoms[1], "Identification"),
        (tops[2], bottoms[3], "Screening"),
        (tops[4], bottoms[4], "Included"),
    ]
    bar_size = fit_bar_size(bars)

    fig, ax = plt.subplots(figsize=(FIG_W, fig_h))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, fig_h)
    ax.axis("off")

    stage_bar(ax, tops[0], bottoms[1], "Identification", bar_size)
    stage_bar(ax, tops[2], bottoms[3], "Screening", bar_size)
    stage_bar(ax, tops[4], bottoms[4], "Included", bar_size)

    for row, block in enumerate(main_blocks):
        included = row == len(main_blocks) - 1
        add_box(
            ax,
            MAIN_X,
            centers[row],
            MAIN_W,
            main_h[row],
            block,
            main_size,
            facecolor=PALE_GREEN if included else PALE_BLUE,
            edgecolor=GREEN if included else EDGE,
        )

    for row, block in side_blocks.items():
        add_box(
            ax,
            SIDE_X,
            centers[row],
            SIDE_W,
            side_h[row],
            block,
            side_size,
            facecolor="white",
            edgecolor=GRAY_EDGE,
            align="left",
        )

    # Main flow: identical vertical runs on the column centre line.
    flow_x = MAIN_X + MAIN_W / 2.0
    for row in range(len(main_blocks) - 1):
        connector(ax, [(flow_x, bottoms[row]), (flow_x, tops[row + 1])], ARROW)

    # Exclusions: pure horizontal runs on the shared box centre line.
    for row in (0, 2, 3):
        connector(ax, [(MAIN_X + MAIN_W, centers[row]), (SIDE_X, centers[row])], GRAY)

    # Other-methods input: orthogonal elbow merging into the candidate pool.
    merge_x = MAIN_X + 0.80 * MAIN_W
    elbow_y = tops[2] + 0.170
    side_center_x = SIDE_X + SIDE_W / 2.0
    connector(
        ax,
        [
            (side_center_x, centers[1] - side_h[1] / 2.0),
            (side_center_x, elbow_y),
            (merge_x, elbow_y),
            (merge_x, tops[2]),
        ],
        ARROW,
    )

    return fig, fig_h, main_size, side_size


def main() -> None:
    EXPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig, fig_h, main_size, side_size = build_figure()
    fig.savefig(
        EXPORTS / "fig3_prisma_flow.svg",
        metadata={"Creator": "Fig. 3 reproducible Python generator", "Date": None},
    )
    fig.savefig(
        EXPORTS / "fig3_prisma_flow.pdf",
        metadata={
            "Creator": "Fig. 3 reproducible Python generator",
            "CreationDate": None,
            "ModDate": None,
        },
    )
    fig.savefig(FIGURES / "fig3_prisma_flow.png", dpi=600)
    plt.close(fig)
    shutil.copy2(EXPORTS / "fig3_prisma_flow.pdf", FIGURES / "fig3_prisma_flow.pdf")
    shutil.copy2(EXPORTS / "fig3_prisma_flow.svg", FIGURES / "fig3_prisma_flow.svg")
    if ROOT.name in {"supplementary_v1.0.5", "github_public_release"}:
        regenerated = FIGURES / "regenerated"
        source_dir = FIGURES / "source"
        regenerated.mkdir(parents=True, exist_ok=True)
        source_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(
            EXPORTS / "fig3_prisma_flow.pdf",
            regenerated / "figure3_prisma_108_corrected.pdf",
        )
        shutil.copy2(
            EXPORTS / "fig3_prisma_flow.svg",
            regenerated / "figure3_prisma_108_corrected.svg",
        )
        shutil.copy2(
            FIGURES / "fig3_prisma_flow.png",
            regenerated / "figure3_prisma_108_corrected.png",
        )
        shutil.copy2(
            FIGURES / "fig3_prisma_flow.png",
            FIGURES / "20260726_fig3_prisma_108_corrected.png",
        )
        shutil.copy2(DATA, regenerated / "figure3_prisma_108_corrected_source.csv")
        shutil.copy2(DATA, source_dir / "figure3_prisma_108_corrected_source.csv")
    print(
        f"PASS: Fig. 3 at {FIG_W:.3f} x {fig_h:.3f} in "
        f"(main {main_size:.1f} pt, side {side_size:.1f} pt), 108-study denominator"
    )


if __name__ == "__main__":
    main()
