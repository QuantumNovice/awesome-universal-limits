"""Luminous intensity in candela, from a candle to the Sun, against the Planck ceiling."""

from __future__ import annotations

from allowed_universe import limits as L
from allowed_universe.charts._bars import BarLine, BarPanel, BarSpec, fmt, render_bars

NAME = "luminous"
DATASETS = ("luminous",)

CATEGORIES = {
    "flame": ("Flames", 1),
    "electric": ("Electric light", 5),
    "astro": ("Space", 2),
    "physics": ("Physics", 4),
}


def bars() -> BarSpec:
    sun_max = L.luminous_intensity_for_power(3.828e26)
    planck = L.luminous_intensity_for_power(L.power_planck())
    return BarSpec(
        name=NAME,
        title="How bright can a light be?",
        dataset="luminous",
        categories=CATEGORIES,
        panels=[
            BarPanel(
                "intensity",
                "",
                "Luminous intensity, candela",
                (0.1, 1e56),
                lines=[
                    BarLine(
                        sun_max,
                        f"The Sun's power all at 555 nm (683 lm/W): {fmt(sun_max)} cd",
                        "material",
                        source_url="https://www.bipm.org/en/publications/si-brochure",
                        citation="BIPM (2019) The International System of Units (SI Brochure), 9th edition: K_cd = 683 lm/W",
                    ),
                    BarLine(planck, f"Planck power c\u2075/G at 683 lm/W: {fmt(planck)} cd", "upper"),
                ],
            )
        ],
        footnote="683 lumens per watt at 555 nm is the most light per watt any source can give (it defines the candela).",
    )


def render():
    return render_bars(bars())
