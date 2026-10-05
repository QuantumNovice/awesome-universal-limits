<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { chartTitle, groupName, locale, pageTitle, t } from "../i18n";
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
    } catch (e) {
      error.value = String(e);
    }
  },
  { immediate: true },
);

const title = computed(() => (chart.value ? chartTitle(chart.value.name, chart.value.title) : ""));
watch(title, (s) => {
  if (s) document.title = pageTitle(s);
});

const TABS = { interactive: "tabInteractive", figure: "tabFigure", data: "tabData", about: "tabAbout" } as const;

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
    { kind: "upper" as const, dashed: false, label: t("benchPerfect"), formula: "100%", source_url: "", citation: "" },
    { kind: "material" as const, dashed: false, label: t("benchLabelError"), formula: "", source_url: "", citation: "" },
    { kind: "gravity" as const, dashed: false, label: t("benchHuman"), formula: "", source_url: "", citation: "" },
    { kind: "lower" as const, dashed: true, label: t("benchChance"), formula: "", source_url: "", citation: "" },
  ];
});

const explainerHtml = computed(() => (chart.value ? renderMarkdown(chart.value.explainer) : ""));
const opts = (width: number) => ({ width, hidden: hidden.value, labels: labels.value });
</script>

<template>
  <article class="chart-view">
    <p v-if="error" class="error">{{ t("loadChartError", { error }) }}</p>
    <template v-else-if="chart">
      <header class="chart-head">
        <p class="eyebrow">{{ groupName(chart.group) }}</p>
        <h1>{{ title }}</h1>
        <p v-if="t('englishNote')" class="lang-note">{{ t("englishNote") }}</p>
      </header>

      <div class="tabs" role="tablist">
        <button
          v-for="tb in ['interactive', 'figure', 'data', 'about'] as const"
          :key="tb"
          role="tab"
          :aria-selected="tab === tb"
          :class="{ on: tab === tb }"
          @click="tab = tb"
        >
          {{ t(TABS[tb]) }}
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
            <span class="dot" :style="{ background: c.color }"></span><span lang="en" dir="ltr">{{ c.label }}</span>
          </button>
          <label class="check"><input v-model="labels" type="checkbox" /> {{ t("labels") }}</label>
        </div>

        <div class="card plot-card" lang="en">
          <PlotHost v-if="chart.kind === 'xy'" :build="(w: number) => xyPlot(chart as any, opts(w))" :deps="[hidden, labels, locale]" />
          <template v-else-if="chart.kind === 'bars'">
            <div v-for="p in chart.panels" :key="p.key" class="bar-panel">
              <h3 v-if="p.title" lang="en" dir="ltr">{{ p.title }}</h3>
              <PlotHost :build="(w: number) => barsPlot(chart as any, p, opts(w))" :deps="[hidden, labels, locale]" />
            </div>
          </template>
          <div v-else class="bench-grid">
            <div v-for="p in chart.panels" :key="p.key" class="bench">
              <h3 lang="en" dir="ltr">{{ p.title }}</h3>
              <PlotHost :build="(w: number) => benchmarkPlot(chart as any, p.key, opts(w))" :deps="[labels, locale]" />
            </div>
          </div>
          <p class="hint" :lang="locale">{{ t("hint") }}</p>
        </div>
        <p v-if="chart.footnote" class="footnote" lang="en" dir="ltr">{{ chart.footnote }}</p>

        <h2 class="sub">{{ t("limitLines") }}</h2>
        <LinesLegend :lines="legendLines" :english="chart.kind !== 'benchmarks'" />
      </section>

      <section v-else-if="tab === 'figure'" class="panel">
        <div class="card figure-card">
          <img :src="asset(chart.png)" :alt="title" loading="lazy" />
        </div>
        <p class="downloads">
          <a :href="asset(chart.png)" download>{{ t("downloadPng") }}</a>
          <a :href="asset(chart.pdf)" download>{{ t("downloadPdf") }}</a>
        </p>
      </section>

      <section v-else-if="tab === 'data'" class="panel">
        <DataTable :chart="chart" />
        <h2 class="sub">{{ t("chartSources") }}</h2>
        <ol class="sources">
          <li v-for="s in chart.sources" :key="s.url" lang="en" dir="ltr">
            {{ s.citation }}. <a :href="s.url" target="_blank" rel="noopener">{{ s.url }}</a>
          </li>
        </ol>
      </section>

      <section v-else class="panel prose" lang="en" dir="ltr" v-html="explainerHtml"></section>
    </template>
    <p v-else class="loading">{{ t("loading") }}</p>
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
.lang-note {
  margin: -6px 0 14px;
  font-size: 13px;
  color: var(--text-3);
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
  margin-inline-start: auto;
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
  padding-inline-start: 22px;
  line-height: 1.5;
}
.sources a {
  overflow-wrap: anywhere;
}
.error {
  color: #c2352f;
}
</style>
