#!/usr/bin/env python3
# ================================================================
#  Orion's Guard — deploy_orionsguard.py
#  Run this from the ROOT of your cloned GitHub repo:
#    cd C:\path\to\orionsguardsite
#    python deploy_orionsguard.py
#
#  What it does:
#    1. Removes Cloudflare Workers files (wrangler.json etc.)
#    2. Writes all Astro site files (pages, CSS, blog posts, etc.)
#    3. Runs: git add -A && git commit && git push  → triggers Cloudflare rebuild
# ================================================================
import os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

def w(rel, content):
    parts = rel.split("/")
    path  = os.path.join(ROOT, *parts)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("  wrote:", rel)

def rm(rel):
    path = os.path.join(ROOT, *rel.split("/"))
    if os.path.exists(path):
        os.remove(path)
        print("  removed:", rel)

print("=" * 60)
print("  Orion's Guard — Deploy Script")
print("=" * 60)
print()
print("  Step 1: Removing Cloudflare Workers files …")
rm("wrangler.json")
rm("worker-configuration.d.ts")
print()
print("  Step 2: Writing site files …")

print()
w('.gitignore', '''\
# build output
dist/
.astro/

# dependencies
node_modules/

# env files
.env
.env.*
!.env.example

# macOS
.DS_Store

# Editors
.vscode/
.idea/
*.swp

''')

w('astro.config.mjs', '''\
// astro.config.mjs — Orion's Guard
import sitemap from "@astrojs/sitemap";
import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://orionsguard.net",
  // output defaults to "static" — Astro pre-renders all pages to plain HTML
  // The dist/ folder is deployed to Cloudflare Pages (free, no Workers needed)
  integrations: [sitemap()],
});

''')

w('package.json', '''\
{
  "name": "orionsguard",
  "type": "module",
  "version": "1.0.0",
  "scripts": {
    "dev":     "astro dev",
    "build":   "astro build",
    "preview": "astro preview"
  },
  "dependencies": {
    "astro":            "^4.16.18",
    "@astrojs/sitemap": "^3.2.1"
  }
}

''')

w('public/styles/global.css', '''\
/* ================================================================
   Orion's Guard — Global CSS
   Enterprise-clean dark theme for Astro / EmDash site
   ================================================================ */

/* ── CSS Variables ─────────────────────────────────────────── */
:root {
  /* Blues */
  --c-blue:        #2563eb;
  --c-blue-mid:    #3b82f6;
  --c-blue-light:  #60a5fa;
  /* Cyan */
  --c-cyan:        #06b6d4;
  --c-cyan-light:  #67e8f9;
  /* Backgrounds */
  --c-bg:          #05090f;
  --c-bg-2:        #09101c;
  --c-bg-3:        #0f1929;
  --c-bg-card:     #0d1520;
  /* Text */
  --c-text:        #f0f4f8;
  --c-text-soft:   #94a3b8;
  --c-text-dim:    #4b6280;
  /* Border */
  --c-border:      rgba(59,130,246,.12);
  --c-border-mid:  rgba(59,130,246,.22);
  /* Layout */
  --nav-h:         64px;
  --max-w:         1160px;
  /* Radii */
  --radius:        8px;
  --radius-lg:     12px;
  /* Transitions */
  --t:             .2s ease;
}

/* ── Reset & Base ──────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html {
  scroll-behavior: smooth;
  -webkit-text-size-adjust: 100%;
}

body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background-color: var(--c-bg);
  color: var(--c-text);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  min-height: 100vh;
}

img, video { max-width: 100%; height: auto; display: block; }
a { color: var(--c-blue-light); text-decoration: none; transition: color var(--t); }
a:hover { color: #93c5fd; }
ul[role="list"] { list-style: none; }

/* ── Reading Progress Bar ──────────────────────────────────── */
#og-progress {
  position: fixed;
  top: 0; left: 0;
  width: 0%;
  height: 3px;
  background: linear-gradient(90deg, var(--c-blue), var(--c-cyan));
  z-index: 9999;
  transition: width .1s linear;
  pointer-events: none;
}

/* ── Navigation ────────────────────────────────────────────── */
.og-nav {
  position: sticky;
  top: 0;
  z-index: 1000;
  height: var(--nav-h);
  background: rgba(5, 9, 15, .82);
  backdrop-filter: blur(20px) saturate(1.6);
  -webkit-backdrop-filter: blur(20px) saturate(1.6);
  border-bottom: 1px solid var(--c-border);
  transition: border-color var(--t), box-shadow var(--t);
}
.og-nav.scrolled {
  border-bottom-color: var(--c-border-mid);
  box-shadow: 0 4px 32px rgba(0,0,0,.4);
}

.og-nav-inner {
  display: flex;
  align-items: center;
  gap: 2rem;
  max-width: var(--max-w);
  margin: 0 auto;
  padding: 0 1.5rem;
  height: 100%;
}

/* Logo */
.og-logo {
  display: flex;
  align-items: center;
  gap: .6rem;
  text-decoration: none;
  flex-shrink: 0;
}
.og-logo img {
  width: 36px; height: 36px;
  object-fit: contain;
  filter: drop-shadow(0 0 8px rgba(37,99,235,.4));
}
.og-logo-name {
  font-size: .95rem;
  font-weight: 800;
  letter-spacing: .02em;
  color: var(--c-text);
  white-space: nowrap;
}
.og-logo-accent { color: var(--c-blue-mid); }

/* Nav links */
.og-nav-links {
  display: flex;
  align-items: center;
  gap: .25rem;
  list-style: none;
  margin-left: 1rem;
}
.og-nav-link {
  font-size: .85rem;
  font-weight: 500;
  color: var(--c-text-soft);
  padding: .4rem .75rem;
  border-radius: var(--radius);
  transition: color var(--t), background var(--t);
  text-decoration: none;
}
.og-nav-link:hover { color: var(--c-text); background: rgba(255,255,255,.05); }
.og-nav-link.active { color: var(--c-blue-light); }

/* Right side */
.og-nav-right {
  display: flex;
  align-items: center;
  gap: .75rem;
  margin-left: auto;
}
.og-nav-search {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px; height: 36px;
  border-radius: var(--radius);
  color: var(--c-text-soft);
  transition: color var(--t), background var(--t);
}
.og-nav-search:hover { color: var(--c-text); background: rgba(255,255,255,.06); }

.og-cta-pill {
  font-size: .8rem;
  font-weight: 700;
  letter-spacing: .04em;
  color: var(--c-blue-light);
  border: 1.5px solid rgba(96,165,250,.4);
  border-radius: 999px;
  padding: .4rem 1.1rem;
  transition: background var(--t), border-color var(--t), color var(--t);
  white-space: nowrap;
}
.og-cta-pill:hover {
  background: rgba(37,99,235,.15);
  border-color: var(--c-blue-mid);
  color: #93c5fd;
}

/* Burger */
.og-burger {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  width: 36px; height: 36px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: .45rem;
}
.og-burger span {
  display: block;
  height: 2px;
  width: 100%;
  background: var(--c-text-soft);
  border-radius: 2px;
  transition: transform var(--t), opacity var(--t), background var(--t);
}
.og-burger.open span:nth-child(1) { transform: translateY(7px) rotate(45deg); background: var(--c-text); }
.og-burger.open span:nth-child(2) { opacity: 0; }
.og-burger.open span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); background: var(--c-text); }

/* Mobile Drawer */
.og-drawer {
  background: var(--c-bg-2);
  border-top: 1px solid var(--c-border);
  padding: 1rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: .25rem;
  box-shadow: 0 16px 48px rgba(0,0,0,.5);
}
.og-drawer-link {
  font-size: .95rem;
  font-weight: 500;
  color: var(--c-text-soft);
  padding: .65rem .75rem;
  border-radius: var(--radius);
  transition: color var(--t), background var(--t);
}
.og-drawer-link:hover { color: var(--c-text); background: rgba(255,255,255,.05); }
.og-drawer-cta {
  margin-top: .75rem;
  text-align: center;
  padding: .75rem;
  background: var(--c-blue);
  color: #fff;
  font-weight: 700;
  border-radius: var(--radius);
  font-size: .9rem;
}

/* ── Buttons ────────────────────────────────────────────────── */
.og-btn {
  display: inline-flex;
  align-items: center;
  gap: .5rem;
  font-size: .9rem;
  font-weight: 700;
  padding: .75rem 1.6rem;
  border-radius: var(--radius);
  transition: background var(--t), color var(--t), transform var(--t), box-shadow var(--t);
  white-space: nowrap;
  cursor: pointer;
  text-decoration: none;
  border: none;
}
.og-btn:active { transform: translateY(1px); }
.og-btn-primary {
  background: var(--c-blue);
  color: #fff;
  box-shadow: 0 0 0 0 rgba(37,99,235,0);
}
.og-btn-primary:hover {
  background: #1d4ed8;
  color: #fff;
  box-shadow: 0 4px 24px rgba(37,99,235,.35);
  transform: translateY(-1px);
}
.og-btn-outline {
  background: transparent;
  color: var(--c-blue-light);
  border: 1.5px solid rgba(96,165,250,.45);
}
.og-btn-outline:hover {
  background: rgba(37,99,235,.1);
  border-color: var(--c-blue-mid);
  color: #93c5fd;
  transform: translateY(-1px);
}

/* ── Hero ───────────────────────────────────────────────────── */
.og-hero {
  position: relative;
  overflow: hidden;
  min-height: 88vh;
  display: flex;
  align-items: center;
  padding: 6rem 1.5rem 5rem;
}

/* Subtle grid overlay */
.og-hero-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(59,130,246,.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(59,130,246,.04) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
}

/* Radial glow */
.og-hero-glow {
  position: absolute;
  top: 0; left: 50%;
  transform: translateX(-50%);
  width: 900px; height: 500px;
  background: radial-gradient(ellipse at 50% 0%,
    rgba(37,99,235,.18) 0%,
    rgba(6,182,212,.06) 50%,
    transparent 70%);
  pointer-events: none;
}

.og-hero-body {
  position: relative;
  max-width: var(--max-w);
  margin: 0 auto;
  width: 100%;
  z-index: 1;
}

/* Eyebrow */
.og-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: .6rem;
  font-size: .75rem;
  font-weight: 700;
  letter-spacing: .1em;
  text-transform: uppercase;
  color: var(--c-cyan);
  margin-bottom: 1.25rem;
}
.og-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--c-cyan);
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(6,182,212,.6); }
  50%       { box-shadow: 0 0 0 6px rgba(6,182,212,0); }
}

/* H1 */
.og-hero-h1 {
  font-size: clamp(2.4rem, 7vw, 4rem);
  font-weight: 900;
  line-height: 1.08;
  letter-spacing: -.04em;
  color: var(--c-text);
  margin-bottom: 1.5rem;
  max-width: 700px;
}
.og-hero-h1 em {
  font-style: italic;
  background: linear-gradient(135deg, var(--c-blue-light), var(--c-cyan));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Lead paragraph */
.og-hero-lead {
  font-size: clamp(.95rem, 2vw, 1.1rem);
  color: var(--c-text-soft);
  line-height: 1.75;
  max-width: 560px;
  margin-bottom: 2.25rem;
}

/* CTA buttons row */
.og-hero-btns {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 2.5rem;
}

/* Compliance chips */
.og-chips {
  display: flex;
  flex-wrap: wrap;
  gap: .5rem;
}
.og-chip {
  font-size: .72rem;
  font-weight: 700;
  letter-spacing: .06em;
  text-transform: uppercase;
  color: var(--c-text-dim);
  border: 1px solid var(--c-border);
  border-radius: 999px;
  padding: .3rem .85rem;
  background: rgba(255,255,255,.02);
  transition: border-color var(--t), color var(--t);
}
.og-chip:hover {
  border-color: var(--c-blue-mid);
  color: var(--c-blue-light);
}

/* ── Stats Strip ────────────────────────────────────────────── */
.og-stats {
  background: var(--c-bg-2);
  border-top: 1px solid var(--c-border);
  border-bottom: 1px solid var(--c-border);
  padding: 2.5rem 1.5rem;
}
.og-stats-inner {
  max-width: var(--max-w);
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  flex-wrap: wrap;
}
.og-stat {
  flex: 1;
  min-width: 200px;
  text-align: center;
  padding: 1rem 2rem;
}
.og-stat-num {
  display: block;
  font-size: clamp(1.8rem, 5vw, 2.5rem);
  font-weight: 900;
  letter-spacing: -.04em;
  background: linear-gradient(135deg, var(--c-blue-light), var(--c-cyan));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: .4rem;
}
.og-stat-label {
  font-size: .82rem;
  color: var(--c-text-soft);
  line-height: 1.4;
}
.og-stat-div {
  width: 1px;
  height: 48px;
  background: var(--c-border);
  flex-shrink: 0;
}

/* ── Interior Page Hero Band ─────────────────────────────────  */
.og-page-hero {
  background: linear-gradient(180deg, var(--c-bg-2) 0%, var(--c-bg) 100%);
  border-bottom: 1px solid var(--c-border);
  padding: 4rem 1.5rem 3rem;
}
.og-page-hero-inner {
  max-width: var(--max-w);
  margin: 0 auto;
}
.og-breadcrumb {
  display: flex;
  align-items: center;
  gap: .5rem;
  font-size: .78rem;
  color: var(--c-text-dim);
  margin-bottom: 1.25rem;
}
.og-breadcrumb a {
  color: var(--c-text-dim);
  text-decoration: none;
  transition: color var(--t);
}
.og-breadcrumb a:hover { color: var(--c-blue-light); }
.og-breadcrumb span { color: var(--c-text-dim); }

.og-page-title {
  font-size: clamp(1.8rem, 5vw, 2.75rem);
  font-weight: 900;
  letter-spacing: -.04em;
  color: var(--c-text);
  line-height: 1.1;
  margin-bottom: .75rem;
}
.og-page-desc {
  font-size: clamp(.9rem, 2vw, 1.05rem);
  color: var(--c-text-soft);
  max-width: 600px;
  line-height: 1.7;
}

/* ── Page Body Container ─────────────────────────────────────── */
.og-page-body {
  max-width: var(--max-w);
  margin: 0 auto;
  padding: 3.5rem 1.5rem 5rem;
}

/* ── Prose (blog posts) ─────────────────────────────────────── */
.og-prose {
  color: var(--c-text-soft);
  font-size: 1rem;
  line-height: 1.85;
  max-width: 720px;
}
.og-prose h1,
.og-prose h2,
.og-prose h3,
.og-prose h4 {
  color: var(--c-text);
  font-weight: 800;
  letter-spacing: -.03em;
  line-height: 1.25;
  margin-top: 2.5rem;
  margin-bottom: .85rem;
}
.og-prose h1 { font-size: 1.9rem; }
.og-prose h2 { font-size: 1.45rem; padding-bottom: .5rem; border-bottom: 1px solid var(--c-border); }
.og-prose h3 { font-size: 1.15rem; }
.og-prose p { margin-bottom: 1.35rem; }
.og-prose ul, .og-prose ol {
  margin: 1rem 0 1.35rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: .4rem;
}
.og-prose li { color: var(--c-text-soft); }
.og-prose a { color: var(--c-blue-light); border-bottom: 1px solid rgba(96,165,250,.25); }
.og-prose a:hover { color: #93c5fd; border-bottom-color: var(--c-blue-mid); }
.og-prose strong { color: var(--c-text); font-weight: 700; }
.og-prose em { color: var(--c-cyan-light); font-style: italic; }
.og-prose code {
  font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
  font-size: .85em;
  background: rgba(37,99,235,.08);
  border: 1px solid var(--c-border);
  border-radius: 4px;
  padding: .15em .45em;
  color: var(--c-blue-light);
}
.og-prose pre {
  background: var(--c-bg-card);
  border: 1px solid var(--c-border);
  border-radius: var(--radius);
  padding: 1.5rem;
  overflow-x: auto;
  margin: 1.5rem 0;
  font-size: .85rem;
  line-height: 1.6;
}
.og-prose pre code {
  background: transparent;
  border: none;
  padding: 0;
  color: var(--c-text-soft);
}
.og-prose blockquote {
  border-left: 3px solid var(--c-blue-mid);
  padding: 1rem 1.5rem;
  background: rgba(37,99,235,.04);
  border-radius: 0 var(--radius) var(--radius) 0;
  margin: 1.5rem 0;
  color: var(--c-text-soft);
  font-style: italic;
}
.og-prose hr {
  border: none;
  border-top: 1px solid var(--c-border);
  margin: 2.5rem 0;
}
.og-prose table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
  font-size: .875rem;
}
.og-prose th {
  background: var(--c-bg-card);
  border: 1px solid var(--c-border);
  padding: .65rem 1rem;
  text-align: left;
  font-weight: 700;
  color: var(--c-text);
  font-size: .75rem;
  letter-spacing: .05em;
  text-transform: uppercase;
}
.og-prose td {
  border: 1px solid var(--c-border);
  padding: .65rem 1rem;
  color: var(--c-text-soft);
}
.og-prose tr:hover td { background: rgba(255,255,255,.02); }

/* ── Footer ─────────────────────────────────────────────────── */
.og-footer {
  background: var(--c-bg-2);
  border-top: 1px solid var(--c-border);
}
.og-footer-inner {
  max-width: var(--max-w);
  margin: 0 auto;
  padding: 4rem 1.5rem 3rem;
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 4rem;
  align-items: start;
}
.og-footer-logo {
  display: flex;
  align-items: center;
  gap: .6rem;
  margin-bottom: 1rem;
}
.og-footer-logo img {
  height: 34px; width: auto;
  object-fit: contain;
  filter: drop-shadow(0 0 6px rgba(37,99,235,.3));
}
.og-footer-logo-name {
  font-size: .95rem;
  font-weight: 800;
  color: var(--c-text);
}
.og-footer-tagline {
  font-size: .85rem;
  color: var(--c-text-dim);
  line-height: 1.6;
}

.og-footer-nav {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}
.og-footer-col-title {
  display: block;
  font-size: .72rem;
  font-weight: 700;
  letter-spacing: .1em;
  text-transform: uppercase;
  color: var(--c-text-dim);
  margin-bottom: 1rem;
}
.og-footer-col ul {
  display: flex;
  flex-direction: column;
  gap: .5rem;
}
.og-footer-col a {
  font-size: .85rem;
  color: var(--c-text-dim);
  text-decoration: none;
  transition: color var(--t);
}
.og-footer-col a:hover { color: var(--c-blue-light); }

.og-footer-bottom {
  max-width: var(--max-w);
  margin: 0 auto;
  padding: 1.25rem 1.5rem;
  border-top: 1px solid var(--c-border);
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: .78rem;
  color: var(--c-text-dim);
}

/* ── Responsive ─────────────────────────────────────────────── */
@media (max-width: 1024px) {
  .og-footer-inner { grid-template-columns: 1fr; gap: 2rem; }
  .og-footer-nav { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 768px) {
  .og-nav-links { display: none; }
  .og-burger { display: flex; }
  .og-cta-pill { display: none; }

  .og-hero { min-height: 75vh; padding: 4rem 1.25rem 3.5rem; }

  .og-stats-inner { flex-direction: column; gap: 1rem; }
  .og-stat-div { display: none; }
  .og-stat { padding: .75rem 1rem; min-width: unset; }

  .og-footer-nav { grid-template-columns: 1fr 1fr; }
  .og-footer-bottom { flex-direction: column; align-items: flex-start; }
}

@media (max-width: 480px) {
  .og-footer-nav { grid-template-columns: 1fr; }
  .og-hero-btns { flex-direction: column; }
  .og-hero-btns .og-btn { width: 100%; justify-content: center; }
}

/* ── Print styles ───────────────────────────────────────────── */
@media print {
  .og-nav, .og-footer, #og-progress, .og-hero { display: none !important; }
  body { background: #fff; color: #000; }
  .og-prose a { color: inherit; border: none; }
}

''')

