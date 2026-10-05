"""The three-layer chart template shared by every size-based chart.

Layer 1: hard bounds (solid red above, solid blue below, region beyond shaded).
Layer 2: practical limits (dotted amber for material, dashed grey for gravity,
         dash-dot grey for other references).
Layer 3: real objects as markers with range bars and a cap at their own maximum.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.ticker import FixedLocator, LogLocator, NullFormatter  # noqa: E402

from allowed_universe import style  # noqa: E402
from allowed_universe.labels import LabelRequest, place_labels  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
FIGURES = ROOT / "figures"

HARD_KINDS = ("upper", "lower")


@dataclass
class Line:
    """One limit line. Give ``y`` (callable of x, or a constant) or ``x`` (vertical line)."""

    id: str
    label: str
    kind: str  # upper | lower | material | gravity | reference
    y: Callable | float | None = None
    x: float | None = None
    dashed: bool = False  # observability floors are dashed
    forbidden: str | None = None  # italic text in the shaded region
    forbidden_xy: tuple[float, float] | None = None  # data coords of that text
    forbidden_rotation: float | str = "auto"  # degrees, or "auto" to follow the line
    formula: str = ""
    shade: bool = True
    enforce: bool = True  # objects must respect this bound (tests)
    source_url: str = ""  # where a measured constant in the line comes from
    citation: str = ""

    def values(self, xs):
        if callable(self.y):
            return np.asarray(self.y(xs), dtype=float) * np.ones_like(xs)
        return np.full_like(xs, float(self.y))


@dataclass
class Track:
    """A connected series of points, e.g. orbits along a Kepler curve."""

    name: str
    x: np.ndarray
    y: np.ndarray
    category: str = "orbit"
    label_index: int = -1


@dataclass
class ChartSpec:
    name: str
    title: str
    xlabel: str
    ylabel: str
    xlim: tuple[float, float]
    ylim: tuple[float, float]
    lines: list[Line]
    objects: pd.DataFrame  # columns: id, name, category, x, lo, hi, ex, mx, source_url, notes
    categories: dict[str, tuple[str, int]]
    xscale: str = "log"
    yscale: str = "log"
    tracks: list[Track] = field(default_factory=list)
    legend_loc: str = "lower left"
    legend_bbox: tuple[float, float] | None = None  # axes-fraction anchor for the legend
    footnote: str = ""
    secondary_y: tuple[str, Callable, Callable] | None = None
    secondary_x: tuple[str, Callable, Callable] | None = None
    range_label: str = "Known range (lowest to highest)"
    max_label: str = "Up to maximum allowable"
    cap_label: str = "Object's own maximum"
    zone_fontsize: float = 12


# -----------------------------------------------------------------------------


def _decade_step(lo: float, hi: float) -> int:
    span = math.log10(hi) - math.log10(lo)
    if span > 100:
        return 20
    if span > 60:
        return 10
    if span > 30:
        return 5
    if span > 14:
        return 2
    return 1


def _log_ticks(axis, lim):
    lo, hi = lim
    step = _decade_step(lo, hi)
    first = math.ceil(math.log10(lo) / step) * step
    last = math.floor(math.log10(hi))
    ticks = [10.0**p for p in range(first, last + 1, step)]
    axis.set_major_locator(FixedLocator(ticks))
    if step == 1:
        axis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10)))
    else:
        minor = max(1, step // 5)
        first_minor = math.ceil(math.log10(lo) / minor) * minor
        axis.set_minor_locator(FixedLocator([10.0**p for p in range(first_minor, last + 1, minor)]))
    axis.set_minor_formatter(NullFormatter())


def _xs(spec: ChartSpec, n: int = 600):
    if spec.xscale == "log":
        return np.logspace(math.log10(spec.xlim[0]), math.log10(spec.xlim[1]), n)
    return np.linspace(spec.xlim[0], spec.xlim[1], n)


def _line_style(line: Line):
    if line.kind == "upper":
        return {"color": style.RED, "lw": 2.5, "ls": "--" if line.dashed else "-"}
    if line.kind == "lower":
        return {"color": style.BLUE, "lw": 2.5, "ls": "--" if line.dashed else "-"}
    if line.kind == "material":
        return {"color": style.AMBER, "lw": 1.8, "ls": ":"}
    if line.kind == "gravity":
        return {"color": style.GREY, "lw": 1.6, "ls": "--"}
    return {"color": style.GREY, "lw": 1.4, "ls": "-."}


def _cat_style(spec: ChartSpec, category: str):
    label, slot = spec.categories[category]
    color, marker = style.SLOTS[slot]
    return label, color, marker


def _line_angle(ax, spec: ChartSpec, line: Line, x: float) -> float:
    """On-screen angle (degrees) of a line at x, so zone labels run parallel to it."""
    if line.x is not None:
        return 90.0
    if spec.xscale == "log":
        x0, x1 = x / 1.5, x * 1.5
    else:
        span = spec.xlim[1] - spec.xlim[0]
        x0, x1 = x - span / 50, x + span / 50
    ys = line.values(np.array([x0, x1], dtype=float))
    (px0, py0), (px1, py1) = ax.transData.transform([(x0, ys[0]), (x1, ys[1])])
    return math.degrees(math.atan2(py1 - py0, px1 - px0))


def draw_lines(ax, spec: ChartSpec):
    xs = _xs(spec)
    y0, y1 = spec.ylim
    texts = []
    for line in spec.lines:
        st = _line_style(line)
        if line.x is not None:
            ax.axvline(line.x, **st, zorder=3)
            if line.kind in HARD_KINDS and line.shade:
                fill_color = style.RED if line.kind == "upper" else style.BLUE
                if line.kind == "upper":
                    ax.axvspan(line.x, spec.xlim[1], color=fill_color, alpha=0.10, lw=0, zorder=1)
                else:
                    ax.axvspan(spec.xlim[0], line.x, color=fill_color, alpha=0.10, lw=0, zorder=1)
        else:
            ys = line.values(xs)
            ax.plot(xs, ys, **st, zorder=3)
            if line.kind in HARD_KINDS and line.shade:
                if line.kind == "upper":
                    ax.fill_between(xs, ys, y1, where=ys < y1, color=style.RED, alpha=0.10, lw=0, zorder=1)
                else:
                    ax.fill_between(xs, y0, ys, where=ys > y0, color=style.BLUE, alpha=0.10, lw=0, zorder=1)
        if line.forbidden and line.forbidden_xy:
            rot = line.forbidden_rotation
            if rot == "auto":
                rot = _line_angle(ax, spec, line, line.forbidden_xy[0])
            texts.append(
                ax.text(
                    *line.forbidden_xy,
                    line.forbidden,
                    style="italic",
                    fontsize=spec.zone_fontsize,
                    ha="center",
                    va="center",
                    rotation=rot,
                    rotation_mode="anchor",
                    clip_on=True,
                    color="black",
                    zorder=4,
                )
            )
    return texts


def draw_objects(ax, spec: ChartSpec):
    """Range bars, caps and markers. Returns label requests."""
    requests = []
    df = spec.objects
    for _, row in df.iterrows():
        _, color, marker = _cat_style(spec, row["category"])
        x = row["x"]
        lo, hi, ex, mx = (row.get(c) for c in ("lo", "hi", "ex", "mx"))
        has = {k: pd.notna(v) for k, v in dict(lo=lo, hi=hi, ex=ex, mx=mx).items()}
        if has["lo"] and has["hi"] and hi > lo:
            ax.plot([x, x], [lo, hi], color=color, lw=3, solid_capstyle="butt", zorder=4)
        top = hi if has["hi"] else (ex if has["ex"] else None)
        if has["mx"]:
            if top is not None and mx > top:
                ax.plot([x, x], [top, mx], color=color, lw=1.6, ls=":", zorder=4)
            ax.plot([x], [mx], marker="_", ms=12, mew=2.2, color="black", ls="none", zorder=5)
        y_mark = ex if has["ex"] else (hi if has["hi"] else (lo if has["lo"] else mx))
        ax.plot([x], [y_mark], marker=marker, ms=8.5, color=color, mec="white", mew=1.0, ls="none", zorder=5)
        requests.append(LabelRequest(x, y_mark, row["name"]))
    for tr in spec.tracks:
        _, color, marker = _cat_style(spec, tr.category)
        ax.plot(tr.x, tr.y, color=color, lw=1.2, zorder=4)
        ax.plot(tr.x, tr.y, marker=marker, ms=6, color=color, mec="white", mew=0.8, ls="none", zorder=5)
        requests.append(LabelRequest(tr.x[tr.label_index], tr.y[tr.label_index], tr.name, priority=1))
    return requests


def legend(ax, spec: ChartSpec):
    handles = []
    for line in spec.lines:
        st = _line_style(line)
        handles.append(Line2D([], [], color=st["color"], lw=st["lw"], ls=st["ls"], label=line.label))
    seen = set()
    cats = list(dict.fromkeys(spec.objects["category"].tolist() + [t.category for t in spec.tracks]))
    for cat in cats:
        label, color, marker = _cat_style(spec, cat)
        if label in seen:
            continue
        seen.add(label)
        handles.append(Line2D([], [], color=color, marker=marker, ms=8, mec="white", ls="none", label=label))
    o = spec.objects
    if (o["lo"].notna() & o["hi"].notna()).any():
        handles.append(Line2D([], [], color="#444444", lw=3, label=spec.range_label))
    if o["mx"].notna().any():
        handles.append(Line2D([], [], color="#444444", lw=1.6, ls=":", label=spec.max_label))
        handles.append(Line2D([], [], color="black", marker="_", ms=12, mew=2.2, ls="none", label=spec.cap_label))
    return ax.legend(handles=handles, loc=spec.legend_loc, bbox_to_anchor=spec.legend_bbox, ncol=1)


def render(spec: ChartSpec):
    style.apply()
    fig, ax = plt.subplots(figsize=style.FIGSIZE)
    ax.set_xscale(spec.xscale)
    ax.set_yscale(spec.yscale)
    ax.set_xlim(*spec.xlim)
    ax.set_ylim(*spec.ylim)
    if spec.xscale == "log":
        _log_ticks(ax.xaxis, spec.xlim)
    if spec.yscale == "log":
        _log_ticks(ax.yaxis, spec.ylim)
    ax.grid(True, which="major")
    ax.grid(False, which="minor")
    ax.set_xlabel(spec.xlabel)
    ax.set_ylabel(spec.ylabel)
    ax.set_title(spec.title, pad=12)
    if spec.secondary_y:
        lab, fwd, inv = spec.secondary_y
        sec = ax.secondary_yaxis("right", functions=(fwd, inv))
        sec.set_ylabel(lab)
    if spec.secondary_x:
        lab, fwd, inv = spec.secondary_x
        sec = ax.secondary_xaxis("top", functions=(fwd, inv))
        sec.set_xlabel(lab)

    zone_texts = draw_lines(ax, spec)
    requests = draw_objects(ax, spec)
    leg = legend(ax, spec)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    obstacles = [leg.get_window_extent(renderer)] + [t.get_window_extent(renderer) for t in zone_texts]
    place_labels(ax, requests, fontsize=10, extra_obstacles=obstacles)
    if spec.footnote:
        fig.text(0.01, 0.005, spec.footnote, fontsize=9, color="#333333", ha="left", va="bottom")
    return fig


def save(fig, name: str, outdir: Path = FIGURES):
    outdir.mkdir(parents=True, exist_ok=True)
    fig.savefig(outdir / f"{name}.png")
    fig.savefig(outdir / f"{name}.pdf")
    plt.close(fig)


# -----------------------------------------------------------------------------
# Checks used by the tests and the build


def violations(spec: ChartSpec, rtol: float = 1e-6):
    """Objects whose values cross an enforced hard bound."""
    bad = []
    for line in spec.lines:
        if line.kind not in HARD_KINDS or not line.enforce:
            continue
        for _, row in spec.objects.iterrows():
            vals = [row[c] for c in ("lo", "hi", "ex", "mx") if pd.notna(row.get(c))]
            if line.x is not None:
                x = row["x"]
                if (line.kind == "upper" and x > line.x * (1 + rtol)) or (
                    line.kind == "lower" and x < line.x * (1 - rtol)
                ):
                    bad.append((row["id"], line.id))
                continue
            bound = float(line.values(np.array([row["x"]], dtype=float))[0])
            for v in vals:
                if (line.kind == "upper" and v > bound * (1 + rtol)) or (
                    line.kind == "lower" and v < bound * (1 - rtol)
                ):
                    bad.append((row["id"], line.id))
                    break
    return bad


def sample_lines(spec: ChartSpec, n: int = 200):
    """Sampled points of every line, for the web site's limits.json."""
    out = []
    xs = _xs(spec, n)
    for line in spec.lines:
        entry = {
            "id": line.id,
            "label": line.label,
            "kind": line.kind,
            "dashed": line.dashed,
            "formula": line.formula,
            "forbidden": line.forbidden,
            "source_url": line.source_url,
            "citation": line.citation,
        }
        if line.x is not None:
            entry["x"] = float(line.x)
        else:
            entry["points"] = [[float(a), float(b)] for a, b in zip(xs, line.values(xs), strict=False)]
        out.append(entry)
    return out
