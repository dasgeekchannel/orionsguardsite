#!/usr/bin/env python3
# fix4_orionsguard.py — uses Windows cmd rmdir to bypass OneDrive lock
import os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

def w(rel, content):
    path = os.path.join(ROOT, *rel.split("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  wrote:   {rel}")

def rm_dir(rel):
    path = os.path.join(ROOT, *rel.split("/"))
    if os.path.isdir(path):
        r = subprocess.run(["cmd", "/c", "rd", "/s", "/q", path], capture_output=True)
        if r.returncode == 0:
            print(f"  deleted dir:  {rel}")
        else:
            print(f"  WARN: could not delete {rel} — delete it manually in Explorer")
    else:
        print(f"  skip:    {rel} (already gone)")

def rm_file(rel):
    path = os.path.join(ROOT, *rel.split("/"))
    if os.path.isfile(path):
        os.remove(path)
        print(f"  deleted file: {rel}")
    else:
        print(f"  skip:    {rel} (already gone)")

print("=" * 60)
print("  Orion's Guard — Strip to Static Site (fix4)")
print("=" * 60)

print("\n  Step 1: Deleting blog / collection code ...")
rm_dir("src/pages/blog")
rm_dir("src/content")
rm_file("src/content.config.ts")
rm_file("src/pages/search.astro")
rm_file("src/pages/rss.xml.js")
rm_file("fix_orionsguard.py")
rm_file("fix2_orionsguard.py")
rm_file("fix3_orionsguard.py")

print("\n  Step 2: Writing clean static files ...")

w("astro.config.mjs", """\
import { defineConfig } from 'astro';
export default defineConfig({
  site: 'https://orionsguard.net',
});
""")

w("src/pages/index.astro", """\
---
const services = [
  { icon: "🛡️", title: "Compliance Consulting",       desc: "Navigate HIPAA, PCI-DSS, SOC 2, and CMMC with practical, cost-effective strategies built for SMBs." },
  { icon: "👤", title: "vCISO Services",               desc: "Enterprise-level security leadership on a fractional basis — strategic guidance without the full-time cost." },
  { icon: "🔍", title: "Risk Assessments",             desc: "Identify your biggest security gaps before attackers do. Actionable, prioritized remediation reports." },
  { icon: "📋", title: "Security Training",            desc: "Turn employees from your biggest vulnerability into your first line of defense with targeted training." },
  { icon: "🚨", title: "Incident Response",            desc: "When things go wrong, we move fast. Containment, investigation, and recovery — on call when you need us." },
  { icon: "📊", title: "Security Program Development", desc: "Build a mature security program from scratch — policies, controls, and procedures aligned to your goals." },
];
---
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Orion's Guard — Cybersecurity consulting built for small and mid-size businesses." />
  <title>Orion's Guard — Cybersecurity for SMBs</title>
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --blue: #2563eb; --cyan: #06b6d4;
      --dark: #0a0f1e; --card: #111827;
      --border: #1e2a3a; --text: #f0f4ff; --muted: #94a3b8;
      --r: 12px;
    }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--dark); color: var(--text); line-height: 1.6; }
    a { color: inherit; text-decoration: none; }

    /* NAV */
    nav { position: sticky; top: 0; z-index: 100; display: flex; align-items: center; justify-content: space-between; padding: 1rem 2rem; background: rgba(10,15,30,.88); backdrop-filter: blur(14px); border-bottom: 1px solid var(--border); }
    .brand { font-size: 1.15rem; font-weight: 800; letter-spacing: -.03em; background: linear-gradient(90deg,var(--blue),var(--cyan)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .nav-links { display: flex; gap: 2rem; font-size: .9rem; color: var(--muted); }
    .nav-links a:hover { color: var(--text); }
    .nav-cta { background: var(--blue); color: #fff; padding: .5rem 1.25rem; border-radius: 8px; font-size: .85rem; font-weight: 600; transition: background .2s; }
    .nav-cta:hover { background: #1d4ed8; }

    /* HERO */
    .hero { text-align: center; padding: 7rem 2rem 5rem; background: radial-gradient(ellipse 80% 50% at 50% 0%, rgba(37,99,235,.18) 0%, transparent 70%); }
    .badge { display: inline-block; background: rgba(37,99,235,.15); border: 1px solid rgba(37,99,235,.3); color: #93c5fd; font-size: .73rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; padding: .35rem 1rem; border-radius: 999px; margin-bottom: 1.5rem; }
    h1 { font-size: clamp(2.2rem,6vw,3.8rem); font-weight: 900; letter-spacing: -.04em; line-height: 1.1; margin-bottom: 1.25rem; }
    h1 span { background: linear-gradient(90deg,var(--blue),var(--cyan)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .hero p { font-size: clamp(1rem,2.5vw,1.15rem); color: var(--muted); max-width: 600px; margin: 0 auto 2.5rem; }
    .btns { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }
    .btn-p { background: var(--blue); color: #fff; padding: .75rem 2rem; border-radius: 10px; font-weight: 700; font-size: .95rem; transition: background .2s, transform .15s; }
    .btn-p:hover { background: #1d4ed8; transform: translateY(-2px); }
    .btn-s { border: 1px solid var(--border); padding: .75rem 2rem; border-radius: 10px; font-weight: 600; font-size: .95rem; transition: border-color .2s, transform .15s; }
    .btn-s:hover { border-color: var(--blue); transform: translateY(-2px); }

    /* SECTIONS */
    .section { padding: 5rem 2rem; max-width: 1100px; margin: 0 auto; }
    .label { font-size: .73rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: #60a5fa; margin-bottom: .65rem; }
    h2 { font-size: clamp(1.6rem,4vw,2.3rem); font-weight: 800; letter-spacing: -.03em; margin-bottom: .9rem; }
    .sub { color: var(--muted); max-width: 580px; margin-bottom: 2.75rem; }

    /* SERVICES GRID */
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.25rem; }
    .card { background: var(--card); border: 1px solid var(--border); border-radius: var(--r); padding: 1.75rem; transition: border-color .2s, transform .2s, box-shadow .2s; }
    .card:hover { border-color: var(--blue); transform: translateY(-3px); box-shadow: 0 8px 32px rgba(37,99,235,.12); }
    .card-icon { font-size: 2rem; margin-bottom: .9rem; }
    .card-title { font-size: 1.05rem; font-weight: 700; margin-bottom: .45rem; }
    .card-desc { font-size: .875rem; color: var(--muted); line-height: 1.65; }

    /* WHY */
    .why-wrap { background: rgba(17,24,39,.6); padding: 5rem 2rem; }
    .why-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 1.25rem; max-width: 1100px; margin: 0 auto; }
    .why-card { text-align: center; padding: 2rem 1.25rem; background: var(--card); border: 1px solid var(--border); border-radius: var(--r); }
    .why-num { font-size: 2.2rem; font-weight: 900; background: linear-gradient(90deg,var(--blue),var(--cyan)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: .4rem; }
    .why-lbl { font-size: .85rem; color: var(--muted); }

    /* CTA */
    .cta { background: linear-gradient(135deg,rgba(37,99,235,.14),rgba(6,182,212,.07)); border: 1px solid rgba(37,99,235,.25); border-radius: 16px; padding: 4rem 2rem; text-align: center; max-width: 860px; margin: 5rem auto; }
    .cta h2 { font-size: clamp(1.4rem,3vw,2rem); margin-bottom: .65rem; }
    .cta p { color: var(--muted); margin-bottom: 2rem; }

    /* FOOTER */
    footer { border-top: 1px solid var(--border); padding: 2.25rem 2rem; text-align: center; color: var(--muted); font-size: .85rem; }
    footer strong { background: linear-gradient(90deg,var(--blue),var(--cyan)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

    @media(max-width:600px) { .nav-links { display: none; } .hero { padding: 5rem 1.25rem 3rem; } .section { padding: 3.5rem 1.25rem; } }
  </style>
</head>
<body>

<nav>
  <span class="brand">Orion's Guard</span>
  <div class="nav-links">
    <a href="#services">Services</a>
    <a href="#why">Why Us</a>
  </div>
  <a href="mailto:contact@orionsguard.net" class="nav-cta">Get in Touch</a>
</nav>

<div class="hero">
  <div class="badge">Cybersecurity for SMBs</div>
  <h1>Security that fits<br /><span>your business</span></h1>
  <p>Orion's Guard delivers enterprise-grade cybersecurity consulting built specifically for small and mid-size businesses — practical, budget-conscious, and built to scale.</p>
  <div class="btns">
    <a href="mailto:contact@orionsguard.net" class="btn-p">Book a Free Discovery Call</a>
    <a href="#services" class="btn-s">Our Services</a>
  </div>
</div>

<div class="section" id="services">
  <p class="label">What We Do</p>
  <h2>Comprehensive security without<br />the enterprise price tag</h2>
  <p class="sub">From compliance to incident response, we cover the full security lifecycle so you can focus on running your business.</p>
  <div class="grid">
    {services.map(s => (
      <div class="card">
        <div class="card-icon">{s.icon}</div>
        <div class="card-title">{s.title}</div>
        <div class="card-desc">{s.desc}</div>
      </div>
    ))}
  </div>
</div>

<div class="why-wrap" id="why">
  <div style="max-width:1100px; margin:0 auto;">
    <p class="label">Why Orion's Guard</p>
    <h2>Built for businesses like yours</h2>
    <p class="sub">Same threats as enterprises. Fraction of the budget. We get it — and we build around it.</p>
  </div>
  <div class="why-grid">
    <div class="why-card"><div class="why-num">SMB</div><div class="why-lbl">Focused exclusively on small &amp; mid-size businesses</div></div>
    <div class="why-card"><div class="why-num">Flat</div><div class="why-lbl">Transparent flat-rate pricing — no surprise invoices</div></div>
    <div class="why-card"><div class="why-num">Fast</div><div class="why-lbl">Security improvements in days, not months</div></div>
    <div class="why-card"><div class="why-num">Real</div><div class="why-lbl">Practical advice you can actually implement</div></div>
  </div>
</div>

<div class="cta">
  <h2>Ready to secure your business?</h2>
  <p>Start with a free 30-minute discovery call — no obligation, no jargon.</p>
  <a href="mailto:contact@orionsguard.net" class="btn-p">Book Your Free Call →</a>
</div>

<footer>
  <p>&copy; {new Date().getFullYear()} <strong>Orion's Guard</strong>. All rights reserved.</p>
  <p style="margin-top:.4rem;"><a href="mailto:contact@orionsguard.net" style="color:#60a5fa;">contact@orionsguard.net</a></p>
</footer>

</body>
</html>
""")

print("\n  Step 3: Committing and pushing ...")
for cmd in [
    ["git", "add", "-A"],
    ["git", "commit", "-m", "simplify: static services page, no blog or collections"],
    ["git", "push"],
]:
    print("  $", " ".join(cmd))
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.stdout.strip(): print("  ", r.stdout.strip())
    if r.returncode != 0:
        print("\n  ERROR:", r.stderr.strip())
        print("  Run manually: git add -A && git commit -m 'simplify' && git push")
        sys.exit(1)

print()
print("=" * 60)
print("  Done! Cloudflare is rebuilding now.")
print("  dash.cloudflare.com -> Pages -> orionsguardsite")
print("=" * 60)
