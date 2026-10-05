"""Chart 1: spin rate vs size."""

from __future__ import annotations

from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line, Track
from allowed_universe.style import PHYSICS_CATEGORIES

NAME = "spin"
DATASETS = ("spin", "spin_orbits")
TRACK_LABELS = {"planets": "Planet orbits", "gw150914": "GW150914 final orbits", "milky-way": "Milky Way rotation"}


def lines() -> list[Line]:
    return [
        Line(
            "light",
            "Rim at light speed: f = c / (πd)",
            "upper",
            y=L.spin_light,
            forbidden="Forbidden: faster than light",
            forbidden_xy=(3e4, 1e13),
            formula="c / (pi d)",
        ),
        Line(
            "quantum",
            "One quantum of spin: f = 12ħ / (π²ρd⁵), ρ = osmium",
            "lower",
            y=L.spin_quantum,
            forbidden="Forbidden: below one quantum",
            forbidden_xy=(2.5e-11, 1e0),
            formula="12 hbar / (pi^2 rho d^5)",
        ),
        Line(
            "age",
            "One turn in the age of the universe (observability floor)",
            "lower",
            y=L.spin_age(),
            dashed=True,
            forbidden="Unobservable: slower than one turn in 13.8 billion years",
            forbidden_xy=(1e10, 3e-19),
            formula="1 / t0",
            source_url="https://doi.org/10.1051/0004-6361/201833910",
            citation="Planck Collaboration (2020) Planck 2018 results. VI. A&A 641, A6 (t0 = 13.787 Gyr)",
        ),
        Line(
            "material",
            "Material strength: rim at 3 km/s",
            "material",
            y=L.spin_material,
            formula="v_rim / (pi d), v_rim = 3 km/s",
        ),
        Line(
            "gravity",
            "Self-gravity breakup of rock (2,000 kg/m³)",
            "gravity",
            y=L.spin_gravity(),
            formula="sqrt(4 pi G rho / 3) / (2 pi)",
            source_url="https://doi.org/10.1016/j.pss.2012.03.009",
            citation="Carry B. (2012) Density of asteroids. Planet Space Sci 73, 98",
        ),
    ]


def spec() -> ChartSpec:
    df = loaders.load("spin")
    obj = loaders.to_objects(df, "size_m", "slowest_hz", "fastest_hz", "example_hz", "max_hz")
    orbits = loaders.load("spin_orbits")
    tracks = []
    for track, g in orbits.groupby("track", sort=False):
        g = g.sort_values("size_m")
        tracks.append(Track(TRACK_LABELS[track], g["size_m"].to_numpy(), g["freq_hz"].to_numpy()))
    return ChartSpec(
        name=NAME,
        title="How fast can things spin?",
        xlabel="Size (diameter), m",
        ylabel="Spin rate, turns per second (Hz)",
        xlim=(1e-12, 1e22),
        ylim=(1e-20, 1e20),
        lines=lines(),
        objects=obj,
        categories=PHYSICS_CATEGORIES,
        tracks=tracks,
        legend_loc="upper right",
        range_label="Known range (slowest to fastest)",
        max_label="Up to maximum allowable spin",
        cap_label="Object's own breakup limit",
    )
