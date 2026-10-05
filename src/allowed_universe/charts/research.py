"""Limits of a researcher: how much can one person read, write and collaborate with?"""

from __future__ import annotations

from allowed_universe import limits as L
from allowed_universe.charts._bars import BarLine, BarPanel, BarSpec, render_bars

NAME = "research"
DATASETS = ("research",)

CATEGORIES = {
    "person": ("One researcher", 1),
    "record": ("Records", 2),
    "world": ("Whole literature", 0),
    "social": ("Cognitive limit", 4),
}

HOURS_PER_PAPER = 1.0


def bars() -> BarSpec:
    ceiling = L.reading_ceiling(HOURS_PER_PAPER)
    return BarSpec(
        name=NAME,
        title="Limits of a researcher",
        dataset="research",
        categories=CATEGORIES,
        panels=[
            BarPanel(
                "papers",
                "a. The reading gap",
                "Papers per year",
                (10, 1e8),
                lines=[BarLine(ceiling, f"One reader, 1 hour per paper, no sleep ({ceiling:,.0f} papers/yr)", "upper")],
                height=5,
            ),
            BarPanel("team", "b. Collaboration size", "People", (10, 1e5), height=4),
        ],
        footnote="A full-time reader could cover about 0.3% of one year's literature.",
    )


def render():
    return render_bars(bars())
