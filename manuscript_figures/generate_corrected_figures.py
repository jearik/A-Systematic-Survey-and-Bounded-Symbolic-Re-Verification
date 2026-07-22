"""Rebuild the manuscript's corrected quantitative and structure figures.

All plotted values are read from the CSV files in ``figure_sources/data``.
The script uses matplotlib exclusively and exports editable PDF/SVG alongside
300-dpi PNG files used by the LaTeX manuscript.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


ROOT = Path(__file__).resolve().parents[1]
DATA = Path(__file__).resolve().parent / "data"
EXPORTS = Path(__file__).resolve().parent / "exports"
FIGURES = ROOT / "figures"

EDGE = "#34495E"
EVIDENCE_COLORS = ["#1F5A96", "#3F7FBE", "#82AFC2", "#CAA053", "#B94545"]

mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "font.size": 7.2,
        "axes.labelsize": 7.2,
        "xtick.labelsize": 7.0,
        "ytick.labelsize": 7.0,
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titleweight": "bold",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
    }
)


def read_rows(filename: str) -> list[dict[str, str]]:
    with (DATA / filename).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def save_all(fig: plt.Figure, stem: str) -> None:
    """Write exact-size manuscript PNG plus editable companion exports."""
    EXPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES / f"{stem}.png", dpi=300)
    fig.savefig(EXPORTS / f"{stem}.pdf")
    fig.savefig(EXPORTS / f"{stem}.svg")
    plt.close(fig)


def clean_bar_axis(ax: plt.Axes) -> None:
    ax.spines["left"].set_color("#111111")
    ax.spines["bottom"].set_color("#111111")
    ax.tick_params(axis="both", width=0.8, length=3, color="#111111")
    ax.grid(False)


def make_image1() -> None:
    """Draw a non-causal audit-relevance path at final column width."""
    fig, ax = plt.subplots(figsize=(3.5, 4.35), constrained_layout=True)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(
        0.5,
        0.975,
        "Cross-domain authentication audit-relevance path",
        ha="center",
        va="top",
        fontsize=8.5,
        fontweight="bold",
    )

    boxes = [
        (0.83, "Context signals", "Standards and documented\ncross-boundary incidents", "#D9E7F5"),
        (0.62, "Audit target", "Cross-domain AKE boundary", "#E1EFDF"),
        (0.41, "Protocol obligations", "Freshness, transcript binding,\nrevocation, and key confirmation", "#FFF0C8"),
        (0.20, "Operational relevance", "ATT&CK for ICS and OT-impact\ncategories to assess", "#E9DFF5"),
    ]
    x, width, height = 0.08, 0.84, 0.135
    for y, heading, body, color in boxes:
        patch = FancyBboxPatch(
            (x, y - height / 2),
            width,
            height,
            boxstyle="round,pad=0.012,rounding_size=0.02",
            linewidth=1.0,
            edgecolor="#285D8F",
            facecolor=color,
        )
        ax.add_patch(patch)
        ax.text(x + 0.035, y + 0.026, heading, ha="left", va="center", fontsize=7.5, fontweight="bold")
        ax.text(x + 0.035, y - 0.026, body, ha="left", va="center", fontsize=7.0)

    arrow_labels = ["motivates audit", "specifies checks", "maps relevance"]
    for index, label in enumerate(arrow_labels):
        y_top = boxes[index][0] - height / 2
        y_bottom = boxes[index + 1][0] + height / 2
        arrow = FancyArrowPatch(
            (0.5, y_top - 0.006),
            (0.5, y_bottom + 0.006),
            arrowstyle="-|>",
            mutation_scale=10,
            linewidth=1.0,
            linestyle=(0, (4, 2)),
            color="#62778B",
        )
        ax.add_patch(arrow)
        ax.text(0.53, (y_top + y_bottom) / 2, label, ha="left", va="center", fontsize=6.2, color="#62778B")

    ax.text(
        0.5,
        0.045,
        "Conceptual review mapping; not observed attack causality",
        ha="center",
        va="center",
        fontsize=6.7,
        color="#5A6673",
        style="italic",
    )
    save_all(fig, "image1")


def make_image4() -> None:
    mechanisms = read_rows("primary_mechanisms.csv")
    facets = read_rows("deployment_facets.csv")
    evidence = read_rows("verification_totals.csv")

    # Designed at its final IEEE single-column width: 3.5 in.
    fig = plt.figure(figsize=(3.5, 8.25))
    grid = fig.add_gridspec(
        3,
        1,
        height_ratios=[1.55, 1.08, 0.92],
        left=0.41,
        right=0.96,
        bottom=0.05,
        top=0.91,
        hspace=0.43,
    )
    fig.suptitle(
        "Three-dimensional classification of\n109 IIoT-relevant studies",
        fontsize=8.6,
        fontweight="normal",
        y=0.975,
    )

    ax = fig.add_subplot(grid[0])
    mechanism_wrap = {
        "Ledger-mediated trust": "Ledger-mediated\ntrust",
        "Certificateless split-key": "Certificateless\nsplit-key",
        "ZK / privacy credential": "ZK / privacy\ncredential",
        "Other / classical-general": "Other / classical-\ngeneral",
        "Hardware-/device-rooted": "Hardware-/device-\nrooted",
        "Group-/ring-signature": "Group-/ring-\nsignature",
        "Post-quantum": "Post-quantum",
    }
    names = [mechanism_wrap[row["mechanism"]] for row in mechanisms]
    values = np.array([int(row["count"]) for row in mechanisms])
    colors = [row["color"] for row in mechanisms]
    y = np.arange(len(names))
    bars = ax.barh(y, values, color=colors, edgecolor=EDGE, linewidth=0.7)
    ax.set_yticks(y, names)
    ax.invert_yaxis()
    ax.set_xlim(0, 64)
    ax.set_xlabel("Studies assigned to one primary family", fontsize=7.2)
    ax.set_title("a  Primary mechanism\n    (single assignment)", loc="left", fontsize=7.8, pad=5)
    ax.bar_label(bars, labels=[str(v) for v in values], padding=2, fontsize=7.0)
    ax.tick_params(axis="y", labelsize=7.0)
    clean_bar_axis(ax)

    ax = fig.add_subplot(grid[1])
    facet_names = [row["facet"] for row in facets]
    facet_values = np.array([int(row["count"]) for row in facets])
    y = np.arange(len(facet_names))
    bars = ax.barh(
        y,
        facet_values,
        color="#86A8C0",
        edgecolor=EDGE,
        linewidth=0.7,
    )
    ax.set_yticks(y, facet_names)
    ax.invert_yaxis()
    ax.set_xlim(0, 112)
    ax.set_xlabel("Studies with facet (facets may overlap)", fontsize=7.2)
    ax.set_title("b  Deployment / cross-cutting\n    (non-exclusive)", loc="left", fontsize=7.8, pad=5)
    ax.bar_label(bars, labels=[str(v) for v in facet_values], padding=2, fontsize=7.0)
    ax.tick_params(axis="y", labelsize=7.0)
    clean_bar_axis(ax)

    ax = fig.add_subplot(grid[2])
    categories = [row["category"] for row in evidence]
    labels = ["Symbolic tool", "Computational proof", "BAN logic", "Formal, untooled", "Informal"]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("c  Verification evidence\n    (orthogonal category axis)", loc="left", fontsize=7.8, pad=5)
    y_positions = [0.78, 0.62, 0.46, 0.30, 0.14]
    for y_pos, category, label, color in zip(y_positions, categories, labels, EVIDENCE_COLORS):
        patch = FancyBboxPatch(
            (0.08, y_pos - 0.055),
            0.12,
            0.11,
            boxstyle="round,pad=0.008,rounding_size=0.018",
            linewidth=0.8,
            edgecolor=EDGE,
            facecolor=color,
        )
        ax.add_patch(patch)
        ax.text(0.14, y_pos, category, ha="center", va="center", color="white", fontsize=7.2, fontweight="bold")
        ax.text(0.25, y_pos, label, ha="left", va="center", fontsize=6.8)
    save_all(fig, "image4")


def make_image5() -> None:
    evidence = read_rows("verification_totals.csv")
    categories = [row["category"] for row in evidence]
    description_wrap = {
        "Symbolic tool": "Symbolic\ntool",
        "Computational proof": "Computational\nproof",
        "BAN logic": "BAN\nlogic",
        "Formal, untooled": "Formal,\nuntooled",
        "Informal": "Informal",
    }
    descriptions = [description_wrap[row["label"]] for row in evidence]
    values = np.array([int(row["count"]) for row in evidence])
    percentages = values / values.sum() * 100.0

    # Designed at final 3.5-in column width, so the font sizes below are final.
    fig, ax = plt.subplots(figsize=(3.5, 3.15), constrained_layout=True)
    bars = ax.bar(categories, values, color=EVIDENCE_COLORS, edgecolor=EDGE, linewidth=0.8)
    ax.set_title("Reported verification-evidence category", loc="left", fontsize=8.7, pad=6)
    ax.set_ylabel("IIoT-relevant studies (n = 109)", fontsize=7.4)
    ax.set_ylim(0, 38)
    ax.set_yticks(np.arange(0, 36, 5))
    ax.set_xticks(
        np.arange(len(categories)),
        [f"{code}\n{label}" for code, label in zip(categories, descriptions)],
    )
    for bar, count, pct in zip(bars, values, percentages):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.45,
            f"{count}\n({pct:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=7.1,
        )
    clean_bar_axis(ax)
    save_all(fig, "image5")


def make_image6() -> None:
    rows = read_rows("verification_by_family.csv")
    columns = ["A", "B", "C", "D", "E"]
    matrix = np.array([[int(row[col]) for col in columns] for row in rows])
    row_totals = matrix.sum(axis=1)
    col_totals = matrix.sum(axis=0)
    family_wrap = {
        "Ledger-mediated trust": "Ledger-mediated\ntrust",
        "Certificateless split-key": "Certificateless\nsplit-key",
        "ZK / privacy credential": "ZK / privacy\ncredential",
        "Other / classical-general": "Other / classical-\ngeneral",
        "Hardware-/device-rooted": "Hardware-/device-\nrooted",
        "Group-/ring-signature": "Group-/ring-\nsignature",
        "Post-quantum": "Post-quantum",
    }
    family_labels = [f'{family_wrap[row["family"]]}\n(n={total})' for row, total in zip(rows, row_totals)]

    cmap = LinearSegmentedColormap.from_list(
        "muted_blues", ["#F6F9FC", "#DCEAF4", "#9CC5DB", "#4F9AC4", "#1F659E", "#123E73"]
    )
    # Compact heatmap designed directly at final single-column width.
    fig, ax = plt.subplots(figsize=(3.5, 4.25), constrained_layout=True)
    # Draw one vector rectangle per cell.  ``imshow`` embeds a raster image in
    # PDF/SVG even when the surrounding labels remain vector objects.
    x_edges = np.arange(matrix.shape[1] + 1) - 0.5
    y_edges = np.arange(matrix.shape[0] + 1) - 0.5
    image = ax.pcolormesh(
        x_edges,
        y_edges,
        matrix,
        cmap=cmap,
        vmin=0,
        vmax=int(matrix.max()),
        shading="flat",
        edgecolors="white",
        linewidth=1.1,
    )
    ax.set_xlim(-0.5, matrix.shape[1] - 0.5)
    ax.set_ylim(matrix.shape[0] - 0.5, -0.5)
    ax.set_title("Mechanism family x verification-evidence\ncategory (n = 109)", loc="left", fontsize=8.2, pad=6)
    ax.set_yticks(np.arange(len(rows)), family_labels)
    ax.set_xticks(
        np.arange(len(columns)),
        [f"{name}\n{total}" for name, total in zip(columns, col_totals)],
    )
    ax.tick_params(axis="x", bottom=True, top=False, labelbottom=True, length=0, labelsize=7.0)
    ax.tick_params(axis="y", length=0, labelsize=7.0, pad=3)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = int(matrix[i, j])
            color = "white" if value >= 11 else "#173A59"
            ax.text(j, i, str(value), ha="center", va="center", color=color, fontsize=7.2)

    for spine in ax.spines.values():
        spine.set_visible(False)
    # Explicit boundaries keep the colour scale as vector rectangles instead
    # of a narrow raster strip in the PDF backend.
    cbar = fig.colorbar(
        image,
        ax=ax,
        fraction=0.05,
        pad=0.03,
        boundaries=np.linspace(0, int(matrix.max()), int(matrix.max()) + 1),
        spacing="proportional",
    )
    cbar.set_label("Studies", fontsize=7.0)
    cbar.ax.tick_params(labelsize=7.0)
    cbar.outline.set_linewidth(0.7)
    save_all(fig, "image6")


def make_image8() -> None:
    """Rebuild the declared P1 latency projection from its input profiles."""
    rows = read_rows("latency_profiles.csv")
    flights = 3
    transmitted_bytes = 1036
    host_time_ms = 247.993 / 1000.0

    names = [row["profile"] for row in rows]
    one_way_ms = np.array([float(row["one_way_latency_ms"]) for row in rows])
    bandwidth_mbps = np.array([float(row["bandwidth_mbps"]) for row in rows])
    serialization_ms = 8.0 * transmitted_bytes / (bandwidth_mbps * 1_000_000.0) * 1000.0
    totals_ms = flights * one_way_ms + serialization_ms + host_time_ms

    expected_ms = np.array([1.830873, 9.413753, 30.330873, 308.535993, 4938.381326, 1651.076793])
    if not np.allclose(totals_ms, expected_ms, rtol=0.0, atol=0.000001):
        raise ValueError("P1 latency totals do not match the manuscript projection")

    colors = ["#4775C5", "#5B9BD3", "#70AD47", "#F27C2A", "#C95709", "#A5A5A5"]
    fig, ax = plt.subplots(figsize=(3.5, 1.8), constrained_layout=True)
    y = np.arange(len(names))
    ax.barh(y, totals_ms, color=colors, edgecolor="none", height=0.56)
    ax.set_xscale("log")
    ax.set_xlim(1.0, 10_000.0)
    ax.set_yticks(y, names)
    ax.invert_yaxis()
    ax.set_xticks([1, 10, 100, 1000, 10000], ["1 ms", "10 ms", "100 ms", "1000 ms", "10000 ms"])
    ax.tick_params(axis="both", length=0, labelsize=7.0)
    ax.grid(axis="x", which="major", color="#CBD3DC", linewidth=0.7)
    ax.grid(axis="x", which="minor", visible=False)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)

    labels = ["1.83 ms", "9.41 ms", "30.33 ms", "0.31 s", "4.94 s", "1.65 s"]
    for ypos, value, label in zip(y, totals_ms, labels):
        ax.annotate(
            label,
            xy=(value, ypos),
            xytext=(5, 0),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=7.0,
            fontweight="bold",
        )
    ax.set_title("Illustrative P1 latency: 3 one-way message flights", fontsize=8.6, fontweight="bold", pad=13)
    ax.text(
        0.5,
        1.06,
        "Assumed link profiles; not field measurements",
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        fontsize=6.8,
        color="#5F6368",
    )
    save_all(fig, "image8")


def make_image9() -> None:
    rows = read_rows("paper_structure.csv")
    by_id = {row["node_id"]: row for row in rows}
    border = "#4A83C4"
    rail = "#6B7C8D"
    # Final single-column dimensions; the 7.0-7.4-pt text is not downscaled.
    fig, ax = plt.subplots(figsize=(3.5, 5.25), constrained_layout=True)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def add_box(
        row: dict[str, str],
        x: float,
        y: float,
        width: float,
        height: float,
        fontsize: float = 7.2,
    ) -> None:
        patch = FancyBboxPatch(
            (x, y - height / 2),
            width,
            height,
            boxstyle="round,pad=0.006,rounding_size=0.008",
            facecolor=row["color"],
            edgecolor=border,
            linewidth=1.0,
        )
        ax.add_patch(patch)
        label = row["label"]
        wrap = {
            "Search, screening, and 109-study corpus": "Search, screening, and 109-study corpus",
            "Three-dimensional coding": "Three-dimensional coding",
            "RQ1 Verification-evidence distribution": "RQ1  Verification-evidence distribution",
            "RQ2 Mechanism/property/threat gaps": "RQ2  Mechanism/property/threat gaps",
            "RQ3 Bounded symbolic re-verification": "RQ3  Bounded symbolic re-verification",
            "RQ4 Boundary-aware cost evidence": "RQ4  Boundary-aware cost evidence",
            "Claim-boundary synthesis and research priorities": "Claim-boundary synthesis and\nresearch priorities",
        }
        ax.text(
            x + width / 2,
            y,
            f'{wrap[label]}\n({row["section"]})',
            ha="center",
            va="center",
            fontsize=fontsize,
            fontweight="bold",
            color="#202124",
            linespacing=1.05,
        )

    def arrow(start: tuple[float, float], end: tuple[float, float], color: str = border) -> None:
        ax.add_patch(
            FancyArrowPatch(
                start,
                end,
                arrowstyle="-|>",
                mutation_scale=10,
                linewidth=1.05,
                color=color,
                shrinkA=0,
                shrinkB=0,
            )
        )

    ax.text(0.5, 0.982, "METHODS", ha="center", va="top", fontsize=7.2, fontweight="bold", color=rail)
    add_box(by_id["methods_search"], 0.10, 0.915, 0.80, 0.090, 7.2)
    add_box(by_id["methods_coding"], 0.17, 0.775, 0.66, 0.085, 7.2)
    arrow((0.5, 0.868), (0.5, 0.820))

    evidence_header_y, evidence_header_h = 0.690, 0.052
    ax.add_patch(
        FancyBboxPatch(
            (0.22, evidence_header_y - evidence_header_h / 2),
            0.56,
            evidence_header_h,
            boxstyle="round,pad=0.004,rounding_size=0.006",
            facecolor="white",
            edgecolor=rail,
            linewidth=0.7,
        )
    )
    ax.text(
        0.5,
        evidence_header_y,
        "EVIDENCE STREAMS\n(parallel analyses)",
        ha="center",
        va="center",
        fontsize=7.0,
        fontweight="bold",
        color=rail,
        linespacing=0.95,
    )
    arrow((0.5, 0.732), (0.5, evidence_header_y + evidence_header_h / 2 + 0.003))

    branch_x, branch_w, branch_h = 0.15, 0.70, 0.090
    branch_centers = [0.595, 0.470, 0.345, 0.220]
    branch_ids = ["rq1", "rq2", "rq3", "rq4"]
    left_rail_x, right_rail_x = 0.075, 0.925
    split_y, merge_y = 0.655, 0.142
    arrow((0.5, evidence_header_y - evidence_header_h / 2 - 0.003), (0.5, split_y), rail)
    ax.plot([0.5, left_rail_x], [split_y, split_y], color=rail, linewidth=1.0)
    ax.plot([left_rail_x, left_rail_x], [split_y, branch_centers[-1]], color=rail, linewidth=1.0)
    ax.plot([right_rail_x, right_rail_x], [branch_centers[0], merge_y], color=rail, linewidth=1.0)
    for node_id, cy in zip(branch_ids, branch_centers):
        add_box(by_id[node_id], branch_x, cy, branch_w, branch_h, 7.0)
        arrow((left_rail_x, cy), (branch_x - 0.006, cy), rail)
        arrow((branch_x + branch_w + 0.006, cy), (right_rail_x, cy), rail)

    synthesis_header_y, synthesis_header_h = 0.132, 0.038
    ax.add_patch(
        FancyBboxPatch(
            (0.35, synthesis_header_y - synthesis_header_h / 2),
            0.30,
            synthesis_header_h,
            boxstyle="round,pad=0.003,rounding_size=0.005",
            facecolor="white",
            edgecolor=rail,
            linewidth=0.7,
        )
    )
    ax.text(
        0.5,
        synthesis_header_y,
        "SYNTHESIS",
        ha="center",
        va="center",
        fontsize=7.2,
        fontweight="bold",
        color=rail,
    )
    arrow((right_rail_x, merge_y), (0.654, merge_y), rail)
    synthesis_y, synthesis_h = 0.054, 0.086
    arrow(
        (0.5, synthesis_header_y - synthesis_header_h / 2 - 0.003),
        (0.5, synthesis_y + synthesis_h / 2 + 0.003),
        rail,
    )
    add_box(by_id["synthesis"], 0.08, synthesis_y, 0.84, synthesis_h, 7.2)
    save_all(fig, "image9")


def validate_sources() -> None:
    totals = read_rows("verification_totals.csv")
    total_counts = np.array([int(row["count"]) for row in totals])
    family = read_rows("verification_by_family.csv")
    family_matrix = np.array(
        [[int(row[col]) for col in ("A", "B", "C", "D", "E")] for row in family]
    )
    if total_counts.sum() != 109:
        raise ValueError(f"Verification totals sum to {total_counts.sum()}, expected 109")
    if not np.array_equal(family_matrix.sum(axis=0), total_counts):
        raise ValueError("Family matrix column totals do not match verification totals")
    if not np.array_equal(family_matrix.sum(axis=1), np.array([57, 15, 9, 10, 7, 6, 5])):
        raise ValueError("Family matrix row totals do not match the taxonomy totals")
    workflow = read_rows("paper_structure.csv")
    expected_nodes = {"methods_search", "methods_coding", "rq1", "rq2", "rq3", "rq4", "synthesis"}
    if {row["node_id"] for row in workflow} != expected_nodes:
        raise ValueError("Evidence workflow must contain the two methods nodes, RQ1-RQ4, and synthesis")
    latency = read_rows("latency_profiles.csv")
    if [row["profile"] for row in latency] != ["Wired LAN", "Wi-Fi", "5G", "LTE-M", "NB-IoT", "GEO satellite"]:
        raise ValueError("Latency profiles are missing or out of manuscript order")


def main() -> None:
    validate_sources()
    make_image1()
    make_image4()
    make_image5()
    make_image6()
    make_image8()
    make_image9()
    print("Generated image1, image4, image5, image6, image8, and image9 (PNG/PDF/SVG).")


if __name__ == "__main__":
    main()
