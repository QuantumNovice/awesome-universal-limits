"""Chart 6: acceleration vs size."""

from __future__ import annotations

from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line
from allowed_universe.style import PHYSICS_CATEGORIES

NAME = "acceleration"
DATASETS = ("acceleration",)


def lines() -> list[Line]:
    return [
        Line(
            "rindler",
            "Rigid-body limit a = c²/d (= black hole surface gravity)",
            "upper",
            y=L.accel_rindler,
            forbidden="Forbidden: the back end would fall behind a horizon",
            forbidden_xy=(1e8, 1e25),
            formula="c^2 / d",
        ),
        Line(
            "planck",
            "Planck acceleration (5.6×10⁵¹ m/s²)",
            "upper",
            y=L.accel_planck(),
            forbidden="Forbidden: beyond the Planck acceleration",
            forbidden_xy=(1e10, 5e52),
            formula="sqrt(c^7 / (hbar G))",
        ),
        Line(
            "age",
            "Covering its own size in the age of the universe (observability floor)",
            "lower",
            y=L.accel_age,
            dashed=True,
            forbidden="Unobservable",
            forbidden_xy=(1e-6, 1e-32),
            formula="d / t0^2",
            source_url="https://doi.org/10.1051/0004-6361/201833910",
            citation="Planck Collaboration (2020) Planck 2018 results. VI. A&A 641, A6 (t0 = 13.787 Gyr)",
        ),
        Line(
            "material",
            "Rim of a rotor spinning at the material limit (3 km/s)",
            "material",
            y=L.accel_material,
            formula="2 v^2 / d",
        ),
    ]


def spec() -> ChartSpec:
    obj = loaders.to_objects(
        loaders.load("acceleration"),
        "size_m",
        "accel_low_m_s2",
        "accel_high_m_s2",
        "accel_example_m_s2",
        "accel_max_m_s2",
    )
    return ChartSpec(
        name=NAME,
        title="How hard can things accelerate?",
        xlabel="Size, m",
        ylabel="Acceleration, m/s²",
        xlim=(1e-16, 1e26),
        ylim=(1e-40, 1e55),
        lines=lines(),
        objects=obj,
        categories=PHYSICS_CATEGORIES,
        legend_loc="lower right",
        cap_label="Tolerance or rated limit",
    )
