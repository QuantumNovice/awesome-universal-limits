<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import ChartView from "./components/ChartView.vue";
import HomeView from "./components/HomeView.vue";
import NavMenu from "./components/NavMenu.vue";
import LanguageSwitch from "./components/LanguageSwitch.vue";
import SourcesView from "./components/SourcesView.vue";
import { pageTitle, t } from "./i18n";
import { loadIndex } from "./lib/data";
import type { SiteIndex } from "./lib/types";

const index = ref<SiteIndex | null>(null);
const error = ref("");
const route = ref(readHash());

function readHash(): string {
  return decodeURIComponent(location.hash.replace(/^#\/?/, ""));
}
function onHash() {
  route.value = readHash();
  window.scrollTo({ top: 0 });
}
function go(r: string) {
  location.hash = `#/${r}`;
}

onMounted(async () => {
  window.addEventListener("hashchange", onHash);
  try {
    index.value = await loadIndex();
  } catch (e) {
    error.value = String(e);
  }
});
onBeforeUnmount(() => window.removeEventListener("hashchange", onHash));

const chartName = computed(() => (route.value.startsWith("chart/") ? route.value.slice(6) : ""));
watch(
  [route, () => t("siteName")],
  ([r]) => {
    if (r === "") document.title = pageTitle();
  },
  { immediate: true },
);
</script>

<template>
  <div class="layout">
    <aside class="side">
      <a class="brand" href="#/">
        <svg viewBox="0 0 32 32" width="26" height="26" aria-hidden="true">
          <rect width="32" height="32" rx="7" fill="var(--surface)" stroke="var(--border)" />
          <path d="M5 5 L27 27" stroke="#e34948" stroke-width="3" />
          <path d="M5 27 Q 14 19 27 25" stroke="#2a78d6" stroke-width="3" fill="none" />
          <circle cx="15" cy="17" r="3" fill="#6250d6" />
        </svg>
        <span>{{ t("siteName") }}</span>
      </a>
      <LanguageSwitch class="lang-switch" />
      <NavMenu v-if="index" :index="index" :current="route" @go="go" />
    </aside>
    <main class="main">
      <p v-if="error" class="error">{{ t("loadIndexError", { error, cmd: "make figures" }) }}</p>
      <template v-else-if="index">
        <ChartView v-if="chartName && index.charts[chartName]" :name="chartName" />
        <SourcesView v-else-if="route === 'sources'" :index="index" />
        <HomeView v-else :index="index" />
      </template>
      <p v-else class="loading">{{ t("loading") }}</p>
      <footer class="foot">
        {{ t("license") }} ·
        <a href="https://github.com/QuantumNovice/awesome-universal-limits" target="_blank" rel="noopener">GitHub</a>
      </footer>
    </main>
  </div>
</template>
