#!/usr/bin/env python3
"""
Static site generator for Maxine Zhou's portfolio.

Everything lives in CONTENT below. Run `python3 build.py` to regenerate
the HTML files. The output is plain static HTML — no runtime dependencies.
"""

import html
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = ROOT  # HTML is written alongside assets/ so the folder deploys as-is

EMAIL = "maxinezhou0302@outlook.com"
LINKEDIN = "https://www.linkedin.com/in/maxine-z-90281422b/"
RESUME = "assets/doc/maxine-zhou-resume.pdf"
SITE_NAME = "Maxine Zhou"
SITE_TAGLINE = "Product Designer"
# Set this once you point a domain at the site (used for canonical + social tags).
BASE_URL = ""

try:
    DIMS = json.load(open(os.path.join(ROOT, "_dims.json")))
except Exception:
    DIMS = {}


# ---------------------------------------------------------------- helpers

def e(t):
    return html.escape(str(t), quote=False)


def rich(t):
    """**bold** -> <strong>, and escape everything else."""
    t = e(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return t


def img_tag(src, alt, cls="", lazy=True, sizes=None):
    d = DIMS.get(src)
    dim = f' width="{d[0]}" height="{d[1]}"' if d else ""
    c = f' class="{cls}"' if cls else ""
    ld = ' loading="lazy" decoding="async"' if lazy else ' decoding="async"'
    sz = f' sizes="{sizes}"' if sizes else ""
    return f'<img src="{{ROOT}}assets/img/{src}" alt="{e(alt)}"{dim}{c}{ld}{sz}>'


# ---------------------------------------------------------------- blocks

def render(blocks):
    out = []
    for b in blocks:
        k = b[0]

        if k == "h2":
            out.append(f"<h2>{rich(b[1])}</h2>")
        elif k == "h3":
            out.append(f"<h3>{rich(b[1])}</h3>")
        elif k == "p":
            out.append(f"<p>{rich(b[1])}</p>")
        elif k == "eyebrow":
            out.append(f'<span class="eyebrow">{e(b[1])}</span>')

        elif k == "ul":
            items = "".join(f"<li>{rich(i)}</li>" for i in b[1])
            out.append(f"<ul>{items}</ul>")

        elif k == "insights":
            items = "".join(f"<li>{rich(i)}</li>" for i in b[1])
            out.append(f'<ol class="insights">{items}</ol>')

        elif k == "questions":
            items = "".join(f"<li>{rich(i)}</li>" for i in b[1])
            out.append(f'<ul class="questions">{items}</ul>')

        elif k == "stats":
            cls = "stats stats-3" if len(b[1]) == 3 else "stats"
            cards = "".join(
                f'<div class="stat"><span class="n">{e(n)}</span>'
                f'<span class="l">{rich(l)}</span></div>'
                for n, l in b[1]
            )
            out.append(f'<div class="{cls}">{cards}</div>')

        elif k == "pull":
            out.append(f'<p class="pull">{rich(b[1])}</p>')

        elif k == "callout":
            inner = render(b[1])
            out.append(f'<div class="callout">{inner}</div>')

        elif k == "h4":
            out.append(f"<h4>{rich(b[1])}</h4>")

        elif k == "fig":
            src, alt = b[1], b[2]
            cap = b[3] if len(b) > 3 else ""
            wide = " wide" if (len(b) > 4 and b[4]) else ""
            fc = f"<figcaption>{rich(cap)}</figcaption>" if cap else ""
            out.append(f'<figure class="reveal{wide}">{img_tag(src, alt)}{fc}</figure>')

        elif k == "figpair":
            figs = "".join(
                f'<figure>{img_tag(s, a)}'
                + (f"<figcaption>{rich(c)}</figcaption>" if c else "")
                + "</figure>"
                for s, a, c in b[1]
            )
            out.append(f'<div class="fig-pair reveal">{figs}</div>')

        elif k == "sequence":
            imgs = "".join(img_tag(s, a) for s, a in b[1])
            out.append(f'<div class="sequence reveal">{imgs}</div>')

        elif k == "video":
            src, cap = b[1], (b[2] if len(b) > 2 else "")
            poster = f' poster="{{ROOT}}assets/img/{b[3]}"' if len(b) > 3 and b[3] else ""
            fc = f"<figcaption>{rich(cap)}</figcaption>" if cap else ""
            out.append(
                f'<figure class="video-block reveal">'
                f'<video controls playsinline preload="metadata"{poster}>'
                f'<source src="{{ROOT}}assets/video/{src}" type="video/mp4">'
                f"</video>{fc}</figure>"
            )

        elif k == "block":
            out.append(f'<div class="block reveal">{render(b[1])}</div>')

        elif k == "raw":
            out.append(b[1])

    return "\n".join(out)


# ---------------------------------------------------------------- chrome

def nav(active, depth):
    r = "../" * depth
    def item(href, label, key, cls=""):
        cur = ' aria-current="page"' if key == active else ""
        c = f' class="{cls}"' if cls else ""
        return f'<a href="{r}{href}"{cur}{c}>{label}</a>'
    return (
        f'<nav class="nav" aria-label="Primary">'
        + item("index.html", "Home", "home")
        + item("about.html", "About", "about")
        + f'<a class="nav-resume" href="{r}{RESUME}" target="_blank" rel="noopener">Résumé</a>'
        + f'<a class="nav-cta" href="mailto:{EMAIL}">'
          '<span class="cta-long">Get in touch</span>'
          '<span class="cta-short">Email</span></a>'
        + "</nav>"
    )


def header(active, depth):
    r = "../" * depth
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{r}index.html">Maxine Zhou <span>· {SITE_TAGLINE}</span></a>
    {nav(active, depth)}
  </div>
</header>"""


def contact_block():
    return f"""<section class="contact" id="contact">
  <div class="wrap">
    <h2>Feeling that I might be a good fit for your team?</h2>
    <p>I'm open to product design roles. The fastest way to reach me is email — I reply to everything.</p>
    <div class="contact-actions">
      <a class="btn btn-primary" href="mailto:{EMAIL}">{EMAIL}</a>
      <a class="btn btn-ghost" href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>
    </div>
  </div>
</section>"""


def footer(depth):
    r = "../" * depth
    return f"""<footer class="site-footer">
  <div class="wrap">
    <p>© <span id="yr">2026</span> Maxine Zhou</p>
    <div class="footer-links">
      <a href="{r}index.html">Home</a>
      <a href="{r}about.html">About</a>
      <a href="{r}{RESUME}" target="_blank" rel="noopener">Résumé</a>
      <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>
    </div>
  </div>
</footer>"""


SCRIPT = """<script>
document.getElementById('yr').textContent = new Date().getFullYear();

// header hairline on scroll
var hd = document.querySelector('.site-header');
var onScroll = function () { hd.classList.toggle('is-stuck', window.scrollY > 8); };
onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

// reveal on scroll
var els = document.querySelectorAll('.reveal');
if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) {
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
  els.forEach(function (el) { io.observe(el); });
} else {
  els.forEach(function (el) { el.classList.add('in'); });
}
</script>"""


def page(path, title, desc, body, active, og_image=None):
    depth = path.count("/")
    r = "../" * depth
    canon = ""
    social = ""
    if BASE_URL:
        canon = f'\n  <link rel="canonical" href="{BASE_URL.rstrip("/")}/{path}">'
        img = f'{BASE_URL.rstrip("/")}/assets/img/{og_image}' if og_image else ""
        social = f"""
  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:url" content="{BASE_URL.rstrip('/')}/{path}">""" + (
            f'\n  <meta property="og:image" content="{img}">'
            '\n  <meta name="twitter:card" content="summary_large_image">' if img else ""
        )

    doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <meta name="author" content="Maxine Zhou">{canon}{social}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Almarai:wght@300;400;700&family=Instrument+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{r}assets/css/site.css">
  <link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  {header(active, depth)}
  <main id="main">
{body}
  </main>
  {contact_block()}
  {footer(depth)}
  {SCRIPT}