w('src/content/blog/cisco-zero-day-cve-2023-20198.md', '''\
---
title: "Cisco Zero-Day Nightmare: CVE-2023-20198 and What It Means for Your Network"
description: "A maximum-severity Cisco IOS XE vulnerability affected tens of thousands of devices worldwide. Here's what happened, the timeline, and how to harden your network perimeter."
date: 2025-09-27
author: "Orion's Guard"
tags: ["Vulnerabilities", "Networking", "CVE"]
draft: false
---

CVE-2023-20198 was assigned a CVSS score of 10.0 — the maximum possible. It affected Cisco IOS XE's web UI feature and allowed an unauthenticated remote attacker to create an account with full administrator-level access. No credentials required. No prior foothold needed.

Within days of public disclosure, researchers identified tens of thousands of compromised devices on the public internet. Most victims were unaware.

## What Happened

Cisco's IOS XE operating system powers a substantial portion of enterprise and service provider networking infrastructure — routers, switches, wireless controllers, and more. The software includes a web-based user interface (Web UI) that administrators can enable for remote management.

CVE-2023-20198 targeted this Web UI. When enabled and exposed to the network, the vulnerability allowed an attacker to:

1. Create a new local user account with privilege level 15 (full administrative access)
2. Use that account to install a malicious implant (a Lua-based backdoor) via a second vulnerability (CVE-2023-20273)
3. Maintain persistent access to the device — even after reboots — until the implant was discovered and removed

Cisco's threat intelligence team first detected active exploitation on October 16, 2023. The activity had likely been ongoing since at least September 18, 2023 — nearly a month of silent exploitation before discovery.

## The Scale of Impact

Security researchers scanning internet-facing Cisco devices found:

- Over 50,000 devices showing indicators of compromise at peak
- Affected organizations included ISPs, managed service providers, enterprises, and government entities
- The implant was designed to survive reboots, making remediation more complex

The attacker methodology suggested a targeted, coordinated campaign — not opportunistic script-kiddie exploitation. The attackers appeared to be selectively deploying the implant rather than mass-compromising every vulnerable device.

## The Remediation Challenge

Cisco's initial advisory recommended disabling the HTTP Server feature (`no ip http server` / `no ip http secure-server`). A patch was released within days of public disclosure.

However, remediation was complicated by several factors:

- **Implant detection was difficult** — the backdoor was designed to evade standard inspection tools
- **The implant modified system files** — some devices required reimaging rather than just patching
- **Many affected devices were unmonitored** — perimeter devices often lack the logging infrastructure of servers

The correct remediation sequence was:
1. Disable the Web UI immediately
2. Check for indicators of compromise (specific HTTP requests in logs, presence of implant file)
3. Apply Cisco's patch
4. For compromised devices: assume full compromise, rotate all credentials, consider reimaging

## Lessons for Small and Mid-Size Businesses

If you're running Cisco networking equipment — or any managed network device — this incident highlights several risk areas:

**1. Management interfaces should never be internet-facing**
Device management UIs should be accessible only from a dedicated management network, VPN, or out-of-band access path. If you can access your router's admin interface from the public internet, so can attackers.

**2. Asset inventory and patch management for network devices**
Most organizations have solid patch management for servers and workstations. Network device firmware and software is often overlooked. Cisco devices, Fortinet appliances, Juniper routers, and similar equipment need the same patching discipline as any other system.

**3. Log monitoring extends to your perimeter**
Network devices generate logs. Those logs — particularly authentication events, configuration changes, and web UI access — should flow to a central logging system (SIEM or log aggregator) where anomalies can be detected.

**4. Default-off features should stay off**
The Cisco Web UI is disabled by default. The affected organizations had explicitly enabled it. Before enabling any management feature on a network device, understand what attack surface it creates.

**5. Have a playbook for vendor zero-days**
When a critical CVE drops for equipment in your environment, what's your response process? Who gets paged? What's the isolation procedure? Having this documented before the incident dramatically reduces response time.

---

*Orion's Guard can help you build a network security program that includes proper segmentation, monitoring, and patch management for all device types. [Book a free discovery call →](/contact/)*

''')

w('src/content/blog/gdpr-guide-smb.md', '''\
---
title: "GDPR Compliance Guide for Small and Mid-Size Businesses"
description: "GDPR applies to any business that handles EU personal data — regardless of where the business is located. Here's a practical compliance roadmap for SMBs."
date: 2025-09-15
author: "Orion's Guard"
tags: ["GDPR", "Compliance", "Privacy"]
draft: false
---

The General Data Protection Regulation (GDPR) came into force in May 2018 and remains one of the most significant data protection laws in the world. Despite being an EU regulation, it applies to any organization — anywhere in the world — that processes the personal data of people in the European Union.

If your business has EU customers, EU website visitors, or EU employees, GDPR applies to you.

This guide is designed for small and mid-size businesses that need a practical compliance roadmap — not a 200-page legal treatise.

## The Core Principles (What GDPR Actually Requires)

GDPR is built around six data protection principles. Everything flows from these:

1. **Lawfulness, fairness, transparency** — you must have a legal basis for processing personal data, and you must be transparent about how you use it
2. **Purpose limitation** — data collected for one purpose cannot be used for a different purpose
3. **Data minimization** — collect only what you actually need
4. **Accuracy** — keep personal data accurate and up to date
5. **Storage limitation** — don't keep data longer than necessary
6. **Integrity and confidentiality** — protect data against unauthorized access, loss, or destruction

There's also a seventh principle sometimes called "accountability" — you must be able to demonstrate that you're complying with all of the above.

## What Counts as Personal Data

Under GDPR, personal data is any information that relates to an identified or identifiable natural person. This is broad:

- Name, email address, phone number
- IP addresses and cookies
- Location data
- Financial information
- Health and medical data
- Behavioral data (browsing history, purchase history)
- Biometric data (fingerprints, facial recognition)

If your website uses Google Analytics, you're processing personal data (IP addresses). If you send marketing emails, you're processing personal data.

## Legal Bases for Processing

You need a legal basis before processing any personal data. The six available bases are:

1. **Consent** — the individual has given clear, affirmative consent
2. **Contract** — processing is necessary to fulfill a contract with the person
3. **Legal obligation** — you're required to process the data by law
4. **Vital interests** — processing is necessary to protect someone's life
5. **Public task** — relevant primarily to public authorities
6. **Legitimate interests** — your interests are balanced against the individual's rights

For most SMBs, the relevant bases are consent, contract, and legitimate interests. **Consent under GDPR must be freely given, specific, informed, and unambiguous** — pre-ticked boxes and bundled consent don't qualify.

## The Compliance Checklist

### Data Inventory (Start Here)
- [ ] Map all personal data you collect, where it comes from, where it goes
- [ ] Document the legal basis for each processing activity
- [ ] Identify all third parties that receive personal data (vendors, processors, analytics)

### Privacy Policy and Notices
- [ ] Update your privacy policy to cover all required disclosures
- [ ] Add cookie consent mechanism to your website (must be opt-in for non-essential cookies)
- [ ] Provide clear information at the point of data collection

### Individual Rights
- [ ] Create a process for handling Subject Access Requests (SARs) — you have 30 days to respond
- [ ] Establish procedures for the right to erasure ("right to be forgotten")
- [ ] Document how you handle data portability requests

### Data Security
- [ ] Implement appropriate technical security measures
- [ ] Use encryption for personal data in transit and at rest
- [ ] Control access on a need-to-know basis
- [ ] Maintain records of processing activities (Article 30)

### Vendor Management
- [ ] Ensure all data processors (vendors who handle your data) have signed Data Processing Agreements (DPAs)
- [ ] Review vendor privacy practices before sharing personal data
- [ ] Assess data transfers outside the EU/UK (requires appropriate safeguards)

### Breach Response
- [ ] Establish a breach notification procedure
- [ ] Personal data breaches must be reported to your supervisory authority within 72 hours
- [ ] If the breach is "high risk," affected individuals must also be notified

## Common Mistakes SMBs Make

**1. Treating consent as the default legal basis for everything**
Consent is often not the appropriate basis. Contract and legitimate interests are frequently better fits and don't require managing consent withdrawal.

**2. Inadequate cookie consent**
Using a cookie banner that doesn't actually block tracking cookies until consent is given. Under GDPR, cookies that aren't strictly necessary cannot fire until the user consents.

**3. Missing Data Processing Agreements**
If you share personal data with any vendor (CRM, email marketing, cloud hosting, analytics), you need a DPA. Most major vendors provide these — but you need to execute them.

**4. No SAR process**
Subject Access Requests are increasingly common. Without a process, you'll miss the 30-day deadline.

**5. Ignoring international data transfers**
Using US-based services (most SaaS tools) constitutes a data transfer to a third country. This requires appropriate safeguards — the EU-US Data Privacy Framework, Standard Contractual Clauses, or binding corporate rules.

## Where to Start

1. Complete a data inventory — know what you have
2. Update your privacy policy
3. Fix your cookie consent mechanism
4. Execute DPAs with your key vendors
5. Document your processing activities (a simple spreadsheet works)
6. Create a SAR response procedure

GDPR compliance isn't a one-time project — it's an ongoing program. But the foundation above is achievable for most SMBs in weeks, not months.

---

*Orion's Guard provides GDPR compliance consulting for small and mid-size businesses — from initial assessment to full program implementation. [Book a free discovery call →](/contact/)*

''')

w('src/content/blog/google-privacy-illusion.md', '''\
---
title: "The Control Illusion: What Google's Privacy Settings Actually Do"
description: "Google offers dozens of privacy controls. Most users assume they limit data collection. Here's what the research and policy documents actually say."
date: 2025-10-04
author: "Orion's Guard"
tags: ["Privacy", "Google", "Data Collection"]
draft: false
---

Google has invested substantially in its privacy settings interface. My Account, Privacy Checkup, Ad Settings, Location History, Web & App Activity — the controls are numerous, well-designed, and prominently marketed. The reasonable inference is that adjusting these settings limits how Google collects and uses your data.

The reality is more complicated.

## What the Settings Actually Control

Google's privacy controls are real in the sense that they affect what appears in your account's activity log and what influences the ads you see. They are less real in the sense that they don't stop data collection — they change how that data is associated with your account and used for personalization.

**Location History**: Disabling Location History stops Google from adding your location data to the "Timeline" feature in Google Maps. It does not stop Google from recording your location through other means — including Web & App Activity, which logs location data from searches, Maps usage, and other Google services even when Location History is off. This was the subject of a 2018 Associated Press investigation and subsequent FTC investigations.

**Ad Personalization**: Turning off ad personalization means Google won't use your data to target you with interest-based ads. It does not mean Google stops collecting that data. The data continues to be collected and retained — it's just not used for that specific purpose.

**Web & App Activity**: Pausing this setting stops new activity from being saved to your account. It doesn't delete existing activity, and it doesn't prevent Google from collecting that data temporarily for operational purposes.

## The Aggregation Problem

Individual data points are often innocuous. Your search for "coffee shops near me" is not sensitive. Your location data on a Tuesday morning is not sensitive. The combination of your search history, location history, YouTube viewing, email content analysis, and device identifiers over years is a different matter.

Google's business model is built on the aggregation of these signals. The privacy settings control surfaces — what you see and what's attributed to your account for personalization — but the underlying data infrastructure continues operating.

## What Actually Reduces Your Exposure

If minimizing Google's data collection is a priority:

1. **Use a non-Google search engine** — DuckDuckGo, Brave Search, or Kagi for searches
2. **Use a non-Chromium browser** — Firefox with uBlock Origin is a well-supported option
3. **Avoid signing into Google accounts** when browsing is the most effective single change
4. **Use DNS-level blocking** (Pi-hole, NextDNS, or a similar tool) to block Google Analytics and advertising endpoints network-wide
5. **Use a VPN** to prevent your ISP and Google's network infrastructure from correlating your IP across sessions

## For Businesses: The Compliance Angle

If your organization uses Google Workspace, Google Analytics, or any Google advertising products, there are compliance implications:

- **GDPR**: Using Google Analytics without proper consent mechanisms and data processing agreements has been ruled illegal in multiple EU countries (Austria, France, Italy, Netherlands)
- **HIPAA**: Google Workspace can be configured for HIPAA compliance — but this requires a Business Associate Agreement and specific configuration choices that aren't defaults
- **Employee Privacy**: Using Google Workspace means employee data — emails, documents, calendar events — passes through Google's infrastructure. This should be addressed in your employee privacy policy

The lesson isn't that Google is uniquely bad — it's that privacy controls and data minimization are two different things, and organizations should understand which one they're actually achieving.

---

*Orion's Guard helps businesses assess third-party data sharing risks and build compliant data handling programs. [Book a free discovery call →](/contact/)*

''')

