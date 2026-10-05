"""Magnetic field vs size, from brain signals to magnetars."""

from __future__ import annotations

from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line

NAME = "magnetic"
DATASETS = ("magnetic",)

CATEGORIES = {
    "living": ("Living things", 0),
    "lab": ("Laboratory records", 5),
    "earth": ("Earth", 1),
    "astro": ("Astronomical", 2),
}


def lines() -> list[Line]:
    return [
        Line(
            "collapse",
            "Field energy would form a black hole: B = √(3μ₀/πG) c²/d",
            "upper",
            y=L.field_collapse,
            forbidden="Forbidden: the field's own energy collapses into a black hole",
            forbidden_xy=(1e14, 1e19),
            formula="sqrt(3 mu0 / (pi G)) c^2 / d",
        ),
        Line(
            "quantum",
            "Quantum critical field 4.4×10⁹ T",
            "gravity",
            y=L.B_QUANTUM,
            formula="m_e^2 c^2 / (e hbar)",
        ),
        Line(
            "lab-dc",
            "Strongest steady laboratory field (45.5 T)",
            "material",
            y=45.5,
            formula="45.5 T",
            source_url="https://doi.org/10.1038/s41586-019-1293-1",
            citation="Hahn S. et al. (2019) 45.5-tesla direct-current magnetic field generated with a high-temperature superconducting magnet. Nature 570, 496",
        ),
    ]


def spec() -> ChartSpec:
    obj = loaders.to_objects(
        loaders.load("magnetic"), "size_m", "field_low_t", "field_high_t", "field_example_t", "field_max_t"
    )
    return ChartSpec(
        name=NAME,
        title="How strong can a magnetic field be?",
        xlabel="Size of the magnetised region, m",
        ylabel="Magnetic field, T",
        xlim=(1e-16, 1e24),
        ylim=(1e-22, 1e30),
        lines=lines(),
        objects=obj,
        categories=CATEGORIES,
        legend_loc="center right",
        footnote="Above 4.4×10⁹ T an electron's cyclotron energy exceeds its rest energy; magnetars live there.",
    )
