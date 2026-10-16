"""The combined portfolio PDF: cover and about pages.

DATA, like every other content file. `python3 printpdf.py --book` turns this
into pdf/maxine-zhou-portfolio.pdf -- cover, about, then the case studies
listed in STUDIES, each condensed by printpdf.py's own CONDENSED lists.

The bio and the links are imported from `_about.py` rather than copied, so
the PDF cannot drift from the About page. Only the cover copy lives here.
Everything on the cover is either Maxine's own wording or read off the case
studies themselves -- no new claims about the work.
"""

# Case studies to include, in order. Motorverse is deliberately out.
STUDIES = ['launchpad', 'design-system-migration', 'analyser']

COVER = {
    # Her own role line, matching the site's title and About summary.
    "name": "Maxine Zhou",
    "role": "Product Designer",
    "tagline": "Product designer working on AI-powered SaaS.",
    "contents_label": "Selected work",
    # Shown large on the cover -- the whole point of the file.
    "site": "maxine-zhou.com",
}