w('src/content/blog/hipaa-basics-smb.md', '''\
---
title: "HIPAA Basics: What Every Small Business Needs to Know"
description: "HIPAA isn't just for hospitals. If your business handles health information in any context, here's what the law requires and how to get compliant."
date: 2025-09-10
author: "Orion's Guard"
tags: ["HIPAA", "Compliance", "Healthcare"]
draft: false
---

The Health Insurance Portability and Accountability Act (HIPAA) is frequently misunderstood as a regulation that applies only to hospitals and large healthcare systems. In practice, it applies to a much broader universe of organizations — including many small businesses that may not realize they're covered.

## Who Does HIPAA Actually Cover?

HIPAA applies to two categories of organizations:

**Covered Entities:**
- Healthcare providers (doctors, dentists, therapists, pharmacies, hospitals)
- Health plans (insurance companies, HMOs, employer-sponsored health plans)
- Healthcare clearinghouses (organizations that process health information between providers and payers)

**Business Associates:**
This is where many small businesses get caught. A Business Associate is any organization that creates, receives, maintains, or transmits Protected Health Information (PHI) on behalf of a Covered Entity. This includes:
- Medical billing companies
- IT service providers and MSPs that handle healthcare client data
- Cloud storage providers used by healthcare organizations
- Legal and accounting firms serving healthcare clients
- Marketing and PR firms working with healthcare organizations
- Transcription services, answering services, and call centers
- Software vendors whose products process PHI

If you provide services to a healthcare organization and your work involves access to patient health information — even incidentally — you are likely a Business Associate and HIPAA applies to you.

## What Is Protected Health Information (PHI)?

PHI is any individually identifiable health information that is:
1. Created or received by a Covered Entity or Business Associate
2. Related to an individual's past, present, or future health condition, treatment, or payment

PHI includes a long list of identifiers — not just the health condition itself, but name, address, date of birth, Social Security number, phone number, email address, and even IP addresses when linked to health information.

**Electronic PHI (ePHI)** is PHI stored, transmitted, or processed electronically — which means most PHI in modern healthcare environments.

## The Three HIPAA Rules

### Privacy Rule
Governs the use and disclosure of PHI. Key requirements:
- Use only the minimum necessary PHI for any given purpose
- Provide patients with a Notice of Privacy Practices
- Give patients the right to access and amend their records
- Obtain patient authorization for non-routine disclosures

### Security Rule
Governs the protection of ePHI. Requires:
- Administrative safeguards (policies, procedures, training, access management)
- Physical safeguards (facility controls, workstation security, device controls)
- Technical safeguards (access controls, audit controls, encryption, transmission security)

The Security Rule is risk-based — it doesn't prescribe specific technologies but requires you to implement "reasonable and appropriate" safeguards based on a risk assessment.

### Breach Notification Rule
Requires notification when ePHI is breached:
- Affected individuals: within 60 days of discovery
- HHS (Department of Health and Human Services): same 60-day window; breaches affecting 500+ individuals must be reported immediately
- Media: for breaches affecting 500+ individuals in a state or jurisdiction

## The HIPAA Security Rule Checklist for Small Businesses

**Administrative Safeguards:**
- [ ] Complete a formal risk analysis
- [ ] Implement a risk management plan based on the analysis
- [ ] Designate a Privacy Officer and Security Officer (can be the same person)
- [ ] Conduct HIPAA training for all workforce members
- [ ] Implement access management procedures (who gets access to what PHI, how it's granted/revoked)
- [ ] Execute Business Associate Agreements (BAAs) with all vendors who handle PHI

**Physical Safeguards:**
- [ ] Control physical access to facilities where ePHI is processed
- [ ] Implement workstation security policies
- [ ] Establish procedures for mobile device and media management (including disposal)

**Technical Safeguards:**
- [ ] Implement unique user IDs for all system access
- [ ] Implement automatic logoff for systems handling ePHI
- [ ] Enable encryption for ePHI at rest and in transit
- [ ] Maintain audit logs of all access to ePHI
- [ ] Implement integrity controls to detect unauthorized modification

## Business Associate Agreements (BAAs)

If you're a Business Associate, you must have a signed BAA with each Covered Entity client before you can handle their PHI. If you're a Covered Entity, you must have BAAs with all your Business Associates.

A BAA must include:
- Permitted uses and disclosures of PHI
- Requirements to use appropriate safeguards
- Obligation to report breaches
- Requirements to flow down obligations to subcontractors
- Procedures for PHI return or destruction upon contract termination

Most major cloud services that can be configured for HIPAA compliance (Microsoft 365, Google Workspace, AWS, Azure) will provide BAAs on request. Make sure you have them before using these services with PHI.

## Penalties

HIPAA penalties are tiered based on the level of culpability:

| Tier | Violation | Minimum | Maximum |
|------|-----------|---------|---------|
| 1 | Unknowing | $100/violation | $50,000/violation |
| 2 | Reasonable cause | $1,000/violation | $50,000/violation |
| 3 | Willful neglect, corrected | $10,000/violation | $50,000/violation |
| 4 | Willful neglect, not corrected | $50,000/violation | $1.9M/year |

Penalties are assessed per violation category per year. Organizations that have suffered a breach due to inadequate security controls face significant financial exposure.

---

*Orion's Guard provides HIPAA compliance consulting for small businesses, MSPs, and healthcare adjacent organizations. We make compliance achievable without breaking your budget. [Book a free discovery call →](/contact/)*

''')

w('src/content/blog/linux-privacy-id.md', '''\
---
title: "They Want Your ID — Is Linux Still the Last Bastion of Privacy?"
description: "Platforms now demand government-issued IDs. Age verification laws are spreading. What does this mean for privacy advocates — and does Linux still offer an escape?"
date: 2026-06-20
author: "Orion's Guard"
tags: ["Privacy", "Linux", "Identity"]
draft: false
---

Something has quietly shifted across the internet over the last few years. Platforms that once required only an email address now want a government-issued ID. Age verification laws are being passed in multiple US states and across the EU. Social media companies, under pressure from regulators, are building identity pipelines that link your real-world self to your online behavior.

For most users, this feels like a minor inconvenience. For security professionals, privacy advocates, and anyone who has thought carefully about data minimization, it's a significant structural change.

## The Creeping Demand for Your Identity

The shift started slowly. Gaming platforms began requiring phone number verification. Social networks added "government ID verification" for disputed accounts. Financial apps — already mandated by KYC regulations — extended biometric checks to lower-value transactions.

Now the logic is spreading beyond regulated industries. Age verification for adult content sites has become law in multiple jurisdictions. Some states are passing legislation requiring social media platforms to verify the ages of minors — which, in practice, means verifying the identity of *everyone*.

The data minimization principle, enshrined in GDPR Article 5, holds that organizations should collect only the personal data necessary for a specific, legitimate purpose. Blanket identity verification for access to general internet services runs directly counter to this principle.

## What This Means in Practice

When you upload a government ID to a platform, you're doing several things simultaneously:

- **Creating a permanent link** between your legal identity and your platform behavior
- **Trusting a private company** with a document that unlocks bank accounts, border crossings, and government services
- **Generating a record** that may survive data breaches, corporate acquisitions, and law enforcement requests

Platforms claim these records are deleted after verification. Some use third-party verification services that claim not to retain the underlying document. The problem is there's no reliable way to verify those claims from the outside.

## Does Linux Still Help?

Linux has long been the operating system of choice for privacy-conscious users, and for good reason. The ecosystem defaults toward open source, transparency, and user control. But it's worth asking: does your choice of operating system still matter when the verification requirements live at the application layer, not the OS layer?

The answer is nuanced.

**What Linux still protects against:**
- Telemetry sent to OS vendors (Windows 11 sends substantial diagnostic data by default)
- Platform-level behavioral tracking built into the OS
- Forced account linking to use basic features
- Automatic cloud sync of files and browsing history

**What Linux cannot protect against:**
- Web-based identity verification requirements (these run in any browser)
- Age-gating laws that apply to the service, not the client software
- Browser fingerprinting that can identify you regardless of OS
- Network-level surveillance by ISPs or government actors

The honest answer is that Linux remains valuable for privacy, but it's not a silver bullet against identity verification mandates. Those mandates exist at the service layer, and no operating system can opt you out of regulatory requirements.

## What Actually Helps

If identity verification is a concern for your organization or your personal threat model, the more effective controls are:

1. **Use services that don't require ID** — there are still many that don't
2. **Compartmentalize identities** — different accounts, different devices, different networks for different purposes
3. **Use a VPN or Tor** for network-layer anonymity, understanding each tool's limitations
4. **Read privacy policies for data retention terms** before uploading any document
5. **Advocate for data minimization** — especially in professional contexts where you influence procurement decisions

For businesses handling customer data: the spread of identity verification requirements is a compliance signal, not just a user experience issue. If your vendors are collecting government IDs, you need to understand what that means for your own data handling obligations under GDPR, HIPAA, or CCPA.

---

*Orion's Guard helps small and mid-size businesses navigate data privacy regulations and build security programs that respect user rights. [Book a free discovery call →](/contact/)*

''')

w('src/content/blog/loyalty-card-surveillance.md', '''\
---
title: "The Hidden Cost of Savings: How Frequent Shopper Cards Surveil You"
description: "That loyalty card saves you a few dollars — and costs you your complete purchase history, behavioral profile, and location data. Here's what actually happens to that data."
date: 2025-11-24
author: "Orion's Guard"
tags: ["Privacy", "Surveillance", "Data Brokers"]
draft: false
---

The loyalty card pitch is simple: swipe your card, save money. What's actually being exchanged is considerably more complex.

Every transaction you make with a loyalty card is logged, timestamped, and linked to your identity. Not just what you bought — when you bought it, which location you visited, how often you return, what you bought in combination with other items, and how your purchasing patterns shift over time.

## What Retailers Actually Collect

Modern retail loyalty programs collect:

- **Full purchase history** — every item, every price paid, every coupon used
- **Location data** — which stores you visit, how frequently, at what times
- **Behavioral patterns** — when you shop (payday patterns, meal timing, seasonal habits)
- **Household composition inferences** — baby products, pet food, and family-size packaging tell a story
- **Health status inferences** — purchases of specific vitamins, medications, or dietary products
- **Financial stress indicators** — shifts toward generic brands, discount items, or smaller package sizes

This data is not just stored — it's analyzed, sold to data brokers, shared with CPG brands for advertising targeting, and increasingly used for credit risk assessment by companies that purchase it from data aggregators.

## The Data Broker Pipeline

When you sign up for a grocery loyalty card, you're creating a data asset that often flows through a pipeline you never consented to explicitly:

1. Retailer collects purchase data tied to your identity
2. Retailer aggregates data internally for marketing
3. Retailer licenses anonymized (but often re-identifiable) data to CPG brands
4. Retailer sells data to data brokers
5. Data brokers aggregate your grocery data with your pharmacy records, your location data from apps, your financial transaction data, and your social media behavior
6. The aggregated profile is sold to insurers, employers, advertisers, and financial institutions

The "anonymization" step at point 3 is largely theatrical. Purchase history is highly identifying — researchers have shown that a small number of transactions are sufficient to re-identify individuals from supposedly anonymized retail datasets.

## What You Can Do

**Use cash for in-store purchases when privacy matters.** It's the most effective opt-out. No loyalty card, no data collection beyond aggregate sales figures.

**Use loyalty programs deliberately.** If you're going to use them, understand what you're trading. For most people, the discount is real and the risk is diffuse. The calculation changes if you're purchasing items related to medical conditions, political affiliations, or other sensitive categories.

**Request your data.** Under CCPA (California) and GDPR (EU), you have the right to request a copy of the data a company holds about you, and to request deletion. Most retailers have privacy portals that honor these requests, though the process is often deliberately cumbersome.

**Opt out of data sharing.** Many loyalty program terms include opt-out options for third-party data sharing. These are typically buried in the privacy settings of the retailer's app or website.

## For Businesses: What This Means for Your Compliance Program

If your organization uses loyalty programs, CRM systems, or any form of behavioral tracking:

- **GDPR Article 22** restricts automated decision-making based on personal data, including behavioral profiling
- **CCPA** requires disclosure of data sales and provides opt-out rights you must honor
- **HIPAA** applies if health-adjacent data is collected in a covered context
- Vendor contracts with data brokers and analytics providers need to be reviewed for data sharing provisions

The regulatory trend is clearly moving toward stronger consumer data rights. Organizations that build privacy-respecting data practices now are better positioned than those that will be forced to retrofit compliance later.

---

*Orion's Guard helps businesses build data handling practices that are both compliant and genuinely privacy-respecting. [Book a free discovery call →](/contact/)*

''')

w('src/content/blog/notepadpp-update-hack.md', '''\
---
title: "The Notepad++ Update Hack: A Case Study in Supply Chain Risk"
description: "A malicious actor hijacked Notepad++ update channels to deliver malware. Here's what happened, who was affected, and what it means for your software update practices."
date: 2026-04-10
author: "Orion's Guard"
tags: ["Supply Chain", "Malware", "Software Security"]
draft: false
---

Software updates are supposed to make you more secure. The process is simple: the vendor ships a patch, your software detects it, you approve, you're protected. What happens when that trusted update channel gets compromised?

The Notepad++ incident is a useful case study — not because it was uniquely sophisticated, but because it happened to a trusted, widely-used tool and followed a pattern that's increasingly common in modern supply chain attacks.

## What Happened

Notepad++ is a free, open-source text editor used by tens of millions of developers, system administrators, and technical users worldwide. Its updater mechanism — built into the application — periodically checks for new versions and prompts users to upgrade.

In this incident, attackers were able to inject a malicious binary into the update delivery path. Users who accepted what appeared to be a routine Notepad++ update instead received a payload that established persistence and connected to attacker-controlled infrastructure.

The attack worked because users reasonably trusted the update prompt. Notepad++ is a legitimate application. The update dialog looked normal. The behavior matched what users expected. Nothing felt wrong — because the trust signal had been hijacked rather than forged.

## Why Supply Chain Attacks Are Effective

Traditional phishing requires the attacker to convince you to take an action you'd normally avoid — click a strange link, open an unexpected attachment, enter credentials on an unfamiliar site. Good security hygiene and user training reduce the effectiveness of these attacks over time.

Supply chain attacks invert this dynamic. They target the trust relationship you've already established with a legitimate vendor or tool. Instead of asking you to do something suspicious, they compromise something you already trust — so you do exactly what you'd normally do, and still get compromised.

This is why supply chain security has become one of the highest-priority concerns in enterprise security programs. The SolarWinds breach (2020), the Kaseya VSA attack (2021), and multiple npm/PyPI package compromises follow the same fundamental pattern: compromise the supplier, reach all the downstream customers.

## What This Means for Small Business

If you're running a small or mid-size business, you probably can't audit the source code of every tool your team uses. That's fine — nobody expects you to. What you can do:

**1. Maintain a software inventory**
Know what's installed on your systems. If you don't know what software you're running, you can't track when it's been compromised.

**2. Use package managers with integrity verification**
Tools like Chocolatey (Windows), Homebrew (Mac), or your OS's native package manager verify checksums and signatures before installation. They're not foolproof, but they add a layer of validation.

**3. Apply the principle of least privilege**
Software that doesn't need to run with elevated privileges shouldn't. An infected application running as a standard user causes significantly less damage than one running as Administrator.

**4. Monitor outbound network connections**
Malware installed via a supply chain attack still needs to phone home. Anomalous outbound connections from trusted applications are a detection signal you can act on.

**5. Have an incident response plan**
When (not if) a trusted tool gets compromised, knowing your response steps in advance dramatically reduces the blast radius. Orion's Guard can help you build one.

## The Takeaway

Updating software is still the right thing to do. Unpatched systems are far more commonly exploited than software update mechanisms. But updates are now part of your threat surface, and treating them with appropriate — if not paranoid — scrutiny is reasonable.

Verify update sources when possible. Be alert to update prompts that appear at unusual times or request unusual permissions. And invest in detection capabilities that can catch the lateral movement and C2 communication that supply chain malware relies on after initial access.

---

*Supply chain risk is a growing concern for organizations of all sizes. Orion's Guard can help you assess and manage third-party and software supply chain risk. [Contact us →](/contact/)*

''')

