"""Gas and water volumes: mass vs volume, with density lines and the black-hole bound."""

from __future__ import annotations

from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line

NAME = "volumes"
DATASETS = ("volumes",)

CATEGORIES = {
    "gas": ("Gas", 5),
    "water": ("Liquid water", 0),
    "ice": ("Ice", 4),
}


def lines() -> list[Line]:
    return [
        Line(
            "black-hole",
            "Black hole of that volume: M = c²d/(4G), d = (6V/π)^(1/3)",
            "upper",
            y=L.mass_black_hole_volume,
            forbidden="Forbidden: it would collapse into a black hole",
            forbidden_xy=(1e10, 1e50),
            formula="c^2 (6V/pi)^(1/3) / (4 G)",
        ),
        Line(
            "water",
            "Water (1,000 kg/m³)",
            "material",
            y=lambda v: 1000 * v,
            formula="1000 V",
        ),
        Line(
            "air",
            "Air at sea level (1.225 kg/m³)",
            "reference",
            y=lambda v: 1.225 * v,
            formula="1.225 V",
            source_url="https://ntrs.nasa.gov/citations/19770009539",
            citation="NOAA/NASA/USAF (1976) U.S. Standard Atmosphere, 1976",
        ),
    ]


def spec() -> ChartSpec:
    obj = loaders.to_objects(
        loaders.load("volumes"), "volume_m3", "mass_low_kg", "mass_high_kg", "mass_example_kg", "mass_max_kg"
    )
    return ChartSpec(
        name=NAME,
        title="How much do gas and water weigh?",
        xlabel="Volume, m³",
        ylabel="Mass, kg",
        xlim=(1e-6, 1e56),
        ylim=(1e-6, 1e70),
        lines=lines(),
        objects=obj,
        categories=CATEGORIES,
        legend_loc="lower right",
        footnote="The atmosphere is plotted at the volume it would fill at sea-level density; a molecular cloud is 10¹⁹ times thinner than air.",
    )
