"""Volumetric flow vs channel size, from a tap to the Antarctic Circumpolar Current."""

from __future__ import annotations

from allowed_universe import constants as k
from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line

NAME = "flow"
DATASETS = ("flow",)

CATEGORIES = {
    "living": ("Living things", 0),
    "human": ("Plumbing", 1),
    "earth": ("Rivers and ocean currents", 5),
}


def lines() -> list[Line]:
    return [
        Line(
            "light",
            "Flow at light speed through the channel: c·πd²/4",
            "upper",
            y=lambda d: L.flow_at_speed(d, k.c),
            forbidden="Forbidden: faster than light",
            forbidden_xy=(1, 1e17),
            formula="c pi d^2 / 4",
        ),
        Line(
            "sound-water",
            "Water moving at its own speed of sound (1,482 m/s)",
            "material",
            y=lambda d: L.flow_at_speed(d, L.SOUND_SPEED_WATER),
            formula="1482 pi d^2 / 4",
        ),
        Line(
            "1ms",
            "Mean speed 1 m/s",
            "reference",
            y=lambda d: L.flow_at_speed(d, 1.0),
            formula="pi d^2 / 4",
        ),
    ]


def spec() -> ChartSpec:
    obj = loaders.to_objects(
        loaders.load("flow"), "width_m", "flow_low_m3_s", "flow_high_m3_s", "flow_example_m3_s", "flow_max_m3_s"
    )
    return ChartSpec(
        name=NAME,
        title="How much can flow through a channel?",
        xlabel="Channel diameter or width, m",
        ylabel="Volumetric flow, m³/s",
        xlim=(1e-3, 1e7),
        ylim=(1e-8, 1e22),
        lines=lines(),
        objects=obj,
        categories=CATEGORIES,
        legend_loc="lower right",
        footnote="1 sverdrup = 10⁶ m³/s. Wide, shallow ocean currents sit far below the circular-pipe lines.",
    )
