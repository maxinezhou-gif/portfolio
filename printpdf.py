#!/usr/bin/env python3
"""Render case studies to paginated PDFs for attaching to job applications.

    python3 printpdf.py                 # every case study, one PDF each
    python3 printpdf.py launchpad       # just that one
    python3 printpdf.py --condensed     # the short cut, into pdf/condensed/
    python3 printpdf.py --book          # ONE combined PDF: cover, about, work
    python3 printpdf.py --lab           # refresh the _prototype print labs

Output lands in pdf/, which is gitignored -- these are build artefacts, the
same as work/*.html, and nothing on the site links to them.

The layout is the @media print block in assets/css/case-study.css; this script
only drives Chrome. If a PDF looks wrong, the stylesheet is what to change --
and _prototype/print-lab-<slug>.html shows it in a normal browser window.

Needs Google Chrome, which does the rendering. No other dependency, in keeping
with the rest of this repo.
"""

import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'pdf')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

# The live v2 case studies, in the order the homepage lists them. The cream
# pages are deliberately absent -- nothing links to them and they are excluded
# from robots.txt, so they are not part of the portfolio.
SLUGS = ['launchpad', 'design-system-migration', 'analyser', 'motorverse']

# --- the condensed cut ------------------------------------------------------
# Which sections to drop with --condensed, by the id the generator already puts
# on each <section>. The full PDFs run 11-19 pages because they are a faithful
# render of a page built to be scrolled; this keeps the spine a hiring manager
# reads -- the context, the insight, the design and the outcome -- and drops the
# research and process detail that the live site is the better place for.
#
# This is a starting point, not a judgement about the work: edit a line and
# re-run. An id that does not exist in a case study is simply ignored.
CONDENSED = {
    # the UX audit, funnel analysis and heat maps -- the longest stretch, and
    # the part that reads as method rather than outcome
    'launchpad': ['research'],
    # the four-phase migration walkthrough, plus the closing reflection
    'design-system-migration': ['approach'],
    # the design-evolution sequence, including the modal exploration that dev
    # constraints blocked -- #research here is only a short framing section
    'analyser': ['insight'],
    # the visual-language deep dive; the hero, process and screens still carry
    # the story for a visual case study
    'motorverse': ['accent', 'gradients', 'collage'],
}


def page_count(path):
    """Pages in a PDF, read straight off the object table."""
    with open(path, 'rb') as fh:
        return len(re.findall(rb'/Type\s*/Page[^s]', fh.read()))


def condensed_copy(src, omit):
    """A temporary sibling of the page with `omit`ted sections hidden.

    It has to be written into work/ rather than a temp directory: the page
    reaches its assets with ../assets/, so a copy anywhere else loses every
    image. The caller deletes it.
    """
    with open(src, encoding='utf-8') as fh:
        html = fh.read()
    hide = ','.join(f'#{sid}' for sid in omit)
    style = f'<style media="print">{hide}{{display:none}}</style>\n</head>'
    tmp = src.replace('.html', '.__condensed.html')
    with open(tmp, 'w', encoding='utf-8') as fh:
        fh.write(html.replace('</head>', style, 1))
    return tmp


def render(slug, condensed=False):
    src = os.path.join(ROOT, 'work', f'{slug}.html')
    if not os.path.exists(src):
        sys.exit(f'no such case study: work/{slug}.html')
    out_dir = os.path.join(OUT, 'condensed') if condensed else OUT
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, f'{slug}.pdf')

    page = src
    if condensed:
        omit = CONDENSED.get(slug, [])
        if not omit:
            print(f'  {slug}: nothing listed in CONDENSED — rendering in full')
        else:
            page = condensed_copy(src, omit)
    try:
        _chrome(page, dest)
    finally:
        if page != src:
            os.remove(page)

    size = os.path.getsize(dest) / 1024 / 1024
    label = os.path.relpath(dest, ROOT)
    print(f'  {label} — {page_count(dest)} pages, {size:.1f} MB')


