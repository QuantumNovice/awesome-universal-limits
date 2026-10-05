<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { asset, loadChart } from "../lib/data";
import { renderMarkdown } from "../lib/markdown";
import { barsPlot, benchmarkPlot, xyPlot } from "../lib/plots";
import type { ChartData } from "../lib/types";
import DataTable from "./DataTable.vue";
import LinesLegend from "./LinesLegend.vue";
import PlotHost from "./PlotHost.vue";

const props = defineProps<{ name: string }>();

const chart = ref<ChartData | null>(null);
const error = ref("");
const tab = ref<"interactive" | "figure" | "data" | "about">("interactive");
const hidden = ref(new Set<string>());
const labels = ref(true);

watch(
  () => props.name,
  async (name) => {
    chart.value = null;
    error.value = "";
    hidden.value = new Set();
    try {
      chart.value = await loadChart(name);
      document.title = `${chart.value.title} · The Allowed Universe`;
    } catch (e) {
      error.value = String(e);
    }
  },
  { immediate: true },
);

const categories = computed(() => {
  const c = chart.value;
  if (!c || c.kind === "benchmarks") return [];
  const used = new Set<string>(
    c.kind === "xy"
      ? [...c.objects.map((o) => o.category), ...c.tracks.map((t) => t.category)]
      : c.panels.flatMap((p) => p.rows.map((r) => r.category)),
  );
  // categories that share a label (e.g. molecular and living) share one chip
  const chips = new Map<string, { keys: string[]; label: string; color: string }>();
  for (const [key, v] of Object.entries(c.categories)) {
    if (!used.has(key)) continue;
    const chip = chips.get(v.label) ?? { keys: [], label: v.label, color: v.color };
    chip.keys.push(key);
    chips.set(v.label, chip);
  }
  return [...chips.values()];
});

function toggle(keys: string[]) {
  const s = new Set(hidden.value);
  const off = keys.every((k) => s.has(k));
  for (const k of keys) {
    if (off) s.delete(k);
    else s.add(k);
  }
  hidden.value = s;
}

const legendLines = computed(() => {
  const c = chart.value;
  if (!c) return [];
  if (c.kind === "xy") return c.lines;
  if (c.kind === "bars")
    return c.panels.flatMap((p) =>
      p.lines.map((l) => ({ ...l, dashed: false, formula: "", source_url: "", citation: "" })),
    );
  return [
    { kind: "upper" as const, dashed: false, label: "Perfect score (hard ceiling)", formula: "100%", source_url: "", citation: "" },
    { kind: "material" as const, dashed: false, label: "Label-error ceiling (MMLU)", formula: "", source_url: "", citation: "" },
    { kind: "gravity" as const, dashed: false, label: "Human baseline", formula: "", source_url: "", citation: "" },
    { kind: "lower" as const, dashed: true, label: "Random guessing", formula: "", source_url: "", citation: "" },
  ];
});

const explainerHtml = computed(() => (chart.value ? renderMarkdown(chart.value.explainer) : ""));
const opts = (width: number) => ({ width, hidden: hidden.value, labels: labels.value });
</script>

