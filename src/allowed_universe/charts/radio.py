"""Radio links: transmit power vs distance, against the Shannon limit for isotropic antennas."""

from __future__ import annotations

from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line

NAME = "radio"
DATASETS = ("radio",)

CATEGORIES = {
    "human": ("Everyday radio", 1),
    "lab": ("Deep-space links", 5),
    "astro": ("Interstellar", 2),
}


def lines() -> list[Line]:
    return [
        Line(
            "shannon-1bps",
            "1 bit/s at the Shannon limit, isotropic antennas, 2.4 GHz, 290 K",
            "gravity",
            y=lambda r: L.shannon_isotropic_power(r, 1.0),
            formula="k T ln2 R (4 pi r f / c)^2, R = 1 bit/s",
            source_url="https://doi.org/10.1002/j.1538-7305.1948.tb01338.x",
            citation="Shannon C.E. (1948) A mathematical theory of communication. Bell Syst Tech J 27, 379",
        ),
        Line(
            "shannon-1mbps",
            "1 Mbit/s at the Shannon limit, same assumptions",
            "material",
            y=lambda r: L.shannon_isotropic_power(r, 1e6),
            formula="k T ln2 R (4 pi r f / c)^2, R = 1 Mbit/s",
        ),
    ]


def spec() -> ChartSpec:
    obj = loaders.to_objects(
        loaders.load("radio"), "distance_m", "power_low_w", "power_high_w", "power_example_w", "power_max_w"
    )
    return ChartSpec(
        name=NAME,
        title="How far can a radio signal reach?",
        xlabel="Distance, m",
        ylabel="Transmit power, W",
        xlim=(1, 1e22),
        ylim=(1e-25, 1e30),
        lines=lines(),
        objects=obj,
        categories=CATEGORIES,
        legend_loc="upper left",
        range_label="Range of transmitter powers",
        footnote="Links below a line need antenna gain: Voyager's 3.7 m dish and the DSN's 70 m dish add about 10¹².",
    )
