#!/usr/bin/env python3
# ================================================================
#  Orion's Guard — fix2_orionsguard.py
#  Run from the ROOT of your cloned repo:
#    cd C:\Users\germa\OneDrive\OrionsGuard\orionsguardsite
#    python fix2_orionsguard.py
#
#  Fixes two remaining Astro 5 issues:
#    1. Delete [slug].astro (wrong name — Astro uses [...slug].astro)
#    2. Rewrite [...slug].astro with correct render(post) + slug stripping
#    3. Fix index.astro + search.astro — strip .md from post.id in URLs
# ================================================================
import os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

def w(rel, content):
    parts = rel.split("/")
    path = os.path.join(ROOT, *parts)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  fixed:   {rel}")

def rm(rel):
    path = os.path.join(ROOT, *rel.split("/"))
    if os.path.exists(path):
        os.remove(path)
        print(f"  deleted: {rel}")
    else:
        print(f"  skip:    {rel} (already gone)")

print("=" * 60)
print("  Orion's Guard — Astro 5 Fix #2")
print("=" * 60)
print()
print("  Step 1: Removing wrongly-named slug file ...")

# Our fix1 created [slug].astro but Astro needs [...slug].astro
rm("src/pages/blog/[slug].astro")

print()
print("  Step 2: Writing corrected files ...")

# ── src/pages/blog/[...slug].astro ──────────────────────────
# Fixes:
#   render(post)  instead of post.render()    (Astro 5)
#   slug = post.id.replace(.md)               (Astro 5: post.id includes extension)
w("src/pages/blog/[...slug].astro", """\
---
import Layout from '../../layouts/Layout.astro';
import { getCollection, render, type CollectionEntry } from 'astro:content';

// In Astro 5, post.id includes the file extension e.g. "my-post.md"
// Strip it for clean URLs: /blog/my-post/
function slugify(id: string) {
  return id.replace(/\\.mdx?$/, '');
}

export async function getStaticPaths() {
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  return posts.map(post => ({
    params: { slug: slugify(post.id) },
    props: { post },
  }));
}

interface Props { post: CollectionEntry<'blog'>; }
const { post } = Astro.props;
const { Content } = await render(post);

const formattedDate = post.data.date.toLocaleDateString('en-US', {
  year: 'numeric', month: 'long', day: 'numeric',
});
---

<Layout
  title={post.data.title}
  description={post.data.description ?? `${post.data.title} — Orion's Guard cybersecurity blog.`}
>

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
      <article class="og-prose">
        <Content />

        {post.data.tags && post.data.tags.length > 0 && (
          <div class="og-post-tags" style="margin-top:3rem; padding-top:1.5rem; border-top:1px solid var(--c-border);">
            <span style="font-size:.75rem; font-weight:700; letter-spacing:.07em; text-transform:uppercase; color:var(--c-text-dim); margin-right:.5rem;">Tags:</span>
            {post.data.tags.map((tag: string) => (
              <span class="og-chip" style="font-size:.72rem;">{tag}</span>
            ))}
          </div>
        )}

        <div style="background:linear-gradient(135deg,rgba(37,99,235,.08),rgba(6,182,212,.05)); border:1px solid rgba(37,99,235,.2); border-radius:var(--radius-lg); padding:2rem; margin-top:3rem; text-align:center;">
          <h3 style="font-size:1.1rem; font-weight:800; color:var(--c-text); margin-bottom:.5rem; letter-spacing:-.025em;">Need help securing your business?</h3>
          <p style="font-size:.875rem; color:var(--c-text-soft); margin-bottom:1.25rem;">Orion's Guard provides expert cybersecurity consulting built for small and mid-size businesses.</p>
          <a href="/contact/" class="og-btn og-btn-primary" style="font-size:.85rem; padding:.6rem 1.5rem;">Book a Free Discovery Call</a>
        </div>
      </article>

      <aside class="og-post-sidebar">
        <div style="background:var(--c-bg-card); border:1px solid var(--c-border); border-radius:var(--radius-lg); padding:1.5rem; position:sticky; top:84px;">
          <h3 style="font-size:.75rem; font-weight:700; letter-spacing:.07em; text-transform:uppercase; color:var(--c-text-dim); margin-bottom:1rem;">About Orion\'s Guard</h3>
          <p style="font-size:.82rem; color:var(--c-text-soft); line-height:1.7; margin-bottom:1.25rem;">Cybersecurity consulting for small and mid-size businesses — practical, budget-friendly, and built to scale with you.</p>
          <a href="/contact/" class="og-btn og-btn-primary" style="font-size:.8rem; padding:.55rem 1.2rem; width:100%; justify-content:center;">Free Discovery Call</a>
          <div style="margin-top:1.5rem; padding-top:1.25rem; border-top:1px solid var(--c-border);">
            <h3 style="font-size:.75rem; font-weight:700; letter-spacing:.07em; text-transform:uppercase; color:var(--c-text-dim); margin-bottom:.75rem;">Services</h3>
            <ul style="list-style:none; display:flex; flex-direction:column; gap:.4rem;">
              {["Compliance Consulting","vCISO Services","Risk Assessments","Security Training","Incident Response"].map(s => (
                <li><a href="/services/" style="font-size:.82rem; color:var(--c-text-soft); text-decoration:none; display:flex; align-items:center; gap:.4rem;"><span style="color:var(--c-cyan);">›</span> {s}</a></li>
              ))}
            </ul>
          </div>
        </div>
      </aside>
    </div>
  </div>
</Layout>

<style>
.og-post-hero-meta { display:flex; align-items:center; gap:.75rem; flex-wrap:wrap; margin-bottom:1rem; font-size:.8rem; color:var(--c-text-dim); }
.og-post-layout { display:grid; grid-template-columns:1fr 300px; gap:3rem; align-items:start; }
@media(max-width:900px) { .og-post-layout { grid-template-columns:1fr; } .og-post-sidebar { display:none; } }
</style>
""")

