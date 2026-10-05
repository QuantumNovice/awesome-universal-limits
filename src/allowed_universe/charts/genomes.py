"""Genome size vs number of protein-coding genes, with DNA length on the top axis."""

from __future__ import annotations

from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line

NAME = "genomes"
DATASETS = ("genomes",)

CATEGORIES = {
    "virus": ("Viruses", 4),
    "bacterium": ("Bacteria", 0),
    "fungus": ("Fungi", 3),
    "plant": ("Plants", 5),
    "animal": ("Animals", 1),
}


def lines() -> list[Line]:
    return [
        Line(
            "dense",
            "One gene per 1,000 base pairs (compact bacterial genomes)",
            "material",
            y=lambda bp: bp / 1e3,
            formula="L / 1000",
        ),
        Line(
            "sparse",
            "One gene per 100,000 base pairs",
            "reference",
            y=lambda bp: bp / 1e5,
            formula="L / 100000",
        ),
        Line(
            "largest",
            "Largest known genome (fork fern, 160 Gbp)",
            "gravity",
            x=1.6045e11,
            formula="160.45 Gbp",
            source_url="https://doi.org/10.1016/j.isci.2024.109889",
            citation="Fernandez P. et al. (2024) A 160 Gbp fork fern genome shatters size record for eukaryotes. iScience 27, 109889",
        ),
    ]


def spec() -> ChartSpec:
    df = loaders.load("genomes")
    obj = df.rename(columns={"genome_bp": "x"})
    obj["lo"] = float("nan")
    obj["hi"] = float("nan")
    obj["ex"] = df["genes"]
    obj["mx"] = float("nan")
    return ChartSpec(
        name=NAME,
        title="How long is a genome, and how many genes does it hold?",
        xlabel="Genome length, base pairs",
        ylabel="Protein-coding genes",
        xlim=(1e3, 1e12),
        ylim=(1, 1e7),
        lines=lines(),
        objects=obj,
        categories=CATEGORIES,
        legend_loc="upper left",
        secondary_x=("Length of the DNA stretched out, m", lambda bp: bp * L.BP_LENGTH_M, lambda m: m / L.BP_LENGTH_M),
        footnote="Past about 10⁸ bp, genomes grow by adding non-coding DNA, not genes (the C-value paradox).",
    )
