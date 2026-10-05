// Shapes of the JSON written by src/allowed_universe/site_export.py.

export interface Category {
  label: string;
  color: string;
  symbol: string;
}

export interface Source {
  url: string;
  citation: string;
}

export type LineKind = "upper" | "lower" | "material" | "gravity" | "reference";

export interface LimitLine {
  id: string;
  label: string;
  kind: LineKind;
  dashed: boolean;
  shade: boolean;
  formula: string;
  forbidden: string | null;
  forbidden_xy: [number, number] | null;
  source_url: string;
  citation: string;
  points?: [number, number | null][];
  x?: number;
}

export interface XYObject {
  id: string;
  name: string;
  category: string;
  x: number;
  lo: number | null;
  hi: number | null;
  ex: number | null;
  mx: number | null;
  source_url: string;
  citation: string;
  notes: string | null;
}

export interface Track {
  name: string;
  category: string;
  points: [number, number][];
}

interface ChartBase {
  name: string;
  title: string;
  group: string;
  datasets: string[];
  explainer: string;
  sources: Source[];
  png: string;
  pdf: string;
  footnote?: string;
}

export interface XYChartData extends ChartBase {
  kind: "xy";
  xlabel: string;
  ylabel: string;
  xlim: [number, number];
  ylim: [number, number];
  xscale: "log" | "linear";
  yscale: "log" | "linear";
  categories: Record<string, Category>;
  lines: LimitLine[];
  objects: XYObject[];
  tracks: Track[];
  labels: { range: string; max: string; cap: string };
}

export interface BarRow {
  id: string;
  name: string;
  category: string;
  value: number;
  low: number | null;
  high: number | null;
  source_url: string;
  citation: string;
  notes: string | null;
}

export interface BarLine {
  x: number;
  label: string;
  kind: LineKind;
  shade: boolean;
}

export interface BarPanel {
  key: string;
  title: string;
  xlabel: string;
  xlim: [number, number];
  xscale: "log" | "linear";
  lines: BarLine[];
  rows: BarRow[];
}

export interface BarsChartData extends ChartBase {
  kind: "bars";
  unit: string;
  categories: Record<string, Category>;
  panels: BarPanel[];
}

export interface BenchmarkScore {
  id: string;
  benchmark: string;
  model: string;
  year: number;
  score_pct: number;
  setting: string;
  source_url: string;
  citation: string;
  notes: string | null;
}

export interface BenchmarkRef {
  id: string;
  benchmark: string;
  level: "chance" | "human" | "ceiling";
  score_pct: number;
  name: string;
  source_url: string;
  citation: string;
  notes: string | null;
}

export interface BenchmarksChartData extends ChartBase {
  kind: "benchmarks";
  panels: { key: string; title: string }[];
  xlim: [number, number];
  scores: BenchmarkScore[];
  refs: BenchmarkRef[];
}

export type ChartData = XYChartData | BarsChartData | BenchmarksChartData;

export interface SiteIndex {
  groups: { name: string; charts: string[] }[];
  charts: Record<string, { title: string; group: string; kind: string }>;
  datasets: Record<string, string>;
}
