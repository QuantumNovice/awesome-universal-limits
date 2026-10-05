"""Electricity: voltage held across a gap of a given size."""

from __future__ import annotations

from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line

NAME = "voltage"
DATASETS = ("voltage",)

CATEGORIES = {
    "atomic": ("Atoms", 4),
    "living": ("Living things", 0),
    "human": ("Human-made", 1),
    "earth": ("Earth", 5),
    "astro": ("Astronomical", 2),
}


def lines() -> list[Line]:
    return [
        Line(
            "planck",
            "Planck voltage c²/√(4πε₀G) ≈ 1.0×10²⁷ V: a charged body at this potential is a black hole",
            "upper",
            y=L.PLANCK_VOLTAGE,
            forbidden="Forbidden: the field's own energy collapses into a black hole",
            forbidden_xy=(1e1, 3e27),
            forbidden_rotation=0,
            formula="c^2 / sqrt(4 pi eps0 G)",
            source_url="https://doi.org/10.1002/andp.19163550905",
            citation="Reissner H. (1916) Uber die Eigengravitation des elektrischen Feldes nach der Einsteinschen Theorie. Ann Phys 355, 106",
        ),
        Line(
            "schwinger",
            "Schwinger field 1.3×10¹⁸ V/m across the gap",
            "upper",
            y=lambda d: L.voltage_for_field(d, L.E_SCHWINGER),
            forbidden="Forbidden for static fields: the vacuum breaks down into electron-positron pairs",
            forbidden_xy=(1e-4, 1e19),
            formula="E_S d",
            source_url="https://doi.org/10.1103/PhysRev.82.664",
            citation="Schwinger J. (1951) On gauge invariance and vacuum polarization. Phys Rev 82, 664",
        ),
        Line(
            "air",
            "Air breakdown 3 MV/m (sparks and lightning)",
            "material",
            y=lambda d: L.voltage_for_field(d, L.E_AIR_BREAKDOWN),
            formula="3e6 d",
        ),
    ]


def spec() -> ChartSpec:
    obj = loaders.to_objects(
        loaders.load("voltage"), "gap_m", "voltage_low_v", "voltage_high_v", "voltage_example_v", "voltage_max_v"
    )
    return ChartSpec(
        name=NAME,
        title="How much voltage can a gap hold?",
        xlabel="Gap size, m",
        ylabel="Voltage, V",
        xlim=(1e-11, 1e14),
        ylim=(1e-9, 1e28),
        lines=lines(),
        objects=obj,
        categories=CATEGORIES,
        legend_loc="lower right",
        footnote="Nerve membranes hold 10 million V/m, three times the field that makes air spark. Beyond 10⁹ m gaps, gravity (not QED) caps the voltage.",
    )
