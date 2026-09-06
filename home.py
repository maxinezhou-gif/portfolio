#!/usr/bin/env python3
"""
Homepage generator.

    python3 home.py        # content/_home.py -> index.html

Same contract as casestudy.py: the page is DATA. Edit content/_home.py, run
this, never touch index.html.

The homepage is a different shape from a case study — one narrow centred
column, one type size, no images in the flow — so it has its own small
stylesheet (assets/css/home.css) and its own script (assets/js/home.js).
It still loads assets/css/case-study.css first, which is where every token,
the reset and the top bar live. Nothing is duplicated.

See HANDOVER §5 for the reference analysis this layout comes from.
"""

import html
import importlib.util
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")

SITE = {"name": "Maxine Zhou"}

# Set once a domain is bought; switches on canonical + OG tags (HANDOVER §8.6).
BASE_URL = "https://maxine-zhou.com"


def e(t):
    return html.escape(str(t), quote=False)


def rich(t):
    """**bold** becomes an accented <strong>; everything else is escaped."""
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", e(t))


def dims(filename):
    """Real pixel size of an image in assets/img, so width/height can be
    written onto the tag and the browser reserves space before it loads."""
    path = os.path.join(ROOT, "assets", "img", filename)
    if not os.path.exists(path):
        return None
    try:
        import struct
        with open(path, "rb") as f:
            head = f.read(2)
            if head == b"\xff\xd8":                       # JPEG
                f.seek(2)
                while True:
                    b = f.read(1)
                    while b and b != b"\xff":
                        b = f.read(1)
                    marker = f.read(1)
                    while marker == b"\xff":
                        marker = f.read(1)
                    if not marker:
                        return None
                    if marker[0] in range(0xC0, 0xD0) and marker[0] not in (0xC4, 0xC8, 0xCC):
                        f.read(3)
                        h, w = struct.unpack(">HH", f.read(4))
                        return w, h
                    size = struct.unpack(">H", f.read(2))[0]
                    f.seek(size - 2, 1)
            f.seek(0)
            if f.read(8) == b"\x89PNG\r\n\x1a\n":          # PNG
                f.seek(16)
                return struct.unpack(">II", f.read(8))
    except Exception:
        return None
    return None


def external(href):
    return href.startswith("http") or href.startswith("mailto:")


def row_html(r, preview=True):
    """One list row. The data-preview attributes are what home.js reads."""
    attrs = [f'class="row"', f'href="{e(r["href"])}"']
    if preview and r.get("img"):
        attrs.append(f'data-preview="assets/img/{e(r["img"])}"')
        attrs.append(f'data-preview-alt="{html.escape(r.get("alt", ""), quote=True)}"')
        if r.get("video"):
            attrs.append(f'data-preview-video="assets/video/{e(r["video"])}"')
    if external(r["href"]):
        attrs.append('target="_blank" rel="noopener"')
    if r["href"].endswith(".pdf"):
        attrs.append('target="_blank" rel="noopener"')
    # desc supports a literal "\n" for a genuine two-line description (e.g.
    # a name + a stat, each short enough alone) -- rare, most rows are one line
    desc = rich(r["desc"]).replace("\n", "<br>")
    return (f'      <a {" ".join(attrs)}>\n'
            f'        <span class="row-name">{e(r["name"])}</span>\n'
            f'        <span class="row-desc">{desc}</span>\n'
            f'      </a>')


def group_html(g, label_id, preview=True):
    rows = "\n".join(row_html(r, preview) for r in g["rows"])
    return (f'    <nav class="home-list" aria-labelledby="{label_id}">\n'
            f'      <p class="home-group-label" id="{label_id}">{e(g["label"])}</p>\n'
            f'{rows}\n'
            f'    </nav>')


def build(home, lowercase=False):
    intro = "\n      ".join(
        (f"<h1>{rich(t)}</h1>" if i == 0 else f"<p>{rich(t)}</p>")
        for i, t in enumerate(home["intro"])
    )

    groups = "\n\n".join(
        group_html(g, f"group-{i}") for i, g in enumerate(home["groups"])
    )
    tail = group_html(home["tail"], "group-tail", preview=False)

    # The preview <img> starts with no src at all; home.js sets it on first
    # hover, so a visitor who never hovers downloads no preview media.
    script = ""
    js_path = os.path.join(ROOT, "assets", "js", "home.js")
    if os.path.exists(js_path):
        script = open(js_path, encoding="utf-8").read()

    body_class = "home lowercase" if lowercase else "home"
    lower_css = ("\n<style>body.lowercase{text-transform:lowercase}"
                 "body.lowercase .row-desc{text-transform:lowercase}</style>"
                 if lowercase else "")

    canon = ""
    if BASE_URL:
        b = BASE_URL.rstrip("/")
        canon = (f'\n<link rel="canonical" href="{b}/">'
                 f'\n<meta property="og:type" content="website">'
                 f'\n<meta property="og:title" content="{e(home["title"])}">'
                 f'\n<meta property="og:description" content="{e(home["summary"])}">'
                 f'\n<meta property="og:url" content="{b}/">')

    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(home['title'])}</title>
<meta name="description" content="{e(home['summary'])}">{canon}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/case-study.css">
<link rel="stylesheet" href="assets/css/home.css">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">{lower_css}
</head>
<body class="{body_class}">
<a class="skip" href="#main">Skip to content</a>

<header class="topbar">
  <div class="wrap">
    <a class="tb-name" href="index.html">{SITE['name']}</a>
    <a class="tb-right" href="about.html">About</a>
  </div>
</header>

<main id="main" class="home-col">

    <section class="home-intro">
      {intro}
    </section>

{groups}

{tail}

    <p class="home-foot">{e(home['foot'])}</p>

</main>

<!-- The two moving parts. One of each for the whole page, so they travel
     rather than blink into place. Inert without JS, and hidden below 1040px
     and on pointer-less devices. -->
<span class="home-dot" aria-hidden="true"></span>
<div class="home-preview" aria-hidden="true">
  <span class="media">
    <img alt="" width="560" height="350" decoding="async">
    <video muted loop playsinline preload="none" width="560" height="350"></video>
  </span>
</div>

<script>
{script}
</script>
</body>
</html>
"""
    path = os.path.join(ROOT, "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(doc)
    return path


def main():
    spec = importlib.util.spec_from_file_location("_home", os.path.join(CONTENT, "_home.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    lower = getattr(mod, "LOWERCASE", False)
    if "--lowercase" in sys.argv:
        lower = True
    if "--sentence-case" in sys.argv:
        lower = False

    path = build(mod.HOME, lowercase=lower)
    n = sum(len(g["rows"]) for g in mod.HOME["groups"]) + len(mod.HOME["tail"]["rows"])
    print(f"built {os.path.relpath(path, ROOT)}  "
          f"({n} rows, {'lowercase' if lower else 'sentence case'})")


if __name__ == "__main__":
    main()
