"""Electric charge vs size."""

from __future__ import annotations

from allowed_universe import constants as k
from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line

NAME = "charge"
DATASETS = ("charge",)

CATEGORIES = {
    "particle": ("Particles and nuclei", 4),
    "lab": ("Laboratory and everyday", 5),
    "earth": ("Earth and lightning", 0),
    "astro": ("Space", 2),
}


def lines() -> list[Line]:
    return [
        Line(
            "elementary",
            "One elementary charge e (free charges come in whole units)",
            "lower",
            y=k.e,
            forbidden="Forbidden: less than one elementary charge",
            forbidden_xy=(1e0, 1e-22),
            formula="e",
            source_url="https://physics.nist.gov/cuu/Constants/",
            citation="Tiesinga E. et al., CODATA 2022 recommended values, NIST",
        ),
        Line(
            "collapse",
            "Field energy would form a black hole (Reissner–Nordström): Q = (d/2) c² √(4πε₀/G)",
            "upper",
            y=L.charge_collapse,
            forbidden="Forbidden: its field collapses into a black hole",
            forbidden_xy=(1e6, 1e28),
            forbidden_rotation=0,
            formula="(d/2) c^2 sqrt(4 pi eps0 / G)",
            source_url="https://doi.org/10.1002/andp.19163550905",
            citation="Reissner H. (1916) Uber die Eigengravitation des elektrischen Feldes nach der Einsteinschen Theorie. Ann Phys 355, 106",
        ),
        Line(
            "planck",
            "Planck charge √(4πε₀ħc) ≈ 11.7 e",
            "reference",
            y=L.PLANCK_CHARGE,
            dashed=True,
            formula="sqrt(4 pi eps0 hbar c)",
        ),
        Line(
            "schwinger",
            "Surface field at the Schwinger limit (1.3×10¹⁸ V/m): vacuum sparks pairs",
            "gravity",
            y=lambda d: L.charge_for_field(d, L.E_SCHWINGER),
            formula="4 pi eps0 (d/2)^2 E_S",
            source_url="https://doi.org/10.1103/PhysRev.82.664",
            citation="Schwinger J. (1951) On gauge invariance and vacuum polarization. Phys Rev 82, 664",
        ),
        Line(
            "air",
            "Surface field at air breakdown (3 MV/m)",
            "material",
            y=lambda d: L.charge_for_field(d, L.E_AIR_BREAKDOWN),
            formula="4 pi eps0 (d/2)^2 x 3e6 V/m",
        ),
        Line(
            "rayleigh",
            "Rayleigh limit of a water drop: q = 8π√(ε₀γr³)",
            "material",
            y=L.charge_rayleigh,
            dashed=True,
            formula="8 pi sqrt(eps0 gamma (d/2)^3), gamma = 0.072 N/m",
            source_url="https://doi.org/10.1080/14786448208628425",
            citation="Rayleigh, Lord (1882) On the equilibrium of liquid conducting masses charged with electricity. Phil Mag 14, 184",
        ),
    ]


def spec() -> ChartSpec:
    obj = loaders.to_objects(
        loaders.load("charge"), "size_m", "charge_low_c", "charge_high_c", "charge_example_c", "charge_max_c"
    )
    return ChartSpec(
        name=NAME,
        title="How much electric charge can an object carry?",
        xlabel="Size, m",
        ylabel="Net charge, C",
        xlim=(1e-16, 1e12),
        ylim=(1e-24, 1e30),
        lines=lines(),
        objects=obj,
        categories=CATEGORIES,
        legend_loc="upper left",
        footnote="Nuclei exceed the Schwinger line (the vacuum only sparks if the field extends beyond the electron's Compton wavelength, i.e. Z above about 173); above Sun size gravity, not QED, sets the ceiling.",
    )