# ── src/pages/blog/index.astro ───────────────────────────────
# Fix: strip .md from post.id for clean URLs
w("src/pages/blog/index.astro", """\
---
import Layout from '../../layouts/Layout.astro';
import { getCollection } from 'astro:content';

function slugify(id: string) { return id.replace(/\\.mdx?$/, ''); }

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
                <a href={`/blog/${slugify(post.id)}/`}>{post.data.title}</a>
              </h2>
              {post.data.description && (
                <p class="og-post-card-desc">{post.data.description}</p>
              )}
              <a href={`/blog/${slugify(post.id)}/`} class="og-post-card-link">Read more</a>
            </div>
          </article>
        ))}
      </div>
    )}
  </div>
</Layout>

<style>
.og-post-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(320px,1fr)); gap:1.5rem; }
.og-post-card { background:var(--c-bg-card); border:1px solid var(--c-border); border-radius:var(--radius-lg); overflow:hidden; transition:border-color var(--t),transform var(--t),box-shadow var(--t); display:flex; flex-direction:column; }
.og-post-card:hover { border-color:var(--c-blue-mid); transform:translateY(-3px); box-shadow:0 8px 32px rgba(37,99,235,.1); }
.og-post-card-body { padding:1.75rem; display:flex; flex-direction:column; gap:.75rem; flex:1; }
.og-post-meta { display:flex; align-items:center; gap:.75rem; font-size:.75rem; color:var(--c-text-dim); }
.og-post-tag { background:rgba(37,99,235,.1); color:var(--c-blue-light); border-radius:999px; padding:.15rem .65rem; font-weight:600; font-size:.7rem; letter-spacing:.04em; text-transform:uppercase; }
.og-post-card-title { font-size:1.05rem; font-weight:700; line-height:1.35; letter-spacing:-.02em; flex:1; }
.og-post-card-title a { color:var(--c-text); text-decoration:none; }
.og-post-card-title a:hover { color:var(--c-blue-light); }
.og-post-card-desc { font-size:.85rem; color:var(--c-text-soft); line-height:1.6; display:-webkit-box; -webkit-line-clamp:3; -webkit-box-orient:vertical; overflow:hidden; }
.og-post-card-link { font-size:.8rem; font-weight:700; letter-spacing:.05em; text-transform:uppercase; color:var(--c-blue-light); text-decoration:none; margin-top:auto; }
</style>
""")

