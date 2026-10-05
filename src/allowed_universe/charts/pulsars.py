"""Pulsars and magnetars: the P-Pdot diagram with field and age lines."""

from __future__ import annotations

from allowed_universe import constants as k
from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line

NAME = "pulsars"
DATASETS = ("pulsars",)

CATEGORIES = {
    "millisecond": ("Millisecond pulsars", 0),
    "pulsar": ("Radio pulsars", 5),
    "magnetar": ("Magnetars", 3),
    "long-period": ("Long-period radio emitter", 4),
}


def lines() -> list[Line]:
    return [
        Line(
            "rim-light",
            "Rim at light speed for a 25 km neutron star (P = πd/c)",
            "lower",
            x=L.min_spin_period(2.5e4),
            forbidden="Forbidden",
            forbidden_xy=(1.6e-4, 1e-14),
            formula="pi d / c",
        ),
        Line(
            "b-quantum",
            "B = 4.4×10⁹ T: quantum critical field",
            "gravity",
            y=lambda p: L.pdot_for_field(p, L.B_QUANTUM),
            formula="(B_q / 3.2e15)^2 / P",
        ),
        Line(
            "b-1e8",
            "B = 10⁸ T (typical young pulsar)",
            "reference",
            y=lambda p: L.pdot_for_field(p, 1e8),
            formula="(1e8 / 3.2e15)^2 / P",
            source_url="https://doi.org/10.1086/150119",
            citation="Goldreich P. & Julian W.H. (1969) Pulsar electrodynamics. ApJ 157, 869",
        ),
        Line(
            "age-1kyr",
            "Spin-down age 1,000 years",
            "material",
            y=lambda p: L.pdot_for_age(p, 1e3 * k.YEAR),
            formula="P / (2 x 1 kyr)",
        ),
        Line(
            "age-age",
            "Spin-down age = age of the universe",
            "upper",
            y=lambda p: L.pdot_for_age(p, k.T0),
            dashed=True,
            shade=False,
            enforce=False,
            formula="P / (2 t0)",
        ),
    ]


def spec() -> ChartSpec:
    df = loaders.load("pulsars")
    obj = df.rename(columns={"period_s": "x"})
    obj["lo"] = float("nan")
    obj["hi"] = float("nan")
    obj["ex"] = df["pdot"]
    obj["mx"] = float("nan")
    return ChartSpec(
        name=NAME,
        title="Pulsars and magnetars: how fast do they spin down?",
        xlabel="Spin period P, s",
        ylabel="Spin-down rate dP/dt, s/s",
        xlim=(1e-4, 1e3),
        ylim=(1e-22, 1e-7),
        lines=lines(),
        objects=obj,
        categories=CATEGORIES,
        legend_loc="lower right",
        footnote="Field from B ≈ 3.2×10¹⁵ T √(PṖ); age τ = P/(2Ṗ). Magnetars sit near or above the quantum critical field.",
    )
