"""Power vs mass: from a brain to merging black holes, under the Planck power."""

from __future__ import annotations

from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line

NAME = "power"
DATASETS = ("power",)

CATEGORIES = {
    "living": ("Living things", 0),
    "human": ("Engines", 1),
    "astro": ("Astronomical", 2),
}


def lines() -> list[Line]:
    return [
        Line(
            "planck",
            "Planck power c⁵/G (3.6×10⁵² W)",
            "upper",
            y=L.power_planck(),
            forbidden="Forbidden: beyond the Planck power",
            forbidden_xy=(1e32, 3e53),
            formula="c^5 / G",
        ),
        Line(
            "eddington",
            "Eddington luminosity: radiation pushes harder than gravity pulls",
            "gravity",
            y=L.eddington_luminosity,
            formula="4 pi G M m_p c / sigma_T",
        ),
        Line(
            "1kw-kg",
            "1 kW per kg",
            "reference",
            y=lambda m: 1e3 * m,
            formula="1e3 M",
        ),
        Line(
            "1mw-kg",
            "1 MW per kg (rocket engines)",
            "material",
            y=lambda m: 1e6 * m,
            formula="1e6 M",
        ),
    ]


def spec() -> ChartSpec:
    obj = loaders.to_objects(
        loaders.load("power"), "mass_kg", "power_low_w", "power_high_w", "power_example_w", "power_max_w"
    )
    return ChartSpec(
        name=NAME,
        title="How powerful can an engine be?",
        xlabel="Mass, kg",
        ylabel="Power, W",
        xlim=(1e-1, 1e45),
        ylim=(1e0, 1e55),
        lines=lines(),
        objects=obj,
        categories=CATEGORIES,
        legend_loc="upper left",
        cap_label="Eddington limit for that mass",
        footnote="Rocket power is jet power (thrust x exhaust speed / 2). GW150914 radiated a thousandth of c⁵/G.",
    )
