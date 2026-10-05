"""One module per chart. Each exposes NAME and DATASETS and one of:
spec() (three-layer template rendered by the engine), bars() (bar-chart template),
or render() alone (custom layout)."""

from __future__ import annotations

import importlib

# Groups are used for the README gallery and the website navigation.
CHART_GROUPS: dict[str, list[str]] = {
    "Size and motion": [
        "spin",
        "oscillation",
        "speed",
        "acceleration",
        "mass",
        "density",
        "pressure",
        "temperature",
        "lifetime",
    ],
    "Energy and power": ["energy_density", "power"],
    "Electricity, magnetism and light": ["charge", "voltage", "magnetic", "radio", "luminous"],
    "Black holes and neutron stars": ["black_holes", "pulsars"],
    "Matter and flow": ["chemistry", "materials", "sound", "flow", "volumes"],
    "Life": ["biology", "genomes", "epidemics"],
    "Built world": ["buildings", "structures"],
    "Artificial intelligence": ["ai_models", "ai_compute", "ai_benchmarks"],
    "Minds and numbers": ["cognition", "research", "numbers"],
}

CHART_MODULES = [name for group in CHART_GROUPS.values() for name in group]


def load(name: str):
    return importlib.import_module(f"allowed_universe.charts.{name}")


def all_charts():
    return [load(n) for n in CHART_MODULES]


def group_of(name: str) -> str:
    for group, names in CHART_GROUPS.items():
        if name in names:
            return group
    raise KeyError(name)
