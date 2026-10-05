"""To-and-fro motion: oscillation frequency vs size."""

from __future__ import annotations

from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line
from allowed_universe.style import PHYSICS_CATEGORIES

NAME = "oscillation"
DATASETS = ("oscillation",)


def lines() -> list[Line]:
    return [
        Line(
            "light",
            "Swinging across its own size at light speed: f = c/(πd)",
            "upper",
            y=L.oscillation_light,
            forbidden="Forbidden: faster than light",
            forbidden_xy=(1e3, 1e13),
            formula="c / (pi d)",
        ),
        Line(
            "sound",
            "Fundamental mode at the fastest possible sound speed (36 km/s)",
            "material",
            y=L.oscillation_sound,
            formula="v_max / (2 d)",
            source_url="https://doi.org/10.1126/sciadv.abc8662",
            citation="Trachenko K. et al. (2020) Speed of sound from fundamental physical constants. Science Advances 6, eabc8662",
        ),
        Line(
            "age",
            "One swing in the age of the universe (observability floor)",
            "lower",
            y=1 / (13.787e9 * 3.15576e7),
            dashed=True,
            forbidden="Unobservable: slower than one cycle since the Big Bang",
            forbidden_xy=(1e3, 2e-19),
            formula="1 / t0",
        ),
    ]


def spec() -> ChartSpec:
    obj = loaders.to_objects(
        loaders.load("oscillation"), "size_m", "freq_low_hz", "freq_high_hz", "freq_example_hz", "freq_max_hz"
    )
    return ChartSpec(
        name=NAME,
        title="How fast can things swing to and fro?",
        xlabel="Size, m",
        ylabel="Oscillation frequency, Hz",
        xlim=(1e-12, 1e12),
        ylim=(1e-20, 1e20),
        lines=lines(),
        objects=obj,
        categories=PHYSICS_CATEGORIES,
        legend_loc="center left",
        footnote="Mechanical resonators sit under the sound line; atoms in a molecule vibrate close to it.",
    )
