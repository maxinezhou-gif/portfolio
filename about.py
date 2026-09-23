#!/usr/bin/env python3
"""
About page generator.

    python3 about.py        # content/_about.py -> about.html

Same contract as home.py: the page is DATA. Edit content/_about.py, run
this, never touch about.html.

Reuses home.py's helpers and its narrow column / intro typography
(.home-col, .home-intro, .home-list) rather than inventing a second set —
this page is a shorter variant of the same pattern, not a different one.
No hover preview, no travelling dot, so home.js is not loaded here: every
row it drives requires a `.row[data-preview]`, and this page has none.
"""

import importlib.util
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")
sys.path.insert(0, ROOT)
import home  # noqa: E402  (after sys.path tweak) -- reuse e(), rich(), dims(), row_html()

SITE = home.SITE
BASE_URL = home.BASE_URL
ANALYTICS = home.ANALYTICS


def build(about, lowercase=False):
    bio = "\n      ".join(f"<p>{home.rich(p)}</p>" for p in about["bio"])

    links = "\n".join(home.row_html(r, preview=False) for r in about["links"])

    body_class = "home lowercase" if lowercase else "home"
    lower_css = ("\n<style>body.lowercase{text-transform:lowercase}"
                 "body.lowercase .row-desc{text-transform:lowercase}</style>"
                 if lowercase else "")

    canon = ""
    if BASE_URL:
        b = BASE_URL.rstrip("/")
        canon = (f'\n<link rel="canonical" href="{b}/about.html">'
                 f'\n<meta property="og:type" content="profile">'
                 f'\n<meta property="og:title" content="{home.e(about["title"])}">'
                 f'\n<meta property="og:description" content="{home.e(about["summary"])}">'
                 f'\n<meta property="og:url" content="{b}/about.html">')

    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{home.e(about['title'])}</title>
<meta name="description" content="{home.e(about['summary'])}">{canon}
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
    <a class="tb-right" href="index.html">Work</a>
  </div>
</header>

<main id="main" class="home-col">

    <section class="home-intro about-intro">
      <h1>{home.e(about['heading'])}</h1>
      {bio}
    </section>

    <nav class="home-list" aria-label="Links">
{links}
    </nav>

    <p class="home-foot">{home.e(about['foot'])}</p>

</main>
{ANALYTICS}
</body>
</html>
"""
    path = os.path.join(ROOT, "about.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(doc)
    return path


def main():
    spec = importlib.util.spec_from_file_location("_about", os.path.join(CONTENT, "_about.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    lower = getattr(mod, "LOWERCASE", False)
    if "--lowercase" in sys.argv:
        lower = True
    if "--sentence-case" in sys.argv:
        lower = False

    path = build(mod.ABOUT, lowercase=lower)
    print(f"built {os.path.relpath(path, ROOT)}")


if __name__ == "__main__":
    main()