</body>
</html>
"""
    doc = doc.replace("{ROOT}", r)
    dest = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(doc)
    return path


# ================================================================
#  CONTENT
# ================================================================

IMG = {
    "wordmark":   "429fa4_33206579b4314f0c8205fe0188b5f3da.jpg",
    "arrow":      "429fa4_33b207bf0d8141c5b79aa3db24d19aed.jpg",
    "cats":       "429fa4_1823bdbaa64c46d8a626dbf4df7914f6.jpg",
    "dog":        "429fa4_e1706cc995cb4d259b6b57c2ad78d6c6.jpg",
    "lp_thumb":   "429fa4_0d9f52c9c8ee4bfc9e760625d05b46ca.jpg",
    "dsm_thumb":  "429fa4_c787f95cc16145b388e883d72cc01bdc.jpg",
    "an_thumb":   "429fa4_9143c074f1eb4336aa0019bf7484727a.jpg",
}

TEAM_TESTIMONIAL_1 = "429fa4_d495b40fa1f24fb8846e89c99ecf3113.jpg"
TEAM_TESTIMONIAL_2 = "429fa4_11e39adffb844cdaa0853b35d76be090.jpg"

PROJECTS = []

# Slugs that have been migrated to v2 and are now generated by casestudy.py
# from content/<slug>.py. They stay in PROJECTS so the work index can still
# link and describe them, but build.py must NOT write their page — both
# generators target the same work/<slug>.html, and whichever ran last wins.
# Running build.py used to silently overwrite the v2 design system migration
# page with the cream one. Add a slug here the moment its content file exists.
MIGRATED = {"design-system-migration"}


def P(**kw):
    PROJECTS.append(kw)
    return kw


# ---------------------------------------------------------------- 1. Launchpad
P(
    slug="underwriting-efficiency",
    featured=True,
    title="Improving Underwriting Efficiency Through Behaviour-Driven Design",
    sub="Turning user data into a smarter navigation model and a dynamic viewport, to give underwriters a better decision environment.",
    tags=["B2B SaaS", "UX/UI", "Workflow", "InsurTech"],
    thumb="429fa4_a3c6ed0d39d248f0980b00bc153ab122.jpg",
    cover="429fa4_a3c6ed0d39d248f0980b00bc153ab122.jpg",
    overview=[
        ("My Role", [("p", "Product Designer (Sole Designer)")]),
        ("Responsibilities", [("ul", [
            "Next version of this product",
            "UX analysis & insight synthesis",
            "Interaction design",
            "Information architecture",
            "Stakeholder alignment",
        ])]),
        ("The Product", [("p", "An internal underwriting application for insurance teams to review and triage submissions, manage workflows, and make faster, more confident decisions.")]),
    ],
    body=[
        ("block", [
            ("h2", "Usage at a glance"),
            ("p", "In a typical month:"),
            ("stats", [
                ("2,720", "Review sessions"),
                ("224h", "Total time spent in active usage"),
                ("26 mins", "Average session length"),
                ("18", "Teams actively using"),
            ]),
        ]),
        ("block", [
            ("h2", "Background & Context"),
            ("p", "Underwriters work in a high-volume, high-stakes environment where speed and accuracy are essential. The application's workflow centred around two primary pages."),
            ("ul", [
                "**Pipeline View** — a table-based workspace for filtering, triaging, and updating submissions",
                "**Submission Detail** — a deep-dive view containing full submission context, documents, analysis, and activity history",
            ]),
            ("figpair", [
                ("429fa4_4e748c80fe2f43b29017c32d9d3b0fa5.jpg", "Pipeline View page — a dense table of submissions with filters", "Pipeline View page"),
                ("429fa4_d416b84ddeca45fc8e1cf939f55f68a8.jpg", "Submission Detail page showing full submission context", "Submission Detail page (deeper dive)"),
            ]),
        ]),
        ("block", [
            ("h2", "Start at UX audit"),
            ("p", "As the sole product designer brought in to shape the next version of this product, I began with a structured UX audit to identify improvement opportunities."),
            ("fig", "429fa4_a8c14759cdd74c84822e9e887ffc0a65.jpg", "Annotated UX audit of the submission detail screen", "Annotating friction points directly on the existing screens.", True),
            ("fig", "429fa4_cb15cf892bcf444488324e341f870dbc.jpg", "Audit findings organised as clustered notes", "Findings clustered into themes before moving into analysis.", True),
        ]),
        ("block", [
            ("h2", "Understanding real usage"),
            ("p", "Following the UX audit, I analysed funnel behaviour, heat maps, feature usage and session data to understand how underwriters actually worked."),
            ("questions", [
                "Where does decision-making actually happen?",
                "What information do users need during triage?",
                "How can the interface better support comparison across submissions?",
                "Are users navigating efficiently, or compensating for missing context?",
            ]),
            ("fig", "429fa4_184c0642d417480f8554f3bb6d79b93e.jpg", "Funnel chart showing session drop-off between pipeline and submission detail", "Funnel analysis across 7.09K sessions.", True),
            ("h3", "What the data revealed"),
            ("insights", [
                "Only **46.1%** of users entered the submission detail page",
                "The **Back button** was the most-used interaction on submission detail",
                "Users frequently **looped** between pipeline and submission detail",
                "Submission detail was used selectively to access specific context — especially **summaries and notes**",
            ]),
        ]),
        ("block", [
            ("h2", "Why the Back button dominance?"),
            ("pull", "Fast comprehension first, depth on demand."),
            ("p", "The pipeline view functioned as the **true decision workspace**, while the submission detail page acted as a short-term inspection layer."),
            ("p", "Underwriters relied on the pipeline page for orientation and comparison, opening submission detail primarily to verify context before returning to continue their review."),
        ]),
        ("block", [
            ("h2", "Design Direction"),
            ("p", "I proposed a design direction that improved the workflow and resolved the key UX friction points:"),
            ("insights", [
                "Rebalanced information hierarchy to surface key signals closer to the pipeline",
                "Cut navigation overhead with pre-filtered views and a 'filters-on-demand' system",
                "Introduced a contextual Details drawer for files, AI insights, activity history, and notes",
                "Implemented an adaptive viewport to support dense data analysis without losing workflow context",
            ]),
            ("fig", "429fa4_d350c620e78b43f4a027b3db0547d249.jpg", "Set of redesigned screens showing the new navigation model", "", True),
        ]),
        ("block", [
            ("h2", "Reducing noise, preserving control"),
            ("p", "I designed a 'filters-on-demand' system that reduced visual complexity while maintaining flexibility. Frequently used filters were prioritised, and reusable filter presets allowed underwriters to quickly re-establish context across sessions."),
            ("video", "cfb9e35608894b62bc457c5b936113f4.mp4", "Filters-on-demand: surfacing only what's needed, when it's needed."),
            ("p", "I proposed consolidating key submission information into a contextual drawer accessible directly from the pipeline page."),
            ("figpair", [
                ("429fa4_4f40ed3f0a4745f4a929bc6de4a8be90.jpg", "Contextual details drawer next to the pipeline table", "Details drawer, opened in place"),
                ("429fa4_432aec980fe34d0f93ebe53e54d5312e.jpg", "Activities hub listing submission tasks and their status", "Activities hub inside the drawer"),
            ]),
            ("video", "bfde2b80ca304fe59b2d908c0ab34c1a.mp4", "The contextual Details drawer in use — context without leaving the workspace."),
        ]),
        ("block", [
            ("h2", "Adaptive viewport for high-density data"),
            ("p", "To accommodate high-density data, I designed an adaptive viewport that supports uninterrupted data analysis while preserving quick access to workflow context and collaboration tools."),
            ("video", "6f86bae969f04d0595f535c881e67525.mp4", "The viewport adapting as the underwriter moves between comparison and detail."),
        ]),
        ("block", [
            ("h2", "Impact"),
            ("p", "With over **224 hours of monthly usage**, even small improvements could scale quickly. Reducing just one minute per session could save over **45 hours per month** across underwriting teams."),
            ("p", "Due to roadmap priorities, this work was positioned as a future optimisation — establishing a clear, data-backed direction for improving underwriting efficiency at scale."),
        ]),
    ],
)


# ---------------------------------------------------------------- 2. Design system migration
P(
    slug="design-system-migration",
    featured=True,
    title="Enterprise Design System Migration Challenge",
    sub="Led design system migration across a 16-product insurance ecosystem, cutting custom components by 94% and establishing governance across three design agencies.",
    tags=["Design System", "Design Ops", "Strategy", "InsurTech"],
    thumb="429fa4_d9606ddbf3a445d2b3b2e8975b3fcf70.jpg",
    cover="429fa4_d9606ddbf3a445d2b3b2e8975b3fcf70.jpg",
    overview=[
        ("Our Design Team", [("p", "Design System Designer (me)"), ("p", "+ Design Manager")]),
        ("Timeline", [("p", "March – December 2025"), ("p", "(10 months)")]),
        ("My Core Deliverables", [("ul", [
            "Four products migrated, with three in active progress",
            "Design library fully built, aligned with Storybook",
            "Documentation and governance frameworks established",
            "Design team culture transformed from siloed to collaborative",
            "Client set up to scale the system independently after the engagement ended",
        ])]),
    ],
    body=[
        ("block", [
            ("h2", "Impact"),
            ("stats", [
                ("49", "components with full tokenisation and documentation"),
                ("35% → 2%", "reduction in custom components (core product pilot)"),
                ("10", "designers across three agencies aligned and collaborative"),
                ("7", "products migrated or in progress within the engagement"),
            ]),
            ("fig", "429fa4_1c3a8c2e3fb5442bb06d134f647be1cf.jpg", "Overview of the design library components", "The design library, covering the full product ecosystem.", True),
        ]),
        ("block", [
            ("h2", "The Challenge"),
            ("p", "The client operated **16+ products** built by multiple contractors, with significant operational challenges:"),
            ("ul", [
                "**83%** of design work required custom components, due to limitations of the existing design system",
                "Three separate design agencies worked in **silos** with inconsistent practices",
                "Designers skipped collaboration meetings and worked independently",
                "**Fragmented user experiences** across the product portfolio",
                "**No clear governance** on when or how to extend the design system",
            ]),
            ("h3", "What my role brought"),
            ("ul", [
                "Build and organise the design library and documentation",
                "Provide design system services and support to designers across agencies",
                "Establish governance processes for consistent adoption",
                "Lead pilot migration to demonstrate value and approach",
                "Transform team culture from siloed to collaborative",
            ]),
            ("figpair", [
                ("429fa4_b5944372986c431380a22c98f4eb852d.jpg", "Product screen before migration", "Before"),
                ("429fa4_4d33c3c898b64582bb5f1bfa7c316c82.jpg", "Product screen after migration to the design system", "After"),
            ]),
        ]),
        ("block", [
            ("eyebrow", "Phase 1"),
            ("h2", "Foundation Building"),
            ("insights", [
                "Built the **Design Library** covering the full product ecosystem",
                "Tokenised design foundations and wrote **component documentation**",
                "Established the cleaned-up version of **Storybook** as the single source of truth",
                "Provided designer **support infrastructure** across all three agencies",
            ]),
            ("fig", "429fa4_4c84c1ebba764d67ab0bf38773e36072.jpg", "The assembled design library shown across product surfaces", "", True),
            ("fig", "429fa4_934a006033b14597a7937e6084584944.jpg", "Slack announcement of the DS 2.0 Figma library release", "Shipping library updates with release notes, so designers were never surprised by a change."),
        ]),
        ("block", [
            ("eyebrow", "Phase 2"),
            ("h2", "Governance & Quality Assurance"),
            ("insights", [
                "Conducted **UX audits** and regular design check-ins across agencies to identify drift",
                "Documented an **Exception Framework** for when deviations make sense — balancing system integrity with design flexibility",
                "Created a 3–4 week component prioritisation pipeline",
                "Hosted **Pattern Workshops** across agencies to identify reusable patterns",
            ]),
            ("figpair", [
                ("429fa4_2aece0e687e544a0b895414de8f9772f.jpg", "UX Audit 2025 documents", "Recurring UX audits to catch drift early"),
                ("429fa4_d861706d33a4423b95920f6aa3351b15.jpg", "Contribution process flow diagram", "The contribution process, made explicit"),
            ]),
            ("fig", "429fa4_35d8c4aab5bb4b30a2c00b58c163b781.jpg", "Cards for design critique, workshops and office hours", "Support infrastructure: critiques, workshops, and a standing design system office hour."),
        ]),
        ("block", [
            ("h2", "The challenge I faced at Phase 2"),
            ("callout", [
                ("h4", "What happened"),
                ("p", "While reviewing some mockups, I noticed many components were heavily customised — spacing, padding, and text weights all differed from the design system."),
                ("h4", "The tension"),
                ("p", "Product designers wanted to preserve user familiarity. The design system manager questioned the purpose of migration if the visuals remained unchanged."),
                ("h4", "What I did to solve the underlying conflict"),
                ("ul", [
                    "**Clarified intent:** migration = technical adoption + gradual alignment, not forced visual conformity.",
                    "**Defined a path forward:** Phase 1 — design system components with overrides; Phase 2 — reassess after research and user acceptance testing.",
                    "**Process improvement:** proposed an Exception Framework to document justified divergences from the design system.",
                ]),
            ]),
            ("fig", "429fa4_81783366317148b9af57efeb531cf56d.jpg", "Message to the design team proposing the Exception Framework", "Taking the proposal to the whole team, in the open."),
        ]),
        ("block", [
            ("eyebrow", "Phase 3"),
            ("h2", "Strategic Migration"),
            ("p", "We ran a low-risk pilot on a simple product to validate the process and build team confidence. Then we migrated the essential product to showcase impact."),
            ("p", "During migration we fixed a number of UX issues, applied semantic tokens, and improved predictability with a unified visual language."),
            ("pull", "Result: 35% → 2% custom components."),
        ]),
        ("block", [
            ("eyebrow", "Phase 4"),
            ("h2", "Scaling & Enablement"),
            ("insights", [
                "Transformed siloed agencies into a collaborative community",
                "Completed four product migrations, with three in progress",
                "Client equipped to continue independently with established processes",
            ]),
            ("figpair", [
                ("429fa4_46c62b14bcb44e5d97ceb07d58778ec3.jpg", "Weekly design system update posted to the team channel", "Weekly updates kept adoption visible"),
                ("429fa4_d79c6c6e9b8d4d5ab853b40804eed1a6.jpg", "Agenda for the weekly design system meeting", "A standing agenda people actually turned up for"),
            ]),
            ("fig", "429fa4_dbe8db9a448b4e6e9d7e10cb47d11eb9.jpg", "Designer asking for guidance on the sorting pattern", "The real signal of success: designers coming to the system before building around it."),
        ]),
        ("block", [
            ("h2", "Impact for the business"),
            ("ul", [
                "Drastic reduction in design and handoff time as design system coverage increased",
                "Migration approach proven through a pilot that other teams can replicate",
                "The team now owns and evolves the design system together",
            ]),
        ]),
        ("block", [
            ("h2", "Reflection and learnings"),
            ("ul", [
                "Design system migration is as much about **people and process** as components. Building trust among design teams by providing support proactively is the key.",
                "I came to understand the importance of **change management**: balancing consistency with designers' needs.",
                "Stakeholder communication and systems thinking are essential.",
                "Finally, I learnt to **choose the battle**. We paused migration on one product with fewer than 10 active users — its designers were reluctant to migrate in the way we suggested, and it was time-consuming to re-onboard them at every design check-in.",
            ]),
        ]),
    ],
)


# ---------------------------------------------------------------- 3. Analyser
P(
    slug="contract-analysis",
    featured=True,
    title="AI-Augmented Contract Analysis Platform",
    sub="Designing trust into AI-powered contract analysis for high-pressure insurance workflows.",
    tags=["AI / ML", "B2B SaaS", "Workflow", "InsurTech"],
    thumb="429fa4_82c4d33150404b6da68fb9b32b4b621c.jpg",
    cover="429fa4_82c4d33150404b6da68fb9b32b4b621c.jpg",
    overview=[
        ("My Role", [("p", "Product Designer (Sole Designer)")]),
        ("Key Outcomes", [("ul", [
            "Streamlined contract review during critical renewal periods",
            "Designed continuous AI training into the workflow, in a way that felt natural to users",
            "Built user trust through transparent AI verification design",
        ])]),
        ("Additional Complexity", [("ul", [
            "Remote collaboration with a dev team in France",
            "Tech constraints: LLM latency, and the inability to build a specific layout",
            "Ecosystem consistency: aligned with two products and fed insights into a core product",
        ])]),
    ],
    body=[
        ("block", [
            ("h2", "The Problem"),
            ("h3", "Fragmented, high-stakes workflows"),
            ("p", "During busy renewal periods, underwriters analyse hundreds of reinsurance and insurance contracts under tight deadlines. Their workflow is chaotic — constantly switching between:"),
            ("ul", ["Contract PDFs", "Email chains", "Notes documents", "Slack conversations", "Dropbox files"]),
            ("h3", "We needed a solution that could"),
            ("ul", [
                "Make contract review instantaneous, not time-consuming",
                "Simplify checking against complex underwriting rules",
                "Reduce compliance risk and financial exposure",
            ]),
            ("pull", "How might we accelerate contract analysis without compromising thoroughness, accuracy, or user confidence in AI-generated insights?"),
        ]),
        ("block", [
            ("h2", "Research and Discovery"),
            ("p", "I conducted stakeholder interviews with underwriters and product managers to understand their workflows, pain points, and needs during high-pressure renewal periods."),
            ("h3", "Key insights that shaped the design"),
            ("insights", [
                "Navigation must be instantaneous and mirror the document's natural flow",
                "Users question AI accuracy — the design should communicate transparency and verifiable sources",
                "AI assistance should feel like productive work, not extra overhead",
            ]),
        ]),
        ("block", [
            ("h2", "Design Evolution"),
            ("p", "I went through three distinct layout approaches, testing each with PMs and users to land on the optimal information hierarchy that also fit within the dev team's technical constraints."),
            ("h3", "Early prototype"),
            ("p", "This is what the UI looked like when I first joined the project."),
            ("p", "#Christmas tree · #Unclear IA · #Long scroll · #Content gets lost"),
            ("fig", "429fa4_b94d91ef55624a489746c184b68237d0.jpg", "The early prototype: a long, undifferentiated scroll of panels", "", True),
            ("h3", "Explored modal-based details (users' favourite)"),
            ("ul", [
                "Rebalanced the information hierarchy across multiple layers of detail",
                "Consolidated all detailed information in a modal to minimise visual noise",
            ]),
            ("p", "*(Blocked by the dev team due to technical constraints.)*"),
            ("fig", "429fa4_28ca0372e92b48c6ba5f791d09296794.jpg", "Modal-based exploration showing detail consolidated in an overlay", "", True),
            ("h3", "Hybrid tabs + accordion (final)"),
            ("ul", [
                "Parent accordions organised by document section, mirroring contract order",
                "Enables side-by-side comparison with one click",
            ]),
            ("fig", "429fa4_cc4f426eab674f4c84ffce216bd7d4a2.jpg", "The final hybrid layout using tabs and nested accordions", "", True),
        ]),
        ("block", [
            ("h2", "AI-powered comparison with source verification"),
            ("p", "Detected wording is compared against preferred language in a clear side-by-side view with concise risk summaries, enabling decisions in seconds."),
            ("fig", "429fa4_494de1d72981497ba758dfab41fd38a5.jpg", "Side-by-side comparison of detected and preferred contract wording", "", True),
            ("video", "b0eeb3a05a8348c489f452e234899176.mp4", "Comparing detected wording against the preferred clause, with the source always one click away."),
        ]),
        ("block", [
            ("h2", "Human-in-the-loop machine training"),
            ("p", "Underwriters can quickly verify or relink AI-detected text within the “Text” view, embedding feedback directly into their normal review workflow. Each correction improves model accuracy over time, ensuring the system evolves with real user judgement."),
            ("fig", "429fa4_9c3a533b37524cd9860f17fcaf4a96a0.jpg", "Relinking flow when no content is detected for a clause", "", True),
            ("video", "b45e86d07663498fa82f1be4f1c46427.mp4", "Relinking a mis-detected clause — correction as a by-product of normal review."),
        ]),
        ("block", [
            ("h2", "Natural review workflow"),
            ("p", "Key validation actions are surfaced at the point of review, enabling one-step decisions and preserving underwriters' analytical flow."),
            ("video", "f927b3974a7b42eabdcdb7dc96754e09.mp4", "Validation actions where the decision actually happens."),
        ]),
        ("block", [
            ("h2", "Action list for faster collaboration"),
            ("p", "Instead of jumping between components to recall what needs discussion, underwriters get a consolidated view of every flagged item, suggested alternative, and comment at a glance. When everything checks out, a single 'Finish Validation' click closes the loop."),
            ("fig", "429fa4_2689de7cd4c0485b92114afb43ee54c7.jpg", "Consolidated action list with flagged clauses and comments", "", True),
        ]),
    ],
)


# ---------------------------------------------------------------- 4. ConvexAI (unlinked, as on the original site)
P(
    slug="workplace-ai-assistant",
    featured=False,
    listed=False,
    title="Building a Smarter, More Connected Workplace AI Assistant",
    sub="Transforming internal productivity through enterprise-grade security, personalisation, accessibility and deep tool integration.",
    tags=["AI / ML", "B2B SaaS", "Workflow", "InsurTech"],
    thumb="429fa4_a7cb45d325b64320bee32e057ae91d09.jpg",
    cover="429fa4_a7cb45d325b64320bee32e057ae91d09.jpg",
    overview=[
        ("My Role", [("p", "Product Designer")]),
        ("Focus", [("ul", [
            "Personalisation and knowledge retention",
            "Deep tool integration",
            "Enterprise-grade security",
            "Accessibility",
        ])]),
    ],
    body=[
        ("block", [
            ("h2", "Product Strategy"),
            ("p", "This product represents a significant step forward in our client's digital strategy. By combining personalisation, deep tool integration, and enterprise-grade security, it addresses the real-world needs of a modern insurance business — empowering employees to work faster, smarter, and with greater confidence in the tools they use."),
            ("fig", "429fa4_3503981c2367415894c44ef4ec84be21.jpg", "The workplace AI assistant interface", "", True),
        ]),
        ("block", [
            ("h2", "Retaining organisational knowledge"),
            ("p", "Users can easily revisit past interactions and build on previous work, with prior conversations grouped by time."),
            ("p", "This setup helps the organisation retain knowledge, cutting down on repeated questions and the need to reconstruct context."),
            ("video", "ce07853230c34022abc0e9a64dd4b755.mp4", "Returning to an earlier thread and picking the work back up."),
        ]),
        ("block", [
            ("h2", "Research and Discovery"),
            ("p", "I conducted stakeholder interviews with underwriters and product managers to understand their workflows, pain points, and needs during high-pressure renewal periods."),
            ("h3", "Key insights that shaped the design"),
            ("insights", [
                "Navigation must be instantaneous and mirror the document's natural flow",
                "Users question AI accuracy — the design should communicate transparency and verifiable sources",
                "AI assistance should feel like productive work, not extra overhead",
            ]),
        ]),
    ],
)


# ---------------------------------------------------------------- 5. JCD content hub
P(
    slug="content-hub-redesign",
    featured=False, earlier=True,
    title="Content Hub Redesign for a Global Outdoor Advertising Company",
    sub="Empowering diverse customer groups through a revolutionary content hub, tailored to deliver resources every day and inspire the creation of deals with our clients.",
    tags=["Marketing", "App Design", "Content Platform"],
    thumb="429fa4_d291a90d5f564735b1e964621fc2e2d5.jpg",
    cover="429fa4_d291a90d5f564735b1e964621fc2e2d5.jpg",
    meta="Dec 2023 · 2 weeks",
    overview=[
        ("The team", [("ul", ["Senior designer", "Junior designer (me)", "Product manager"])]),
        ("What I did", [("ul", ["UX audit", "Competitive analysis", "Prototyping"])]),
        ("Limitations", [("ul", ["Direct access to end users was unavailable", "No brand guidelines"])]),
        ("Timeline & tools", [("p", "2 weeks"), ("p", "Figma, Miro, hybrid workshops")]),
    ],
    body=[
        ("block", [
            ("h2", "The client"),
            ("p", "A global outdoor advertising company that wants to leverage a digital hub to attract and inspire experts to build their marketing cases."),
            ("p", "**Category:** marketing, self-contained platform  ·  **Service:** app design"),
        ]),
        ("block", [
            ("h2", "The Challenge"),
            ("pull", "Help the client redesign their content hub to attract more visitors, inspiring them to explore our client's services and build cases based on the content."),
            ("p", "To assist our clients in securing more deals, we were assigned the task of crafting an inclusive and intuitive user experience to elevate overall user engagement."),
        ]),
        ("block", [
            ("h2", "How their product looked before"),
            ("p", "While our client has great and insightful content, accessibility issues such as a lack of visual cues — and other UX concerns, like an unclear value proposition in the hero section — may lead users to feel confused during interactions with the product. It also isn't easy for them to stay engaged."),
            ("fig", "429fa4_4cf67b0fad6b4b059546dfdfea6bfa87.jpg", "The previous content hub interface", "", True),
            ("fig", "429fa4_9ffea35f9b754ab0b71df9ce33a77f8d.jpg", "Grid of existing content hub screens", "", True),
        ]),
        ("block", [
            ("h2", "UX Audit"),
            ("p", "We conducted a UX audit to address usability issues, heuristic problems, and pain points. Given the deadline and limited resources for additional user research, the audit gave us the fastest route to defensible problems."),
            ("fig", "429fa4_6c95e34db07a46408e2c08349ddb4382.jpg", "Annotated audit of the hero section", "", True),
            ("figpair", [
                ("429fa4_aba7bbae2551411bb3e9898cde932102.jpg", "Annotated audit of the podcast series section", ""),
                ("429fa4_0a54db9817c84d0b8d3008c6aa991df0.jpg", "Annotated audit of a content detail page", ""),
            ]),
            ("h3", "Problem identification"),
            ("p", "After synthesising our research findings, we identified three major UX problems on the previous content hub."),
            ("insights", [
                "**Unclear value proposition in the hero section.** Users lack a clear understanding of what the content hub offers and how it meets their needs, leading to a potentially high bounce rate.",
                "**Poor usability with unattractive content.** The absence of filtering and sorting features hinders users from locating their desired content. The product also lacks personalised content, further limiting the experience.",
                "**Lacking visual cues.** The client has genuinely desirable content, but without visual cues for interactive content — and for content hosting layers of information — users cannot tell what is explorable.",
            ]),
        ]),
        ("block", [
            ("h2", "Design explorations"),
            ("h3", "Interactive interests selection"),
            ("p", "To address reduced satisfaction when users select diverse content types during onboarding, we explored creating a simple and interactive onboarding process."),
            ("fig", "429fa4_13cdd90cda2c410b834d87d98259f9f7.jpg", "Three explorations of the interests-selection interaction", "", True),
            ("h3", "Podcast episode page"),
            ("p", "We held varying opinions on the podcast episode page UI. To decide, we ran a brief dot-voting process and chose the design that prioritised consistency."),
            ("fig", "429fa4_08ad98ee866e495ba6fead99e3be64e9.jpg", "Podcast episode page explorations shown side by side", "", True),
        ]),
        ("block", [
            ("h2", "Design solutions"),
            ("h3", "A dynamic and engaging user experience"),
            ("ul", [
                "Designed with mobile optimisation in mind",
                "Clear and compelling CTAs",
                "Personalised dashboard with interactive widgets",
            ]),
            ("fig", "429fa4_c0bd487eb8fd4c858285d345072cbafd.jpg", "Final mobile screens of the redesigned content hub", "", True),
            ("h3", "A captivating swipe-down animation"),
            ("p", "By transforming the podcasts page into an interactive and visually appealing hub, we anticipate an increase in user engagement, longer session durations, and higher retention."),
        ]),
        ("block", [
            ("h2", "The result"),
            ("pull", "After completing Immersion, we were re-engaged by the client to build the MVP."),
        ]),
    ],
)


# ---------------------------------------------------------------- 6. Rads redesign
P(
    slug="rads-redesign",
    featured=False, earlier=True,
    title="Radically Digital Website Redesign",
    sub="Rebuilding a consultancy's website so the UI finally matched the brand — and stopped getting in the way of the content.",
    tags=["Web", "Usability research", "Consultancy"],
    thumb="429fa4_e1c54e9e1f914ac2bbde7c42884bdc6e.jpg",
    cover="429fa4_e1c54e9e1f914ac2bbde7c42884bdc6e.jpg",
    meta="1 week",
    overview=[
        ("The team", [("p", "Senior designer"), ("p", "Junior designer (me)")]),
        ("What I did", [("ul", ["Usability research", "High-fidelity wireframes", "Prototype"])]),
        ("Timeline", [("p", "1 week")]),
        ("Constraints", [("ul", [
            "No access to Hotjar",
            "Icons and corner radius were not welcomed by business stakeholders",
        ])]),
    ],
    body=[
        ("block", [
            ("h2", "Problems & constraints"),
            ("p", "Radically Digital is a startup tech consultancy offering product design and development services in London. The website required an iteration, as the outdated UI did not represent the current branding and value."),
            ("p", "Additionally, there were usability issues preventing users from exploring content further. This could act as a gatekeeper, hindering their ability to reach more clients."),
        ]),
        ("block", [
            ("h2", "The redesign"),
            ("sequence", [
                ("429fa4_1a9489d6f825475fb1f62766efdfef6f.jpg", "Redesigned website screen"),
                ("429fa4_a3ef5be81c0141bab90171c6e5a51992.jpg", "Redesigned website screen"),
                ("429fa4_31303413984e4a3d9b637747de7d23ac.jpg", "Redesigned website screen"),
                ("429fa4_c44031234f214170a950fbce3d8cd511.jpg", "Redesigned website screen"),
            ]),
        ]),
    ],
)


# ---------------------------------------------------------------- 7. Diago
P(
    slug="diago",
    featured=False, earlier=True,
    title="Diago",
    sub="Increase hospital efficiency, cover more families, and provide daily physical condition monitoring as well.",
    tags=["Healthcare", "Wearables", "Individual project"],
    thumb="429fa4_acb480e3dd264b1ca7f73e44db294bb2.jpg",
    cover="429fa4_acb480e3dd264b1ca7f73e44db294bb2.jpg",
    meta="January 2020 · Individual project",
    overview=[
        ("Type", [("p", "Individual project")]),
        ("Time", [("p", "January 2020")]),
        ("Tools", [("p", "Sketch, Axure, Figma")]),
    ],
    body=[
        ("block", [
            ("h2", "Overview"),
            ("p", "A healthcare app with wearable devices for families in the US."),
            ("p", "Because of the pandemic, many drawbacks of the healthcare system in the US were exposed. The shortage of medical resources made getting treatment harder for patients, especially those without medical insurance. So I set out to relieve pressure on the US healthcare system and provide a better, quicker diagnosis experience for patients."),
        ]),
        ("block", [
            ("h2", "The work"),
            ("p", "*Note: the full functionality cannot be conveyed in this format, due to the failure of a previous MacBook.*"),
            ("sequence", [
                ("429fa4_89cdc6eb766a4343a36d1b8d53a456cd.jpg", "Diago project board"),
                ("429fa4_bc01d02df53c4a9b9cb948cf695cc273.jpg", "Diago project board"),
                ("429fa4_9bc0912c787f4ee58bacdef681e2ba7a.jpg", "Diago project board"),
                ("429fa4_94c973bcdcb045dbb8b14dc00b466b2b.jpg", "Diago project board"),
                ("429fa4_b365b43f890a49458bf564a3f16b57f2.jpg", "Diago project board"),
                ("429fa4_29cb2bcfc37d479dbf9435a31cc19566.jpg", "Diago project board"),
            ]),
        ]),
    ],
)


# ---------------------------------------------------------------- 8. Know-all
P(
    slug="know-all",
    featured=False, earlier=True,
    title="Know-all",
    sub="Enabling all residents to browse updated information easily, while encouraging older residents to participate in community activities more often.",
    tags=["Information kiosk", "Accessibility", "Individual project"],
    thumb="429fa4_76e8b680dbbc477c8833a8e4298bc2ab.jpg",
    cover="429fa4_76e8b680dbbc477c8833a8e4298bc2ab.jpg",
    meta="July 2020 · Individual project",
    overview=[
        ("Type", [("p", "Individual project")]),
        ("Time", [("p", "July 2020")]),
        ("Tools", [("p", "Sketch, Axure, Figma")]),
    ],
    body=[
        ("block", [
            ("h2", "Overview"),
            ("p", "Information kiosk design."),
            ("p", "China currently faces an ageing population, and many older communities in my city are made up mainly of elderly residents. However, most infrastructure in these existing communities is not user-friendly, especially for the elderly."),
            ("p", "After research, I decided to use the bulletin board built into every old community as a touchpoint to provide updated information, notifications and news. This could enable more interaction among residents, and bring fun and happiness to the elderly in their retirement."),
        ]),
        ("block", [
            ("h2", "The work"),
            ("p", "*Note: the full functionality cannot be conveyed in this format, due to the failure of a previous MacBook.*"),
            ("sequence", [
                ("429fa4_1a4a4561d45b4aa3bea682c2ffc02a0d.jpg", "Know-all project board"),
                ("429fa4_fd162756d1a04c17aea461d1202d8e75.jpg", "Know-all project board"),
                ("429fa4_3fbd4053fa244e1eb07a2bd4f352ca83.jpg", "Know-all project board"),
                ("429fa4_44fbe1cfd5d642e3b4e8f2be92036496.jpg", "Know-all project board"),
                ("429fa4_4081434e88124e7e81282292244ed0a3.jpg", "Know-all project board"),
                ("429fa4_16286becef714712ab44136704fb5846.jpg", "Know-all project board"),
                ("429fa4_62f59eb461b24fc9928ed642ae971353.jpg", "Know-all project board"),
                ("429fa4_04a46e8822c345b8985248f1aa69ef04.jpg", "Know-all project board"),
                ("429fa4_4937b898495649b3a12d67bf3572bc9f.jpg", "Know-all project board"),
            ]),
        ]),
    ],
)


# ================================================================
#  PAGE ASSEMBLY
# ================================================================

BY_SLUG = {p["slug"]: p for p in PROJECTS}
FEATURED = [p for p in PROJECTS if p.get("featured")]
EARLIER = [p for p in PROJECTS if p.get("earlier")]


def work_card(p, depth, small=False):
    r = "../" * depth
    tags = "".join(f"<li>{e(t)}</li>" for t in p["tags"])
    return f"""<a class="work-card reveal" href="{r}work/{p['slug']}.html">
  <div class="thumb">{img_tag(p['thumb'], p['title']).replace('{ROOT}', r)}</div>
  <div class="card-body">
    <h3>{e(p['title'])}</h3>
    {'' if small else f'<p class="card-sub">{e(p["sub"])}</p>'}
    <ul class="tags">{tags}</ul>
    <span class="card-more">Read case study</span>
  </div>
