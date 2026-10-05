<script setup lang="ts">
import { t } from "../i18n";
import { lineSwatch } from "../lib/plots";
import type { LimitLine } from "../lib/types";

// english: the labels come from the (English) chart data rather than from the translations.
withDefaults(
  defineProps<{
    lines: Pick<LimitLine, "kind" | "dashed" | "label" | "formula" | "source_url" | "citation">[];
    english?: boolean;
  }>(),
  { english: true },
);

const KIND = {
  upper: "kindUpper",
  lower: "kindLower",
  material: "kindPractical",
  gravity: "kindPractical",
  reference: "kindReference",
} as const;
</script>

<template>
  <ul class="legend">
    <li v-for="l in lines" :key="l.label">
      <span class="swatch" v-html="lineSwatch(l)"></span>
      <span class="text">
        <span class="label" :lang="english ? 'en' : undefined" :dir="english ? 'ltr' : undefined">{{ l.label }}</span>
        <span class="meta">
          {{ t(KIND[l.kind]) }}<template v-if="l.dashed && (l.kind === 'upper' || l.kind === 'lower')"> · {{ t("observabilityFloor") }}</template>
          <template v-if="l.formula"> · <code dir="ltr">{{ l.formula }}</code></template>
          <template v-if="l.source_url">
            · <a :href="l.source_url" target="_blank" rel="noopener" lang="en" dir="ltr">{{ l.citation || t("source") }}</a>
          </template>
        </span>
      </span>
    </li>
  </ul>
</template>

<style scoped>
.legend {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 8px;
}
li {
  display: flex;
  gap: 10px;
  align-items: flex-start;
}
.swatch {
  flex: none;
  padding-top: 4px;
}
.label {
  display: block;
  font-size: 14px;
}
.meta {
  display: block;
  font-size: 12px;
  color: var(--text-3);
  overflow-wrap: anywhere;
}
code {
  font-size: 11.5px;
}
</style>