w('src/content/blog/pairdrop-secure-sharing.md', '''\
---
title: "Sharing Huge Files Securely: Why PairDrop Deserves a Place in Your Toolkit"
description: "Most file-sharing tools route your data through servers you don't control. PairDrop changes that with local-network, peer-to-peer transfer — no account, no cloud, no retention."
date: 2026-05-15
author: "Orion's Guard"
tags: ["Privacy", "File Sharing", "Tools"]
draft: false
---

When you send a file through Dropbox, Google Drive, WeTransfer, or any cloud-based file sharing service, that file travels through a server you don't control. It's stored — at least temporarily — on infrastructure owned by a third party. It may be scanned, indexed, or retained beyond the period you assume.

For most files, this is an acceptable trade-off. For sensitive documents — contracts, HR records, financial data, client information — it's a risk that deserves a second look.

## The Problem with Most File Sharing Tools

Cloud file sharing services have built their business model around convenience. Upload your file, get a link, share it anywhere. The problem is that "anywhere" includes their servers, their security practices, their legal teams, and their response to law enforcement requests.

Even services that offer end-to-end encryption often store encryption keys themselves, meaning "encrypted" doesn't always mean "private."

For businesses subject to HIPAA, GDPR, or similar regulations, this matters even more. If you share patient data or personal information through an unvetted third-party service, you may be creating a compliance exposure you didn't intend to.

## What PairDrop Does Differently

[PairDrop](https://pairdrop.net) is an open-source, browser-based file transfer tool that works over your local network — or optionally over a temporary peer connection. The key differences:

- **No account required** — nothing to create, nothing to breach
- **No server storage** — files transfer directly between devices
- **Works on any device with a browser** — Windows, Mac, Linux, iOS, Android
- **Open source** — the code is auditable; you can self-host it

On a local network (same Wi-Fi), PairDrop uses WebRTC to establish a direct peer-to-peer connection. Files never leave your network. On different networks, PairDrop uses a signaling server to establish the connection, but the file data still passes between devices directly — the server only facilitates the handshake.

## When to Use PairDrop

**Great use cases:**
- Transferring large files between your own devices (phone to laptop, etc.)
- Sharing files with colleagues on the same office network without cloud upload
- Moving sensitive documents between trusted parties who are physically nearby
- Avoiding cloud services for data you'd prefer to keep local

**Not ideal for:**
- Asynchronous transfers (both devices must be online simultaneously)
- Long-term file storage (this is a transfer tool, not a storage solution)
- Transfers across organizations where you need an audit trail

## Self-Hosting for Business Use

If you want to use PairDrop in a business context with full control, you can self-host it. The project is available on GitHub and runs easily in Docker. Self-hosting eliminates reliance on the public instance entirely — your signaling server stays within your infrastructure.

```bash
docker run -d \
  --name pairdrop \
  -p 3000:3000 \
  -e RATE_LIMIT=false \
  lscr.io/linuxserver/pairdrop:latest
```

This gives you a private PairDrop instance accessible only on your network or VPN.

## The Broader Point: Data Minimization

PairDrop is useful, but the more important principle is **data minimization** — the idea that sensitive data should travel through as few systems as possible, and be retained by as few parties as possible.

When evaluating any file-sharing tool for business use, ask:
1. Where does the file live during transit?
2. Where does it live after transit? For how long?
3. Who has access to encryption keys?
4. What does the provider's privacy policy say about scanning or indexing?
5. What happens if there's a law enforcement request?

These aren't paranoid questions — they're the baseline for any organization handling sensitive data responsibly.

---

*Orion's Guard helps businesses select and implement security tools that match their compliance requirements and risk tolerance. [Book a free discovery call →](/contact/)*

''')

w('src/content/blog/passkeys-balanced-look.md', '''\
---
title: "Passkeys: A Balanced Look at the Future of Authentication"
description: "Passkeys promise a passwordless future — and they deliver on many fronts. But before you mandate them enterprise-wide, here's what the tradeoffs actually look like."
date: 2026-03-05
author: "Orion's Guard"
tags: ["Authentication", "Passkeys", "MFA"]
draft: false
---

The password has been declared dead so many times that the announcements have become background noise. But passkeys — the FIDO2/WebAuthn-based authentication standard backed by Apple, Google, and Microsoft — represent something meaningfully different from previous attempts to kill the password.

They're real. They're shipping. And they genuinely improve security in important ways. They also introduce new considerations that organizations should understand before adopting them broadly.

## What Passkeys Actually Are

A passkey is a cryptographic key pair generated on your device. When you register with a service, your device generates a public key (shared with the service) and a private key (stored securely on your device, never transmitted). When you authenticate, the service challenges your device, your device signs the challenge with the private key, and the service verifies the signature with the public key.

The private key never leaves your device. There's no password to phish. No credential database to breach. No replay attacks.

This is a meaningful security improvement. The majority of account takeovers rely on stolen or guessed passwords. Passkeys eliminate that entire attack surface.

## Where Passkeys Genuinely Excel

**Phishing resistance**: A passkey is bound to the specific domain it was created for. A credential phishing site — even a perfect visual replica of the real site — cannot receive a valid passkey authentication because the domain doesn't match. This is categorically different from TOTP codes and push notifications, which can be intercepted in real-time phishing attacks.

**No server-side secrets**: When the service's database gets breached, the attacker gets public keys. Public keys are worthless without the private key on your device. This is a fundamentally better posture than even well-hashed password storage.

**User experience**: For most users, passkey authentication is faster and less frustrating than remembering passwords or juggling a password manager.

## The Real Tradeoffs

**Account recovery is harder**: If you lose access to your device (or all devices where a passkey is stored), recovery processes vary widely by service and can be complex. This is a meaningful operational consideration for organizations.

**Sync and cross-device access**: Apple, Google, and Microsoft all offer passkey sync within their respective ecosystems. This solves the device-loss problem but reintroduces a form of server-side storage — your passkeys live in iCloud Keychain, Google Password Manager, or Windows Hello. For high-security environments, this may be a concern.

**Enterprise management immaturity**: Most enterprise MDM and identity provider integrations for passkeys are still maturing. Provisioning and deprovisioning passkeys for employees at scale is not as simple as it sounds today.

**Not all implementations are equal**: Passkeys stored in a platform authenticator (device TPM, Secure Enclave) are more secure than those synced to cloud keychains. "We support passkeys" can mean several different things.

## What This Means for Your Business

Passkeys are worth adopting — particularly for consumer-facing applications where phishing resistance is high value and where users benefit from the improved experience. For internal enterprise applications, the calculus involves your identity provider's support, your MDM capabilities, and your recovery workflows.

A reasonable path forward:
1. Enable passkeys as an *option* alongside existing authentication methods
2. Educate users on the benefits and recovery procedures
3. Monitor your identity provider's passkey roadmap
4. For high-privilege accounts (admins, executives), prioritize hardware security keys (FIDO2 hardware tokens), which offer passkey-equivalent security without sync dependencies

Passkeys are not a magic bullet — nothing in security is. But they represent a genuine, significant improvement in authentication security that's worth taking seriously.

---

*Orion's Guard helps businesses design and implement authentication strategies that balance security with operational reality. [Book a free discovery call →](/contact/)*

''')

w('src/content/blog/private-photo-storage.md', '''\
---
title: "Guarding Your Glimpses: A Practical Guide to Private Photo Storage"
description: "Your photos contain more sensitive data than almost any other file type. Here's how to take control of where they live and who can access them."
date: 2025-10-01
author: "Orion's Guard"
tags: ["Privacy", "Cloud Storage", "Photos"]
draft: false
---

Photos are among the most personal data we generate — and among the most carelessly stored. Most smartphone users have their entire photo library automatically backed up to a cloud service they've never reviewed the privacy policy of, on servers in jurisdictions they've never considered, with retention terms they've never read.

This guide covers practical options for individuals and small businesses that want meaningful control over where their photos live.

## Why Photos Are High-Risk Data

Beyond the obvious privacy concerns about personal photos, photos contain metadata that most people never think about:

- **EXIF data** — embedded in the file itself, may include GPS coordinates, device model, date/time, and camera settings
- **Facial recognition data** — cloud photo services increasingly analyze faces for organization features; this data may be retained even if you delete photos
- **Content analysis** — machine learning analysis of photo content (objects, scenes, text visible in images) is standard in most cloud photo services

For businesses, employee photos, client event photos, and product development images may all contain sensitive information that warrants careful handling.

## The Main Options

### Option 1: Apple iCloud Photos
**Privacy posture:** Moderate. Apple has strong privacy commitments and end-to-end encryption for most data. iCloud Photos specifically uses encryption in transit and at rest, but Apple holds keys and can access photos for law enforcement requests. Apple's Advanced Data Protection feature enables end-to-end encryption for photos, meaning Apple cannot access them — but this must be explicitly enabled.

**Best for:** Apple ecosystem users who want convenience with meaningful privacy protections, provided they enable Advanced Data Protection.

### Option 2: Google Photos
**Privacy posture:** Lower. Google analyzes photo content for its services and the data interacts with Google's advertising infrastructure. Free tier has been discontinued. Privacy settings provide limited actual data minimization.

**Best for:** Users prioritizing search and organization features over privacy, who accept Google's data model.

### Option 3: Proton Drive
**Privacy posture:** High. End-to-end encrypted by default, zero-knowledge architecture, Switzerland-based (strong privacy laws). No free unlimited tier. Relatively new photo-specific features.

**Best for:** Users with strong privacy requirements who are willing to pay and accept a less polished photo experience.

### Option 4: Self-Hosted (Immich, Nextcloud)
**Privacy posture:** Highest, when configured correctly. Your data, your server, your jurisdiction. Requires technical setup and ongoing maintenance.

**Immich** is an open-source, self-hostable photo management application designed as a Google Photos alternative. It supports automatic mobile backup, face recognition (processed locally), and a polished web/mobile interface.

**Best for:** Technical users and organizations that require full data sovereignty.

## Stripping EXIF Data Before Sharing

Before sharing photos externally — particularly on social media or with clients — strip EXIF metadata.

**On Windows:** Right-click the image → Properties → Details → "Remove Properties and Personal Information"

**Using ExifTool (cross-platform, command line):**
```bash
exiftool -all= photo.jpg
```

**For bulk processing:**
```bash
exiftool -all= -r /path/to/photos/
```

## For Businesses

If your organization handles photos of clients, patients, or employees, consider:

1. **Data classification** — are these photos personal data under GDPR or HIPAA?
2. **Retention policy** — how long do you keep them, and what's the deletion process?
3. **Third-party sharing** — if photos go to a vendor (photographer, designer), what's in the contract about their retention and usage?
4. **EXIF metadata** — client photos often contain location data that shouldn't be shared

A photo storage and handling policy is a small investment that can prevent significant compliance exposure.

---

*Orion's Guard helps businesses develop data handling policies that cover every data type, including photos and media. [Book a free discovery call →](/contact/)*

''')

w('src/content/blog/samsung-privacy-policy.md', '''\
---
title: "Samsung Privacy Policy Review: What Your Smart TV Is Telling Them"
description: "Samsung's privacy policy is one of the most expansive in consumer electronics. Here's what it actually says about your Smart TV, your voice commands, and your viewing habits."
date: 2025-09-21
author: "Orion's Guard"
tags: ["Privacy", "Smart Devices", "IoT"]
draft: false
---

Smart TVs are the most underrated surveillance device in most homes. They're large-screened, always-on, internet-connected, voice-activated, and positioned in the room where most households spend the majority of their leisure time. And most people have never read the privacy policy they agreed to when they turned the TV on for the first time.

Samsung is the world's largest TV manufacturer. Their privacy policy is worth reading carefully.

## What Samsung Collects from Smart TVs

Samsung's Smart TV privacy policy covers data collection across several categories:

**Viewing data**: Samsung collects information about what you watch, including content from cable, over-the-air broadcast, and streaming services. This is accomplished through Automatic Content Recognition (ACR) technology, which analyzes what's displayed on screen — regardless of whether it came from a Samsung app. The data is used for advertising targeting and sold to third parties including advertisers and analytics firms.

**Voice data**: Samsung's voice recognition feature, when enabled, transmits voice commands — and the audio around them — to Samsung's servers and to third-party voice recognition processors. Samsung's earlier privacy policies explicitly noted that "please be aware that if your spoken words include personal or other sensitive information, that information will be among the data captured and transmitted to a third party." The language has since been softened but the underlying data flow remains similar.

**Usage patterns**: Which apps you use, when you use them, how long you watch, what content you interact with, and your navigation patterns within the Smart TV interface.

**Network data**: Your IP address, network identifiers, and information about devices on your home network that interact with the TV.

## The ACR Problem

Automatic Content Recognition is the most broadly impactful data collection feature in Smart TVs, and the least understood by consumers.

ACR works by periodically capturing a portion of the image displayed on screen and comparing it against a database of known content fingerprints. This allows Samsung (and their ACR vendor, which has varied over time) to determine exactly what you're watching — whether it's a Netflix show, a cable channel, a YouTube video, or content from a physical media player.

This data is valuable because it closes the measurement gap that has always existed in traditional television ratings. Advertisers can now know, with high precision, which households watched which ads, what they watched before and after, and whether they took any purchasing actions afterward.

For consumers, this means the TV that sits in your living room is reporting your viewing behavior to parties you likely haven't considered.

## What You Can Do

**Disable ACR**: Samsung calls their ACR system "Viewing Information Services" or similar (the name changes with TV generations). It's in Settings → Support → Terms & Privacy or Settings → General → Privacy. Turn it off.

**Disable voice recognition when not in use**: If you don't use the voice features, disable the microphone. On most Samsung TVs: Settings → General → Voice → Turn off Blink to Wake or Voice Wake-up.

**Use an external streaming device**: An Apple TV, Roku, or dedicated streaming stick limits what the TV's onboard software can observe. Content from HDMI inputs is still captured by ACR unless you disable it.

**Network segmentation**: Placing smart TVs on a separate IoT VLAN prevents them from accessing other devices on your home network. This is more relevant for home offices and small businesses where the TV is in a conference room.

**Review the privacy policy at each major firmware update**: Samsung (like most manufacturers) updates privacy policies periodically. Major TV firmware updates sometimes introduce new data collection features.

## For Businesses: Conference Room TVs

If your organization uses Smart TVs in conference rooms, meeting spaces, or client-facing areas:

- Conference room TVs with voice activation enabled are potential listening devices in sensitive business discussions
- ACR captures content shown on screen during presentations, potentially including confidential business materials
- Smart TVs connected to your corporate network expose the network to IoT-class risks

For conference rooms, consider: disabling all smart features and using the TV as a dumb display via HDMI, deploying a separate streaming solution on an isolated network, and reviewing your acceptable use policy to include guidance on smart device security.

---

*IoT device security is part of any comprehensive security program. Orion's Guard helps businesses identify and manage smart device risks. [Book a free discovery call →](/contact/)*

''')

