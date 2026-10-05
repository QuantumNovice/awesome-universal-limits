"""Horizontal bar-chart template shared by the category charts.

One row per item: a thin bar from the left edge to its value, a marker, a whisker
for the reported range, and the value printed beside it. Limit lines are vertical
and use the same colours and shading as the size-based charts.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass, field

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

from allowed_universe import loaders, style


def fmt(v: float) -> str:
    """1234 -> '1,234'; 1.5e14 -> '1.5 x 10^14' in mathtext."""
    if v < 1e5:
        return f"{v:,.0f}" if v >= 10 else f"{v:g}"
    exp = int(math.floor(math.log10(v)))
    mant = v / 10**exp
    m = f"{mant:.2g}"
    return rf"$10^{{{exp}}}$" if m == "1" else rf"${m}\times10^{{{exp}}}$"


def fmt_db(v: float) -> str:
    return f"{v:g} dB"


@dataclass
class BarLine:
    x: float
    label: str
    kind: str  # upper | lower | material | gravity | reference
    shade: bool = True
    source_url: str = ""
    citation: str = ""


@dataclass
class BarPanel:
    key: str
    title: str
    xlabel: str
    xlim: tuple[float, float]
    xscale: str = "log"
    lines: list[BarLine] = field(default_factory=list)
    height: float = 1.0


@dataclass
class BarSpec:
    name: str
    title: str
    dataset: str
    panels: list[BarPanel]
    categories: dict[str, tuple[str, int]]
    footnote: str = ""
    value_fmt: Callable[[float], str] = fmt


LINE_STYLE = {
    "upper": {"color": style.RED, "lw": 2.5, "ls": "-"},
    "lower": {"color": style.BLUE, "lw": 2.5, "ls": "-"},
    "material": {"color": style.AMBER, "lw": 1.8, "ls": ":"},
    "gravity": {"color": style.GREY, "lw": 1.6, "ls": "--"},
    "reference": {"color": style.GREY, "lw": 1.4, "ls": "-."},
}


def bar_panel(ax, df, categories: dict, panel: BarPanel, value_fmt=fmt):
    """Draw one panel of horizontal bars."""
    df = df.sort_values("value").reset_index(drop=True)
    y = np.arange(len(df))
    ax.set_xscale(panel.xscale)
    ax.set_xlim(*panel.xlim)
    ax.set_ylim(-0.7, len(df) - 0.3)
    x0 = panel.xlim[0]
    for i, r in df.iterrows():
        label, slot = categories[r["category"]]
        color, marker = style.SLOTS[slot]
        ax.plot([x0, r["value"]], [i, i], color=color, lw=3, alpha=0.35, solid_capstyle="butt", zorder=2)
        lo, hi = r.get("low"), r.get("high")
        has_range = lo is not None and hi is not None and lo == lo and hi == hi
        if has_range:
            ax.plot([lo, hi], [i, i], color=color, lw=1.6, zorder=3)
            ax.plot([lo, hi], [i, i], marker="|", ms=9, mew=1.6, color=color, ls="none", zorder=3)
        ax.plot([r["value"]], [i], marker=marker, ms=9, color=color, mec="white", ls="none", zorder=4)
        ax.annotate(
            value_fmt(r["value"]),
            (max(hi, r["value"]) if has_range else r["value"], i),
            xytext=(8, 0),
            textcoords="offset points",
            va="center",
            fontsize=10,
        )
    for line in panel.lines:
        st = LINE_STYLE[line.kind]
        ax.axvline(line.x, **st, zorder=3)
        if line.shade and line.kind == "upper":
            ax.axvspan(line.x, panel.xlim[1], color=style.RED, alpha=0.10, lw=0)
        elif line.shade and line.kind == "lower":
            ax.axvspan(panel.xlim[0], line.x, color=style.BLUE, alpha=0.10, lw=0)
    if panel.xscale == "log":
        from allowed_universe.engine import _log_ticks

        _log_ticks(ax.xaxis, panel.xlim)
        ax.grid(False, which="minor")
    ax.set_yticks(y)
    ax.set_yticklabels(df["name"])
    ax.set_xlabel(panel.xlabel)
    ax.set_title(panel.title, fontsize=14, loc="left")
    ax.grid(True, axis="x")
    ax.grid(False, axis="y")
    return df


def legend_handles(categories: dict, used):
    out, seen = [], set()
    for cat in used:
        label, slot = categories[cat]
        if label in seen:
            continue
        seen.add(label)
        color, marker = style.SLOTS[slot]
        out.append(Line2D([], [], color=color, marker=marker, ms=9, mec="white", ls="none", label=label))
    return out


def render_bars(spec: BarSpec):
    style.apply()
    df = loaders.load(spec.dataset)
    for col in ("low", "high"):
        if col not in df:
            df[col] = float("nan")
    heights = [max(p.height, 0.5) for p in spec.panels]
    fig, axes = plt.subplots(
        len(spec.panels), 1, figsize=style.FIGSIZE, gridspec_kw={"height_ratios": heights}, squeeze=False
    )
    axes = axes[:, 0]
    for ax, panel in zip(axes, spec.panels, strict=True):
        bar_panel(ax, df[df["panel"] == panel.key], spec.categories, panel, spec.value_fmt)
    handles = legend_handles(spec.categories, df["category"].tolist())
    if ((df["low"].notna()) & (df["high"].notna())).any():
        handles.append(Line2D([], [], color="#555555", lw=1.6, marker="|", ms=9, label="Reported range"))
    for panel in spec.panels:
        for line in panel.lines:
            st = LINE_STYLE[line.kind]
            handles.append(Line2D([], [], color=st["color"], lw=st["lw"], ls=st["ls"], label=line.label))
    rows = (len(handles) + 2) // 3
    fig.legend(handles=handles, loc="lower center", ncol=3, fontsize=9, frameon=False, bbox_to_anchor=(0.5, 0.015))
    fig.suptitle(spec.title, fontsize=17)
    fig.tight_layout(rect=(0, 0.03 + 0.022 * rows, 1, 0.97))
    if spec.footnote:
        fig.text(0.01, 0.003, spec.footnote, fontsize=9, color="#333333")
    return fig


def lines_of(spec: BarSpec):
    """Every limit line of a bar spec (for references and the site)."""
    return [line for panel in spec.panels for line in panel.lines]
