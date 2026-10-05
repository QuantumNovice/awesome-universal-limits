"""Chart 2: mass vs size."""

from __future__ import annotations

from allowed_universe import constants as k
from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line
from allowed_universe.style import PHYSICS_CATEGORIES

NAME = "mass"
DATASETS = ("mass",)


def lines() -> list[Line]:
    return [
        Line(
            "black-hole",
            "Black hole: M = c²d / (4G)",
            "upper",
            y=L.mass_black_hole,
            forbidden="Forbidden: inside its own horizon",
            forbidden_xy=(1e-22, 1e25),
            formula="c^2 d / (4 G)",
        ),
        Line(
            "compton",
            "Quantum: size below Compton wavelength, M = h / (cd)",
            "lower",
            y=L.mass_compton,
            forbidden="Forbidden: smaller than\nits own quantum wavelength",
            forbidden_xy=(3e-29, 1e-29),
            forbidden_rotation=0,
            formula="h / (c d)",
        ),
        Line(
            "nuclear",
            "Nuclear density (2.7×10¹⁷ kg/m³)",
            "gravity",
            y=lambda d: L.mass_at_density(d, k.RHO_NUCLEAR),
            formula="rho_n pi d^3 / 6",
            source_url="https://doi.org/10.1016/j.adt.2011.12.006",
            citation="Nuclear saturation density n0 = 0.16 fm^-3; see Angeli & Marinova (2013) ADNDT 99, 69",
        ),
        Line(
            "atomic",
            "Densest ordinary matter (osmium, 22,590 kg/m³)",
            "material",
            y=lambda d: L.mass_at_density(d, k.RHO_OSMIUM),
            formula="rho_Os pi d^3 / 6",
            source_url="https://technology.matthey.com/article/33/1/14-16/",
            citation="Arblaster J.W. (1989) Densities of osmium and iridium. Platinum Metals Review 33, 14",
        ),
    ]


def spec() -> ChartSpec:
    obj = loaders.to_objects(
        loaders.load("mass"), "size_m", "mass_low_kg", "mass_high_kg", "mass_example_kg", "mass_max_kg"
    )
    return ChartSpec(
        name=NAME,
        title="How much mass can fit in a given size?",
        xlabel="Size (diameter), m",
        ylabel="Mass, kg",
        xlim=(1e-36, 1e28),
        ylim=(1e-35, 1e60),
        lines=lines(),
        objects=obj,
        categories=PHYSICS_CATEGORIES,
        legend_loc="lower right",
        cap_label="Maximum mass for its kind",
        footnote="The black hole line applies to static objects; an expanding universe is not bound by it.",
    )
