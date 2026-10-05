"""Chart 5: density vs size."""

from __future__ import annotations

import math

from allowed_universe import constants as k
from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line
from allowed_universe.style import PHYSICS_CATEGORIES

NAME = "density"
DATASETS = ("density",)

RHO_CRIT = 3 * k.H0**2 / (8 * math.pi * k.G)


def lines() -> list[Line]:
    return [
        Line(
            "black-hole",
            "Black hole: ρ = 3c² / (2πGd²)",
            "upper",
            y=L.density_black_hole,
            forbidden="Forbidden: denser than a black hole of that size",
            forbidden_xy=(1e8, 1e45),
            formula="3 c^2 / (2 pi G d^2)",
        ),
        Line(
            "nuclear",
            "Nuclear density (2.7×10¹⁷ kg/m³)",
            "gravity",
            y=k.RHO_NUCLEAR,
            formula="0.16 fm^-3 x m_n",
            source_url="https://doi.org/10.1016/j.adt.2011.12.006",
            citation="Angeli I. & Marinova K.P. (2013) Table of experimental nuclear ground state charge radii: an update. ADNDT 99, 69",
        ),
        Line(
            "critical",
            "Mean density of the universe (critical density)",
            "reference",
            y=RHO_CRIT,
            formula="3 H0^2 / (8 pi G)",
            source_url="https://doi.org/10.1051/0004-6361/201833910",
            citation="Planck Collaboration (2020) Planck 2018 results. VI. A&A 641, A6",
        ),
    ]


def spec() -> ChartSpec:
    obj = loaders.to_objects(
        loaders.load("density"),
        "size_m",
        "density_low_kg_m3",
        "density_high_kg_m3",
        "density_example_kg_m3",
        "density_max_kg_m3",
    )
    return ChartSpec(
        name=NAME,
        title="How dense can things be?",
        xlabel="Size, m",
        ylabel="Density, kg/m³",
        xlim=(1e-18, 1e28),
        ylim=(1e-32, 1e60),
        lines=lines(),
        objects=obj,
        categories=PHYSICS_CATEGORIES,
        legend_loc="lower left",
    )
