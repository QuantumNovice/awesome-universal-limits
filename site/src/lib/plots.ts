import * as Plot from "@observablehq/plot";
import { formatValue, logTicks, powerOfTen } from "./format";
import type {
  BarPanel,
  BarRow,
  BarsChartData,
  BenchmarksChartData,
  LimitLine,
  LineKind,
  XYChartData,
  XYObject,
} from "./types";

export const LINE_STYLE: Record<LineKind, { stroke: string; width: number; dash?: string }> = {
  upper: { stroke: "#e34948", width: 2.5 },
  lower: { stroke: "#2a78d6", width: 2.5 },
  material: { stroke: "#d08a00", width: 1.8, dash: "2,3" },
  gravity: { stroke: "#888888", width: 1.6, dash: "7,4" },
  reference: { stroke: "#888888", width: 1.4, dash: "8,3,2,3" },
};

export function lineDash(l: { kind: LineKind; dashed?: boolean }): string | undefined {
  if ((l.kind === "upper" || l.kind === "lower") && l.dashed) return "8,5";
  return LINE_STYLE[l.kind].dash;
}

/** Horizontal bar used as the "own maximum" cap. */
const CAP = {
  draw(context: CanvasPath, size: number) {
    const w = Math.sqrt(size) * 1.1;
    context.moveTo(-w, 0);
    context.lineTo(w, 0);
  },
};

export interface PlotOptions {
  width: number;
  hidden: Set<string>;
  labels: boolean;
}

type Scale = "log" | "linear";

function axis(type: Scale, domain: [number, number], label: string, pixels: number, fmt?: (v: number) => string) {
  if (type === "log") {
    return {
      type,
      domain,
      label,
      grid: true,
      ticks: logTicks(domain[0], domain[1], Math.max(3, Math.floor(pixels / 64))),
      tickFormat: powerOfTen,
    };
  }
  return { type, domain, label, grid: true, nice: false, ticks: Math.max(3, Math.floor(pixels / 80)), tickFormat: fmt };
}

export function markY(o: XYObject): number | null {
  return o.ex ?? o.hi ?? o.lo ?? o.mx;
}

// ---------------------------------------------------------------------------
// Label placement: greedy, in pixels, avoiding other labels, markers and lines.

interface Box {
  x0: number;
  y0: number;
  x1: number;
  y1: number;
}

interface LabelItem {
  px: number;
  py: number;
  text: string;
}

interface Placed {
  px: number;
  py: number;
  text: string;
  anchor: "start" | "end" | "middle";
}

const overlap = (a: Box, b: Box) => a.x0 < b.x1 && b.x0 < a.x1 && a.y0 < b.y1 && b.y0 < a.y1;

export function placeLabels(
  items: LabelItem[],
  obstaclePoints: [number, number][],
  frame: Box,
  fontSize = 11,
): Placed[] {
  const charW = fontSize * 0.56;
  const h = fontSize + 2;
  const placed: Box[] = [];
  const markers: Box[] = items.map((it) => ({ x0: it.px - 6, y0: it.py - 6, x1: it.px + 6, y1: it.py + 6 }));
  const out: Placed[] = [];
  const cands: [number, number, Placed["anchor"]][] = [];
  for (const d of [9, 18, 30]) {
    cands.push([d, 0, "start"], [-d, 0, "end"], [0, -d - 2, "middle"], [0, d + 4, "middle"]);
    cands.push([d * 0.8, -d * 0.8, "start"], [d * 0.8, d * 0.8, "start"], [-d * 0.8, -d * 0.8, "end"], [-d * 0.8, d * 0.8, "end"]);
  }
  items.forEach((it, i) => {
    const w = it.text.length * charW;
    let best: { score: number; box: Box; p: Placed } | null = null;
    for (const [dx, dy, anchor] of cands) {
      const x = it.px + dx;
      const y = it.py + dy;
      const x0 = anchor === "start" ? x : anchor === "end" ? x - w : x - w / 2;
      const box = { x0, y0: y - h / 2, x1: x0 + w, y1: y + h / 2 };
      let score = 0;
      if (box.x0 < frame.x0 || box.x1 > frame.x1 || box.y0 < frame.y0 || box.y1 > frame.y1) score += 100;
      for (const b of placed) if (overlap(box, b)) score += 10;
      markers.forEach((m, j) => {
        if (j !== i && overlap(box, m)) score += 5;
      });
      for (const [ox, oy] of obstaclePoints) {
        if (ox > box.x0 && ox < box.x1 && oy > box.y0 && oy < box.y1) {
          score += 2;
          break;
        }
      }
      score += Math.hypot(dx, dy) / 40;
      if (!best || score < best.score) best = { score, box, p: { px: x, py: y, text: it.text, anchor } };
      if (score < 1) break;
    }
    if (best) {
      placed.push(best.box);
      out.push(best.p);
    }
  });
  return out;
}

