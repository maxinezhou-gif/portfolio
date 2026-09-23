#!/usr/bin/env python3
"""
Case study generator.

A case study is DATA, not markup. Write a dict in content/<slug>.py, run this,
and get a finished page using the design system in assets/css/case-study.css.

    python3 casestudy.py            # build every case study in content/
    python3 casestudy.py launchpad  # build just one

Adding a new case study means writing content. It should not mean touching
this file, and it should never mean touching CSS.

--------------------------------------------------------------------------
BLOCK REFERENCE — the vocabulary available in `body`
--------------------------------------------------------------------------
("eyebrow", "Research")                     small uppercase label
("h2", "Two pages, one workflow")           section heading
("h3", "Pipeline View")                     sub-heading
("p",  "Body copy. **Bold** is accented.")  paragraph
("note", "(In a typical month)")            quiet parenthetical
("pull", "Fast comprehension first.")       large quote

("head", [blocks])                          heading group; 40px to what follows
("div", {"classes": ["inset"], "blocks": [blocks]})  generic wrapper for a
                                             utility class -- "inset" (extra
                                             gutter), "center-block" (true
                                             centred text), "stack-40" (40px
                                             between children)
("centred", [blocks])                       centre-aligned section
("prose", [blocks])                         plain reading column of body copy

("stats", [("2,720", "Review sessions"), ...])          up to 4 stat tiles
("overview", [("My Role", ["..."]), ...])               label / value columns
("findings", ["Only **46.1%** of users...", ...])       inline-numbered list
("steps", ["Rebalanced hierarchy...", ...])             numbered cards (01..)
                                                         an entry can also be
                                                         {"text": "...", "img": "...",
                                                          "alt": "..."} for a card
                                                         with its own screenshot
("questions", ["Where does decision-making happen?"])   question chips
("bullets", ["First point", ...])                        plain bullet list
("numbered", ["First point", ...])                       plain numbered list
("collapsible", {"toggle": "My reflects",                collapsed by default;
                 "panel_id": "reflect-panel",             a click reveals it
                 "blocks": [blocks]})
("callout", [blocks])                                   aside in a tinted box
("chapter", "Phase 1 · Foundation building")            quiet chapter divider
("features", [ (text_blocks, figure), ... ])            text 384 / media 520 rows
                                                         swap the pair -- (figure, text_blocks)
                                                         -- to put the media on the left
("label", "What happened")                              accent label inside a callout

("fig",   {...})                            one figure, full width
("scrolly", [ (label_blocks, figure), ... ]) sticky label per figure
("reveal", {"before": {...}, "after": {...}})  full-bleed before/after crossfade

A figure dict:
    {"img": "file.jpg", "alt": "...", "caption": "..."}
    {"video": "file.mp4", "poster": "file.jpg", "ar": "1500 / 853",
     "op": "bottom", "caption": "..."}

`ar` is the CONTENT aspect ratio — the frame minus any black letterbox bar —
and `op` pushes the crop against that edge. See MEDIA.md for how to measure a
new recording.
"""

import html
import importlib.util
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")
OUT = os.path.join(ROOT, "work")
IMG = os.path.join(ROOT, "assets", "img")

SITE = {
    "name": "Maxine Zhou",
    "email": "maxinezhou0302@outlook.com",
    "linkedin": "https://www.linkedin.com/in/maxine-z-90281422b/",
}

# Set once a domain is bought; switches on canonical + OG tags, same as home.py.
BASE_URL = "https://maxine-zhou.com"

# Cloudflare Web Analytics beacon. Cookieless, so no consent banner is
# needed. The token is public -- it ships in the HTML of every page.
# Duplicated in home.py, same as BASE_URL above; keep them in step.
ANALYTICS = (
    "<!-- Cloudflare Web Analytics --><script type='module' "
    "src='https://static.cloudflareinsights.com/beacon.min.js' "
    "data-cf-beacon='{\"token\": \"eeb616c5b6d545fca29f3f65f1dd1791\"}'>"
    "</script><!-- End Cloudflare Web Analytics -->"
)

# The homepage's own preview image for each case study, reused as its OG
# image -- already the right shape (1200x750-ish) and already exists.
OG_IMAGE = {
    "launchpad": "home-launchpad.jpg",
    "design-system-migration": "home-design-system-migration.jpg",
    "analyser": "home-analyser.jpg",
}


# ---------------------------------------------------------------- helpers

def e(t):
    return html.escape(str(t), quote=False)


def rich(t):
    """**bold** becomes accented <strong>; a literal newline becomes <br>
    (for the rare heading that's genuinely two lines of one element).
    Everything else is escaped."""
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", e(t))
    return s.replace("\n", "<br>")


