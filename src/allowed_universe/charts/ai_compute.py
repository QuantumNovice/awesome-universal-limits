"""Training compute vs model size, against the compute-optimal (Chinchilla) line."""

from __future__ import annotations

from allowed_universe import limits as L
from allowed_universe import loaders
from allowed_universe.charts.ai_models import CATEGORIES
from allowed_universe.engine import ChartSpec, Line

NAME = "ai_compute"
DATASETS = ("ai_models",)
EXPLAINER = "ai_models"


def lines() -> list[Line]:
    return [
        Line(
            "chinchilla",
            "Compute-optimal training: C = 6ND with D = 20N",
            "reference",
            y=L.chinchilla_compute,
            formula="120 N^2",
            source_url="https://arxiv.org/abs/2203.15556",
            citation="Hoffmann J. et al. (2022) Training compute-optimal large language models. arXiv:2203.15556",
        ),
    ]


def spec() -> ChartSpec:
    df = loaders.load("ai_models")
    df = df[df["training_flop"].notna()].copy()
    obj = df.copy()
    obj["x"] = df["params_active"].fillna(df["params_total"])
    obj["lo"] = float("nan")
    obj["hi"] = float("nan")
    obj["ex"] = df["training_flop"]
    obj["mx"] = float("nan")
    return ChartSpec(
        name=NAME,
        title="How much compute trains a model?",
        xlabel="Parameters used per token (active parameters for mixture-of-experts)",
        ylabel="Training compute, FLOP",
        xlim=(1e8, 1e13),
        ylim=(1e18, 1e28),
        lines=lines(),
        objects=obj,
        categories=CATEGORIES,
        legend_loc="upper left",
        footnote="Points above the Chinchilla line trained on more than 20 tokens per parameter.",
    )
