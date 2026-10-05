"""The scale of numbers: counts from people to Planck volumes, against the holographic bound."""

from __future__ import annotations

from allowed_universe import limits as L
from allowed_universe.charts._bars import BarLine, BarPanel, BarSpec, fmt, render_bars

NAME = "numbers"
DATASETS = ("numbers",)

CATEGORIES = {
    "life": ("Life", 0),
    "earth": ("Earth", 5),
    "cosmos": ("Cosmos", 2),
    "games": ("Games", 1),
    "physics": ("Physics", 4),
}


def bars() -> BarSpec:
    holo = L.holographic_bits(L.OBSERVABLE_RADIUS)
    return BarSpec(
        name=NAME,
        title="How big do numbers get?",
        dataset="numbers",
        categories=CATEGORIES,
        panels=[
            BarPanel(
                "count",
                "",
                "Count",
                (1e8, 1e190),
                lines=[
                    BarLine(
                        holo,
                        f"Holographic bound: most bits the observable universe can hold ({fmt(holo)})",
                        "gravity",
                        shade=False,
                        source_url="https://doi.org/10.1088/0004-637X/710/2/1825",
                        citation="Egan C.A. & Lineweaver C.H. (2010) A larger estimate of the entropy of the universe. ApJ 710, 1825",
                    )
                ],
            )
        ],
        footnote="Numbers right of the dashed line can be named and counted, but never all written down in this universe.",
    )


def render():
    return render_bars(bars())