_dim_cache = {}


def dims(filename):
    """Intrinsic pixel size, so the browser reserves space before load."""
    if filename in _dim_cache:
        return _dim_cache[filename]
    path = os.path.join(IMG, filename)
    if not os.path.exists(path):
        _dim_cache[filename] = None
        return None
    out = subprocess.run(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", path],
        capture_output=True, text=True).stdout
    w = re.search(r"pixelWidth:\s*(\d+)", out)
    h = re.search(r"pixelHeight:\s*(\d+)", out)
    val = (w.group(1), h.group(1)) if w and h else None
    _dim_cache[filename] = val
    return val


def figure(f, reveal=True):
    """One framed, clipped, captioned piece of media."""
    rv = " rv" if reveal else ""
    cap = f.get("caption")
    caption = f'<figcaption>{rich(cap)}</figcaption>' if cap else ""

    if "video" in f:
        style = []
        if f.get("ar"):
            style.append(f'--ar: {f["ar"]}')
        if f.get("op"):
            style.append(f'--op: {f["op"]}')
        st = f' style="{"; ".join(style)}"' if style else ""
        poster = f' poster="../assets/img/{f["poster"]}"' if f.get("poster") else ""
        media = (
            # No `controls`: it's what draws the native, hover-triggered dark
            # scrim over the whole frame. These autoplay on scroll instead
            # (case-study.js) -- controls are added back by JS, but only
            # under prefers-reduced-motion, where autoplay is skipped and
            # controls are the only way to watch it at all.
            f'<video playsinline preload="none" muted loop{poster}{st}>'
            f'<source src="../assets/video/{f["video"]}" type="video/mp4">'
            f"</video>"
        )
    else:
        d = dims(f["img"])
        wh = f' width="{d[0]}" height="{d[1]}"' if d else ""
        media = (
            f'<img src="../assets/img/{f["img"]}" alt="{e(f.get("alt", ""))}"'
            f'{wh} loading="lazy" decoding="async">'
        )

    return (f'<figure class="fig{rv}">'
            f'<div class="frame"><div class="clip">{media}</div></div>'
            f"{caption}</figure>")


# ---------------------------------------------------------------- blocks

