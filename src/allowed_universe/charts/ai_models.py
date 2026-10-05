"""Neural network size over time (parameters vs year)."""

from __future__ import annotations

from allowed_universe import loaders
from allowed_universe.engine import ChartSpec, Line

NAME = "ai_models"
DATASETS = ("ai_models",)

CATEGORIES = {
    "early": ("Early networks", 4),
    "cnn": ("Convolutional networks", 0),
    "rnn": ("Recurrent networks", 5),
    "transformer": ("Dense transformers", 2),
    "moe": ("Mixture-of-experts (bar: active to total)", 1),
}

SYNAPSES = 1.5e14
NEURONS = 8.6e10


def lines() -> list[Line]:
    return [
        Line(
            "synapses",
            "Synapses in the human neocortex (1.5×10¹⁴)",
            "gravity",
            y=SYNAPSES,
            formula="1.5e14",
            source_url="https://doi.org/10.1016/S0531-5565(02)00151-1",
            citation="Pakkenberg B. et al. (2003) Aging and the human neocortex. Exp Gerontol 38, 95",
        ),
        Line(
            "neurons",
            "Neurons in the human brain (8.6×10¹⁰)",
            "reference",
            y=NEURONS,
            formula="8.6e10",
            source_url="https://doi.org/10.1002/cne.21974",
            citation="Azevedo F.A.C. et al. (2009) Equal numbers of neuronal and nonneuronal cells make the human brain an isometrically scaled-up primate brain. J Comp Neurol 513, 532",
        ),
    ]


def spec() -> ChartSpec:
    df = loaders.load("ai_models")
    obj = df.rename(columns={"year": "x"})
    obj["lo"] = df["params_active"]
    obj["hi"] = df["params_total"].where(df["params_active"].notna())
    obj["ex"] = df["params_total"]
    obj["mx"] = float("nan")
    return ChartSpec(
        name=NAME,
        title="How big are neural networks?",
        xlabel="Year published",
        ylabel="Trainable parameters",
        xlim=(1996, 2027),
        ylim=(1e4, 1e15),
        xscale="linear",
        lines=lines(),
        objects=obj,
        categories=CATEGORIES,
        legend_loc="lower right",
        range_label="Active to total parameters",
        footnote="A parameter is not a synapse: the brain lines are for scale only, not a capability bound.",
    )
