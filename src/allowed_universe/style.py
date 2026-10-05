"""Shared matplotlib style so every chart reads as one series."""

from __future__ import annotations

import matplotlib as mpl

FIGSIZE = (12, 10)  # inches
DPI = 200

RED = "#e34948"  # upper hard bound
BLUE = "#2a78d6"  # lower hard bound
AMBER = "#d08a00"  # material / practical limit
GREY = "#888888"  # gravity / reference limit
GRID = "#dddddd"

# Categorical slots: colour + marker shape, so colour never carries meaning alone.
# Order is fixed (validated with the dataviz palette checker: CVD and normal-vision
# separation pass). Charts map their categories onto slots in this order.
SLOTS = [
    ("#1baf7a", "o"),  # teal circle
    ("#eb6834", "^"),  # orange triangle
    ("#6250d6", "D"),  # violet diamond
    ("#d55181", "s"),  # pink square
    ("#9a7b00", "h"),  # olive hexagon
    ("#1f93b8", "v"),  # cyan down-triangle
    ("#a0522d", "P"),  # sienna plus
]

# Spec categories for the physics charts (style guide table).
PHYSICS_CATEGORIES = {
    "molecular": ("Molecular / living", 0),
    "living": ("Molecular / living", 0),
    "human": ("Human-made", 1),
    "astro": ("Astronomical", 2),
    "orbit": ("Orbits", 3),
    "particle": ("Particles & nuclei", 4),
    "lab": ("Laboratory records", 5),
}


def apply() -> None:
    """Install the shared rcParams."""
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Liberation Serif", "DejaVu Serif"],
            "mathtext.fontset": "stix",
            "font.size": 12,
            "axes.labelsize": 15,
            "axes.titlesize": 17,
            "axes.edgecolor": "black",
            "axes.labelcolor": "black",
            "text.color": "black",
            "xtick.color": "black",
            "ytick.color": "black",
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
            "axes.grid": True,
            "axes.axisbelow": True,
            "grid.color": GRID,
            "grid.linewidth": 0.6,
            "legend.fontsize": 10,
            "legend.framealpha": 0.95,
            "legend.edgecolor": "#bbbbbb",
            "savefig.dpi": DPI,
            "savefig.bbox": "tight",
            "pdf.fonttype": 42,
        }
    )
