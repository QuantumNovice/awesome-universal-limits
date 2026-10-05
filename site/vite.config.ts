import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// Relative base so the built site works from any path (GitHub Pages project site, a sub-folder, file preview).
export default defineConfig({
  base: "./",
  plugins: [vue()],
  build: { outDir: "dist", chunkSizeWarningLimit: 1500 },
});
