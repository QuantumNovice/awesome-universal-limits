const SUP: Record<string, string> = {
  "0": "⁰",
  "1": "¹",
  "2": "²",
  "3": "³",
  "4": "⁴",
  "5": "⁵",
  "6": "⁶",
  "7": "⁷",
  "8": "⁸",
  "9": "⁹",
  "-": "⁻",
};

export function superscript(n: number | string): string {
  return String(n)
    .split("")
    .map((c) => SUP[c] ?? c)
    .join("");
}

/** 10ⁿ for a power of ten (axis ticks). */
export function powerOfTen(v: number): string {
  const e = Math.round(Math.log10(v));
  if (e === 0) return "1";
  if (e === 1) return "10";
  return "10" + superscript(e);
}

/** Human-readable number: 1,234 or 1.5×10¹⁴ or 3.2×10⁻⁶. */
export function formatValue(v: number | null | undefined, unit = ""): string {
  if (v === null || v === undefined || !isFinite(v)) return "—";
  const a = Math.abs(v);
  let s: string;
  if (a === 0) s = "0";
  else if (a >= 1e5 || a < 1e-3) {
    const e = Math.floor(Math.log10(a));
    const m = v / 10 ** e;
    const ms = Number(m.toPrecision(3)).toString();
    s = ms === "1" ? "10" + superscript(e) : `${ms}×10${superscript(e)}`;
  } else if (a >= 100) s = Math.round(v).toLocaleString("en-US");
  else s = Number(v.toPrecision(3)).toString();
  return unit ? `${s} ${unit}` : s;
}

/** Decade ticks spaced so that at most `maxTicks` appear. */
export function logTicks(lo: number, hi: number, maxTicks: number): number[] {
  const a = Math.ceil(Math.log10(lo) - 1e-9);
  const b = Math.floor(Math.log10(hi) + 1e-9);
  const span = Math.max(1, b - a);
  const steps = [1, 2, 5, 10, 20, 25, 50, 100];
  const step = steps.find((s) => span / s <= maxTicks) ?? 100;
  const first = Math.ceil(a / step) * step;
  const out: number[] = [];
  for (let p = first; p <= b; p += step) out.push(10 ** p);
  return out;
}

export function slug(s: string): string {
  return s.toLowerCase().replace(/[^a-z0-9]+/g, "-");
}