# ── src/pages/search.astro ───────────────────────────────────
# Fix: strip .md from post.id for clean URLs
w("src/pages/search.astro", """\
---
import Layout from '../layouts/Layout.astro';
import { getCollection } from 'astro:content';

function slugify(id: string) { return id.replace(/\\.mdx?$/, ''); }

const posts = (await getCollection('blog', ({ data }) => !data.draft))
  .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());

const postsJson = JSON.stringify(posts.map(p => ({
  id: slugify(p.id),
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
      <input id="og-search-input" type="search" placeholder="Search posts..." aria-label="Search blog posts" autofocus />
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

function renderPosts(matches) {
  results.innerHTML = matches.map(p => `
    <article class="og-post-card">
      <div class="og-post-card-body">
        <div class="og-post-meta">
          <time datetime="${p.date}">${formatDate(p.date)}</time>
          ${p.tags[0] ? `<span class="og-post-tag">${p.tags[0]}</span>` : ''}
        </div>
        <h2 class="og-post-card-title"><a href="/blog/${p.id}/">${p.title}</a></h2>
        ${p.description ? `<p class="og-post-card-desc">${p.description}</p>` : ''}
        <a href="/blog/${p.id}/" class="og-post-card-link">Read more</a>
      </div>
    </article>
  `).join('');
  countEl.textContent = matches.length === POSTS.length
    ? `Showing all ${POSTS.length} posts`
    : `${matches.length} result${matches.length !== 1 ? 's' : ''}`;
  noResults.hidden = matches.length > 0;
}

function search(q) {
  if (!q.trim()) return renderPosts(POSTS);
  const terms = q.toLowerCase().split(/\\s+/);
  renderPosts(POSTS.filter(p => {
    const hay = [p.title, p.description, ...p.tags].join(' ').toLowerCase();
    return terms.every(t => hay.includes(t));
  }));
}

renderPosts(POSTS);
input.addEventListener('input', e => search(e.target.value));
</script>

<style>
.og-search-bar { display:flex; align-items:center; gap:.75rem; background:var(--c-bg-card); border:1px solid var(--c-border); border-radius:var(--radius-lg); padding:.75rem 1.25rem; margin-bottom:1.25rem; }
.og-search-bar input { flex:1; background:transparent; border:none; outline:none; color:var(--c-text); font-size:1rem; font-family:inherit; }
.og-search-bar input::placeholder { color:var(--c-text-dim); }
.og-post-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:1.25rem; }
.og-post-card { background:var(--c-bg-card); border:1px solid var(--c-border); border-radius:var(--radius-lg); overflow:hidden; transition:border-color var(--t),transform var(--t); }
.og-post-card:hover { border-color:var(--c-blue-mid); transform:translateY(-2px); }
.og-post-card-body { padding:1.5rem; display:flex; flex-direction:column; gap:.6rem; }
.og-post-meta { display:flex; align-items:center; gap:.6rem; font-size:.75rem; color:var(--c-text-dim); }
.og-post-tag { background:rgba(37,99,235,.1); color:var(--c-blue-light); border-radius:999px; padding:.15rem .6rem; font-weight:600; font-size:.7rem; letter-spacing:.04em; text-transform:uppercase; }
.og-post-card-title { font-size:1rem; font-weight:700; line-height:1.35; }
.og-post-card-title a { color:var(--c-text); text-decoration:none; }
.og-post-card-title a:hover { color:var(--c-blue-light); }
.og-post-card-desc { font-size:.83rem; color:var(--c-text-soft); line-height:1.6; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }
.og-post-card-link { font-size:.78rem; font-weight:700; letter-spacing:.05em; text-transform:uppercase; color:var(--c-blue-light); }
</style>
""")

print()
print("  Step 3: Committing and pushing ...")
print()

for cmd in [
    ["git", "add", "-A"],
    ["git", "commit", "-m", "fix: strip .md from post.id, use [...slug].astro, clean URLs"],
    ["git", "push"],
]:
    print("  $", " ".join(cmd))
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.stdout.strip(): print("  ", r.stdout.strip())
    if r.returncode != 0:
        print("\n  ERROR:", r.stderr.strip())
        print("\n  Run manually: git add -A && git commit -m 'fix2' && git push")
        sys.exit(1)

print()
print("=" * 60)
print("  All fixes pushed. Cloudflare is rebuilding now.")
print("  dash.cloudflare.com -> Pages -> orionsguardsite")
print("=" * 60)