def _chrome(src, dest):
    subprocess.run(
        [
            CHROME,
            '--headless=new',
            '--disable-gpu',
            '--no-sandbox',
            '--no-pdf-header-footer',
            # Long pages lazy-load their figures. Give Chrome enough virtual
            # time to settle, or the lower half of a case study prints blank.
            '--virtual-time-budget=25000',
            f'--print-to-pdf={dest}',
            f'file://{src}',
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _load(name):
    """Read a content file's module-level data without importing a package."""
    ns = {}
    with open(os.path.join(ROOT, 'content', name), encoding='utf-8') as fh:
        exec(compile(fh.read(), name, 'exec'), ns)
    return ns


def _sections(main_html):
    """Split a <main> body into its top-level <section> chunks."""
    head, *rest = main_html.split('<section ')
    return head, ['<section ' + chunk for chunk in rest]


def build_book():
    """Assemble cover + about + the condensed case studies into one document."""
    book = _load('_book.py')
    about = _load('_about.py')['ABOUT']
    cover, studies = book['COVER'], book['STUDIES']

    # --- the work, condensed, with the omitted sections actually removed -----
    # Not hidden: all three case studies carry the same section ids (#context,
    # #impact...), and duplicate ids in one document make an #id selector match
    # only the first. The ids are dropped here too, for the same reason.
    body, contents = [], []
    for slug in studies:
        with open(os.path.join(ROOT, 'work', f'{slug}.html'), encoding='utf-8') as fh:
            page = fh.read()
        inner = re.search(r'<main id="main">(.*?)</main>', page, re.S).group(1)
        lead, chunks = _sections(inner)
        omit = CONDENSED.get(slug, [])

        def keep(chunk):
            found = re.search(r'id="([^"]+)"', chunk[:200])
            return found is None or found.group(1) not in omit

        kept = [re.sub(r'\s+id="[^"]+"', '', c, count=1)
                for c in chunks if keep(c)]
        body.append(lead + ''.join(kept))

        title = re.search(r'<h1>(.*?)</h1>', page, re.S).group(1)
        label = re.search(r'<p class="project-label">(.*?)</p>', page)
        contents.append((label.group(1) if label else slug, re.sub(r'<[^>]+>', '', title)))

    # --- cover ---------------------------------------------------------------
    rows = '\n'.join(
        f'      <li><span class="ttl">{t}</span><span class="meta">{p}</span></li>'
        for p, t in contents)
    cover_html = f"""
  <section class="pdf-cover wrap">
    <div class="pdf-cover-head">
      <div>
        <h1>{cover['name']}</h1>
        <p class="role">{cover['role']}</p>
      </div>
      <p class="site">{cover['site']}</p>
    </div>
    <p class="tagline">{cover['tagline']}</p>
    <div class="pdf-contents">
      <span class="eyebrow">{cover['contents_label']}</span>
      <ol>
{rows}
      </ol>
    </div>
  </section>"""

    # --- about: her own bio and links, imported, never retyped ---------------
    photo = about.get('photo')
    img = (f'<img class="pdf-about-photo" src="../assets/img/{photo["file"]}"'
           f' alt="{photo["alt"]}" width="534" height="700">') if photo else ''
    paras = '\n        '.join(f'<p>{p}</p>' for p in about['bio'])
    links = '\n        '.join(
        f'<div class="row"><span class="row-name">{l["name"]}</span>'
        f'<span class="row-desc">{l["desc"]}</span></div>'
        for l in about['links'] if l['name'] != 'Resume')
    about_html = f"""
  <section class="pdf-about wrap">
    <div class="pdf-about-grid">
      <div>{img}</div>
      <div>
        <h1>{about['heading']}</h1>
        {paras}
        <div class="links">
        {links}
        <div class="row"><span class="row-name">Portfolio</span>
          <span class="row-desc">{cover['site']}</span></div>
        </div>
      </div>
    </div>
  </section>"""

    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{cover['name']} — {cover['role']}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/css/case-study.css">
</head>
<body>
<main id="main">
{cover_html}
{about_html}
{''.join(body)}
</main>
</body>
</html>
"""
    # scripts drive scroll behaviour that print has already neutralised, and
    # three copies of the same IIFE in one document is asking for trouble
    return re.sub(r'<script\b.*?</script>', '', doc, flags=re.S)


LAB_BANNER = """/* GENERATED BY printpdf.py --lab -- DO NOT EDIT.
   case-study.css with `@media print` rewritten to `@media screen`, so the
   print labs show the paginated layout in a normal browser window. */
"""


def build_labs():
    """Rewrite _prototype's print labs against the current stylesheet.

    Worth a command rather than a one-off: a lab left behind by a stylesheet
    change shows the OLD layout, and a browser caches the copied stylesheet
    hard on top of that. Both have already sent someone chasing a bug that
    was not in the CSS. The ?v= on the link is the cache-bust.
    """
    css_path = os.path.join(ROOT, 'assets', 'css', 'case-study.css')
    with open(css_path, encoding='utf-8') as fh:
        css = fh.read().replace('@media print {', '@media screen {')
    lab_css = os.path.join(ROOT, '_prototype', 'lab-assets', 'print-preview.css')
    with open(lab_css, 'w', encoding='utf-8') as fh:
        fh.write(LAB_BANNER + css)

    link = f'lab-assets/print-preview.css?v={int(os.path.getmtime(css_path))}'
    for slug in SLUGS:
        with open(os.path.join(ROOT, 'work', f'{slug}.html'), encoding='utf-8') as fh:
            page = fh.read()
        page = page.replace('../assets/css/case-study.css', link)
        page = page.replace('<title>', '<title>PRINT LAB — ')
        out = os.path.join(ROOT, '_prototype', f'print-lab-{slug}.html')
        with open(out, 'w', encoding='utf-8') as fh:
            fh.write(page)
        print(f'  _prototype/print-lab-{slug}.html')

    book = build_book().replace('../assets/css/case-study.css', link)
    with open(os.path.join(ROOT, '_prototype', 'print-lab-book.html'),
              'w', encoding='utf-8') as fh:
        fh.write(book)
    print('  _prototype/print-lab-book.html')


def main():
    if '--lab' in sys.argv[1:]:
        print('Refreshing the print labs:')
        build_labs()
        return
    if not os.path.exists(CHROME):
        sys.exit('Google Chrome not found — it does the rendering.')
    os.makedirs(OUT, exist_ok=True)
    args = sys.argv[1:]

    if '--book' in args:
        tmp = os.path.join(ROOT, 'work', '__book.html')
        dest = os.path.join(OUT, 'maxine-zhou-portfolio.pdf')
        with open(tmp, 'w', encoding='utf-8') as fh:
            fh.write(build_book())
        try:
            _chrome(tmp, dest)
        finally:
            os.remove(tmp)
        size = os.path.getsize(dest) / 1024 / 1024
        print(f'  pdf/maxine-zhou-portfolio.pdf — '
              f'{page_count(dest)} pages, {size:.1f} MB')
        return

    condensed = '--condensed' in args
    slugs = [a for a in args if not a.startswith('-')] or SLUGS
    cut = 'condensed' if condensed else 'full'
    print(f'Rendering {len(slugs)} case stud'
          f'{"y" if len(slugs) == 1 else "ies"} ({cut}):')
    for slug in slugs:
        render(slug, condensed=condensed)


if __name__ == '__main__':
    main()