</a>"""


def featured_section(depth, heading="Featured Recent Work (2023–2025)", exclude=None):
    cards = "\n".join(
        work_card(p, depth) for p in FEATURED if p["slug"] != exclude
    )
    return f"""<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><h2>{e(heading)}</h2></div>
    <div class="work-list">{cards}</div>
  </div>
</section>"""


# ---------------------------------------------------------------- home
def build_home():
    body = f"""<section class="hero">
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <h1>Designing honest products that get jobs done, with no fuss.</h1>
        <p class="hero-lede">Product designer with hands-on experience owning end-to-end design for AI-powered SaaS products in fast-moving environments.</p>
      </div>
      <div class="hero-body">
        <p>Over the past two years, I've designed products for a global insurance organisation, including an <strong>AI contract analysis product</strong>, a <strong>design system migration</strong> across 10+ designers from multiple agencies (which reduced custom component work by <strong>94%</strong>), and a redesigned insurance platform used by <strong>68 underwriters across 18 teams</strong> (2,700+ monthly sessions).</p>
        <p>I particularly enjoy working on AI products where clarity, consistency and long-term scalability are as crucial as usability.</p>
        <p>I work hard so my pets can live a better life.</p>
        <a class="scroll-cue" href="#work">Curious to see those projects?</a>
      </div>
    </div>
  </div>
