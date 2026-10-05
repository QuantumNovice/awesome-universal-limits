<script setup lang="ts">
import { computed } from "vue";
import { t } from "../i18n";
import { formatValue } from "../lib/format";
import type { ChartData } from "../lib/types";
import { asset } from "../lib/data";
import { markY } from "../lib/plots";

const props = defineProps<{ chart: ChartData }>();

interface Row {
  key: string;
  name: string;
  category: string;
  value: string;
  range: string;
  notes: string;
  url: string;
  citation: string;
}

const rows = computed<Row[]>(() => {
  const c = props.chart;
  if (c.kind === "xy") {
    return c.objects.map((o) => ({
      key: o.id,
      name: o.name,
      category: c.categories[o.category]?.label ?? o.category,
      value: t("valueAt", { v: formatValue(markY(o)), x: formatValue(o.x) }),
      range: o.lo !== null && o.hi !== null ? t("rangeTo", { lo: formatValue(o.lo), hi: formatValue(o.hi) }) : "",
      notes: o.notes ?? "",
      url: o.source_url,
      citation: o.citation,
    }));
  }
  if (c.kind === "bars") {
    return c.panels.flatMap((p) =>
      p.rows.map((r) => ({
        key: r.id,
        name: r.name,
        category: c.categories[r.category]?.label ?? r.category,
        value: formatValue(r.value, c.unit),
        range:
          r.low !== null && r.high !== null ? t("rangeTo", { lo: formatValue(r.low, c.unit), hi: formatValue(r.high, c.unit) }) : "",
        notes: r.notes ?? "",
        url: r.source_url,
        citation: r.citation,
      })),
    );
  }
  return c.scores.map((s) => ({
    key: s.id,
    name: s.model,
    category: s.benchmark,
    value: `${s.score_pct}% (${s.year.toFixed(1)})`,
    range: s.setting,
    notes: s.notes ?? "",
    url: s.source_url,
    citation: s.citation,
  }));
});
</script>

<template>
  <div class="downloads">
    {{ t("download") }}
    <template v-for="ds in chart.datasets" :key="ds">
      <a :href="asset(`data/json/${ds}.json`)" download>{{ ds }}.json</a>
      <a :href="`https://github.com/QuantumNovice/awesome-universal-limits/blob/main/data/${ds}.csv`" target="_blank" rel="noopener"
        >{{ ds }}.csv</a
      >
    </template>
  </div>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>{{ t("colObject") }}</th>
          <th>{{ t("colClass") }}</th>
          <th>{{ t("colValue") }}</th>
          <th>{{ t("colRange") }}</th>
          <th>{{ t("colSource") }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in rows" :key="r.key">
          <td lang="en" dir="ltr">
            <strong>{{ r.name }}</strong>
            <div v-if="r.notes" class="notes">{{ r.notes }}</div>
          </td>
          <td lang="en" dir="ltr">{{ r.category }}</td>
          <td class="num"><bdi>{{ r.value }}</bdi></td>
          <td class="num"><bdi>{{ r.range }}</bdi></td>
          <td class="src" lang="en" dir="ltr">
            <a :href="r.url" target="_blank" rel="noopener">{{ r.citation }}</a>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.downloads {
  display: flex;
  flex-wrap: wrap;
  gap: 6px 12px;
  font-size: 13px;
  margin-bottom: 12px;
  color: var(--text-3);
}
.table-wrap {
  overflow-x: auto;
  border: 1px solid var(--border);
  border-radius: 10px;
}
table {
  border-collapse: collapse;
  width: 100%;
  font-size: 13px;
  min-width: 640px;
}
th,
td {
  text-align: start;
  vertical-align: top;
  padding: 8px 10px;
  border-bottom: 1px solid var(--border);
}
th {
  position: sticky;
  top: 0;
  background: var(--surface);
  font-weight: 600;
  color: var(--text-2);
}
tr:last-child td {
  border-bottom: none;
}
.num {
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}
.notes {
  color: var(--text-3);
  font-size: 12px;
  margin-top: 2px;
}
.src {
  max-width: 340px;
  font-size: 12px;
}
</style>
