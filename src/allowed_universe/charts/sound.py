"""Sound levels in air and in water, against the point where the trough reaches vacuum."""

from __future__ import annotations

from allowed_universe import limits as L
from allowed_universe.charts._bars import BarLine, BarPanel, BarSpec, fmt_db, render_bars

NAME = "sound"
DATASETS = ("sound",)

CATEGORIES = {
    "living": ("Animals and hearing", 0),
    "human": ("Human-made", 1),
    "nature": ("Nature", 2),
    "limit": ("Exposure limits", 4),
}


def bars() -> BarSpec:
    air_max = L.spl_db(L.P_ATM, 20e-6)
    water_max = L.spl_db(L.P_ATM, 1e-6)
    return BarSpec(
        name=NAME,
        title="How loud can a sound be?",
        dataset="sound",
        categories=CATEGORIES,
        value_fmt=fmt_db,
        panels=[
            BarPanel(
                "air",
                "a. In air (dB re 20 \u00b5Pa)",
                "Sound pressure level, dB",
                (-10, 205),
                xscale="linear",
                lines=[
                    BarLine(
                        air_max,
                        f"{air_max:.0f} dB in air: the trough reaches vacuum (amplitude = 1 atm)",
                        "upper",
                    )
                ],
                height=4,
            ),
            BarPanel(
                "water",
                "b. In water (dB re 1 \u00b5Pa at 1 m)",
                "Source level, dB",
                (150, 245),
                xscale="linear",
                lines=[
                    BarLine(
                        water_max,
                        f"{water_max:.0f} dB: cavitation near the surface (deeper water allows more)",
                        "material",
                    )
                ],
                height=3,
            ),
        ],
        footnote="Air and water levels use different reference pressures and cannot be compared directly.",
    )


def render():
    return render_bars(bars())
