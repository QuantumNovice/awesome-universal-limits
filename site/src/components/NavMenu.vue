<script setup lang="ts">
import { chartTitle, groupName, t } from "../i18n";
import type { SiteIndex } from "../lib/types";

defineProps<{ index: SiteIndex; current: string }>();
const emit = defineEmits<{ go: [route: string] }>();

function onSelect(e: Event) {
  emit("go", (e.target as HTMLSelectElement).value);
}
</script>

<template>
  <nav class="nav" :aria-label="t('charts')">
    <label class="nav-select">
      <span class="sr-only">{{ t("chooseChart") }}</span>
      <select :value="current" @change="onSelect">
        <option value="">{{ t("overview") }}</option>
        <optgroup v-for="g in index.groups" :key="g.name" :label="groupName(g.name)">
          <option v-for="c in g.charts" :key="c" :value="`chart/${c}`">{{ chartTitle(c, index.charts[c].title) }}</option>
        </optgroup>
        <option value="sources">{{ t("allSources") }}</option>
      </select>
    </label>
    <div class="nav-list">
      <a href="#/" :class="{ active: current === '' }">{{ t("overview") }}</a>
      <section v-for="g in index.groups" :key="g.name">
        <h3>{{ groupName(g.name) }}</h3>
        <a
          v-for="c in g.charts"
          :key="c"
          :href="`#/chart/${c}`"
          :class="{ active: current === `chart/${c}` }"
          >{{ chartTitle(c, index.charts[c].title) }}</a
        >
      </section>
      <section>
        <h3>{{ t("reference") }}</h3>
        <a href="#/sources" :class="{ active: current === 'sources' }">{{ t("allSources") }}</a>
      </section>
    </div>
  </nav>
</template>

<style scoped>
.nav-select {
  display: none;
}
.nav-select select {
  width: 100%;
  max-width: 100%;
  text-overflow: ellipsis;
  font: inherit;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text);
}
.nav-list a {
  display: block;
  padding: 5px 10px;
  border-radius: 6px;
  color: var(--text-2);
  text-decoration: none;
  font-size: 14px;
  line-height: 1.35;
}
.nav-list a:hover {
  background: var(--hover);
  color: var(--text);
}
.nav-list a.active {
  background: var(--accent-soft);
  color: var(--text);
  font-weight: 600;
}
h3 {
  margin: 18px 10px 4px;
  font-size: 11px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--text-3);
}
@media (max-width: 900px) {
  .nav-select {
    display: block;
  }
  .nav-list {
    display: none;
  }
}
</style>
