"""Chart 7: lifetime vs size."""

from __future__ import annotations

from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line
from allowed_universe.style import PHYSICS_CATEGORIES

NAME = "lifetime"
DATASETS = ("lifetime",)


def lines() -> list[Line]:
    return [
        Line(
            "planck",
            "Planck time (5.4×10⁻⁴⁴ s)",
            "lower",
            y=L.lifetime_planck(),
            forbidden="Forbidden: shorter than the Planck time",
            forbidden_xy=(1e-5, 1e-47),
            formula="sqrt(hbar G / c^5)",
        ),
        Line(
            "age",
            "Age of the universe: longer lifetimes are inferred, never watched",
            "upper",
            y=L.lifetime_age(),
            dashed=True,
            shade=False,
            enforce=False,
            formula="t0",
            source_url="https://doi.org/10.1051/0004-6361/201833910",
            citation="Planck Collaboration (2020) Planck 2018 results. VI. A&A 641, A6 (t0 = 13.787 Gyr)",
        ),
        Line(
            "hawking",
            "Evaporation time of a black hole of this size",
            "reference",
            y=L.lifetime_hawking,
            formula="5120 pi G^2 M^3 / (hbar c^4), M = c^2 d / 4G",
            source_url="https://doi.org/10.1103/PhysRevD.13.198",
            citation="Page D.N. (1976) Particle emission rates from a black hole. Phys Rev D 13, 198",
        ),
        Line(
            "light-crossing",
            "Light-crossing time d/c",
            "gravity",
            y=L.lifetime_light_crossing,
            formula="d / c",
        ),
    ]


def spec() -> ChartSpec:
    obj = loaders.to_objects(
        loaders.load("lifetime"), "size_m", "lifetime_low_s", "lifetime_high_s", "lifetime_example_s", "lifetime_max_s"
    )
    return ChartSpec(
        name=NAME,
        title="How long can things last?",
        xlabel="Size, m (point particles at their Compton wavelength)",
        ylabel="Lifetime, s",
        xlim=(1e-20, 1e12),
        ylim=(1e-50, 1e90),
        lines=lines(),
        objects=obj,
        categories=PHYSICS_CATEGORIES,
        legend_loc="upper left",
        cap_label="Record (oldest known)",
        footnote="The proton point is a lower limit: no proton decay has ever been seen.",
    )
