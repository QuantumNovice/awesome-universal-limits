<script setup lang="ts">
import type { SiteIndex } from "../lib/types";

defineProps<{ index: SiteIndex; current: string }>();
const emit = defineEmits<{ go: [route: string] }>();

function onSelect(e: Event) {
  emit("go", (e.target as HTMLSelectElement).value);
}
</script>

<template>
  <nav class="nav" aria-label="Charts">
    <label class="nav-select">
      <span class="sr-only">Choose a chart</span>
      <select :value="current" @change="onSelect">
        <option value="">Overview</option>
        <optgroup v-for="g in index.groups" :key="g.name" :label="g.name">
          <option v-for="c in g.charts" :key="c" :value="`chart/${c}`">{{ index.charts[c].title }}</option>
        </optgroup>
        <option value="sources">All sources</option>
      </select>
    </label>
    <div class="nav-list">
      <a href="#/" :class="{ active: current === '' }">Overview</a>
      <section v-for="g in index.groups" :key="g.name">
        <h3>{{ g.name }}</h3>
        <a
          v-for="c in g.charts"
          :key="c"
          :href="`#/chart/${c}`"
          :class="{ active: current === `chart/${c}` }"
          >{{ index.charts[c].title }}</a
        >
      </section>
      <section>
        <h3>Reference</h3>
        <a href="#/sources" :class="{ active: current === 'sources' }">All sources</a>
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