function labelMarks(
  placed: Placed[],
  sx: { invert?: (v: number) => unknown },
  sy: { invert?: (v: number) => unknown },
  fontSize = 11,
) {
  const inv = (s: { invert?: (v: number) => unknown }, v: number) => Number(s.invert!(v));
  return (["start", "end", "middle"] as const).map((anchor) =>
    Plot.text(
      placed.filter((p) => p.anchor === anchor),
      {
        x: (p: Placed) => inv(sx, p.px),
        y: (p: Placed) => inv(sy, p.py),
        text: "text",
        textAnchor: anchor,
        fontSize,
        fill: "currentColor",
        stroke: "var(--bg)",
        strokeWidth: 3,
        paintOrder: "stroke",
      },
    ),
  );
}

// ---------------------------------------------------------------------------
// Three-layer x-y chart

export function xyPlot(d: XYChartData, opts: PlotOptions): Element {
  const width = Math.max(300, opts.width);
  const narrow = width < 560;
  const height = Math.round(Math.min(Math.max(width * (narrow ? 1.0 : 0.66), 360), 760));
  const margin = { left: narrow ? 50 : 66, right: 14, top: 18, bottom: 46 };
  const [x0, x1] = d.xlim;
  const [y0, y1] = d.ylim;
  const okY = (v: number | null | undefined): v is number =>
    v !== null && v !== undefined && isFinite(v) && (d.yscale !== "log" || v > 0);
  const clampY = (v: number) => Math.min(Math.max(v, y0), y1);
  const color = (c: string) => d.categories[c]?.color ?? "#777";
  const symbol = (c: string) => d.categories[c]?.symbol ?? "circle";

  const sx = Plot.scale({ x: { type: d.xscale, domain: d.xlim, range: [margin.left, width - margin.right] } });
  const sy = Plot.scale({ y: { type: d.yscale, domain: d.ylim, range: [height - margin.bottom, margin.top] } });
  const px = (v: number) => Number(sx.apply(v));
  const py = (v: number) => Number(sy.apply(v));

  const marks: Plot.Markish[] = [];
  const linePixels: [number, number][] = [];

  // Layer 1 and 2: limit lines and forbidden zones
  for (const l of d.lines) {
    const st = LINE_STYLE[l.kind];
    const hard = l.kind === "upper" || l.kind === "lower";
    if (l.x !== undefined && l.x !== null) {
      if (hard && l.shade) {
        const r = l.kind === "upper" ? { x1: l.x, x2: x1 } : { x1: x0, x2: l.x };
        marks.push(Plot.rect([{ ...r, y1: y0, y2: y1 }], { x1: "x1", x2: "x2", y1: "y1", y2: "y2", fill: st.stroke, fillOpacity: 0.1 }));
      }
      marks.push(Plot.ruleX([l.x], { stroke: st.stroke, strokeWidth: st.width, strokeDasharray: lineDash(l) }));
      for (let t = 0; t <= 60; t++) linePixels.push([px(l.x), margin.top + ((height - margin.top - margin.bottom) * t) / 60]);
    } else if (l.points) {
      const pts = l.points.filter((p): p is [number, number] => okY(p[1]));
      if (hard && l.shade) {
        marks.push(
          Plot.areaY(pts, {
            x: (p: [number, number]) => p[0],
            y1: (p: [number, number]) => clampY(p[1]),
            y2: () => (l.kind === "upper" ? y1 : y0),
            fill: st.stroke,
            fillOpacity: 0.1,
          }),
        );
      }
      marks.push(
        Plot.line(pts, {
          x: (p: [number, number]) => p[0],
          y: (p: [number, number]) => p[1],
          stroke: st.stroke,
          strokeWidth: st.width,
          strokeDasharray: lineDash(l),
          clip: "frame",
        }),
      );
      for (const p of pts) if (p[1] >= y0 && p[1] <= y1) linePixels.push([px(p[0]), py(p[1])]);
    }
    if (l.forbidden && l.forbidden_xy) {
      // keep the zone label inside the frame (it is drawn horizontally on the web)
      const fs = narrow ? 10 : 12;
      const maxChars = narrow ? 16 : 34;
      const longest = Math.min(l.forbidden.length, maxChars);
      const half = (longest * fs * 0.62) / 2;
      const cx = Math.min(Math.max(px(l.forbidden_xy[0]), margin.left + half + 4), width - margin.right - half - 4);
      const cy = Math.min(Math.max(py(l.forbidden_xy[1]), margin.top + fs * 1.5), height - margin.bottom - fs * 1.5);
      const at: [number, number] = [Number(sx.invert!(cx)), Number(sy.invert!(cy))];
      marks.push(
        Plot.text([at], {
          x: (p: [number, number]) => p[0],
          y: (p: [number, number]) => p[1],
          text: () => l.forbidden,
          fontStyle: "italic",
          fontSize: narrow ? 10 : 12,
          lineWidth: narrow ? 16 : 34,
          fill: "currentColor",
          fillOpacity: 0.85,
          clip: "frame",
        }),
      );
    }
  }

  // Layer 3: objects
  const visible = d.objects.filter((o) => !opts.hidden.has(o.category));
  const ranges = visible.filter((o) => okY(o.lo) && okY(o.hi) && (o.hi as number) > (o.lo as number));
  marks.push(Plot.ruleX(ranges, { x: "x", y1: "lo", y2: "hi", stroke: (o: XYObject) => color(o.category), strokeWidth: 3 }));
  const top = (o: XYObject) => o.hi ?? o.ex;
  const maxes = visible.filter((o) => okY(o.mx));
  marks.push(
    Plot.ruleX(
      maxes.filter((o) => okY(top(o)) && (o.mx as number) > (top(o) as number)),
      { x: "x", y1: (o: XYObject) => top(o), y2: "mx", stroke: (o: XYObject) => color(o.category), strokeWidth: 1.6, strokeDasharray: "2,3" },
    ),
  );
  marks.push(Plot.dot(maxes, { x: "x", y: "mx", symbol: () => CAP, stroke: "currentColor", strokeWidth: 2.4, r: 7 }));

  for (const t of d.tracks.filter((t) => !opts.hidden.has(t.category))) {
    marks.push(Plot.line(t.points, { x: (p: number[]) => p[0], y: (p: number[]) => p[1], stroke: color(t.category), strokeWidth: 1.4 }));
    marks.push(
      Plot.dot(t.points, {
        x: (p: number[]) => p[0],
        y: (p: number[]) => p[1],
        symbol: () => symbol(t.category),
        fill: color(t.category),
        r: 4.5,
        tip: true,
        title: (p: number[]) => `${t.name}\nx = ${formatValue(p[0])}\ny = ${formatValue(p[1])}`,
      }),
    );
  }

  const pts = visible.filter((o) => okY(markY(o))).map((o) => ({ ...o, y: markY(o) as number }));
  marks.push(
    Plot.dot(pts, {
      x: "x",
      y: "y",
      symbol: (o: XYObject) => symbol(o.category),
      fill: (o: XYObject) => color(o.category),
      stroke: "var(--bg)",
      strokeWidth: 1,
      r: narrow ? 5 : 6.5,
      channels: {
        Object: "name",
        [d.xlabel]: (o: XYObject) => formatValue(o.x),
        Value: (o: XYObject) => formatValue(markY(o)),
        Range: (o: XYObject) => (o.lo !== null && o.hi !== null ? `${formatValue(o.lo)} to ${formatValue(o.hi)}` : ""),
        Maximum: (o: XYObject) => (o.mx !== null ? formatValue(o.mx) : ""),
        Notes: (o: XYObject) => o.notes ?? "",
        Source: "citation",
      },
      tip: { format: { x: false, y: false, fill: false, symbol: false, stroke: false }, lineWidth: 40 },
    }),
  );

  if (opts.labels) {
    const items = pts.map((o) => ({ px: px(o.x), py: py(o.y), text: o.name }));
    for (const t of d.tracks.filter((t) => !opts.hidden.has(t.category))) {
      const p = t.points[t.points.length - 1];
      items.push({ px: px(p[0]), py: py(p[1]), text: t.name });
    }
    const frame = { x0: margin.left, y0: margin.top, x1: width - margin.right, y1: height - margin.bottom };
    marks.push(...labelMarks(placeLabels(items, linePixels, frame, narrow ? 10 : 11), sx, sy, narrow ? 10 : 11));
  }

  return Plot.plot({
    width,
    height,
    marginLeft: margin.left,
    marginRight: margin.right,
    marginTop: margin.top,
    marginBottom: margin.bottom,
    style: { background: "transparent", fontFamily: "var(--font-sans)", fontSize: "12px", overflow: "visible" },
    x: axis(d.xscale, d.xlim, d.xlabel, width - margin.left - margin.right, (v) => String(Math.round(v))),
    y: axis(d.yscale, d.ylim, d.ylabel, height - margin.top - margin.bottom),
    color: { type: "identity" },
    symbol: { type: "identity" },
    marks,
  });
}

