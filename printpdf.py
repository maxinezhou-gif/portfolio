#!/usr/bin/env python3
"""Render case studies to paginated PDFs for attaching to job applications.

    python3 printpdf.py                 # every case study, one PDF each
    python3 printpdf.py launchpad       # just that one
    python3 printpdf.py --condensed     # the short cut, into pdf/condensed/

Output lands in pdf/, which is gitignored -- these are build artefacts, the
same as work/*.html, and nothing on the site links to them.

The layout is the @media print block in assets/css/case-study.css; this script
only drives Chrome. If a PDF looks wrong, the stylesheet is what to change --
and _prototype/print-lab.html shows that layout in a normal browser window.

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


def main():
    if not os.path.exists(CHROME):
        sys.exit('Google Chrome not found — it does the rendering.')
    os.makedirs(OUT, exist_ok=True)
    args = sys.argv[1:]
    condensed = '--condensed' in args
    slugs = [a for a in args if not a.startswith('-')] or SLUGS
    cut = 'condensed' if condensed else 'full'
    print(f'Rendering {len(slugs)} case stud'
          f'{"y" if len(slugs) == 1 else "ies"} ({cut}):')
    for slug in slugs:
        render(slug, condensed=condensed)


if __name__ == '__main__':
    main()
