"""Stored energy per kilogram, from pumped hydro to black-hole accretion, against E = mc^2."""

from __future__ import annotations

from allowed_universe import limits as L
from allowed_universe.charts._bars import BarLine, BarPanel, BarSpec, render_bars

NAME = "energy_density"
DATASETS = ("energy_density",)

CATEGORIES = {
    "gravitational": ("Gravitational", 4),
    "electrochemical": ("Batteries and capacitors", 1),
    "chemical": ("Chemical fuels", 0),
    "nuclear": ("Nuclear and gravitational collapse", 2),
    "mechanical": ("Mechanical", 5),
}


def bars() -> BarSpec:
    return BarSpec(
        name=NAME,
        title="How much energy can a kilogram hold?",
        dataset="energy_density",
        categories=CATEGORIES,
        panels=[
            BarPanel(
                "store",
                "",
                "Specific energy, J/kg",
                (1e2, 1e18),
                lines=[
                    BarLine(L.specific_energy_mc2(), "E = mc\u00b2: all of the mass turned into energy", "upper"),
                ],
            )
        ],
        footnote="Batteries hold about a millionth of what uranium fission releases, and a hundred-billionth of mc\u00b2.",
    )


def render():
    return render_bars(bars())