// ---------------------------------------------------------------------------
// Bar charts

export function barsPlot(d: BarsChartData, panel: BarPanel, opts: PlotOptions): Element {
  const width = Math.max(300, opts.width);
  const narrow = width < 640;
  const rows = panel.rows.filter((r) => !opts.hidden.has(r.category)).sort((a, b) => b.value - a.value);
  const rowH = narrow ? 44 : 30;
  const longest = Math.max(10, ...rows.map((r) => r.name.length));
  const margin = { left: narrow ? 10 : Math.min(320, longest * 6.6 + 14), right: 70, top: 10, bottom: 44 };
  const height = rows.length * rowH + margin.top + margin.bottom;
  const [x0, x1] = panel.xlim;
  const color = (c: string) => d.categories[c]?.color ?? "#777";
  const unit = d.unit;
  const marks: Plot.Markish[] = [];

  for (const l of panel.lines) {
    const st = LINE_STYLE[l.kind];
    if (l.shade && (l.kind === "upper" || l.kind === "lower")) {
      const r = l.kind === "upper" ? { x1: l.x, x2: x1 } : { x1: x0, x2: l.x };
      marks.push(Plot.rectX([r], { x1: "x1", x2: "x2", fill: st.stroke, fillOpacity: 0.1 }));
    }
    marks.push(Plot.ruleX([l.x], { stroke: st.stroke, strokeWidth: st.width, strokeDasharray: lineDash(l) }));
  }
  marks.push(
    Plot.ruleY(rows, { y: "name", x1: x0, x2: "value", stroke: (r) => color(r.category), strokeOpacity: 0.35, strokeWidth: 4 }),
  );
  const ranged = rows.filter((r) => r.low !== null && r.high !== null);
  marks.push(Plot.ruleY(ranged, { y: "name", x1: "low", x2: "high", stroke: (r: BarRow) => color(r.category), strokeWidth: 1.6 }));
  marks.push(Plot.tickX(ranged, { y: "name", x: "low", stroke: (r) => color(r.category), strokeWidth: 1.6, inset: rowH * 0.3 }));
  marks.push(Plot.tickX(ranged, { y: "name", x: "high", stroke: (r) => color(r.category), strokeWidth: 1.6, inset: rowH * 0.3 }));
  marks.push(
    Plot.dot(rows, {
      y: "name",
      x: "value",
      fill: (r) => color(r.category),
      symbol: (r: BarRow) => d.categories[r.category]?.symbol ?? "circle",
      stroke: "var(--bg)",
      r: 6.5,
      channels: {
        Item: "name",
        Value: (r) => formatValue(r.value, unit),
        Range: (r) => (r.low !== null && r.high !== null ? `${formatValue(r.low, unit)} to ${formatValue(r.high, unit)}` : ""),
        Notes: (r) => r.notes ?? "",
        Source: "citation",
      },
      tip: { format: { x: false, y: false, fill: false, symbol: false, stroke: false }, lineWidth: 40 },
    }),
  );
  marks.push(
    Plot.text(rows, {
      y: "name",
      x: (r) => (r.high !== null ? Math.max(r.high, r.value) : r.value),
      text: (r) => formatValue(r.value, unit),
      dx: 10,
      textAnchor: "start",
      fontSize: 11,
      fill: "currentColor",
    }),
  );
  if (narrow) {
    marks.push(
      Plot.text(rows, { y: "name", x: x0, text: "name", dy: -13, dx: 2, textAnchor: "start", fontSize: 11, fill: "currentColor" }),
    );
  }

  return Plot.plot({
    width,
    height,
    marginLeft: margin.left,
    marginRight: margin.right,
    marginTop: margin.top,
    marginBottom: margin.bottom,
    style: { background: "transparent", fontFamily: "var(--font-sans)", fontSize: "12px", overflow: "visible" },
    x: axis(panel.xscale, panel.xlim, panel.xlabel, width - margin.left - margin.right, (v) => String(v)),
    y: { type: "band", domain: rows.map((r) => r.name), label: null, axis: narrow ? null : "left", tickSize: 0, padding: 0.4 },
    color: { type: "identity" },
    symbol: { type: "identity" },
    marks,
  });
}