w('src/content/blog/smb-security-checklist.md', '''\
---
title: "SMB Security Checklist: 10 Steps to Protect Your Business Today"
description: "A practical, prioritized security checklist for small and mid-size businesses. No jargon, no enterprise-only tools — just actionable steps you can start on Monday."
date: 2025-09-05
author: "Orion's Guard"
tags: ["SMB Security", "Checklist", "Getting Started"]
draft: false
---

Most small businesses don't have a dedicated security team. What they do have is a real attack surface, real threat actors targeting them, and the same regulatory obligations as much larger organizations. The good news: a focused effort on the fundamentals closes the majority of your risk.

This checklist is ordered by impact. Start at the top and work down.

---

## ☑ 1. Enable Multi-Factor Authentication (MFA) Everywhere

**Impact: Very High. Effort: Low.**

The single most impactful security control available to any organization is multi-factor authentication. MFA prevents the majority of account takeover attacks — including those using stolen or phished passwords.

**Priority order for MFA rollout:**
1. Email accounts (especially if on Microsoft 365 or Google Workspace)
2. Financial accounts (banking, payroll, accounting software)
3. Administrative accounts (domain registrar, DNS, cloud hosting)
4. SaaS tools (CRM, HR software, project management)
5. Everything else

Use an authenticator app (Google Authenticator, Microsoft Authenticator, or Authy) rather than SMS-based MFA whenever possible. SMS MFA is better than nothing but is vulnerable to SIM-swapping attacks.

---

## ☑ 2. Deploy a Password Manager

**Impact: High. Effort: Low-Medium.**

Password reuse is one of the most common attack vectors for small business breaches. When one service gets breached, attackers try those credentials everywhere. A password manager solves this by making it practical to use unique, strong passwords for every account.

**Recommended options for SMBs:**
- **1Password Business** — excellent team sharing and admin controls
- **Bitwarden** (open source, self-hostable, very affordable)
- **Keeper** — strong compliance reporting features

Require all employees to use the company password manager for any business account.

---

## ☑ 3. Keep Software and Systems Patched

**Impact: Very High. Effort: Medium.**

The majority of successful attacks exploit known vulnerabilities for which patches already exist. Patch management is not glamorous, but it's essential.

**Minimum requirements:**
- Enable automatic updates for operating systems on all devices
- Enable automatic updates for web browsers
- Set a monthly cadence for reviewing and applying patches to business applications
- Don't forget network devices — router and switch firmware needs patching too

---

## ☑ 4. Back Up Your Data — and Test Those Backups

**Impact: Very High (especially for ransomware defense). Effort: Medium.**

Ransomware works by encrypting your data and demanding payment for the decryption key. Organizations with clean, tested backups can recover without paying the ransom. Organizations without them often can't.

**Backup requirements:**
- **3-2-1 rule**: 3 copies, 2 different media types, 1 offsite/offline
- Backups must be isolated from your network — a backup drive that's always connected will be encrypted by ransomware along with everything else
- **Test restoration quarterly** — a backup you've never tested is a backup you can't trust
- For critical data: consider immutable backup solutions (backups that can't be modified or deleted even by an admin)

---

## ☑ 5. Train Employees to Recognize Phishing

**Impact: High. Effort: Medium.**

Phishing is the most common initial access vector for small business breaches. Your employees need to know what modern phishing looks like — which is increasingly sophisticated and no longer limited to obvious Nigerian prince emails.

**Minimum training requirements:**
- Annual security awareness training for all employees
- Phishing simulation exercises (send simulated phishing emails to test and train)
- Clear reporting procedure: "If I think this is phishing, I do X"
- Special focus: business email compromise (BEC), invoice fraud, and executive impersonation

---

## ☑ 6. Control Who Has Access to What

**Impact: High. Effort: Medium.**

Least-privilege access means every user has exactly the access they need for their job — and nothing more. This limits the blast radius of a compromised account or a malicious insider.

**Actions:**
- Audit all user accounts quarterly — remove accounts for departed employees immediately
- Separate administrative accounts from daily-use accounts
- No shared accounts — every user gets their own login
- Document who has admin access to critical systems
- Use role-based access control in your key applications

---

## ☑ 7. Secure Your Wi-Fi and Network

**Impact: Medium-High. Effort: Low-Medium.**

Your network is the connective tissue of your business. Weak network security gives attackers a foothold into everything connected to it.

**Requirements:**
- Use WPA3 (or at minimum WPA2) on all Wi-Fi networks
- Separate guest Wi-Fi from your business network
- Separate IoT devices (smart TVs, cameras, printers) onto their own network segment
- Change default admin passwords on all network devices
- Disable remote management on your router unless specifically needed

---

## ☑ 8. Deploy Endpoint Detection and Response (EDR)

**Impact: High. Effort: Medium.**

Legacy antivirus is no longer sufficient. Modern endpoint protection (EDR) products detect behavior-based threats that signature-based tools miss — including ransomware, fileless malware, and supply chain attacks.

**Options at SMB scale:**
- **Microsoft Defender for Business** — included with Microsoft 365 Business Premium; solid protection at low marginal cost
- **SentinelOne Singularity** — industry-leading detection, SMB-friendly pricing available
- **CrowdStrike Falcon Go** — strong option for growing businesses

Centralized management visibility is important — you need to be able to see what's happening across all endpoints, not just on individual machines.

---

## ☑ 9. Create and Test an Incident Response Plan

**Impact: High when you need it. Effort: Medium.**

When something goes wrong — and eventually something will — having a documented response plan is the difference between a contained incident and a catastrophic one.

**Your incident response plan must answer:**
- Who is the incident response coordinator?
- Who do we call first? (IT contact, legal counsel, cyber insurance provider)
- What systems do we isolate immediately?
- How do we communicate internally during an incident?
- What are our regulatory notification obligations?
- Where do we go if our email system is compromised?

Review and tabletop-test this plan annually.

---

## ☑ 10. Review Your Cyber Insurance Coverage

**Impact: Financial protection. Effort: Low.**

Cyber insurance doesn't prevent breaches, but it significantly limits their financial impact. Most cyber policies cover incident response costs, legal fees, regulatory fines, customer notification, and business interruption.

**When reviewing your policy, ask:**
- Does the policy require specific security controls to be in place? (Many do — and if you don't have them, you may not be covered)
- What's the ransomware sublimit?
- Does the policy cover business email compromise and wire fraud?
- What's the incident response process?

A cyber insurance broker who specializes in cyber (not a generalist) is worth using for this.

---

## Where to Start

If this list feels overwhelming, here's the prioritized first week:

**Day 1:** Enable MFA on email and financial accounts  
**Day 2-3:** Deploy a password manager, require it for all employees  
**Day 4:** Verify backups are running and test one restore  
**Day 5:** Review admin account access and remove any departed employees  

These five actions, completed in a week, eliminate a significant percentage of your risk. Everything else can be layered in from there.

---

*Orion's Guard can help you build a security program that covers all ten steps — designed for your team size, budget, and industry. [Book a free discovery call →](/contact/)*

''')

w('src/content/blog/zero-trust-smb.md', '''\
---
title: "Zero Trust Security: A Practical Implementation Guide for Small Businesses"
description: "Zero Trust isn't just for enterprises. Here's how small and mid-size businesses can implement the core principles without a Fortune 500 budget."
date: 2025-09-18
author: "Orion's Guard"
tags: ["Zero Trust", "Security Architecture", "SMB"]
draft: false
---

"Never trust, always verify" is the foundational principle of Zero Trust security. It sounds simple. The marketing around it has made it sound complex and expensive. The reality is somewhere in between — and much more accessible to small businesses than the enterprise vendor ecosystem would have you believe.

## What Zero Trust Actually Means

Traditional network security operated on a perimeter model: build a strong wall, trust everything inside it. The problem is that the perimeter has effectively dissolved. Employees work from home, from coffee shops, from client sites. Applications live in SaaS platforms and cloud infrastructure. The "inside" of your network is not a meaningful security boundary anymore.

Zero Trust replaces the perimeter model with a continuous verification model:

- **Every request is authenticated and authorized**, regardless of where it originates
- **Least-privilege access** — users and systems get exactly the access they need, nothing more
- **Assume breach** — design your systems as if the attacker is already inside
- **Inspect and log everything** — visibility into all traffic and access events

The principles aren't new. What's new is that the tooling to implement them is now accessible to organizations well below the enterprise tier.

## Zero Trust for Small Businesses: Where to Start

### Step 1: Identity and Access Management

Identity is the new perimeter. Controlling who can access what — and verifying it continuously — is the foundation of Zero Trust.

**Immediate actions:**
- Enable Multi-Factor Authentication (MFA) on every account, prioritizing email, financial systems, and admin accounts
- Use a password manager organization-wide
- Review user access quarterly — remove accounts for departed employees immediately
- Implement role-based access control: your accountant doesn't need access to your source code repository

**Tools accessible at SMB scale:**
- Okta, Microsoft Entra ID (formerly Azure AD), or Google Workspace Identity for SSO and MFA
- 1Password Business or Bitwarden for enterprise password management

### Step 2: Device Trust

Zero Trust requires knowing the security posture of devices before granting access.

**Immediate actions:**
- Require company devices (or approved personal devices) for accessing sensitive systems
- Enable full-disk encryption on all devices (BitLocker on Windows, FileVault on Mac)
- Implement Mobile Device Management (MDM) to enforce security policies
- Ensure endpoint protection (EDR) is deployed and monitored

**Tools:**
- Microsoft Intune, Jamf, or Kandji for MDM
- SentinelOne, CrowdStrike Falcon Go, or Microsoft Defender for endpoint protection

### Step 3: Network Segmentation

Stop treating your network as a flat, trusted zone.

**Immediate actions:**
- Separate IoT devices, guest Wi-Fi, and production systems onto different network segments
- Use a VPN for remote access (WireGuard-based solutions are modern and performant)
- Block outbound internet access for systems that don't need it
- Implement DNS filtering (Cloudflare Gateway, Cisco Umbrella) to block malicious domains

### Step 4: Application Access Control

Rather than VPN access to your entire network, give users access to specific applications.

**Consider:**
- Zero Trust Network Access (ZTNA) products — Cloudflare Access, Zscaler, or Tailscale provide application-level access without network-level exposure
- Web application firewalls for internet-facing applications
- Just-in-time privileged access for administrative functions

### Step 5: Monitor and Respond

Zero Trust without visibility is incomplete.

**Immediate actions:**
- Centralize logging from critical systems (Microsoft Sentinel, Elastic, or a managed SIEM service)
- Set up alerts for failed authentication attempts, privilege escalation, and unusual access patterns
- Establish an incident response procedure — who gets called, what gets isolated, how you communicate

## A Realistic Roadmap

**Month 1-2:** MFA everywhere, password manager deployment, basic access review
**Month 3-4:** MDM deployment, endpoint protection, network segmentation
**Month 5-6:** ZTNA for remote access, DNS filtering, centralized logging
**Ongoing:** Quarterly access reviews, annual risk assessment, continuous monitoring

Zero Trust is a journey, not a product. Starting with identity and access management delivers immediate, measurable risk reduction and creates the foundation for everything that follows.

---

*Orion's Guard helps small and mid-size businesses design and implement Zero Trust architectures that fit their budget and their team. [Book a free discovery call →](/contact/)*

''')

w('src/content/config.ts', '''\
// src/content/config.ts — Astro content collection schema for blog posts
import { defineCollection, z } from "astro:content";

const blog = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    date: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    author: z.string().default("Orion's Guard"),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };

''')

w('src/layouts/Layout.astro', '''\
---
// src/layouts/Layout.astro — Main site layout for Orion's Guard EmDash site
export interface Props {
  title?: string;
  description?: string;
  image?: string;
  isHome?: boolean;
}

const {
  title = "Orion's Guard",
  description = "Enterprise-grade cybersecurity consulting for small and medium-sized businesses. GDPR, HIPAA, SOC 2, CMMC compliance — practical, budget-friendly, scalable.",
  image = "/images/og-logo.png",
  isHome = false,
} = Astro.props;

const siteTitle = isHome ? "Orion's Guard — Cybersecurity Consulting for SMBs" : `${title} | Orion's Guard`;
const canonicalURL = new URL(Astro.url.pathname, Astro.site);
const navLinks = [
  { label: "Home",     href: "/" },
  { label: "Services", href: "/services/" },
  { label: "About",    href: "/about/" },
  { label: "Blog",     href: "/blog/" },
  { label: "Contact",  href: "/contact/" },
];
const path = Astro.url.pathname;
---

<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{siteTitle}</title>
  <meta name="description" content={description} />
  <link rel="canonical" href={canonicalURL} />
  <link rel="icon" type="image/png" href="/images/og-logo.png" />

  <!-- Open Graph -->
  <meta property="og:type" content="website" />
  <meta property="og:url" content={canonicalURL} />
  <meta property="og:title" content={siteTitle} />
  <meta property="og:description" content={description} />
  <meta property="og:image" content={new URL(image, Astro.site)} />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content={siteTitle} />
  <meta name="twitter:description" content={description} />
  <meta name="twitter:image" content={new URL(image, Astro.site)} />

  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" />

  <!-- Global CSS -->
  <link rel="stylesheet" href="/styles/global.css" />

  <!-- Reading progress bar (posts only) -->
  <div id="og-progress" aria-hidden="true"></div>
</head>
<body>

  <!-- ── NAVIGATION ── -->
  <nav class="og-nav" id="og-nav" role="navigation" aria-label="Main">
    <div class="og-nav-inner">
      <a href="/" class="og-logo" aria-label="Orion's Guard Home">
        <img src="/images/og-logo.png" alt="Orion's Guard shield logo" width="36" height="36" />
        <span class="og-logo-name">Orion<span class="og-logo-accent">'s Guard</span></span>
      </a>

      <ul class="og-nav-links" role="list">
        {navLinks.map(link => (
          <li>
            <a
              href={link.href}
              class={`og-nav-link${path === link.href || (link.href !== '/' && path.startsWith(link.href)) ? ' active' : ''}`}
            >{link.label}</a>
          </li>
        ))}
      </ul>

      <div class="og-nav-right">
        <a href="/search/" class="og-nav-search" aria-label="Search">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
        </a>
        <a href="/contact/" class="og-cta-pill">Get Started</a>
        <button class="og-burger" id="og-burger" aria-label="Toggle menu" aria-expanded="false" aria-controls="og-drawer">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>

    <!-- Mobile drawer -->
    <div class="og-drawer" id="og-drawer" hidden>
      {navLinks.map(link => (
        <a href={link.href} class="og-drawer-link">{link.label}</a>
      ))}
      <a href="/contact/" class="og-drawer-cta">Get Started</a>
    </div>
  </nav>

  <!-- ── MAIN CONTENT ── -->
  <main id="main-content">
    <slot />
  </main>

  <!-- ── FOOTER ── -->
  <footer class="og-footer" role="contentinfo">
    <div class="og-footer-inner">
      <div>
        <div class="og-footer-logo">
          <img src="/images/og-logo.png" alt="Orion's Guard logo" height="34" />
          <span class="og-footer-logo-name">Orion's Guard</span>
        </div>
        <p class="og-footer-tagline">
          Cybersecurity consulting built for<br />small and mid-size businesses.
        </p>
      </div>

      <nav class="og-footer-nav" aria-label="Footer navigation">
        <div class="og-footer-col">
          <span class="og-footer-col-title">Services</span>
          <ul role="list">
            <li><a href="/services/#compliance">Compliance Consulting</a></li>
            <li><a href="/services/#vciso">vCISO Services</a></li>
            <li><a href="/services/#risk">Risk Assessments</a></li>
            <li><a href="/services/#training">Security Training</a></li>
            <li><a href="/services/#ir">Incident Response</a></li>
          </ul>
        </div>
        <div class="og-footer-col">
          <span class="og-footer-col-title">Company</span>
          <ul role="list">
            <li><a href="/about/">About Us</a></li>
            <li><a href="/blog/">Blog</a></li>
            <li><a href="/contact/">Contact</a></li>
          </ul>
        </div>
        <div class="og-footer-col">
          <span class="og-footer-col-title">Connect</span>
          <ul role="list">
            <li><a href="https://linkedin.com/company/orionsguard" target="_blank" rel="noopener">LinkedIn</a></li>
            <li><a href="mailto:contact@orionsguard.net">Email Us</a></li>
          </ul>
        </div>
      </nav>
    </div>

    <div class="og-footer-bottom">
      <span>© {new Date().getFullYear()} Orion's Guard LLC. All rights reserved.</span>
      <span style="margin-left:auto; display:flex; gap:.75rem;">
        <a href="/privacy/" style="color:inherit; opacity:.6; font-size:.72rem;">Privacy</a>
        <a href="/terms/" style="color:inherit; opacity:.6; font-size:.72rem;">Terms</a>
      </span>
    </div>
  </footer>

  <script>
    // Sticky nav shadow on scroll
    const nav = document.getElementById('og-nav');
    if (nav) {
      window.addEventListener('scroll', () => {
        nav.classList.toggle('scrolled', window.scrollY > 8);
      }, { passive: true });
    }

    // Mobile burger menu
    const burger = document.getElementById('og-burger');
    const drawer = document.getElementById('og-drawer');
    if (burger && drawer) {
      burger.addEventListener('click', () => {
        const open = !drawer.hidden;
        drawer.hidden = open;
        burger.setAttribute('aria-expanded', String(!open));
        burger.classList.toggle('open', !open);
        document.body.style.overflow = open ? '' : 'hidden';
      });
      // Close drawer on nav link click
      drawer.querySelectorAll('a').forEach(a => {
        a.addEventListener('click', () => {
          drawer.hidden = true;
          burger.setAttribute('aria-expanded', 'false');
          burger.classList.remove('open');
          document.body.style.overflow = '';
        });
      });
    }

    // Reading progress bar
    const bar = document.getElementById('og-progress');
    if (bar) {
      window.addEventListener('scroll', () => {
        const doc = document.documentElement;
        const pct = (doc.scrollTop / (doc.scrollHeight - doc.clientHeight)) * 100;
        bar.style.width = pct + '%';
      }, { passive: true });
    }
  </script>
</body>
</html>

''')

