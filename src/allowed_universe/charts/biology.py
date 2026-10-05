"""Living things: mass vs length, from proteins to the largest organisms.

Biology has no hard bound of its own on this chart (the physics bounds of the mass
chart sit dozens of decades away), so only practical limits are drawn.
"""

from __future__ import annotations

from allowed_universe import constants as k
from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line

NAME = "biology"
DATASETS = ("biology",)

CATEGORIES = {
    "molecule": ("Biomolecules", 4),
    "virus": ("Viruses", 5),
    "cell": ("Single cells", 0),
    "animal": ("Animals", 1),
    "plant": ("Plants", 2),
    "fungus": ("Fungi", 3),
}


def lines() -> list[Line]:
    return [
        Line(
            "water-sphere",
            "Water-density sphere: M = ρπL³/6",
            "reference",
            y=lambda d: L.mass_at_density(d, k.RHO_WATER),
            formula="1000 pi L^3 / 6",
        ),
        Line(
            "min-cell",
            "Smallest viable free-living cell (~250 nm)",
            "material",
            x=2.5e-7,
            formula="d ~ 250 nm",
            source_url="https://doi.org/10.17226/9638",
            citation="National Research Council (1999) Size Limits of Very Small Microorganisms: Proceedings of a Workshop. National Academies Press",
        ),
        Line(
            "tree-height",
            "Hydraulic limit to tree height (122-130 m)",
            "gravity",
            x=130.0,
            formula="water column tension vs gravity",
            source_url="https://doi.org/10.1038/nature02417",
            citation="Koch G.W. et al. (2004) The limits to tree height. Nature 428, 851",
        ),
    ]


def spec() -> ChartSpec:
    obj = loaders.to_objects(
        loaders.load("biology"), "length_m", "mass_low_kg", "mass_high_kg", "mass_example_kg", "mass_max_kg"
    )
    return ChartSpec(
        name=NAME,
        title="How small and how big can living things be?",
        xlabel="Length (largest dimension), m",
        ylabel="Mass, kg",
        xlim=(1e-9, 1e4),
        ylim=(1e-24, 1e8),
        lines=lines(),
        objects=obj,
        categories=CATEGORIES,
        legend_loc="upper left",
        footnote="Left of the cell line sit parts of life (molecules, viruses) that cannot copy themselves alone.",
    )