// ---------------------------------------------------------------------------
// AI benchmark small multiples

export function benchmarkPlot(d: BenchmarksChartData, key: string, opts: PlotOptions): Element {
  const width = Math.max(260, opts.width);
  const height = Math.round(Math.min(Math.max(width * 0.75, 240), 380));
  const margin = { left: 40, right: 12, top: 10, bottom: 34 };
  const scores = d.scores.filter((s) => s.benchmark === key).sort((a, b) => a.year - b.year);
  const refs = d.refs.filter((r) => r.benchmark === key);
  const [x0, x1] = d.xlim;
  const marks: Plot.Markish[] = [
    Plot.rect([{ x1: x0, x2: x1, y1: 100, y2: 108 }], { x1: "x1", x2: "x2", y1: "y1", y2: "y2", fill: LINE_STYLE.upper.stroke, fillOpacity: 0.1 }),
    Plot.ruleY([100], { stroke: LINE_STYLE.upper.stroke, strokeWidth: 2.5 }),
  ];
  for (const r of refs) {
    if (r.level === "chance") {
      marks.push(Plot.rect([{ x1: x0, x2: x1, y1: 0, y2: r.score_pct }], { x1: "x1", x2: "x2", y1: "y1", y2: "y2", fill: LINE_STYLE.lower.stroke, fillOpacity: 0.08 }));
      marks.push(Plot.ruleY([r.score_pct], { stroke: LINE_STYLE.lower.stroke, strokeWidth: 2, strokeDasharray: "8,5" }));
    } else if (r.level === "human") {
      marks.push(Plot.ruleY([r.score_pct], { stroke: LINE_STYLE.gravity.stroke, strokeWidth: 1.6, strokeDasharray: "7,4", tip: true, title: () => `${r.name}: ${r.score_pct}%\n${r.citation}` }));
    } else {
      marks.push(Plot.ruleY([r.score_pct], { stroke: LINE_STYLE.material.stroke, strokeWidth: 1.8, strokeDasharray: "2,3", tip: true, title: () => `${r.name}: ${r.score_pct}%\n${r.citation}` }));
    }
  }
  const color = "#6250d6";
  marks.push(Plot.line(scores, { x: "year", y: "score_pct", stroke: color, strokeWidth: 1.4 }));
  marks.push(
    Plot.dot(scores, {
      x: "year",
      y: "score_pct",
      fill: color,
      symbol: "diamond",
      r: 5,
      stroke: "var(--bg)",
      channels: { Model: "model", Score: (s) => `${s.score_pct}%`, Setting: "setting", Notes: (s) => s.notes ?? "", Source: "citation" },
      tip: { format: { x: false, y: false, fill: false, symbol: false, stroke: false }, lineWidth: 40 },
    }),
  );
  if (opts.labels) {
    const sx = Plot.scale({ x: { type: "linear", domain: d.xlim, range: [margin.left, width - margin.right] } });
    const sy = Plot.scale({ y: { type: "linear", domain: [0, 108], range: [height - margin.bottom, margin.top] } });
    const items = scores.map((s) => ({ px: Number(sx.apply(s.year)), py: Number(sy.apply(s.score_pct)), text: s.model }));
    const frame = { x0: margin.left, y0: margin.top, x1: width - margin.right, y1: height - margin.bottom };
    marks.push(...labelMarks(placeLabels(items, [], frame, 9.5), sx, sy, 9.5));
  }
  return Plot.plot({
    width,
    height,
    marginLeft: margin.left,
    marginRight: margin.right,
    marginTop: margin.top,
    marginBottom: margin.bottom,
    style: { background: "transparent", fontFamily: "var(--font-sans)", fontSize: "11px", overflow: "visible" },
    x: { domain: d.xlim, label: null, tickFormat: "d", ticks: 4, grid: true },
    y: { domain: [0, 108], label: "Score, %", grid: true, ticks: [0, 25, 50, 75, 100] },
    marks,
  });
}

export function lineSwatch(l: Pick<LimitLine, "kind" | "dashed">): string {
  const st = LINE_STYLE[l.kind];
  const dash = lineDash(l) ? `stroke-dasharray="${lineDash(l)}"` : "";
  return `<svg width="34" height="10" aria-hidden="true"><line x1="1" y1="5" x2="33" y2="5" stroke="${st.stroke}" stroke-width="${st.width}" ${dash}/></svg>`;
}
