"""Materials: tensile strength vs density (an Ashby chart with a relativistic ceiling)."""

from __future__ import annotations

from allowed_universe import constants as k
from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line

NAME = "materials"
DATASETS = ("materials",)

CATEGORIES = {
    "natural": ("Natural materials", 0),
    "metal": ("Metals", 1),
    "nano": ("Nanomaterials", 2),
    "polymer": ("Polymer fibres", 3),
    "ceramic": ("Ceramics", 4),
    "fibre": ("Glass and carbon fibres", 5),
}


def lines() -> list[Line]:
    elevator = L.space_elevator_specific_strength()
    return [
        Line(
            "energy-condition",
            "Dominant energy condition: σ ≤ ρc²",
            "upper",
            y=L.strength_energy_condition,
            forbidden="Forbidden: tension greater than the energy density of the material",
            forbidden_xy=(2.5e3, 1e21),
            formula="rho c^2",
        ),
        Line(
            "rim-3km",
            "Characteristic speed √(σ/ρ) = 3 km/s (spin-chart rim limit)",
            "material",
            y=lambda rho: L.strength_for_speed(rho, k.V_RIM_MATERIAL),
            formula="rho (3 km/s)^2",
        ),
        Line(
            "space-elevator",
            f"Uniform cable to geostationary orbit: σ/ρ = {elevator / 1e6:.0f} MJ/kg",
            "gravity",
            y=lambda rho: rho * elevator,
            formula="GM(1/R - 1/R_geo) - omega^2 (R_geo^2 - R^2) / 2",
        ),
    ]


def spec() -> ChartSpec:
    obj = loaders.to_objects(
        loaders.load("materials"),
        "density_kg_m3",
        "strength_low_pa",
        "strength_high_pa",
        "strength_example_pa",
        "strength_max_pa",
    )
    return ChartSpec(
        name=NAME,
        title="How strong can a material be?",
        xlabel="Density, kg/m³",
        ylabel="Tensile strength, Pa",
        xlim=(500, 2e4),
        ylim=(1e7, 1e22),
        lines=lines(),
        objects=obj,
        categories=CATEGORIES,
        legend_loc="center right",
        footnote="Everyday materials sit ten orders of magnitude below the relativistic ceiling.",
    )
