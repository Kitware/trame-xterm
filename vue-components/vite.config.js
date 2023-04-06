import { defineConfig } from "vite";

export default defineConfig({
  base: "./",
  build: {
    lib: {
      entry: "./src/main.js",
      name: "trame_xterm",
      format: "umd",
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
    outDir: "../trame_xterm/module/serve",
    assetsDir: ".",
  },
});
