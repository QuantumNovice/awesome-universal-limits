<script setup lang="ts">
import { lineSwatch } from "../lib/plots";
import type { LimitLine } from "../lib/types";

defineProps<{ lines: Pick<LimitLine, "kind" | "dashed" | "label" | "formula" | "source_url" | "citation">[] }>();

const KIND: Record<string, string> = {
  upper: "Hard bound (upper)",
  lower: "Hard bound (lower)",
  material: "Practical limit",
  gravity: "Practical limit",
  reference: "Reference",
};
</script>

<template>
  <ul class="legend">
    <li v-for="l in lines" :key="l.label">
      <span class="swatch" v-html="lineSwatch(l)"></span>
      <span class="text">
        <span class="label">{{ l.label }}</span>
        <span class="meta">
          {{ KIND[l.kind] }}<template v-if="l.dashed"> · observability floor</template>
          <template v-if="l.formula"> · <code>{{ l.formula }}</code></template>
          <template v-if="l.source_url">
            · <a :href="l.source_url" target="_blank" rel="noopener">{{ l.citation || "source" }}</a>
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
