<script setup lang="ts">
import { onMounted, ref } from "vue";
import { loadChart } from "../lib/data";
import type { SiteIndex, Source } from "../lib/types";

const props = defineProps<{ index: SiteIndex }>();
const groups = ref<{ name: string; title: string; sources: Source[] }[]>([]);
const total = ref(0);

onMounted(async () => {
  const names = props.index.groups.flatMap((g) => g.charts);
  const docs = await Promise.all(names.map((n) => loadChart(n)));
  groups.value = docs.map((d) => ({ name: d.name, title: d.title, sources: d.sources }));
  total.value = new Set(docs.flatMap((d) => d.sources.map((s) => s.url))).size;
  document.title = "All sources · The Allowed Universe";
});
</script>

<template>
  <section class="prose">
    <h1>All sources</h1>
    <p>
      {{ total || "Every" }} distinct sources back the values and limit lines on this site. Journal sources are DOIs,
      checked against Crossref by <code>make sources</code>. The same list is in
      <a href="https://github.com/QuantumNovice/the-allowed-universe/blob/main/docs/REFERENCES.md" target="_blank" rel="noopener"
        >docs/REFERENCES.md</a
      >
      and as BibTeX in
      <a href="https://github.com/QuantumNovice/the-allowed-universe/blob/main/docs/references.bib" target="_blank" rel="noopener"
        >docs/references.bib</a
      >.
    </p>
    <section v-for="g in groups" :key="g.name">
      <h2><a :href="`#/chart/${g.name}`">{{ g.title }}</a></h2>
      <ol>
        <li v-for="s in g.sources" :key="s.url">
          {{ s.citation }}. <a :href="s.url" target="_blank" rel="noopener">{{ s.url }}</a>
        </li>
      </ol>
    </section>
  </section>
</template>

<style scoped>
ol {
  font-size: 13px;
  line-height: 1.5;
}
a {
  overflow-wrap: anywhere;
}
h2 {
  font-size: 17px;
}
</style>
