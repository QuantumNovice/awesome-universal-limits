"""Chart 3: speed vs size."""

from __future__ import annotations

from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line
from allowed_universe.style import PHYSICS_CATEGORIES

NAME = "speed"
DATASETS = ("speed",)


def lines() -> list[Line]:
    return [
        Line(
            "light",
            "Speed of light, c",
            "upper",
            y=L.speed_light(),
            forbidden="Forbidden: faster than light",
            forbidden_xy=(1e5, 1e9),
            formula="c",
        ),
        Line(
            "age",
            "Moving its own size once in the age of the universe (observability floor)",
            "lower",
            y=L.speed_age,
            dashed=True,
            forbidden="Unobservable: too slow to move\nits own size since the Big Bang",
            forbidden_xy=(1e18, 1e-20),
            forbidden_rotation=0,
            formula="d / t0",
            source_url="https://doi.org/10.1051/0004-6361/201833910",
            citation="Planck Collaboration (2020) Planck 2018 results. VI. A&A 641, A6 (t0 = 13.787 Gyr)",
        ),
        Line(
            "sound-max",
            "Fastest possible sound in solids and liquids (~36 km/s)",
            "material",
            y=L.speed_sound_max(),
            formula="alpha sqrt(m_e / (2 m_p)) c",
            source_url="https://doi.org/10.1126/sciadv.abc8662",
            citation="Trachenko K. et al. (2020) Speed of sound from fundamental physical constants. Science Advances 6, eabc8662",
        ),
        Line(
            "sound-air",
            "Speed of sound in air (343 m/s)",
            "reference",
            y=343.0,
            formula="343 m/s at 20 C",
            source_url="https://ntrs.nasa.gov/citations/19770009539",
            citation="NOAA/NASA/USAF (1976) U.S. Standard Atmosphere, 1976",
        ),
    ]


def spec() -> ChartSpec:
    obj = loaders.to_objects(
        loaders.load("speed"), "size_m", "speed_low_m_s", "speed_high_m_s", "speed_example_m_s", "speed_max_m_s"
    )
    return ChartSpec(
        name=NAME,
        title="How fast can things move?",
        xlabel="Size, m",
        ylabel="Speed, m/s",
        xlim=(1e-18, 1e27),
        ylim=(1e-25, 1e10),
        lines=lines(),
        objects=obj,
        categories=PHYSICS_CATEGORIES,
        legend_loc="lower left",
        cap_label="Escape speed (leaves its system)",
    )