</section>

<div id="work"></div>
{featured_section(0)}

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head reveal"><h2>Earlier work (2020–2023)</h2></div>
    <div class="grid-2">{"".join(work_card(p, 0, small=True) for p in EARLIER)}</div>
  </div>
</section>"""
    return page("index.html",
                "Maxine Zhou — Product Designer",
                "Product designer working on AI-powered SaaS, design systems and complex B2B workflows. Portfolio and case studies.",
                body, "home", og_image=IMG["lp_thumb"])


# ---------------------------------------------------------------- projects
def build_projects():
    body = f"""<section class="section" style="padding-bottom:0">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Work</span>
      <h1>Selected projects</h1>
      <p>Case studies from AI-powered SaaS, design systems, and complex B2B workflows.</p>
    </div>
  </div>
</section>

{featured_section(0)}

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head reveal"><h2>Earlier work (2020–2023)</h2></div>
    <div class="grid-2">{"".join(work_card(p, 0, small=True) for p in EARLIER)}</div>
  </div>
</section>"""
    return page("projects.html", "Work — Maxine Zhou",
                "Product design case studies: AI contract analysis, enterprise design system migration, underwriting workflow design.",
                body, "projects", og_image=IMG["dsm_thumb"])


# ---------------------------------------------------------------- about
def build_about():
    body = f"""<section class="section">
  <div class="narrow">
    <div class="section-head reveal">
      <span class="eyebrow">About</span>
      <h1>Hi, I'm Maxine.</h1>
    </div>
    <div class="block reveal">
      <p>I'm a product designer with hands-on experience owning end-to-end design for AI-powered SaaS products in fast-moving environments.</p>
      <p>Over the past two years I've designed products for a global insurance organisation — an AI contract analysis product, a design system migration across 10+ designers from multiple agencies, and a redesigned insurance platform used by 68 underwriters across 18 teams.</p>
      <p>I particularly enjoy working on AI products where clarity, consistency and long-term scalability are as crucial as usability.</p>
    </div>

    <div class="block reveal">
      <h2>During work</h2>
      <p class="pull">Prototype · Proactive · Curious · Team player</p>
    </div>

    <div class="block reveal">
      <h2>What people I've worked with say</h2>
      <div class="fig-pair">
        <figure class="plain">{img_tag(TEAM_TESTIMONIAL_1, "Message from a colleague praising prototyping skills and initiative").replace('{ROOT}', '')}</figure>
        <figure class="plain">{img_tag(TEAM_TESTIMONIAL_2, "Message from a colleague praising enthusiasm and initiative").replace('{ROOT}', '')}</figure>
      </div>
    </div>

    <div class="block reveal">
      <h2>Outside of work</h2>
      <p>I work hard so my pets can live a better life.</p>
      <div class="fig-pair">
        <figure>{img_tag(IMG["cats"], "Two cats sitting together at home").replace('{ROOT}', '')}</figure>
        <figure>{img_tag(IMG["dog"], "Maxine hugging a shiba inu").replace('{ROOT}', '')}</figure>
      </div>
    </div>

    <div class="block reveal">
      <h2>Curious about my design skills?</h2>
      <p>Take a look at the projects I've worked on in my case studies.</p>
      <p><a class="btn btn-primary" style="background:var(--ink);color:var(--cream)" href="projects.html">See the work</a></p>
    </div>
  </div>