w('src/pages/about.astro', '''\
---
import Layout from '../layouts/Layout.astro';
---

<Layout title="About" description="About Orion's Guard — cybersecurity consulting built for small and mid-size businesses. Learn our mission, approach, and the team behind the shield.">

  <div class="og-page-hero">
    <div class="og-page-hero-inner">
      <nav class="og-breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a><span>/</span><span>About</span>
      </nav>
      <h1 class="og-page-title">About Orion's Guard</h1>
      <p class="og-page-desc">Built by security professionals who believe every business deserves enterprise-grade protection.</p>
    </div>
  </div>

  <div class="og-page-body">

    <!-- Mission -->
    <section style="display:grid; grid-template-columns:1fr 1fr; gap:4rem; align-items:center; margin-bottom:4rem;">
      <div>
        <div class="og-eyebrow">Our Mission</div>
        <h2 style="font-size:clamp(1.5rem,3.5vw,2rem); font-weight:900; letter-spacing:-.03em; color:var(--c-text); margin-bottom:1rem; line-height:1.2;">
          Cybersecurity shouldn't be a luxury
        </h2>
        <p style="color:var(--c-text-soft); line-height:1.8; margin-bottom:1rem;">
          Orion's Guard is a cybersecurity consulting firm providing expertise for small to medium-sized businesses. We work with companies looking to become compliant with GDPR, HIPAA, and other regulations. Our solutions are robust but budget-friendly and can grow with the client.
        </p>
        <p style="color:var(--c-text-soft); line-height:1.8;">
          We believe every company — regardless of size — deserves the same caliber of security strategy that Fortune 500 organizations rely on. We strip out the enterprise overhead and deliver what actually matters: practical, actionable cybersecurity that fits your budget and your roadmap.
        </p>
      </div>
      <div style="display:flex; justify-content:center;">
        <img src="/images/og-mascot.png" alt="Orion's Guard mascot" style="max-width:260px; height:auto; filter:drop-shadow(0 0 40px rgba(37,99,235,.25));" />
      </div>
    </section>

    <!-- Values -->
    <section style="margin-bottom:4rem;">
      <div class="og-eyebrow" style="justify-content:center;">Our Values</div>
      <h2 style="font-size:clamp(1.4rem,3vw,1.8rem); font-weight:800; text-align:center; letter-spacing:-.03em; color:var(--c-text); margin-bottom:2.5rem;">
        How we operate
      </h2>
      <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(240px, 1fr)); gap:1.25rem;">
        {[
          { icon:"🎯", title:"Clarity over complexity", desc:"We translate security requirements into plain English your whole team can understand and act on." },
          { icon:"📈", title:"Scalable by design", desc:"Our engagements are structured to grow with you — from startup to mid-market without starting over." },
          { icon:"🤝", title:"Partnership, not transactions", desc:"We're your long-term security partner, not a vendor you call once and forget." },
          { icon:"💡", title:"Practical outcomes", desc:"Every recommendation comes with clear implementation steps. No jargon, no theoretical frameworks that gather dust." },
        ].map(v => (
          <div style="background:var(--c-bg-card); border:1px solid var(--c-border); border-radius:var(--radius-lg); padding:1.75rem;">
            <span style="font-size:1.75rem; margin-bottom:.75rem; display:block;">{v.icon}</span>
            <h3 style="font-size:1rem; font-weight:700; color:var(--c-text); margin-bottom:.5rem;">{v.title}</h3>
            <p style="font-size:.875rem; color:var(--c-text-soft); line-height:1.6;">{v.desc}</p>
          </div>
        ))}
      </div>
    </section>

    <!-- Expertise -->
    <section style="background:var(--c-bg-card); border:1px solid var(--c-border); border-radius:var(--radius-lg); padding:2.5rem; margin-bottom:4rem;">
      <div class="og-eyebrow">Areas of Expertise</div>
      <h2 style="font-size:1.4rem; font-weight:800; color:var(--c-text); letter-spacing:-.025em; margin-bottom:1.5rem;">What we know deeply</h2>
      <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(200px, 1fr)); gap:.75rem;">
        {["GDPR","HIPAA","SOC 2","CMMC","PCI-DSS","NIST CSF","Zero Trust","Cloud Security","Incident Response","Risk Assessment","Security Architecture","Security Awareness","vCISO","Penetration Testing","Vendor Risk Management"].map(tag => (
          <div style="display:flex; align-items:center; gap:.5rem; font-size:.85rem; color:var(--c-text-soft); background:rgba(37,99,235,.06); border:1px solid rgba(37,99,235,.15); border-radius:6px; padding:.5rem .85rem;">
            <span style="width:6px; height:6px; border-radius:50%; background:var(--c-cyan); flex-shrink:0;"></span>
            {tag}
          </div>
        ))}
      </div>
    </section>

    <!-- CTA -->
    <div style="text-align:center; padding:2rem 0 1rem;">
      <h2 style="font-size:1.5rem; font-weight:800; color:var(--c-text); letter-spacing:-.03em; margin-bottom:.75rem;">Ready to work together?</h2>
      <p style="color:var(--c-text-soft); margin-bottom:1.75rem;">Let's start with a free discovery call to understand your security landscape.</p>
      <a href="/contact/" class="og-btn og-btn-primary">Book a Free Discovery Call</a>
    </div>

  </div>
</Layout>

<style>
@media(max-width:768px) {
  section[style*="grid-template-columns:1fr 1fr"] {
    grid-template-columns: 1fr !important;
  }
}
</style>

''')

w('src/pages/blog/[slug].astro', '''\
---
import Layout from '../../layouts/Layout.astro';
import { getCollection, type CollectionEntry } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  return posts.map(post => ({
    params: { slug: post.slug },
    props: { post },
  }));
}

interface Props { post: CollectionEntry<'blog'>; }
const { post } = Astro.props;
const { Content } = await post.render();

const formattedDate = post.data.date.toLocaleDateString('en-US', {
  year: 'numeric', month: 'long', day: 'numeric',
});
---

<Layout
  title={post.data.title}
  description={post.data.description ?? `${post.data.title} — Orion's Guard cybersecurity blog.`}
>

  <!-- Reading progress bar fills via JS in Layout -->

  <div class="og-page-hero">
    <div class="og-page-hero-inner">
      <nav class="og-breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a>
        <span>/</span>
        <a href="/blog/">Blog</a>
        <span>/</span>
        <span>{post.data.title}</span>
      </nav>
      <div class="og-post-hero-meta">
        <time datetime={post.data.date.toISOString()}>{formattedDate}</time>
        {post.data.tags && post.data.tags.map((tag: string) => (
          <span class="og-chip" style="font-size:.7rem; padding:.2rem .7rem;">{tag}</span>
        ))}
      </div>
      <h1 class="og-page-title" style="font-size:clamp(1.6rem,5vw,2.5rem);">{post.data.title}</h1>
      {post.data.description && (
        <p class="og-page-desc" style="font-size:1.05rem;">{post.data.description}</p>
      )}
    </div>
  </div>

  <div class="og-page-body">
    <div class="og-post-layout">
      <!-- Main article -->
      <article class="og-prose">
        <Content />

        <!-- Tags -->
        {post.data.tags && post.data.tags.length > 0 && (
          <div class="og-post-tags" style="margin-top:3rem; padding-top:1.5rem; border-top:1px solid var(--c-border);">
            <span style="font-size:.75rem; font-weight:700; letter-spacing:.07em; text-transform:uppercase; color:var(--c-text-dim); margin-right:.5rem;">Tags:</span>
            {post.data.tags.map((tag: string) => (
              <span class="og-chip" style="font-size:.72rem;">{tag}</span>
            ))}
          </div>
        )}

        <!-- Post CTA -->
        <div style="background:linear-gradient(135deg,rgba(37,99,235,.08),rgba(6,182,212,.05)); border:1px solid rgba(37,99,235,.2); border-radius:var(--radius-lg); padding:2rem; margin-top:3rem; text-align:center;">
          <h3 style="font-size:1.1rem; font-weight:800; color:var(--c-text); margin-bottom:.5rem; letter-spacing:-.025em;">Need help securing your business?</h3>
          <p style="font-size:.875rem; color:var(--c-text-soft); margin-bottom:1.25rem;">Orion's Guard provides expert cybersecurity consulting built for small and mid-size businesses.</p>
          <a href="/contact/" class="og-btn og-btn-primary" style="font-size:.85rem; padding:.6rem 1.5rem;">Book a Free Discovery Call →</a>
        </div>
      </article>

      <!-- Sidebar -->
      <aside class="og-post-sidebar">
        <div style="background:var(--c-bg-card); border:1px solid var(--c-border); border-radius:var(--radius-lg); padding:1.5rem; position:sticky; top:84px;">
          <h3 style="font-size:.75rem; font-weight:700; letter-spacing:.07em; text-transform:uppercase; color:var(--c-text-dim); margin-bottom:1rem;">About Orion's Guard</h3>
          <p style="font-size:.82rem; color:var(--c-text-soft); line-height:1.7; margin-bottom:1.25rem;">
            Cybersecurity consulting for small and mid-size businesses — practical, budget-friendly, and built to scale with you.
          </p>
          <a href="/contact/" class="og-btn og-btn-primary" style="font-size:.8rem; padding:.55rem 1.2rem; width:100%; justify-content:center;">Free Discovery Call</a>

          <div style="margin-top:1.5rem; padding-top:1.25rem; border-top:1px solid var(--c-border);">
            <h3 style="font-size:.75rem; font-weight:700; letter-spacing:.07em; text-transform:uppercase; color:var(--c-text-dim); margin-bottom:.75rem;">Services</h3>
            <ul style="list-style:none; display:flex; flex-direction:column; gap:.4rem;">
              {["Compliance Consulting","vCISO Services","Risk Assessments","Security Training","Incident Response"].map(s => (
                <li>
                  <a href="/services/" style="font-size:.82rem; color:var(--c-text-soft); text-decoration:none; display:flex; align-items:center; gap:.4rem;">
                    <span style="color:var(--c-cyan);">›</span> {s}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </aside>
    </div>
  </div>
</Layout>

<style>
.og-post-hero-meta {
  display: flex;
  align-items: center;
  gap: .75rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
  font-size: .8rem;
  color: var(--c-text-dim);
}
.og-post-layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 3rem;
  align-items: start;
}
@media(max-width:900px) {
  .og-post-layout { grid-template-columns: 1fr; }
  .og-post-sidebar { display: none; }
}
</style>

''')

w('src/pages/blog/index.astro', '''\
---
import Layout from '../../layouts/Layout.astro';
import { getCollection } from 'astro:content';

const posts = (await getCollection('blog', ({ data }) => !data.draft))
  .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
---

<Layout title="Blog" description="Cybersecurity insights, threat analysis, compliance guides, and privacy tips from the Orion's Guard team.">

  <div class="og-page-hero">
    <div class="og-page-hero-inner">
      <nav class="og-breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a><span>/</span><span>Blog</span>
      </nav>
      <h1 class="og-page-title">Security Insights</h1>
      <p class="og-page-desc">Threat analysis, compliance guides, and practical security tips for your business.</p>
    </div>
  </div>

  <div class="og-page-body">
    {posts.length === 0 ? (
      <p style="color:var(--c-text-soft); text-align:center; padding:4rem 0;">No posts yet — check back soon.</p>
    ) : (
      <div class="og-post-grid">
        {posts.map(post => (
          <article class="og-post-card">
            <div class="og-post-card-body">
              <div class="og-post-meta">
                <time datetime={post.data.date.toISOString()}>
                  {post.data.date.toLocaleDateString('en-US', { year:'numeric', month:'long', day:'numeric' })}
                </time>
                {post.data.tags && post.data.tags.length > 0 && (
                  <span class="og-post-tag">{post.data.tags[0]}</span>
                )}
              </div>
              <h2 class="og-post-card-title">
                <a href={`/blog/${post.slug}/`}>{post.data.title}</a>
              </h2>
              {post.data.description && (
                <p class="og-post-card-desc">{post.data.description}</p>
              )}
              <a href={`/blog/${post.slug}/`} class="og-post-card-link">Read more →</a>
            </div>
          </article>
        ))}
      </div>
    )}
  </div>
</Layout>

<style>
.og-post-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}
.og-post-card {
  background: var(--c-bg-card);
  border: 1px solid var(--c-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: border-color var(--t), transform var(--t), box-shadow var(--t);
  display: flex;
  flex-direction: column;
}
.og-post-card:hover {
  border-color: var(--c-blue-mid);
  transform: translateY(-3px);
  box-shadow: 0 8px 32px rgba(37,99,235,.1);
}
.og-post-card-body {
  padding: 1.75rem;
  display: flex;
  flex-direction: column;
  gap: .75rem;
  flex: 1;
}
.og-post-meta {
  display: flex;
  align-items: center;
  gap: .75rem;
  font-size: .75rem;
  color: var(--c-text-dim);
}
.og-post-tag {
  background: rgba(37,99,235,.1);
  color: var(--c-blue-light);
  border-radius: 999px;
  padding: .15rem .65rem;
  font-weight: 600;
  font-size: .7rem;
  letter-spacing: .04em;
  text-transform: uppercase;
}
.og-post-card-title {
  font-size: 1.05rem;
  font-weight: 700;
  line-height: 1.35;
  letter-spacing: -.02em;
  flex: 1;
}
.og-post-card-title a {
  color: var(--c-text);
  text-decoration: none;
}
.og-post-card-title a:hover { color: var(--c-blue-light); }
.og-post-card-desc {
  font-size: .85rem;
  color: var(--c-text-soft);
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.og-post-card-link {
  font-size: .8rem;
  font-weight: 700;
  letter-spacing: .05em;
  text-transform: uppercase;
  color: var(--c-blue-light);
  text-decoration: none;
  margin-top: auto;
}
</style>

''')

