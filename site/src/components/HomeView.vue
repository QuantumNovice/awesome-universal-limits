<script setup lang="ts">
import { chartTitle, groupName, t } from "../i18n";
import { asset } from "../lib/data";
import type { SiteIndex } from "../lib/types";

defineProps<{ index: SiteIndex }>();
</script>

<template>
  <section class="home">
    <header class="hero">
      <h1>{{ t("siteName") }}</h1>
      <p class="lede">{{ t("tagline") }}</p>
      <div class="keys">
        <span><i class="k red"></i><span><strong>{{ t("keyForbiddenStrong") }}</strong> {{ t("keyForbidden") }}</span></span>
        <span><i class="k amber"></i><span><strong>{{ t("keyPracticalStrong") }}</strong> {{ t("keyPractical") }}</span></span>
        <span><i class="k violet"></i><span><strong>{{ t("keyMarkersStrong") }}</strong> {{ t("keyMarkers") }}</span></span>
      </div>
    </header>

    <section v-for="g in index.groups" :key="g.name" class="group">
      <h2>{{ groupName(g.name) }}</h2>
      <div class="grid">
        <a v-for="c in g.charts" :key="c" class="tile" :href="`#/chart/${c}`">
          <img :src="asset(`figures/${c}.png`)" :alt="chartTitle(c, index.charts[c].title)" loading="lazy" />
          <span>{{ chartTitle(c, index.charts[c].title) }}</span>
        </a>
      </div>
    </section>
  </section>
</template>

<style scoped>
.hero h1 {
  font-size: clamp(30px, 5vw, 46px);
  margin: 4px 0 6px;
  line-height: 1.05;
}
.lede {
  font-size: clamp(16px, 2.2vw, 19px);
  color: var(--text-2);
  margin: 0 0 16px;
}
.keys {
  display: grid;
  gap: 6px;
  font-size: 14px;
  color: var(--text-2);
  margin-bottom: 8px;
}
.keys span {
  display: flex;
  gap: 8px;
  align-items: baseline;
}
.k {
  display: inline-block;
  width: 22px;
  height: 0;
  border-top: 3px solid;
  flex: none;
  transform: translateY(-3px);
}
.k.red {
  border-color: #e34948;
}
.k.amber {
  border-top-style: dotted;
  border-color: #d08a00;
}
.k.violet {
  border-color: #6250d6;
  width: 10px;
  height: 10px;
  border: none;
  background: #6250d6;
  transform: rotate(45deg);
}
.group h2 {
  font-size: 18px;
  margin: 28px 0 10px;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 220px), 1fr));
  gap: 12px;
}
.tile {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 10px;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--surface);
  text-decoration: none;
  color: var(--text);
  transition:
    border-color 0.15s,
    transform 0.15s;
}
.tile:hover {
  border-color: var(--accent);
  transform: translateY(-1px);
}
.tile img {
  width: 100%;
  aspect-ratio: 6 / 5;
  object-fit: cover;
  object-position: top;
  border-radius: 6px;
  background: #fff;
}
.tile span {
  font-size: 14px;
  font-weight: 600;
  line-height: 1.3;
}
</style>
