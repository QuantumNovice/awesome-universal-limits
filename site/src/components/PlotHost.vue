<script setup lang="ts">
// Renders an Observable Plot figure into a div and re-renders when the width or inputs change.
import { onBeforeUnmount, onMounted, ref, watch } from "vue";

const props = defineProps<{ build: (width: number) => Element; deps?: unknown[] }>();
const el = ref<HTMLDivElement | null>(null);
const width = ref(0);
let ro: ResizeObserver | null = null;

function render() {
  if (!el.value || width.value === 0) return;
  const node = props.build(width.value);
  el.value.replaceChildren(node);
}

onMounted(() => {
  ro = new ResizeObserver((entries) => {
    const w = Math.floor(entries[0].contentRect.width);
    if (Math.abs(w - width.value) > 4) {
      width.value = w;
      render();
    }
  });
  if (el.value) {
    ro.observe(el.value);
    // render once right away; the observer handles later resizes
    width.value = Math.floor(el.value.clientWidth);
    render();
  }
});
onBeforeUnmount(() => ro?.disconnect());
watch(
  () => [props.build, ...(props.deps ?? [])],
  () => render(),
);
</script>

<template>
  <div ref="el" class="plot-host"></div>
</template>

<style scoped>
.plot-host {
  width: 100%;
  min-height: 120px;
}
</style>