w('src/pages/contact.astro', '''\
---
import Layout from '../layouts/Layout.astro';
---

<Layout title="Contact" description="Book a free discovery call with Orion's Guard. Get expert cybersecurity consulting tailored to your small or mid-size business.">

  <div class="og-page-hero">
    <div class="og-page-hero-inner">
      <nav class="og-breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a><span>/</span><span>Contact</span>
      </nav>
      <h1 class="og-page-title">Let's Talk Security</h1>
      <p class="og-page-desc">Book a free 30-minute discovery call — no obligations, no sales pressure.</p>
    </div>
  </div>

  <div class="og-page-body">
    <div class="og-contact-layout">

      <!-- Left: Info -->
      <div class="og-contact-info">
        <h2>What to expect</h2>
        <p>
          During your discovery call we'll review your current security posture, identify your most pressing risks, and recommend the right engagement. Whether you need compliance help, a risk assessment, or ongoing vCISO support — we'll give you a straight answer.
        </p>
        <ul class="og-check-list" style="margin-top:1.25rem;">
          <li>30-minute conversation, zero fluff</li>
          <li>We review your current tech stack &amp; compliance status</li>
          <li>You get a clear next-step recommendation — free</li>
          <li>No long-term commitment required to start</li>
        </ul>

        <div style="margin-top:2rem; padding-top:1.5rem; border-top:1px solid var(--c-border);">
          <h3 style="font-size:.9rem; font-weight:700; letter-spacing:.06em; text-transform:uppercase; color:var(--c-text-dim); margin-bottom:.75rem;">Direct Contact</h3>
          <a href="mailto:contact@orionsguard.net" style="display:flex; align-items:center; gap:.6rem; color:var(--c-text-soft); font-size:.9rem; text-decoration:none; margin-bottom:.5rem;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
            contact@orionsguard.net
          </a>
          <a href="https://linkedin.com/company/orionsguard" target="_blank" rel="noopener" style="display:flex; align-items:center; gap:.6rem; color:var(--c-text-soft); font-size:.9rem; text-decoration:none;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>
            LinkedIn
          </a>
        </div>
      </div>

      <!-- Right: Form -->
      <div class="og-contact-form-wrap">
        <form
          id="og-contact-form"
          action="https://api.web3forms.com/submit"
          method="POST"
          class="og-contact-form"
          novalidate
        >
          <!-- Web3Forms access key — replace with your actual key from web3forms.com -->
          <input type="hidden" name="access_key" value="YOUR_WEB3FORMS_ACCESS_KEY" />
          <input type="hidden" name="subject" value="New Inquiry — Orion's Guard" />
          <input type="hidden" name="redirect" value="https://orionsguard.net/contact/?sent=1" />
          <!-- Honeypot spam protection -->
          <input type="checkbox" name="botcheck" style="display:none;" tabindex="-1" autocomplete="off" />

          <div class="og-field">
            <label for="name">Full Name <span aria-hidden="true">*</span></label>
            <input type="text" id="name" name="name" required autocomplete="name" placeholder="Jane Smith" />
          </div>

          <div class="og-field">
            <label for="email">Business Email <span aria-hidden="true">*</span></label>
            <input type="email" id="email" name="email" required autocomplete="email" placeholder="jane@yourcompany.com" />
          </div>

          <div class="og-field">
            <label for="company">Company Name</label>
            <input type="text" id="company" name="company" autocomplete="organization" placeholder="Acme Corp" />
          </div>

          <div class="og-field">
            <label for="service">Service of Interest</label>
            <select id="service" name="service">
              <option value="">Select a service…</option>
              <option value="compliance">Compliance Consulting (GDPR, HIPAA, SOC 2, CMMC)</option>
              <option value="vciso">Virtual CISO (vCISO)</option>
              <option value="risk">Risk Assessment</option>
              <option value="training">Security Awareness Training</option>
              <option value="ir">Incident Response</option>
              <option value="architecture">Security Architecture</option>
              <option value="other">Other / Not Sure Yet</option>
            </select>
          </div>

          <div class="og-field">
            <label for="message">How can we help? <span aria-hidden="true">*</span></label>
            <textarea id="message" name="message" rows="5" required placeholder="Tell us about your business, your biggest security concern, or what you're trying to accomplish…"></textarea>
          </div>

          <button type="submit" class="og-btn og-btn-primary" style="width:100%; justify-content:center;" id="og-submit-btn">
            Send Message
          </button>

          <div id="og-form-success" hidden style="margin-top:1rem; padding:1rem; background:rgba(6,182,212,.08); border:1px solid rgba(6,182,212,.25); border-radius:var(--radius); color:var(--c-cyan); font-size:.9rem; text-align:center;">
            ✓ Message sent! We'll be in touch within one business day.
          </div>
          <div id="og-form-error" hidden style="margin-top:1rem; padding:1rem; background:rgba(239,68,68,.08); border:1px solid rgba(239,68,68,.25); border-radius:var(--radius); color:#f87171; font-size:.9rem; text-align:center;">
            Something went wrong. Please email us directly at contact@orionsguard.net
          </div>
        </form>
      </div>

    </div>
  </div>
</Layout>

<style>
.og-contact-layout {
  display: grid;
  grid-template-columns: 1fr 1.4fr;
  gap: 4rem;
  align-items: start;
}
.og-contact-info h2 {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--c-text);
  margin-bottom: .75rem;
  letter-spacing: -.025em;
}
.og-contact-info p {
  color: var(--c-text-soft);
  line-height: 1.8;
  font-size: .9rem;
}
.og-check-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: .6rem;
}
.og-check-list li {
  display: flex;
  align-items: flex-start;
  gap: .5rem;
  font-size: .875rem;
  color: var(--c-text-soft);
}
.og-check-list li::before {
  content: '';
  display: inline-block;
  width: 16px; height: 16px;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2306b6d4' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='20 6 9 17 4 12'/%3E%3C/svg%3E") center/contain no-repeat;
  flex-shrink: 0;
  margin-top: 2px;
}
.og-contact-form-wrap {
  background: var(--c-bg-card);
  border: 1px solid var(--c-border);
  border-radius: var(--radius-lg);
  padding: 2rem;
}
.og-contact-form { display: flex; flex-direction: column; gap: 1.25rem; }
.og-field { display: flex; flex-direction: column; gap: .4rem; }
.og-field label { font-size: .8rem; font-weight: 600; letter-spacing: .04em; text-transform: uppercase; color: var(--c-text-dim); }
.og-field input, .og-field select, .og-field textarea {
  background: var(--c-bg-2);
  border: 1px solid var(--c-border);
  border-radius: var(--radius);
  color: var(--c-text);
  font-size: .9rem;
  padding: .65rem .85rem;
  transition: border-color var(--t), box-shadow var(--t);
  font-family: inherit;
  width: 100%;
  box-sizing: border-box;
}
.og-field input:focus, .og-field select:focus, .og-field textarea:focus {
  outline: none;
  border-color: var(--c-blue-mid);
  box-shadow: 0 0 0 3px rgba(37,99,235,.15);
}
.og-field textarea { resize: vertical; min-height: 120px; }
.og-field input::placeholder, .og-field textarea::placeholder { color: var(--c-text-dim); }
@media(max-width:768px) {
  .og-contact-layout { grid-template-columns: 1fr; gap: 2rem; }
}
</style>

<script>
// Show success/error states without full page reload
const form = document.getElementById('og-contact-form') as HTMLFormElement;
const btn = document.getElementById('og-submit-btn') as HTMLButtonElement;
const successMsg = document.getElementById('og-form-success');
const errorMsg = document.getElementById('og-form-error');

if (form) {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    btn.textContent = 'Sending…';
    btn.disabled = true;
    try {
      const res = await fetch(form.action, { method: 'POST', body: new FormData(form) });
      if (res.ok) {
        form.reset();
        if (successMsg) successMsg.hidden = false;
      } else {
        if (errorMsg) errorMsg.hidden = false;
      }
    } catch {
      if (errorMsg) errorMsg.hidden = false;
    } finally {
      btn.textContent = 'Send Message';
      btn.disabled = false;
    }
  });
}
</script>

''')

w('src/pages/index.astro', '''\
---
// src/pages/index.astro — Orion's Guard Homepage
import Layout from '../layouts/Layout.astro';
---

<Layout isHome={true} title="Orion's Guard" description="Enterprise-grade cybersecurity consulting for small and mid-size businesses. GDPR, HIPAA, SOC 2, CMMC, PCI-DSS compliance — practical, budget-friendly, scalable security.">

  <!-- ── HERO ── -->
  <section class="og-hero" aria-label="Hero">
    <div class="og-hero-grid" aria-hidden="true"></div>
    <div class="og-hero-glow" aria-hidden="true"></div>
    <div class="og-hero-body">
      <div class="og-eyebrow">
        <span class="og-dot" aria-hidden="true"></span>
        Cybersecurity Consulting for Small &amp; Mid-Size Business
      </div>

      <h1 class="og-hero-h1">
        Protect What<br /><em>You've Built.</em>
      </h1>

      <p class="og-hero-lead">
        Orion's Guard is a cybersecurity consulting firm built for small and medium-sized businesses.
        We help startups, growing companies, and established SMBs navigate compliance — GDPR, HIPAA, SOC&nbsp;2,
        and beyond — with practical, scalable security strategies that protect your data without breaking your budget.
      </p>

      <div class="og-hero-btns">
        <a href="/contact/" class="og-btn og-btn-primary">Book a Free Discovery Call</a>
        <a href="/services/" class="og-btn og-btn-outline">Explore Services</a>
      </div>

      <div class="og-chips" aria-label="Compliance frameworks we cover">
        {["GDPR","HIPAA","SOC 2","CMMC","PCI-DSS","NIST CSF","vCISO","Zero Trust"].map(c => (
          <span class="og-chip">{c}</span>
        ))}
      </div>
    </div>
  </section>

  <!-- ── STATS STRIP ── -->
  <section class="og-stats" aria-label="Cybersecurity statistics">
    <div class="og-stats-inner">
      <div class="og-stat">
        <span class="og-stat-num">$10.5T</span>
        <span class="og-stat-label">Global cybercrime cost by 2025 — and rising every year</span>
      </div>
      <div class="og-stat-div" aria-hidden="true"></div>
      <div class="og-stat">
        <span class="og-stat-num">43%</span>
        <span class="og-stat-label">Of cyberattacks target small businesses specifically</span>
      </div>
      <div class="og-stat-div" aria-hidden="true"></div>
      <div class="og-stat">
        <span class="og-stat-num">60%</span>
        <span class="og-stat-label">Of SMBs close within six months of a breach</span>
      </div>
    </div>
  </section>

  <!-- ── SERVICES PREVIEW ── -->
  <section class="og-page-body" aria-label="Our services">
    <div style="text-align:center; margin-bottom:3rem;">
      <div class="og-eyebrow" style="justify-content:center;">What We Do</div>
      <h2 style="font-size:clamp(1.6rem,4vw,2.25rem); font-weight:900; letter-spacing:-.03em; color:var(--c-text); margin-bottom:.75rem;">
        Enterprise Security, SMB Budget
      </h2>
      <p style="color:var(--c-text-soft); max-width:560px; margin:0 auto; font-size:1rem; line-height:1.7;">
        We deliver the same caliber of cybersecurity strategy that Fortune 500 companies rely on — scaled and priced for organizations like yours.
      </p>
    </div>

    <div class="og-services-grid">
      {[
        {
          icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>`,
          title: "Compliance Consulting",
          desc: "Navigate GDPR, HIPAA, SOC 2, CMMC, and PCI-DSS with a clear roadmap — no surprises, no bloated retainers.",
          href: "/services/#compliance",
        },
        {
          icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M6 20v-2a6 6 0 0 1 12 0v2"/></svg>`,
          title: "vCISO Services",
          desc: "A seasoned Chief Information Security Officer on your team — without the executive salary. Strategic oversight on demand.",
          href: "/services/#vciso",
        },
        {
          icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/><path d="M11 8v6"/><path d="M8 11h6"/></svg>`,
          title: "Risk Assessments",
          desc: "Identify vulnerabilities before attackers do. Comprehensive gap analysis mapped to your business operations.",
          href: "/services/#risk",
        },
        {
          icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>`,
          title: "Security Training",
          desc: "Your employees are your first — and often weakest — line of defense. We make security awareness stick.",
          href: "/services/#training",
        },
        {
          icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>`,
          title: "Incident Response",
          desc: "When the worst happens, response speed is everything. We provide rapid triage, containment, and recovery planning.",
          href: "/services/#ir",
        },
        {
          icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8"/><path d="M12 17v4"/></svg>`,
          title: "Security Architecture",
          desc: "Zero Trust frameworks, network segmentation, cloud security — built right from the start so you don't have to retrofit later.",
          href: "/services/#architecture",
        },
      ].map(svc => (
        <a href={svc.href} class="og-svc-card" aria-label={svc.title}>
          <div class="og-svc-icon" aria-hidden="true" set:html={svc.icon} />
          <h3 class="og-svc-title">{svc.title}</h3>
          <p class="og-svc-desc">{svc.desc}</p>
          <span class="og-svc-cta">Learn more →</span>
        </a>
      ))}
    </div>
  </section>

  <!-- ── TRUST SECTION ── -->
  <section style="background:var(--c-bg-2); border-top:1px solid var(--c-border); border-bottom:1px solid var(--c-border); padding:4rem 1.5rem;">
    <div style="max-width:var(--max-w); margin:0 auto; display:grid; grid-template-columns:1fr 1fr; gap:4rem; align-items:center;">
      <div>
        <div class="og-eyebrow">Why Orion's Guard</div>
        <h2 style="font-size:clamp(1.5rem,3.5vw,2.1rem); font-weight:900; letter-spacing:-.03em; color:var(--c-text); margin-bottom:1rem; line-height:1.15;">
          Cybersecurity expertise that scales with your business
        </h2>
        <p style="color:var(--c-text-soft); line-height:1.8; margin-bottom:1.5rem;">
          Orion's Guard delivers enterprise-caliber cybersecurity consulting for organizations that don't have enterprise-sized budgets. Our solutions are robust, budget-friendly, and designed to grow with your client as your business evolves.
        </p>
        <ul style="list-style:none; display:flex; flex-direction:column; gap:.75rem;">
          {[
            "Flat-rate and retainer engagements — no surprise invoices",
            "Frameworks tailored to your industry and size",
            "Plain-English reporting — no jargon, just action items",
            "Long-term partner, not a one-time vendor",
          ].map(item => (
            <li style="display:flex; align-items:flex-start; gap:.6rem; color:var(--c-text-soft); font-size:.9rem;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--c-cyan)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0; margin-top:2px;"><polyline points="20 6 9 17 4 12"/></svg>
              {item}
            </li>
          ))}
        </ul>
      </div>
      <div style="display:flex; justify-content:center; align-items:center;">
        <img src="/images/og-mascot.png" alt="Orion's Guard mascot — a honey badger in a circuit-patterned hoodie" style="max-width:280px; height:auto; filter:drop-shadow(0 0 40px rgba(37,99,235,.3));" />
      </div>
    </div>
  </section>

  <!-- ── CTA BANNER ── -->
  <section style="padding:5rem 1.5rem; text-align:center; background:var(--c-bg);">
    <div style="max-width:640px; margin:0 auto;">
      <div class="og-eyebrow" style="justify-content:center;">Ready to Get Started?</div>
      <h2 style="font-size:clamp(1.6rem,4vw,2.25rem); font-weight:900; letter-spacing:-.03em; color:var(--c-text); margin-bottom:1rem;">
        Let's secure your business — together
      </h2>
      <p style="color:var(--c-text-soft); line-height:1.7; margin-bottom:2rem;">
        Book a free, no-obligation discovery call. We'll review your current security posture and show you exactly where to focus.
      </p>
      <div style="display:flex; justify-content:center; gap:1rem; flex-wrap:wrap;">
        <a href="/contact/" class="og-btn og-btn-primary">Book Free Discovery Call</a>
        <a href="/services/" class="og-btn og-btn-outline">View All Services</a>
      </div>
    </div>
  </section>

</Layout>

<style>
.og-services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.25rem;
  margin-bottom: 3rem;
}
.og-svc-card {
  background: var(--c-bg-card);
  border: 1px solid var(--c-border);
  border-radius: var(--radius-lg);
  padding: 1.75rem;
  display: flex;
  flex-direction: column;
  gap: .75rem;
  transition: border-color var(--t), transform var(--t), box-shadow var(--t);
  color: inherit;
  text-decoration: none;
}
.og-svc-card:hover {
  border-color: var(--c-blue-mid);
  transform: translateY(-3px);
  box-shadow: 0 8px 32px rgba(37,99,235,.12);
}
.og-svc-icon {
  width: 48px; height: 48px;
  background: rgba(37,99,235,.08);
  border: 1px solid var(--c-border);
  border-radius: var(--radius);
  display: flex; align-items: center; justify-content: center;
  color: var(--c-blue-light);
  flex-shrink: 0;
}
.og-svc-title { font-size: 1rem; font-weight: 700; color: var(--c-text); }
.og-svc-desc { font-size: .88rem; color: var(--c-text-soft); line-height: 1.6; flex: 1; }
.og-svc-cta { font-size: .76rem; font-weight: 700; letter-spacing: .05em; text-transform: uppercase; color: var(--c-blue-light); }

@media(max-width:900px) {
  .og-trust-split { grid-template-columns: 1fr !important; }
  .og-trust-split img { max-width: 200px !important; }
}
</style>

''')

