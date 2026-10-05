"""Binding energy vs size: from the helium dimer to the uranium nucleus."""

from __future__ import annotations

from allowed_universe import constants as k
from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line

NAME = "chemistry"
DATASETS = ("chemistry",)

CATEGORIES = {
    "nuclear": ("Nuclei (strong force)", 4),
    "atomic": ("Atoms (ionisation)", 5),
    "covalent": ("Covalent bonds", 0),
    "ionic": ("Ionic bonds", 1),
    "weak": ("Hydrogen and van der Waals bonds", 2),
}


def lines() -> list[Line]:
    return [
        Line(
            "coulomb",
            "Coulomb energy of two unit charges: e²/(4πε₀d)",
            "reference",
            y=L.coulomb_energy,
            formula="e^2 / (4 pi eps0 d)",
        ),
        Line(
            "confinement",
            "Electron confined to a box of width d: h²/(8mₑd²)",
            "gravity",
            y=L.confinement_energy,
            formula="h^2 / (8 m_e d^2)",
        ),
        Line(
            "thermal",
            "Thermal energy at room temperature, kT (300 K)",
            "material",
            y=L.thermal_energy(300.0),
            formula="k_B x 300 K",
        ),
    ]


def spec() -> ChartSpec:
    obj = loaders.to_objects(
        loaders.load("chemistry"), "size_m", "energy_low_j", "energy_high_j", "energy_example_j", "energy_max_j"
    )
    return ChartSpec(
        name=NAME,
        title="How tightly can matter hold together?",
        xlabel="Size (bond length or diameter), m",
        ylabel="Binding energy, J",
        xlim=(1e-16, 1e-5),
        ylim=(1e-28, 1e-8),
        lines=lines(),
        objects=obj,
        categories=CATEGORIES,
        legend_loc="upper right",
        secondary_y=("Binding energy, eV", lambda j: j / k.eV, lambda ev: ev * k.eV),
        footnote="Bonds below the kT line fall apart at room temperature; they exist only in the cold.",
    )
