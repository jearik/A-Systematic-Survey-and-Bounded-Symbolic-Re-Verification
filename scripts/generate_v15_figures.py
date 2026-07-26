#!/usr/bin/env python3
"""Generate synchronized final manuscript figures from the validated 108-row table.

Figure contract
---------------
Core conclusion: mechanism, deployment facets, and verification evidence are
distinct coding dimensions; ledger presence is much broader than ledger as the
dominant trust-establishment mechanism.
Archetype: quantitative grid (Figs. 4-6). Fig. 3 is generated independently by
``manuscript_figures/generate_fig3_prisma.py`` from its declared count table.
Target/output: IEEE two-column manuscript; Python/matplotlib only; editable SVG,
PDF, and 600-dpi PNG with source-data CSVs.
Reviewer risks: denominator drift, facet double counting, illegible labels, and
misreading A-E as a technology hierarchy.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Liberation Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["font.size"] = 7
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.linewidth"] = 0.8

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data" / "S1_ROWLEVEL_CODING_INCLUDED_108.csv"
OUT = HERE.parent / "figures" / "regenerated"
OUT.mkdir(exist_ok=True)

ORDER = [
    "Ledger-mediated trust",
    "Certificateless split-key",
    "Zero-knowledge/privacy credential",
    "Other/classical-general",
    "Hardware-/device-rooted",
    "Group-/ring-signature",
    "Post-quantum",
]
SHORT = {
    "Ledger-mediated trust": "Ledger-mediated trust",
    "Certificateless split-key": "Certificateless split-key",
    "Zero-knowledge/privacy credential": "ZK / privacy credential",
    "Other/classical-general": "Other / classical-general",
    "Hardware-/device-rooted": "Hardware-/device-rooted",
    "Group-/ring-signature": "Group-/ring-signature",
    "Post-quantum": "Post-quantum",
}
PALETTE = ["#0F4D92", "#3775BA", "#42949E", "#9A4D8E", "#C49A52", "#7884B4", "#B64342"]
LEVEL_COLORS = ["#0F4D92", "#3775BA", "#7FAFC4", "#C49A52", "#B64342"]


def rows() -> list[dict[str, str]]:
    with DATA.open("r", encoding="utf-8-sig", newline="") as f:
        data = list(csv.DictReader(f))
    assert len(data) == 108
    return data


def save(fig, stem: str) -> None:
    for ext, kwargs in {
        "svg": {},
        "pdf": {},
        "png": {"dpi": 600},
    }.items():
        fig.savefig(OUT / f"{stem}.{ext}", bbox_inches="tight", facecolor="white", **kwargs)
    plt.close(fig)


def write_source(stem: str, fields: list[str], data: list[dict[str, object]]) -> None:
    with (OUT / f"{stem}_source.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(data)


def figure4(data: list[dict[str, str]]) -> None:
    family = Counter(r["mechanism_family"] for r in data)
    levels = Counter(r["verification_level"] for r in data)
    facet_order = ["ledger-present", "privacy/anonymity-layer", "edge/fog-mediated", "multi-ledger", "no-ledger"]
    facet_labels = ["ledger present", "privacy / anonymity", "edge / fog mediated", "multi-ledger", "no ledger"]
    facets = Counter()
    for r in data:
        facets.update(x.strip() for x in r["deployment_crosscutting_facets"].split(";") if x.strip())

    fig, axes = plt.subplots(3, 1, figsize=(3.3, 5.45), gridspec_kw={"height_ratios": [1.4, 1.05, 0.85]})
    ax = axes[0]
    vals = [family[f] for f in ORDER]
    y = np.arange(len(ORDER))[::-1]
    ax.barh(y, vals, color=PALETTE, edgecolor="#314C69", linewidth=0.5)
    ax.set_yticks(y, [SHORT[f] for f in ORDER], fontsize=5.4)
    ax.set_xlabel("Primary studies", fontsize=6.5)
    ax.set_xlim(0, 64)
    for yi, v in zip(y, vals): ax.text(v + 0.8, yi, str(v), va="center", fontsize=6)
    ax.set_title("a  Primary mechanism\n(single assignment)", loc="left", fontweight="bold", fontsize=7)

    ax = axes[1]
    fvals = [facets[f] for f in facet_order]
    y2 = np.arange(len(facet_order))[::-1]
    ax.barh(y2, fvals, color="#7FA1BA", edgecolor="#314C69", linewidth=0.5)
    ax.set_yticks(y2, facet_labels, fontsize=5.4)
    ax.set_xlabel("Studies with facet", fontsize=6.5)
    ax.set_xlim(0, 112)
    for yi, v in zip(y2, fvals): ax.text(v + 1.0, yi, str(v), va="center", fontsize=6)
    ax.set_title("b  Deployment / cross-cutting\n(non-exclusive)", loc="left", fontweight="bold", fontsize=7)

    ax = axes[2]
    lev = [levels[x] for x in "ABCDE"]
    ax.bar(range(5), lev, color=LEVEL_COLORS, edgecolor="#314C69", linewidth=0.5)
    ax.set_xticks(range(5), list("ABCDE"), fontsize=6)
    ax.set_ylabel("Studies", fontsize=6.5)
    ax.set_ylim(0, 41)
    for i, v in enumerate(lev): ax.text(i, v + 0.7, str(v), ha="center", fontsize=6)
    ax.set_title("c  Verification evidence\n(orthogonal)", loc="left", fontweight="bold", fontsize=7)
    fig.suptitle("Three-dimensional classification of 108 primary studies", fontsize=7.5, y=1.005)
    fig.tight_layout(h_pad=0.9)
    save(fig, "figure4_taxonomy_3D_108_corrected")

    source = []
    for f in ORDER: source.append({"panel": "mechanism", "category": f, "count": family[f]})
    for f in facet_order: source.append({"panel": "facet", "category": f, "count": facets[f]})
    for f in "ABCDE": source.append({"panel": "verification", "category": f, "count": levels[f]})
    write_source("figure4_taxonomy_3D_108_corrected", ["panel", "category", "count"], source)


def figure5(data: list[dict[str, str]]) -> None:
    levels = Counter(r["verification_level"] for r in data)
    vals = [levels[x] for x in "ABCDE"]
    labels = ["A\nSymbolic tool", "B\nComputational", "C\nBAN logic", "D\nFormal, untooled", "E\nInformal"]
    fig, ax = plt.subplots(figsize=(3.3, 2.15))
    bars = ax.bar(range(5), vals, color=LEVEL_COLORS, edgecolor="#314C69", linewidth=0.7)
    ax.set_xticks(range(5), labels, fontsize=5.2)
    ax.set_ylabel("Primary studies (n = 108)", fontsize=6)
    ax.set_ylim(0, 41)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, v + 0.7, f"{v}\n({100*v/108:.1f}%)", ha="center", fontsize=5.5)
    ax.set_title("Strongest reported verification evidence", loc="left", fontweight="bold", fontsize=7)
    fig.tight_layout()
    save(fig, "figure5_verification_distribution_108_corrected")
    write_source("figure5_verification_distribution_108_corrected", ["level", "count", "share_pct"],
                 [{"level": k, "count": levels[k], "share_pct": round(100*levels[k]/108, 1)} for k in "ABCDE"])


def figure6(data: list[dict[str, str]]) -> None:
    matrix = np.array([[sum(r["mechanism_family"] == f and r["verification_level"] == l for r in data)
                        for l in "ABCDE"] for f in ORDER])
    totals = [sum(r["mechanism_family"] == f for r in data) for f in ORDER]
    fig, ax = plt.subplots(figsize=(3.3, 3.05))
    im = ax.imshow(matrix, cmap="Blues", aspect="auto", vmin=0, vmax=matrix.max())
    ax.set_xticks(range(5), ["A tool", "B proof", "C BAN", "D formal", "E informal"],
                  rotation=20, ha="right", fontsize=5.2)
    ax.set_yticks(range(len(ORDER)), [f"{SHORT[f]} ({n})" for f, n in zip(ORDER, totals)], fontsize=5.0)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            v = matrix[i, j]
            ax.text(j, i, str(v), ha="center", va="center", fontsize=6,
                    color="white" if v >= 11 else "#1F3D5A")
    cbar = fig.colorbar(im, ax=ax, shrink=0.82, pad=0.025)
    cbar.set_label("Studies", fontsize=6.5)
    cbar.ax.tick_params(labelsize=6)
    ax.set_title("Mechanism family x verification evidence (n = 108)", loc="left",
                 fontweight="bold", fontsize=6.8)
    fig.tight_layout()
    save(fig, "figure6_family_x_verification_108_corrected")
    src = []
    for i, f in enumerate(ORDER):
        for j, l in enumerate("ABCDE"):
            src.append({"family": f, "level": l, "count": int(matrix[i, j])})
    write_source("figure6_family_x_verification_108_corrected", ["family", "level", "count"], src)


def main() -> None:
    data = rows()
    figure4(data)
    figure5(data)
    figure6(data)
    print(OUT)


if __name__ == "__main__":
    main()