</section>"""
    return page("about.html", "About — Maxine Zhou",
                "Product designer focused on AI-powered SaaS, design systems and complex B2B workflows.",
                body, "about", og_image=IMG["dog"])


# ---------------------------------------------------------------- case studies
def build_case(p):
    depth = 1
    r = "../"
    tags = "".join(f"<li>{e(t)}</li>" for t in p["tags"])
    meta = f'<p class="card-sub" style="margin-top:18px;color:var(--muted)">{e(p["meta"])}</p>' if p.get("meta") else ""

    ov = "".join(
        f"<div><h3>{rich(label)}</h3>{render(blocks)}</div>"
        for label, blocks in p.get("overview", [])
    )
    overview = f'<div class="overview reveal">{ov}</div>' if ov else ""

    body = f"""<section class="cs-hero">
  <div class="wrap">
    <a class="back-link" href="{r}index.html">All work</a>
    <h1>{e(p['title'])}</h1>
    <p class="cs-sub">{e(p['sub'])}</p>
    <ul class="tags">{tags}</ul>
    {meta}
  </div>
</section>

<div class="wrap">
  <figure class="cs-cover">{img_tag(p['cover'], p['title'], lazy=False)}</figure>
</div>

<div class="wrap">{overview}</div>

<section class="cs-body">
  <div class="narrow">
{render(p['body'])}
  </div>
