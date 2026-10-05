"""Reported AI benchmark scores over time, one small multiple per benchmark.

Same three layers as the physics charts: a hard ceiling (100 percent, or the
label-noise ceiling where one is measured), reference levels (chance, human),
and the reported results as points joined in time order.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from allowed_universe import loaders, style
from allowed_universe.labels import LabelRequest, place_labels

NAME = "ai_benchmarks"
DATASETS = ("ai_benchmarks", "ai_benchmark_refs")

PANELS = [
    ("imagenet", "ImageNet classification (top-5)"),
    ("mmlu", "MMLU (57 academic subjects)"),
    ("gsm8k", "GSM8K (grade-school maths)"),
    ("gpqa", "GPQA (graduate science, Diamond)"),
    ("swebench", "SWE-bench Verified (real GitHub issues)"),
    ("arcagi", "ARC-AGI-1 (abstract puzzles)"),
]
XLIM = (2010, 2026.3)
TITLE = "How close are AI systems to the ceiling of their benchmarks?"


def render():
    style.apply()
    scores = loaders.load("ai_benchmarks")
    refs = loaders.load("ai_benchmark_refs")
    fig, axes = plt.subplots(2, 3, figsize=style.FIGSIZE, sharey=True)
    color, marker = style.SLOTS[2]
    for ax, (bench, title) in zip(axes.flat, PANELS, strict=False):
        ax.set_xlim(*XLIM)
        ax.set_ylim(0, 108)
        ax.set_title(title, fontsize=13)
        ax.axhline(100, color=style.RED, lw=2.5, zorder=3)
        ax.axhspan(100, 108, color=style.RED, alpha=0.10, lw=0)
        zone = ax.text(2010.4, 104, "Forbidden: above 100%", style="italic", fontsize=9, va="center")
        for _, r in refs[refs["benchmark"] == bench].iterrows():
            if r["level"] == "chance":
                ax.axhline(r["score_pct"], color=style.BLUE, lw=2.0, ls="--", zorder=3)
                ax.axhspan(0, r["score_pct"], color=style.BLUE, alpha=0.08, lw=0)
            elif r["level"] == "human":
                ax.axhline(r["score_pct"], color=style.GREY, lw=1.6, ls="--", zorder=3)
            else:
                ax.axhline(r["score_pct"], color=style.AMBER, lw=1.8, ls=":", zorder=3)
        s = scores[scores["benchmark"] == bench].sort_values("year")
        ax.plot(s["year"], s["score_pct"], color=color, lw=1.2, zorder=4)
        ax.plot(s["year"], s["score_pct"], marker=marker, ms=7, color=color, mec="white", ls="none", zorder=5)
        reqs = [LabelRequest(x, y, m) for x, y, m in zip(s["year"], s["score_pct"], s["model"], strict=False)]
        ax.figure.canvas.draw()
        renderer = ax.figure.canvas.get_renderer()
        place_labels(ax, reqs, fontsize=8, extra_obstacles=[zone.get_window_extent(renderer)])
        ax.grid(True)
    for ax in axes[:, 0]:
        ax.set_ylabel("Reported score, %")
    for ax in axes[1, :]:
        ax.set_xlabel("Year reported")
    handles = [
        Line2D([], [], color=style.RED, lw=2.5, label="Perfect score (hard ceiling)"),
        Line2D([], [], color=style.AMBER, lw=1.8, ls=":", label="Label-error ceiling (MMLU)"),
        Line2D([], [], color=style.GREY, lw=1.6, ls="--", label="Human baseline"),
        Line2D([], [], color=style.BLUE, lw=2.0, ls="--", label="Random guessing"),
        Line2D([], [], color=color, marker=marker, ms=7, mec="white", label="Reported result"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=5, frameon=False, bbox_to_anchor=(0.5, -0.005))
    fig.suptitle(TITLE, fontsize=17)
    fig.tight_layout(rect=(0, 0.04, 1, 0.97))
    fig.text(
        0.01,
        -0.005,
        "Scores are as reported by the authors or developers; settings differ (see data/ai_benchmarks.csv).",
        fontsize=9,
        color="#333333",
    )
    return fig
