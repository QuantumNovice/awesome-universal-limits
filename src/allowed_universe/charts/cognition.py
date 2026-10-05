"""Human cognitive limits: information rates and memory/social capacities."""

from __future__ import annotations

from allowed_universe import limits as L
from allowed_universe.charts._bars import BarLine, BarPanel, BarSpec, fmt, render_bars

NAME = "cognition"
DATASETS = ("cognition",)

CATEGORIES = {
    "behaviour": ("Conscious behaviour", 1),
    "language": ("Language", 3),
    "sensory": ("Senses", 0),
    "memory": ("Memory", 2),
    "social": ("Social", 4),
    "physics": ("Brain hardware", 5),
}

BRAIN_POWER_W = 20.0  # Raichle & Gusnard (2002)
BODY_T_K = 310.0


def landauer_rate() -> float:
    """Bits per second a 20 W brain at 310 K could erase at the Landauer limit."""
    return L.landauer_bit_rate(BRAIN_POWER_W, BODY_T_K)


def bars() -> BarSpec:
    lim = landauer_rate()
    return BarSpec(
        name=NAME,
        title="Limits of the human mind",
        dataset="cognition",
        categories=CATEGORIES,
        panels=[
            BarPanel(
                "rate",
                "a. How fast do we process?",
                "Information rate, bits per second",
                (1, 1e23),
                lines=[
                    BarLine(
                        lim,
                        f"Landauer limit for a 20 W brain at 310 K ({fmt(lim)} bits/s)",
                        "upper",
                        source_url="https://doi.org/10.1147/rd.53.0183",
                        citation="Landauer R. (1961) Irreversibility and heat generation in the computing process. IBM J Res Dev 5, 183",
                    )
                ],
                height=4,
            ),
            BarPanel("capacity", "b. How much can we hold?", "Count", (1, 1e16), height=8),
        ],
        footnote="Behaviour runs near 10 bits/s while the senses deliver about 10⁹ bits/s: a gap of eight orders of magnitude.",
    )


EXTRA_SOURCES = [
    (
        "https://doi.org/10.1073/pnas.172399499",
        "Raichle M.E. & Gusnard D.A. (2002) Appraising the brain's energy budget. PNAS 99, 10237",
    ),
]


def render():
    return render_bars(bars())
