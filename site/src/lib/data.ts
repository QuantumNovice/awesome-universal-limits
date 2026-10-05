import type { ChartData, SiteIndex } from "./types";

export const base = import.meta.env.BASE_URL;

export function asset(path: string): string {
  return `${base}${path}`;
}

let indexPromise: Promise<SiteIndex> | null = null;
const charts = new Map<string, Promise<ChartData>>();

export function loadIndex(): Promise<SiteIndex> {
  indexPromise ??= fetch(asset("data/index.json")).then((r) => {
    if (!r.ok) throw new Error(`index.json: HTTP ${r.status}`);
    return r.json();
  });
  return indexPromise;
}

export function loadChart(name: string): Promise<ChartData> {
  if (!charts.has(name)) {
    charts.set(
      name,
      fetch(asset(`data/charts/${name}.json`)).then((r) => {
        if (!r.ok) throw new Error(`${name}.json: HTTP ${r.status}`);
        return r.json();
      }),
    );
  }
  return charts.get(name)!;
}
