"""How fast infections spread: basic reproduction number vs serial interval."""

from __future__ import annotations

from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line

NAME = "epidemics"
DATASETS = ("epidemics",)

CATEGORIES = {
    "airborne": ("Airborne", 3),
    "contact": ("Close contact", 1),
    "influenza": ("Influenza", 5),
    "coronavirus": ("Coronaviruses", 2),
}


def lines() -> list[Line]:
    return [
        Line(
            "threshold",
            "R₀ = 1: epidemic threshold",
            "lower",
            y=1.0,
            enforce=False,
            forbidden="Outbreaks fizzle out (each case infects fewer than one)",
            forbidden_xy=(14.5, 0.6),
            forbidden_rotation=0,
            formula="R0 = 1",
            source_url="https://doi.org/10.1098/rspa.1927.0118",
            citation="Kermack W.O. & McKendrick A.G. (1927) A contribution to the mathematical theory of epidemics. Proc R Soc A 115, 700",
        ),
        Line(
            "double-2d",
            "Cases double every 2 days",
            "material",
            y=lambda t: L.r0_for_doubling(t, 2.0),
            formula="2^(T / 2 d)",
        ),
        Line(
            "double-7d",
            "Cases double every week",
            "gravity",
            y=lambda t: L.r0_for_doubling(t, 7.0),
            formula="2^(T / 7 d)",
        ),
        Line(
            "double-30d",
            "Cases double every month",
            "reference",
            y=lambda t: L.r0_for_doubling(t, 30.0),
            formula="2^(T / 30 d)",
        ),
    ]


def spec() -> ChartSpec:
    obj = loaders.to_objects(
        loaders.load("epidemics"), "serial_days", "r0_low_x", "r0_high_x", "r0_example_x", "r0_max_x"
    )
    return ChartSpec(
        name=NAME,
        title="How fast can an infection spread?",
        xlabel="Serial interval (days between one case and the next)",
        ylabel="Basic reproduction number R₀",
        xlim=(0, 20),
        ylim=(0.4, 40),
        xscale="linear",
        lines=lines(),
        objects=obj,
        categories=CATEGORIES,
        legend_loc="upper right",
        range_label="Reported range of R₀",
        footnote="Doubling-time curves use R₀ = 2^(T/t_d), ignoring immunity and interventions.",
    )