<template>
  <article class="chart-view">
    <p v-if="error" class="error">Could not load this chart: {{ error }}</p>
    <template v-else-if="chart">
      <header class="chart-head">
        <p class="eyebrow">{{ chart.group }}</p>
        <h1>{{ chart.title }}</h1>
      </header>

      <div class="tabs" role="tablist">
        <button
          v-for="t in ['interactive', 'figure', 'data', 'about'] as const"
          :key="t"
          role="tab"
          :aria-selected="tab === t"
          :class="{ on: tab === t }"
          @click="tab = t"
        >
          {{ { interactive: "Interactive", figure: "Print figure", data: "Data & sources", about: "Explainer" }[t] }}
        </button>
      </div>

      <section v-if="tab === 'interactive'" class="panel">
        <div class="controls">
          <button
            v-for="c in categories"
            :key="c.label"
            class="chip"
            :class="{ off: c.keys.every((k) => hidden.has(k)) }"
            :aria-pressed="!c.keys.every((k) => hidden.has(k))"
            @click="toggle(c.keys)"
          >
            <span class="dot" :style="{ background: c.color }"></span>{{ c.label }}
          </button>
          <label class="check"><input v-model="labels" type="checkbox" /> Labels</label>
        </div>

        <div class="card plot-card">
          <PlotHost v-if="chart.kind === 'xy'" :build="(w: number) => xyPlot(chart as any, opts(w))" :deps="[hidden, labels]" />
          <template v-else-if="chart.kind === 'bars'">
            <div v-for="p in chart.panels" :key="p.key" class="bar-panel">
              <h3 v-if="p.title">{{ p.title }}</h3>
              <PlotHost :build="(w: number) => barsPlot(chart as any, p, opts(w))" :deps="[hidden, labels]" />
            </div>
          </template>
          <div v-else class="bench-grid">
            <div v-for="p in chart.panels" :key="p.key" class="bench">
              <h3>{{ p.title }}</h3>
              <PlotHost :build="(w: number) => benchmarkPlot(chart as any, p.key, opts(w))" :deps="[labels]" />
            </div>
          </div>
          <p class="hint">Hover or tap a marker for its value, notes and source.</p>
        </div>
        <p v-if="chart.footnote" class="footnote">{{ chart.footnote }}</p>

        <h2 class="sub">Limit lines</h2>
        <LinesLegend :lines="legendLines" />
      </section>

      <section v-else-if="tab === 'figure'" class="panel">
        <div class="card figure-card">
          <img :src="asset(chart.png)" :alt="chart.title" loading="lazy" />
        </div>
        <p class="downloads">
          <a :href="asset(chart.png)" download>Download PNG (200 dpi)</a>
          <a :href="asset(chart.pdf)" download>Download PDF (vector)</a>
        </p>
      </section>

      <section v-else-if="tab === 'data'" class="panel">
        <DataTable :chart="chart" />
        <h2 class="sub">All sources for this chart</h2>
        <ol class="sources">
          <li v-for="s in chart.sources" :key="s.url">
            {{ s.citation }}. <a :href="s.url" target="_blank" rel="noopener">{{ s.url }}</a>
          </li>
        </ol>
      </section>

      <section v-else class="panel prose" v-html="explainerHtml"></section>
    </template>
    <p v-else class="loading">Loading…</p>
  </article>
</template>

<style scoped>
.chart-view {
  min-width: 0;
}
.chart-head h1 {
  margin: 2px 0 14px;
  font-size: clamp(22px, 3.2vw, 32px);
  line-height: 1.15;
}
.eyebrow {
  margin: 0;
  font-size: 12px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--text-3);
}
.tabs {
  display: flex;
  gap: 4px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 16px;
  overflow-x: auto;
}
.tabs button {
  font: inherit;
  font-size: 14px;
  background: none;
  border: none;
  color: var(--text-2);
  padding: 9px 12px;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  white-space: nowrap;
}
.tabs button.on {
  color: var(--text);
  border-bottom-color: var(--accent);
  font-weight: 600;
}
.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: center;
  margin-bottom: 10px;
}
.chip {
  font: inherit;
  font-size: 13px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 10px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text);
  cursor: pointer;
}
.chip.off {
  opacity: 0.45;
  text-decoration: line-through;
}
.chip .dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}
.check {
  font-size: 13px;
  margin-left: auto;
  display: inline-flex;
  gap: 6px;
  align-items: center;
  color: var(--text-2);
}
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 12px;
}
.plot-card {
  color: var(--text);
}
.bar-panel h3,
.bench h3 {
  font-size: 14px;
  margin: 6px 4px;
  font-weight: 600;
}
.bench-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr));
  gap: 12px;
}
.hint {
  margin: 6px 4px 0;
  font-size: 12px;
  color: var(--text-3);
}
.footnote {
  font-size: 13px;
  color: var(--text-2);
}
.sub {
  font-size: 17px;
  margin: 26px 0 10px;
}
.figure-card img {
  width: 100%;
  height: auto;
  display: block;
  border-radius: 6px;
  background: #fff;
}
.downloads {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}
.sources {
  font-size: 13px;
  padding-left: 22px;
  line-height: 1.5;
}
.sources a {
  overflow-wrap: anywhere;
}
.error {
  color: #c2352f;
}
</style>