def render(blocks, indent=2):
    pad = "  " * indent
    out = []

    for b in blocks:
        kind = b[0]

        if kind in ("h2", "h3"):
            out.append(f"{pad}<{kind}>{rich(b[1])}</{kind}>")
        elif kind == "p":
            out.append(f'{pad}<p class="body">{rich(b[1])}</p>')
        elif kind == "note":
            out.append(f'{pad}<p class="note">{rich(b[1])}</p>')
        elif kind == "small":
            out.append(f'{pad}<p class="small">{rich(b[1])}</p>')
        elif kind == "eyebrow":
            out.append(f'{pad}<span class="eyebrow">{e(b[1])}</span>')
        elif kind == "pull":
            out.append(f'{pad}<p class="pull rv">{rich(b[1])}</p>')

        elif kind == "head":
            out.append(f'{pad}<div class="sec-head rv">')
            out.append(render(b[1], indent + 1))
            out.append(f"{pad}</div>")

        elif kind == "div":
            cfg = b[1]
            cls = " ".join(["rv"] + cfg.get("classes", []))
            out.append(f'{pad}<div class="{cls}">')
            out.append(render(cfg["blocks"], indent + 1))
            out.append(f"{pad}</div>")

        elif kind in ("centred", "prose"):
            out.append(f'{pad}<div class="prose rv">')
            out.append(render(b[1], indent + 1))
            out.append(f"{pad}</div>")

        elif kind == "stats":
            tiles = "".join(
                f'<div class="stat"><span class="n">{e(n)}</span>'
                f'<span class="l">{rich(l)}</span></div>'
                for n, l in b[1])
            out.append(f'{pad}<div class="stats rv">{tiles}</div>')

        elif kind == "overview":
            cols = []
            for col in b[1]:
                label, items = col[0], col[1]
                ordered = col[2] if len(col) > 2 else False
                if len(items) == 1:
                    inner = f'<p class="body">{rich(items[0])}</p>'
                else:
                    tag = "ol" if ordered else "ul"
                    inner = f"<{tag}>" + "".join(f"<li>{rich(i)}</li>" for i in items) + f"</{tag}>"
                cols.append(f'<div class="ov"><h3>{rich(label)}</h3>{inner}</div>')
            out.append(f'{pad}<div class="overview rv">{"".join(cols)}</div>')

        elif kind == "findings":
            items = "".join(f"<li>{rich(i)}</li>" for i in b[1])
            out.append(f'{pad}<ol class="findings rv">{items}</ol>')

        elif kind == "steps":
            def step_li(i, entry):
                # a plain string, or {"text": "...", "img": "...", "alt": "..."}
                # for a step that carries its own screenshot -- optionally
                # {"title": "...", "text": "..."} to split out a real <h3>
                # title (black) above the muted body text
                title = None
                if isinstance(entry, dict):
                    text, img = entry["text"], entry.get("img")
                    alt, title = entry.get("alt", ""), entry.get("title")
                else:
                    text, img = entry, None
                media = ""
                if img:
                    d = dims(img)
                    wh = f' width="{d[0]}" height="{d[1]}"' if d else ""
                    media = (f'<div class="step-media"><img src="../assets/img/{img}" '
                             f'alt="{e(alt)}"{wh} loading="lazy" decoding="async"></div>')
                heading = f"<h3>{rich(title)}</h3>" if title else ""
                return (f'<li>{media}<span class="n">{i + 1:02d}</span>{heading}'
                        f'<span class="t">{rich(text)}</span></li>')
            items = "".join(step_li(i, entry) for i, entry in enumerate(b[1]))
            out.append(f'{pad}<ol class="step-cards rv">{items}</ol>')

        elif kind == "chapter":
            out.append(f'{pad}<h2 class="chapter rv">{rich(b[1])}</h2>')

        elif kind == "features":
            out.append(f'{pad}<div class="features">')
            for a, c in b[1]:
                # either (text_blocks, fig) or (fig, text_blocks) -- the dict
                # is always the figure, so order tells us which side it's on.
                rev = isinstance(a, dict)
                fig, text_blocks = (a, c) if rev else (c, a)
                cls = "feature rv rev" if rev else "feature rv"
                text_div = (f'{pad}    <div class="feature-text">\n'
                            + render(text_blocks, indent + 3)
                            + f"\n{pad}    </div>")
                fig_html = pad + "    " + figure(fig, reveal=False)
                out.append(f'{pad}  <div class="{cls}">')
                out.append(fig_html + "\n" + text_div if rev else text_div + "\n" + fig_html)
                out.append(f"{pad}  </div>")
            out.append(f"{pad}</div>")

        elif kind == "bullets":
            items = "".join(f"<li>{rich(i)}</li>" for i in b[1])
            out.append(f'{pad}<ul class="bullets rv">{items}</ul>')

        elif kind == "numbered":
            items = "".join(f"<li>{rich(i)}</li>" for i in b[1])
            out.append(f'{pad}<ol class="numbered rv">{items}</ol>')

        elif kind == "collapsible":
            cfg = b[1]
            pid = cfg["panel_id"]
            chevron = ('<svg class="chevron" viewBox="0 0 16 16" fill="none" aria-hidden="true">'
                       '<path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" '
                       'stroke-linecap="round" stroke-linejoin="round"/></svg>')
            out.append(f'{pad}<button type="button" class="dock-pill collapse-toggle" '
                       f'aria-expanded="false" aria-controls="{pid}">'
                       f'{e(cfg["toggle"])}{chevron}</button>')
            out.append(f'{pad}<div class="collapse-panel" id="{pid}" hidden>')
            out.append(render(cfg["blocks"], indent + 1))
            out.append(f"{pad}</div>")

        elif kind == "callout":
            out.append(f'{pad}<div class="callout rv">')
            out.append(render(b[1], indent + 1))
            out.append(f"{pad}</div>")

        elif kind == "label":
            out.append(f'{pad}<span class="label">{e(b[1])}</span>')

        elif kind == "questions":
            items = "".join(f"<li>{rich(q)}</li>" for q in b[1])
            out.append(f'{pad}<ul class="q-list">{items}</ul>')

        elif kind == "reveal":
            cfg = b[1]
            def pane(side, f):
                d = dims(f["img"])
                wh = f' width="{d[0]}" height="{d[1]}"' if d else ""
                return (f'{pad}  <div class="pane is-{side}">'
                        f'<div class="pane-inner">'
                        f'<div class="pane-head"><h3>{e(f.get("label", side.title()))}</h3>'
                        f'<p class="pane-body">{rich(f["body"])}</p></div>'
                        f'<figure class="fig pane-media"><div class="frame"><div class="clip">'
                        f'<img src="../assets/img/{f["img"]}" alt="{e(f.get("alt", ""))}"{wh}'
                        f' loading="lazy" decoding="async"></div></div></figure>'
                        f'</div></div>')
            out.append(f'{pad}<div class="reveal">')
            out.append(pane("before", cfg["before"]))
            out.append(pane("after", cfg["after"]))
            out.append(f"{pad}</div>")

        elif kind == "fig":
            out.append(pad + figure(b[1]))

        elif kind == "scrolly":
            pairs = b[1]
            out.append(f'{pad}<div class="scrolly" style="--pairs:{len(pairs)}">')
            for label_blocks, fig in pairs:
                out.append(f'{pad}  <div class="st">')
                out.append(f'{pad}    <div class="def">')
                out.append(render(label_blocks, indent + 3))
                out.append(f"{pad}    </div>")
                out.append(f"{pad}  </div>")
                out.append(pad + "  " + figure(fig))
            out.append(f"{pad}</div>")

        elif kind == "raw":
            out.append(pad + b[1])

        else:
            raise ValueError(f"unknown block type: {kind!r}")

    return "\n".join(out)


