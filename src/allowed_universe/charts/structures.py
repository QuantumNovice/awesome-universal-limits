"""Structure mass vs height."""

from __future__ import annotations

from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line

NAME = "structures"
DATASETS = ("structures",)

CATEGORIES = {
    "ancient": ("Ancient", 4),
    "tower": ("Towers", 5),
    "skyscraper": ("Skyscrapers", 1),
    "dam": ("Dams", 0),
}


def lines() -> list[Line]:
    return [
        Line(
            "concrete-crush",
            "Uniform concrete column crushes its own base (1.7 km)",
            "material",
            x=L.crushing_height(40e6, 2400),
            formula="sigma / (rho g), 40 MPa",
        ),
        Line(
            "steel-crush",
            "Uniform steel column yields (4.6 km)",
            "gravity",
            x=L.crushing_height(355e6, 7850),
            formula="sigma / (rho g), 355 MPa",
        ),
        Line(
            "solid-cube",
            "Solid concrete cube of that height (2,400 kg/m³)",
            "reference",
            y=lambda h: 2400 * h**3,
            formula="2400 h^3",
        ),
        Line(
            "solid-cone",
            "Solid concrete cone, base width = height",
            "reference",
            y=lambda h: 2400 * 3.141592653589793 * h**3 / 12,
            formula="2400 pi h^3 / 12",
        ),
    ]


def spec() -> ChartSpec:
    obj = loaders.to_objects(
        loaders.load("structures"), "height_m", "mass_low_kg", "mass_high_kg", "mass_example_kg", "mass_max_kg"
    )
    return ChartSpec(
        name=NAME,
        title="How heavy are the biggest structures?",
        xlabel="Height, m",
        ylabel="Mass, kg",
        xlim=(50, 6000),
        ylim=(1e5, 1e13),
        lines=lines(),
        objects=obj,
        categories=CATEGORIES,
        legend_loc="upper left",
        footnote="Skyscrapers are mostly air: the Empire State Building weighs about 1/400 of a solid concrete cube of its height.",
    )
