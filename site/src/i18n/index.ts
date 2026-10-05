// A deliberately small i18n layer: one reactive locale, string lookup with {placeholders},
// and translated chart titles and group names that fall back to the English JSON.
//
// The locale comes from ?lang= in the URL, then the visitor's saved choice, then the
// browser language, then English. Choosing a language saves it and puts ?lang= in the URL
// so the link can be shared.

import { computed, ref } from "vue";
import { GROUPS, LOCALES, MESSAGES, RTL, TITLES, type Locale, type MessageKey } from "./messages";

export { LANGUAGE_NAMES, LOCALES, type Locale } from "./messages";

const STORAGE_KEY = "lang";

function isLocale(v: string | null | undefined): v is Locale {
  return !!v && (LOCALES as readonly string[]).includes(v);
}

function detect(): Locale {
  const fromUrl = new URLSearchParams(location.search).get("lang");
  if (isLocale(fromUrl)) return fromUrl;
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (isLocale(saved)) return saved;
  } catch {
    // storage blocked (private mode, sandboxed preview): fall through
  }
  for (const lang of navigator.languages ?? [navigator.language]) {
    const short = lang.slice(0, 2).toLowerCase();
    if (isLocale(short)) return short;
  }
  return "en";
}

export const locale = ref<Locale>(detect());
export const isRtl = computed(() => RTL.has(locale.value));

function applyToDocument() {
  document.documentElement.lang = locale.value;
  document.documentElement.dir = isRtl.value ? "rtl" : "ltr";
}
applyToDocument();

export function setLocale(l: Locale) {
  locale.value = l;
  try {
    localStorage.setItem(STORAGE_KEY, l);
  } catch {
    // not persisted; the URL below still carries it
  }
  const url = new URL(location.href);
  if (l === "en") url.searchParams.delete("lang");
  else url.searchParams.set("lang", l);
  history.replaceState(history.state, "", url);
  applyToDocument();
}

/** Look up an interface string; {name} placeholders are filled from `params`. */
export function t(key: MessageKey, params: Record<string, string | number> = {}): string {
  const s = MESSAGES[locale.value][key] || MESSAGES.en[key];
  return s.replace(/\{(\w+)\}/g, (m, k: string) => (k in params ? String(params[k]) : m));
}

export function chartTitle(name: string, english: string): string {
  return TITLES[locale.value][name] ?? english;
}

export function groupName(english: string): string {
  return GROUPS[locale.value][english] ?? english;
}

/** "<page> · The Allowed Universe" in the current language. */
export function pageTitle(page?: string): string {
  return page ? `${page} · ${t("siteName")}` : t("siteName");
}
