"""Chart 4: temperature vs size."""

from __future__ import annotations

from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line
from allowed_universe.style import PHYSICS_CATEGORIES

NAME = "temperature"
DATASETS = ("temperature",)


def lines() -> list[Line]:
    return [
        Line(
            "planck",
            "Planck temperature (1.4×10³² K)",
            "upper",
            y=L.temperature_planck(),
            forbidden="Forbidden: beyond the Planck temperature",
            forbidden_xy=(1e-8, 1.5e33),
            formula="sqrt(hbar c^5 / G) / k_B",
        ),
        Line(
            "collapse",
            "Black-body radiation this hot, filling the object, would form a black hole",
            "gravity",
            y=L.temperature_collapse,
            formula="(3 c^4 / (2 pi G a d^2))^(1/4)",
        ),
        Line(
            "melting",
            "No known solid survives above ~4,200 K (HfC)",
            "material",
            y=4232.0,
            formula="4232 K",
            source_url="https://doi.org/10.1038/srep37962",
            citation="Cedillos-Barraza O. et al. (2016) Investigating the highest melting temperature materials: a laser melting study of the TaC-HfC system. Sci Rep 6, 37962",
        ),
        Line(
            "hawking",
            "Hawking temperature of a black hole of this size",
            "reference",
            y=L.temperature_hawking,
            formula="hbar c / (2 pi k_B d)",
            source_url="https://doi.org/10.1007/BF02345020",
            citation="Hawking S.W. (1975) Particle creation by black holes. Commun Math Phys 43, 199",
        ),
    ]


def spec() -> ChartSpec:
    obj = loaders.to_objects(
        loaders.load("temperature"),
        "size_m",
        "temperature_low_k",
        "temperature_high_k",
        "temperature_example_k",
        "temperature_max_k",
    )
    return ChartSpec(
        name=NAME,
        title="How hot and how cold can things be?",
        xlabel="Size, m",
        ylabel="Temperature, K",
        xlim=(1e-20, 1e28),
        ylim=(1e-22, 1e35),
        lines=lines(),
        objects=obj,
        categories=PHYSICS_CATEGORIES,
        legend_loc="upper right",
        legend_bbox=(1.0, 0.94),
        cap_label="Survival limit",
        footnote="Absolute zero (0 K) lies infinitely far below on a log axis: it can be approached but never reached.",
    )