def section(sec):
    """A page section. `sec` is a dict: id, classes, blocks, full."""
    # `full: True` drops the gutter, for full-bleed content like the reveal
    tail = [] if sec.get("full") else ["wrap"]
    cls = " ".join(["section"] + sec.get("classes", []) + tail)
    sid = f' id="{sec["id"]}"' if sec.get("id") else ""
    return (f'  <section class="{cls}"{sid}>\n'
            + render(sec["blocks"], 2)
            + "\n  </section>")


# ---------------------------------------------------------------- page

SCRIPT = open(os.path.join(ROOT, "assets", "js", "case-study.js")).read() \
    if os.path.exists(os.path.join(ROOT, "assets", "js", "case-study.js")) else ""


def build(cs):
    nav = cs.get("dock", [])
    links = "".join(f'<a href="#{target}">{e(label)}</a>' for label, target in nav)

    prev_next = ""
    if cs.get("next"):
        prev_next = f'<a class="dock-pill" href="{cs["next"][1]}">{e(cs["next"][0])} →</a>'

    pills = "".join(
        f'<li class="is-key">{e(t)}</li>' for t in cs.get("tags_key", [])
    ) + "".join(
        f"<li>{e(t)}</li>" for t in cs.get("tags", [])
    )

    body = "\n\n".join(section(s) for s in cs["sections"])

    canon = ""
    if BASE_URL:
        b = BASE_URL.rstrip("/")
        path = f"work/{cs['slug']}.html"
        canon = f'\n<link rel="canonical" href="{b}/{path}">'
        canon += f'\n<meta property="og:type" content="article">'
        canon += f'\n<meta property="og:title" content="{e(cs["title"])} — {SITE["name"]}">'
        canon += f'\n<meta property="og:description" content="{e(cs["summary"])}">'
        canon += f'\n<meta property="og:url" content="{b}/{path}">'
        og_image = OG_IMAGE.get(cs["slug"])
        if og_image:
            canon += f'\n<meta property="og:image" content="{b}/assets/img/{og_image}">'

    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(cs['title'])} — {SITE['name']}</title>
<meta name="description" content="{e(cs['summary'])}">{canon}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/css/case-study.css">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="topbar">
  <div class="wrap">
    <a class="tb-name" href="../index.html">{SITE['name']}</a>
    <a class="tb-right" href="../about.html">About</a>
  </div>
</header>

<main id="main">

  <section class="hero wrap">
    <ul class="pills">{pills}</ul>
    <p class="project-label">{e(cs['project'])}</p>
    <h1>{rich(cs['title'])}</h1>
    <p class="hero-sub">{rich(cs['summary'])}</p>
  </section>

{body}

</main>

<nav class="dock" aria-label="Section navigation">
  <div class="dock-inner">
    <a class="dock-pill" href="../index.html">↖ All work</a>
    <div class="dock-links">{links}</div>
    {prev_next}
  </div>
</nav>

<script>
{SCRIPT}
</script>
{ANALYTICS}
</body>
</html>
"""
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, cs["slug"] + ".html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(doc)
    return path


def load(slug):
    path = os.path.join(CONTENT, slug + ".py")
    spec = importlib.util.spec_from_file_location(slug, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CASE_STUDY


def main():
    which = sys.argv[1:] or [
        f[:-3] for f in sorted(os.listdir(CONTENT))
        if f.endswith(".py") and not f.startswith("_")
    ]
    for slug in which:
        cs = load(slug)
        path = build(cs)
        print(f"built {os.path.relpath(path, ROOT)}  ({cs['title']})")


if __name__ == "__main__":
    main()