w('src/pages/search.astro', '''\
---
import Layout from '../layouts/Layout.astro';
import { getCollection } from 'astro:content';

const posts = (await getCollection('blog', ({ data }) => !data.draft))
  .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());

// Pass posts as JSON to client-side search script
const postsJson = JSON.stringify(posts.map(p => ({
  slug: p.slug,
  title: p.data.title,
  description: p.data.description ?? '',
  tags: p.data.tags ?? [],
  date: p.data.date.toISOString(),
})));
---

<Layout title="Search" description="Search Orion's Guard blog posts and cybersecurity resources.">

  <div class="og-page-hero">
    <div class="og-page-hero-inner">
      <nav class="og-breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a><span>/</span><span>Search</span>
      </nav>
      <h1 class="og-page-title">Search</h1>
      <p class="og-page-desc">Find blog posts and security resources.</p>
    </div>
  </div>

  <div class="og-page-body">
    <div class="og-search-bar">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
      <input
        id="og-search-input"
        type="search"
        placeholder="Search posts…"
        aria-label="Search blog posts"
        autofocus
      />
    </div>
    <p id="og-search-count" style="color:var(--c-text-dim); font-size:.85rem; margin-bottom:1.5rem;"></p>
    <div id="og-search-results" class="og-post-grid"></div>
    <p id="og-no-results" hidden style="color:var(--c-text-soft); text-align:center; padding:3rem 0;">No posts found. Try a different search term.</p>
  </div>
</Layout>

<script define:vars={{ postsJson }}>
const POSTS = JSON.parse(postsJson);
const input = document.getElementById('og-search-input');
const results = document.getElementById('og-search-results');
const countEl = document.getElementById('og-search-count');
const noResults = document.getElementById('og-no-results');

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('en-US', { year:'numeric', month:'long', day:'numeric' });
}

function render(matches) {
  results.innerHTML = matches.map(p => `
    <article class="og-post-card">
      <div class="og-post-card-body">
        <div class="og-post-meta">
          <time datetime="${p.date}">${formatDate(p.date)}</time>
          ${p.tags[0] ? `<span class="og-post-tag">${p.tags[0]}</span>` : ''}
        </div>
        <h2 class="og-post-card-title">
          <a href="/blog/${p.slug}/">${p.title}</a>
        </h2>
        ${p.description ? `<p class="og-post-card-desc">${p.description}</p>` : ''}
        <a href="/blog/${p.slug}/" class="og-post-card-link">Read more →</a>
      </div>
    </article>
  `).join('');

  countEl.textContent = matches.length === POSTS.length
    ? `Showing all ${POSTS.length} posts`
    : `${matches.length} result${matches.length !== 1 ? 's' : ''}`;
  noResults.hidden = matches.length > 0;
}

function search(q) {
  if (!q.trim()) return render(POSTS);
  const terms = q.toLowerCase().split(/\s+/);
  const filtered = POSTS.filter(p => {
    const haystack = [p.title, p.description, ...p.tags].join(' ').toLowerCase();
    return terms.every(t => haystack.includes(t));
  });
  render(filtered);
}

// Initial render
render(POSTS);

// Search on input
input.addEventListener('input', (e) => search(e.target.value));
</script>

<style>
.og-search-bar {
  display: flex;
  align-items: center;
  gap: .75rem;
  background: var(--c-bg-card);
  border: 1px solid var(--c-border);
  border-radius: var(--radius-lg);
  padding: .75rem 1.25rem;
  margin-bottom: 1.25rem;
}
.og-search-bar input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: var(--c-text);
  font-size: 1rem;
  font-family: inherit;
}
.og-search-bar input::placeholder { color: var(--c-text-dim); }
.og-post-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.25rem;
}
.og-post-card {
  background: var(--c-bg-card);
  border: 1px solid var(--c-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: border-color var(--t), transform var(--t);
}
.og-post-card:hover { border-color: var(--c-blue-mid); transform: translateY(-2px); }
.og-post-card-body { padding: 1.5rem; display:flex; flex-direction:column; gap:.6rem; }
.og-post-meta { display:flex; align-items:center; gap:.6rem; font-size:.75rem; color:var(--c-text-dim); }
.og-post-tag { background:rgba(37,99,235,.1); color:var(--c-blue-light); border-radius:999px; padding:.15rem .6rem; font-weight:600; font-size:.7rem; letter-spacing:.04em; text-transform:uppercase; }
.og-post-card-title { font-size:1rem; font-weight:700; line-height:1.35; }
.og-post-card-title a { color:var(--c-text); text-decoration:none; }
.og-post-card-title a:hover { color:var(--c-blue-light); }
.og-post-card-desc { font-size:.83rem; color:var(--c-text-soft); line-height:1.6; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }
.og-post-card-link { font-size:.78rem; font-weight:700; letter-spacing:.05em; text-transform:uppercase; color:var(--c-blue-light); }
</style>

''')

w('src/pages/services.astro', '''\
---
import Layout from '../layouts/Layout.astro';
---

<Layout
  title="Services"
  description="Cybersecurity consulting services for SMBs: compliance (GDPR, HIPAA, SOC 2, CMMC), vCISO, risk assessments, security training, and incident response."
>

  <!-- Inner Hero -->
  <div class="og-page-hero">
    <div class="og-page-hero-inner">
      <nav class="og-breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a>
        <span aria-hidden="true">/</span>
        <span>Services</span>
      </nav>
      <h1 class="og-page-title">Cybersecurity Services</h1>
      <p class="og-page-desc">
        Enterprise-caliber security consulting — scoped and priced for small and mid-size businesses.
      </p>
    </div>
  </div>

  <div class="og-page-body">

    <!-- Compliance Consulting -->
    <section id="compliance" class="og-service-section">
      <div class="og-service-icon-wrap" aria-hidden="true">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
      </div>
      <div class="og-service-body">
        <h2>Compliance Consulting</h2>
        <p>
          Whether you're facing your first GDPR audit or preparing for a SOC 2 Type II examination, Orion's Guard maps a clear, step-by-step path to certification. We translate dense regulatory language into concrete action items your team can actually execute — no consultant-speak, no bloated deliverables.
        </p>
        <ul class="og-check-list">
          <li>GDPR &amp; CCPA data protection programs</li>
          <li>HIPAA Security Rule gap analysis &amp; remediation</li>
          <li>SOC 2 Type I &amp; Type II readiness</li>
          <li>CMMC Level 1–3 assessment &amp; implementation</li>
          <li>PCI-DSS scope reduction &amp; audit preparation</li>
          <li>NIST CSF program design</li>
        </ul>
        <a href="/contact/" class="og-btn og-btn-primary" style="display:inline-block; margin-top:1.5rem;">Get Compliance Help →</a>
      </div>
    </section>

    <!-- vCISO -->
    <section id="vciso" class="og-service-section">
      <div class="og-service-icon-wrap" aria-hidden="true">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M6 20v-2a6 6 0 0 1 12 0v2"/></svg>
      </div>
      <div class="og-service-body">
        <h2>Virtual CISO (vCISO)</h2>
        <p>
          A Chief Information Security Officer brings strategic direction to your entire security program — but hiring one full-time costs $200K+ per year. Our vCISO service gives you seasoned security leadership on a flexible retainer, so you get the strategy without the executive overhead.
        </p>
        <ul class="og-check-list">
          <li>Security program design &amp; roadmap</li>
          <li>Board-level risk reporting</li>
          <li>Vendor risk management oversight</li>
          <li>Policy development &amp; review</li>
          <li>Regulatory liaison support</li>
          <li>Monthly advisory sessions</li>
        </ul>
        <a href="/contact/" class="og-btn og-btn-primary" style="display:inline-block; margin-top:1.5rem;">Explore vCISO →</a>
      </div>
    </section>

    <!-- Risk Assessments -->
    <section id="risk" class="og-service-section">
      <div class="og-service-icon-wrap" aria-hidden="true">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
      </div>
      <div class="og-service-body">
        <h2>Risk Assessments</h2>
        <p>
          You can't defend what you don't understand. Our risk assessments give you a complete, prioritized picture of where your business is exposed — mapped to real-world threat scenarios, not just theoretical checklists. Every finding comes with a practical remediation plan.
        </p>
        <ul class="og-check-list">
          <li>Technical vulnerability assessments</li>
          <li>Third-party &amp; supply chain risk review</li>
          <li>Cloud security posture assessment (AWS, Azure, GCP)</li>
          <li>Business continuity &amp; disaster recovery gaps</li>
          <li>Phishing &amp; social engineering exposure analysis</li>
          <li>Executive summary + technical findings report</li>
        </ul>
        <a href="/contact/" class="og-btn og-btn-primary" style="display:inline-block; margin-top:1.5rem;">Request an Assessment →</a>
      </div>
    </section>

    <!-- Security Training -->
    <section id="training" class="og-service-section">
      <div class="og-service-icon-wrap" aria-hidden="true">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
      </div>
      <div class="og-service-body">
        <h2>Security Awareness Training</h2>
        <p>
          Humans remain the number one attack vector in most breaches. Phishing, credential stuffing, social engineering — your employees need to know what these look like in the real world, not just in a slide deck. We deliver engaging, practical training that actually changes behavior.
        </p>
        <ul class="og-check-list">
          <li>Role-based security awareness programs</li>
          <li>Live phishing simulations &amp; reporting</li>
          <li>Password hygiene &amp; MFA adoption workshops</li>
          <li>Executive &amp; board-level security briefings</li>
          <li>Compliance-specific training (HIPAA, PCI-DSS)</li>
          <li>Ongoing microtraining campaigns</li>
        </ul>
        <a href="/contact/" class="og-btn og-btn-primary" style="display:inline-block; margin-top:1.5rem;">Start Training →</a>
      </div>
    </section>

    <!-- Incident Response -->
    <section id="ir" class="og-service-section">
      <div class="og-service-icon-wrap" aria-hidden="true">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
      </div>
      <div class="og-service-body">
        <h2>Incident Response</h2>
        <p>
          When a breach occurs, every minute counts. Orion's Guard provides rapid triage, expert containment, forensic analysis, and a clear path to recovery — while keeping you informed and in control throughout the process. We also help you document the incident for regulatory reporting requirements.
        </p>
        <ul class="og-check-list">
          <li>Rapid triage &amp; initial containment</li>
          <li>Forensic evidence preservation</li>
          <li>Root cause analysis</li>
          <li>Regulatory breach notification guidance</li>
          <li>Recovery planning &amp; hardening</li>
          <li>Post-incident review &amp; lessons-learned report</li>
        </ul>
        <a href="/contact/" class="og-btn og-btn-primary" style="display:inline-block; margin-top:1.5rem;">Prepare Now →</a>
      </div>
    </section>

    <!-- Security Architecture -->
    <section id="architecture" class="og-service-section" style="border-bottom:none; margin-bottom:0; padding-bottom:0;">
      <div class="og-service-icon-wrap" aria-hidden="true">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8"/><path d="M12 17v4"/></svg>
      </div>
      <div class="og-service-body">
        <h2>Security Architecture &amp; Design</h2>
        <p>
          Building something new? Migrating to the cloud? This is the time to architect security in, not bolt it on later. We design Zero Trust frameworks, network segmentation strategies, and identity &amp; access management systems that protect you from day one.
        </p>
        <ul class="og-check-list">
          <li>Zero Trust network architecture</li>
          <li>Cloud security design (AWS, Azure, GCP)</li>
          <li>Identity &amp; Access Management (IAM)</li>
          <li>Network segmentation &amp; micro-segmentation</li>
          <li>Secure SDLC integration</li>
          <li>Security tooling selection &amp; implementation</li>
        </ul>
        <a href="/contact/" class="og-btn og-btn-primary" style="display:inline-block; margin-top:1.5rem;">Start Your Architecture →</a>
      </div>
    </section>

    <!-- CTA -->
    <div style="background:var(--c-bg-card); border:1px solid var(--c-border); border-radius:var(--radius-lg); padding:3rem 2rem; text-align:center; margin-top:4rem;">
      <h2 style="font-size:1.6rem; font-weight:800; letter-spacing:-.03em; color:var(--c-text); margin-bottom:.75rem;">Not sure which service fits?</h2>
      <p style="color:var(--c-text-soft); margin-bottom:1.75rem; max-width:480px; margin-left:auto; margin-right:auto;">
        Book a free 30-minute discovery call. We'll review your situation and recommend the right engagement — no pressure, no sales pitch.
      </p>
      <a href="/contact/" class="og-btn og-btn-primary">Book Free Discovery Call</a>
    </div>

  </div>
</Layout>

<style>
.og-service-section {
  display: grid;
  grid-template-columns: 64px 1fr;
  gap: 2rem;
  padding: 3rem 0;
  border-bottom: 1px solid var(--c-border);
  align-items: start;
}
.og-service-icon-wrap {
  width: 56px; height: 56px;
  background: rgba(37,99,235,.08);
  border: 1px solid var(--c-border);
  border-radius: var(--radius);
  display: flex; align-items: center; justify-content: center;
  color: var(--c-blue-light);
  flex-shrink: 0;
  margin-top: .25rem;
}
.og-service-body h2 {
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--c-text);
  margin-bottom: .75rem;
  letter-spacing: -.025em;
}
.og-service-body p {
  color: var(--c-text-soft);
  line-height: 1.8;
  margin-bottom: 1rem;
}
.og-check-list {
  list-style: none;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: .5rem;
}
.og-check-list li {
  display: flex;
  align-items: flex-start;
  gap: .5rem;
  font-size: .88rem;
  color: var(--c-text-soft);
}
.og-check-list li::before {
  content: '';
  display: inline-block;
  width: 16px; height: 16px;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2306b6d4' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='20 6 9 17 4 12'/%3E%3C/svg%3E") center/contain no-repeat;
  flex-shrink: 0;
  margin-top: 2px;
}
@media(max-width:640px) {
  .og-service-section { grid-template-columns: 1fr; }
  .og-check-list { grid-template-columns: 1fr; }
}
</style>

''')

w('tsconfig.json', '''\
{
  "extends": "astro/tsconfigs/strict",
  "compilerOptions": {
    "strictNullChecks": true
  }
}

''')

print()
print("=" * 60)
print("  Done! All files written.")
print()
print("  NEXT STEPS:")
print("  1. Copy og-logo.png + og-mascot.png into public/images/")
print("  2. npm install")
print("  3. npm run dev    # preview at localhost:4321")
print("  4. npm run build  # builds to dist/")
print("  5. Deploy dist/ to Cloudflare Pages")
print("=" * 60)
# ── Git: add, commit, push ────────────────────────────────────
print()
print("  Step 3: Committing and pushing to GitHub …")
print()

git_cmds = [
    ["git", "add", "-A"],
    ["git", "commit", "-m", "chore: deploy Orion's Guard Astro site"],
    ["git", "push"],
]

for cmd in git_cmds:
    print("  $", " ".join(cmd))
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if result.stdout.strip():
        print("   ", result.stdout.strip())
    if result.returncode != 0:
        print()
        print("  ❌ git command failed:")
        print("  ", result.stderr.strip())
        print()
        print("  Fix the git error above, then manually run:")
        print("    git add -A")
        print("    git commit -m 'deploy Orion Guard site'")
        print("    git push")
        sys.exit(1)

print()
print("=" * 60)
print("  ✅  All done!  Cloudflare is rebuilding orionsguard.net …")
print()
print("  Cloudflare build takes ~2 min. Check progress at:")
print("  https://dash.cloudflare.com → Workers & Pages")
print()
print("  IMPORTANT — two manual steps still needed:")
print("  1. Copy your logo/mascot images into public/images/")
print("     og-logo.png  and  og-mascot.png")
print("     (from your old Hugo static/images/ folder)")
print()
print("  2. Replace YOUR_WEB3FORMS_ACCESS_KEY in:")
print("     src/pages/contact.astro")
print("     Get a free key at: https://web3forms.com")
print("=" * 60)

