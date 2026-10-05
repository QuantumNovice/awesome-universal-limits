"""Pressure vs size: from interstellar gas to the inside of a proton."""

from __future__ import annotations

from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line

NAME = "pressure"
DATASETS = ("pressure",)

CATEGORIES = {
    "particle": ("Particles", 4),
    "lab": ("Laboratory records", 5),
    "earth": ("Planets", 1),
    "astro": ("Stars and space", 2),
}


def lines() -> list[Line]:
    return [
        Line(
            "black-hole",
            "Pressure of black-hole-density matter at the energy-condition limit: 3c⁴/(2πGd²)",
            "upper",
            y=L.pressure_black_hole,
            forbidden="Forbidden: more pressure than a black hole of that size holds",
            forbidden_xy=(1e-6, 1e60),
            formula="3 c^4 / (2 pi G d^2)",
        ),
        Line(
            "atm",
            "Sea-level atmosphere (101,325 Pa)",
            "reference",
            y=101325.0,
            formula="1 atm",
        ),
    ]


def spec() -> ChartSpec:
    obj = loaders.to_objects(
        loaders.load("pressure"),
        "size_m",
        "pressure_low_pa",
        "pressure_high_pa",
        "pressure_example_pa",
        "pressure_max_pa",
    )
    return ChartSpec(
        name=NAME,
        title="How much pressure can matter take?",
        xlabel="Size, m",
        ylabel="Pressure, Pa",
        xlim=(1e-16, 1e18),
        ylim=(1e-16, 1e80),
        lines=lines(),
        objects=obj,
        categories=CATEGORIES,
        legend_loc="upper right",
    )