</section>"""

    return page(f"work/{p['slug']}.html",
                f"{p['title']} — Maxine Zhou",
                p["sub"][:180],
                body, "projects", og_image=p["cover"])


# ---------------------------------------------------------------- 404
def build_404():
    body = """<div class="center-page">
  <div class="wrap">
    <h1>Page not found</h1>
    <p>That link doesn't lead anywhere. Let's get you back to the work.</p>
    <a class="btn btn-primary" href="/">Back to home</a>
  </div>
</div>"""
    return page("404.html", "Page not found — Maxine Zhou",
                "Page not found.", body, "")


# ---------------------------------------------------------------- favicon
FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="14" fill="#191818"/>
  <text x="32" y="44" font-family="Helvetica,Arial,sans-serif" font-size="34"
        font-weight="700" fill="#F4F0EB" text-anchor="middle">M</text>
</svg>
"""


def main():
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    with open(os.path.join(OUT, "assets", "favicon.svg"), "w") as f:
        f.write(FAVICON)

    # index.html is generated by home.py now (the v2 homepage), not here.
    # Leaving build_home() in the list would overwrite it on every build —
    # exactly the "two designs at one URL" problem the migration is closing.
    # build_home() itself is kept so the old markup stays readable while the
    # remaining cream pages are ported. Delete both at HANDOVER §8 step 4.
    #
    # about.html is generated by about.py now (the v2 about page), for the
    # same reason -- build_about() is kept below for the same reference
    # purpose but must not run here.
    #
    # projects.html is folded away per Maxine's call on 2026-09-06 -- only
    # the three v2 case studies should be reachable for now. build_projects()
    # is kept below, unused, same as build_home()/build_about() above.
    written = [build_404()]
    for p in PROJECTS:
        if p["slug"] in MIGRATED:
            continue          # casestudy.py owns this page — see MIGRATED
        written.append(build_case(p))

    # sitemap + robots (only useful once BASE_URL is set)
    if BASE_URL:
        b = BASE_URL.rstrip("/")
        urls = "".join(f"<url><loc>{b}/{w}</loc></url>" for w in written if w != "404.html")
        with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>'
                    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                    + urls + "</urlset>")
        with open(os.path.join(OUT, "robots.txt"), "w") as f:
            f.write(f"User-agent: *\nAllow: /\nSitemap: {b}/sitemap.xml\n")

    print(f"Built {len(written)} pages:")
    for w in written:
        print("  ", w)


if __name__ == "__main__":
    main()
