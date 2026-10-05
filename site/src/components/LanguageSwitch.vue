<script setup lang="ts">
import { LANGUAGE_NAMES, LOCALES, locale, setLocale, t, type Locale } from "../i18n";

function onChange(e: Event) {
  setLocale((e.target as HTMLSelectElement).value as Locale);
}
</script>

<template>
  <label class="lang">
    <span class="sr-only">{{ t("language") }}</span>
    <svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">
      <circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.6" />
      <path d="M3 12h18M12 3c2.6 2.6 2.6 15.4 0 18M12 3c-2.6 2.6-2.6 15.4 0 18" fill="none" stroke="currentColor" stroke-width="1.6" />
    </svg>
    <select :value="locale" @change="onChange">
      <option v-for="l in LOCALES" :key="l" :value="l" :lang="l">{{ LANGUAGE_NAMES[l] }}</option>
    </select>
  </label>
</template>

<style scoped>
.lang {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--text-3);
}
select {
  font: inherit;
  font-size: 13px;
  padding: 4px 8px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text);
}
</style>
