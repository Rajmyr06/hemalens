import { copyFile, mkdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";

const files = [
  ["node_modules/htmx.org/dist/htmx.min.js", "app/static/vendor/htmx.min.js"],
  ["node_modules/alpinejs/dist/cdn.min.js", "app/static/vendor/alpine.min.js"],
];

for (const [source, destination] of files) {
  const outputPath = resolve(destination);
  await mkdir(dirname(outputPath), { recursive: true });
  await copyFile(resolve(source), outputPath);
}

console.log("Frontend vendor assets copied.");
