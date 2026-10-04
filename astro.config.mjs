// astro.config.mjs — Orion's Guard
import sitemap from "@astrojs/sitemap";
import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://orionsguard.net",
  // output defaults to "static" — Astro pre-renders all pages to plain HTML
  // The dist/ folder is deployed to Cloudflare Pages (free, no Workers needed)
  integrations: [sitemap()],
});

