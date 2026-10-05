"""Tallest buildings and towers since 1880, against the crushing height of their materials."""

from __future__ import annotations

from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line

NAME = "buildings"
DATASETS = ("buildings",)

CATEGORIES = {
    "ancient": ("Ancient", 4),
    "tower": ("Towers", 5),
    "skyscraper": ("Skyscrapers", 1),
}

ASHBY = (
    "https://doi.org/10.1016/B978-1-85617-663-7.00005-9",
    "Ashby M.F. (2011) Materials Selection in Mechanical Design, 4th ed., Butterworth-Heinemann",
)


def lines() -> list[Line]:
    return [
        Line(
            "concrete",
            "Uniform concrete column crushes its own base (40 MPa): 1.7 km",
            "material",
            y=L.crushing_height(40e6, 2400),
            formula="sigma / (rho g), 40 MPa, 2400 kg/m^3",
            source_url=ASHBY[0],
            citation=ASHBY[1],
        ),
        Line(
            "steel",
            "Uniform steel column yields (355 MPa): 4.6 km",
            "material",
            y=L.crushing_height(355e6, 7850),
            formula="sigma / (rho g), 355 MPa, 7850 kg/m^3",
        ),
        Line(
            "mountain",
            "Mountains on Earth: rock flows under its own weight near 10 km",
            "gravity",
            y=1e4,
            formula="~10 km",
            source_url="https://doi.org/10.1126/science.187.4177.605",
            citation="Weisskopf V.F. (1975) Of atoms, mountains, and stars: a study in qualitative physics. Science 187, 605",
        ),
        Line(
            "pyramid",
            "Great Pyramid (146.6 m): tallest structure for about 3,800 years",
            "reference",
            y=146.6,
            formula="146.6 m",
            source_url="https://www.britannica.com/topic/Pyramids-of-Giza",
            citation="Encyclopaedia Britannica, Pyramids of Giza",
        ),
    ]


def spec() -> ChartSpec:
    df = loaders.load("buildings")
    obj = df.rename(columns={"year": "x"})
    obj["lo"] = float("nan")
    obj["hi"] = float("nan")
    obj["ex"] = df["height_m"]
    obj["mx"] = float("nan")
    return ChartSpec(
        name=NAME,
        title="How tall can a building be?",
        xlabel="Year completed",
        ylabel="Height, m",
        xlim=(1875, 2035),
        ylim=(100, 3e4),
        xscale="linear",
        lines=lines(),
        objects=obj,
        categories=CATEGORIES,
        legend_loc="upper left",
        footnote="Real towers taper, so they can beat a uniform column; wind, sway and lift time stop them first.",
    )
