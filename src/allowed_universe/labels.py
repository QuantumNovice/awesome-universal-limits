"""Greedy label placement that avoids lines, markers and other labels.

Each label tries a ring of candidate offsets around its marker, nearest first.
A candidate is accepted when its bounding box stays inside the axes and touches
no other label, no marker and no drawn line (limit lines, range bars, tracks).
If no candidate is clean, the one with the fewest collisions is used and a thin
leader line is drawn back to the marker.
"""

from __future__ import annotations

from dataclasses import dataclass

from matplotlib.path import Path
from matplotlib.transforms import Bbox

# (dx, dy) in points, horizontal and vertical alignment
_RING = [
    (1, 0, "left", "center"),
    (-1, 0, "right", "center"),
    (0, 1, "center", "bottom"),
    (0, -1, "center", "top"),
    (0.7, 0.7, "left", "bottom"),
    (0.7, -0.7, "left", "top"),
    (-0.7, 0.7, "right", "bottom"),
    (-0.7, -0.7, "right", "top"),
    (0.92, 0.38, "left", "bottom"),
    (0.92, -0.38, "left", "top"),
    (-0.92, 0.38, "right", "bottom"),
    (-0.92, -0.38, "right", "top"),
    (0.38, 0.92, "left", "bottom"),
    (0.38, -0.92, "left", "top"),
    (-0.38, 0.92, "right", "bottom"),
    (-0.38, -0.92, "right", "top"),
]
_DISTANCES = [6, 12, 20, 30, 44, 60, 80, 105, 135]
_LEADER_FROM = 2  # index into _DISTANCES from which a leader line is drawn


@dataclass
class LabelRequest:
    x: float
    y: float
    text: str
    color: str = "black"
    priority: int = 0


def _padded(bb: Bbox, pad: float) -> Bbox:
    return Bbox.from_extents(bb.x0 - pad, bb.y0 - pad, bb.x1 + pad, bb.y1 + pad)


def _line_paths(ax):
    """All drawn lines (and fill edges) in display coordinates."""
    paths = []
    for line in ax.get_lines():
        if not line.get_visible() or line.get_linestyle() in ("None", "none", ""):
            continue
        xy = line.get_xydata()
        if len(xy) < 2:
            continue
        disp = line.get_transform().transform(xy)
        paths.append(Path(disp))
    return paths


def place_labels(ax, requests: list[LabelRequest], fontsize: float = 10, extra_obstacles=()):
    """Place every label; returns the list of created Text artists."""
    fig = ax.figure
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    ax_bb = ax.get_window_extent(renderer)
    px_per_pt = fig.dpi / 72.0

    line_paths = _line_paths(ax)
    marker_boxes = []
    for req in requests:
        px, py = ax.transData.transform((req.x, req.y))
        r = 5 * px_per_pt
        marker_boxes.append(Bbox.from_extents(px - r, py - r, px + r, py + r))
    placed: list[Bbox] = [_padded(b, 2) for b in extra_obstacles]

    texts = []
    order = sorted(range(len(requests)), key=lambda i: -requests[i].priority)
    for i in order:
        req = requests[i]
        best = None
        for dist in _DISTANCES:
            for dx, dy, ha, va in _RING:
                ann = ax.annotate(
                    req.text,
                    (req.x, req.y),
                    xytext=(dx * dist, dy * dist),
                    textcoords="offset points",
                    ha=ha,
                    va=va,
                    fontsize=fontsize,
                    color=req.color,
                    zorder=6,
                )
                bb = ann.get_window_extent(renderer)
                ann.remove()
                score = 0
                if not ax_bb.contains(bb.x0, bb.y0) or not ax_bb.contains(bb.x1, bb.y1):
                    score += 100
                pb = _padded(bb, 1.5)
                score += sum(10 for other in placed if pb.overlaps(other))
                score += sum(5 for j, mb in enumerate(marker_boxes) if j != i and pb.overlaps(mb))
                score += sum(3 for p in line_paths if p.intersects_bbox(pb, filled=False))
                if dist >= _DISTANCES[_LEADER_FROM]:
                    px, py = ax.transData.transform((req.x, req.y))
                    cx = min(max(px, bb.x0), bb.x1)
                    cy = min(max(py, bb.y0), bb.y1)
                    leader = Path([(px, py), (cx, cy)])
                    score += sum(4 for other in placed if leader.intersects_bbox(other, filled=True))
                    score += 1  # mild preference for labels without leaders
                cand = (score, dist, dx, dy, ha, va, bb)
                if best is None or cand[0] < best[0]:
                    best = cand
                if score == 0:
                    break
            if best[0] == 0 or (best[0] <= 1 and dist >= _DISTANCES[_LEADER_FROM]):
                break
        score, dist, dx, dy, ha, va, bb = best
        arrow = None
        if dist >= _DISTANCES[_LEADER_FROM]:
            arrow = {"arrowstyle": "-", "color": "#555555", "lw": 0.6, "shrinkA": 0, "shrinkB": 4}
        t = ax.annotate(
            req.text,
            (req.x, req.y),
            xytext=(dx * dist, dy * dist),
            textcoords="offset points",
            ha=ha,
            va=va,
            fontsize=fontsize,
            color=req.color,
            zorder=6,
            arrowprops=arrow,
        )
        t._placement_score = score  # inspected by tests
        placed.append(bb)
        if arrow:
            px, py = ax.transData.transform((req.x, req.y))
            line_paths.append(Path([(px, py), ((bb.x0 + bb.x1) / 2, (bb.y0 + bb.y1) / 2)]))
        texts.append(t)
    return texts
