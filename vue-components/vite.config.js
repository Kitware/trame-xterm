import { defineConfig } from "vite";

export default defineConfig({
  base: "./",
  build: {
    lib: {
      entry: "./src/main.js",
      name: "trame_xterm",
      formats: ["umd"],
      fileName: "trame-xterm",
    },
    rollupOptions: {
      external: ["vue"],
      output: {
        globals: {
          vue: "Vue",
        },
      },
    },
    outDir: "../src/trame_xterm/module/serve",
    assetsDir: ".",
  },
});
