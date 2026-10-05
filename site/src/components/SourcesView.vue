<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { chartTitle, pageTitle, t } from "../i18n";
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
});
watch(
  () => t("allSources"),
  (s) => (document.title = pageTitle(s)),
  { immediate: true },
);

const REPO_DOCS = "https://github.com/QuantumNovice/awesome-universal-limits/blob/main/docs";
const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const link = (file: string) => `<a href="${REPO_DOCS}/${file}" target="_blank" rel="noopener" dir="ltr">docs/${file}</a>`;
// Word order differs between languages, so the links go into the translated sentence.
const intro = computed(() => {
  const parts: Record<string, string> = {
    n: total.value ? String(total.value) : "…",
    cmd: '<code dir="ltr">make sources</code>',
    md: link("REFERENCES.md"),
    bib: link("references.bib"),
  };
  return esc(t("sourcesIntro")).replace(/\{(\w+)\}/g, (m, k: string) => parts[k] ?? m);
});
</script>

<template>
  <section class="prose">
    <h1>{{ t("allSources") }}</h1>
    <p v-html="intro"></p>
    <section v-for="g in groups" :key="g.name">
      <h2><a :href="`#/chart/${g.name}`">{{ chartTitle(g.name, g.title) }}</a></h2>
      <ol>
        <li v-for="s in g.sources" :key="s.url" lang="en" dir="ltr">
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
