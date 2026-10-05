"""Black hole spin vs mass: every measured spin sits below a = 1."""

from __future__ import annotations

from allowed_universe import constants as k
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line

NAME = "black_holes"
DATASETS = ("black_holes",)

CATEGORIES = {
    "stellar": ("Stellar-mass (X-ray binaries)", 2),
    "merger": ("Merger remnants (gravitational waves)", 3),
    "supermassive": ("Supermassive", 5),
}


def lines() -> list[Line]:
    return [
        Line(
            "kerr",
            "a = 1: maximal Kerr spin",
            "upper",
            y=1.0,
            forbidden="Forbidden: a naked singularity (cosmic censorship)",
            forbidden_xy=(1e35, 1.05),
            formula="a = J c / (G M^2) <= 1",
        ),
        Line(
            "thorne",
            "Thorne limit a = 0.998: accretion cannot spin a hole faster",
            "material",
            y=0.998,
            formula="0.998",
            source_url="https://doi.org/10.1086/152991",
            citation="Thorne K.S. (1974) Disk-accretion onto a black hole. II. Evolution of the hole. ApJ 191, 507",
        ),
    ]


def spec() -> ChartSpec:
    obj = loaders.to_objects(
        loaders.load("black_holes"), "mass_kg", "spin_low_a", "spin_high_a", "spin_example_a", "spin_max_a"
    )
    return ChartSpec(
        name=NAME,
        title="How fast do black holes spin?",
        xlabel="Mass, kg",
        ylabel="Spin parameter a = Jc/GM²",
        xlim=(1e30, 1e41),
        ylim=(0, 1.1),
        yscale="linear",
        lines=lines(),
        objects=obj,
        categories=CATEGORIES,
        legend_loc="lower right",
        range_label="Measured spin (range or lower limit)",
        secondary_x=("Mass, solar masses", lambda kg: kg / k.M_SUN, lambda m: m * k.M_SUN),
    )
