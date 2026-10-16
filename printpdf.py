#!/usr/bin/env python3
"""Render case studies to paginated PDFs for attaching to job applications.

    python3 printpdf.py                 # every case study, one PDF each
    python3 printpdf.py launchpad       # just that one

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


def page_count(path):
    """Pages in a PDF, read straight off the object table."""
    with open(path, 'rb') as fh:
        return len(re.findall(rb'/Type\s*/Page[^s]', fh.read()))


def render(slug):
    src = os.path.join(ROOT, 'work', f'{slug}.html')
    if not os.path.exists(src):
        sys.exit(f'no such case study: work/{slug}.html')
    dest = os.path.join(OUT, f'{slug}.pdf')
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
    size = os.path.getsize(dest) / 1024 / 1024
    print(f'  pdf/{slug}.pdf — {page_count(dest)} pages, {size:.1f} MB')


def main():
    if not os.path.exists(CHROME):
        sys.exit('Google Chrome not found — it does the rendering.')
    os.makedirs(OUT, exist_ok=True)
    slugs = sys.argv[1:] or SLUGS
    print(f'Rendering {len(slugs)} case stud{"y" if len(slugs) == 1 else "ies"}:')
    for slug in slugs:
        render(slug)


if __name__ == '__main__':
    main()
