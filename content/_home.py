"""
Homepage content.

Same principle as a case study: this is DATA. `python3 home.py` turns it into
index.html. There is no HTML to write here and no CSS to touch.

The layout is niklas.space's, expressed in Maxine's tokens — see HANDOVER §5
for what was measured and why. The thing that pattern needs is SHORT names:
the row is name-over-description at one type size, and a name that wraps to
two lines breaks the rhythm the whole page is built on. So the long case study
titles are shortened here. The full titles still live on the pages themselves.

>>> The seven descriptions below are a first draft and want Maxine's eye. <<<
Each is one line, and changing one changes one line.
"""

# The reference site forces `lowercase` on the whole body. It is a big part of
# why it reads the way it does, but it is a personality choice, and the case
# studies are sentence case. Defaulting to sentence case per HANDOVER §5;
# flip this to True to see the other version.
LOWERCASE = False

HOME = {
    "title": "Maxine Zhou — Product Designer",
    "summary": "Product designer working on AI-powered SaaS. Case studies in "
               "underwriting workflow, design systems and AI contract analysis.",

    "intro": [
        "Hello, I’m Maxine Zhou",
        "I design honest products that get users’ job done, with no fuss.",
    ],

    # (name, description, href, preview image, alt)
    # `video` is optional — add "video": "file.mp4" to a row and the preview
    # plays instead of sitting still. Keep any such clip under ~1MB; see the
    # note at the bottom of this file.
    "groups": [
        {
            "label": "Selected work · 2023–2025",
            "rows": [
                {"name": "Launchpad",
                 "desc": "Behaviour-driven underwriting design",
                 "href": "work/launchpad.html",                      # v2
                 "img": "home-launchpad.jpg",
                 "alt": "The Launchpad underwriting platform, showing the "
                        "pipeline view and submission detail side by side",
                 "video": "home-launchpad.mp4"},

                {"name": "Design system migration",
                 "desc": "16 products, 3 agencies\n94% fewer custom components",
                 "href": "work/design-system-migration.html",        # v2
                 "img": "home-design-system-migration.jpg",
                 "alt": "A collage of interface fragments and comments from "
                        "the Enterprise Design System Migration project"},

                {"name": "Analyser",
                 "desc": "AI-empowered contract analysis",
                 "href": "work/analyser.html",                       # v2
                 "img": "home-analyser.jpg",
                 "alt": "The Analyser contract review platform, showing a "
                        "flagged clause with its suggested replacement",
                 "video": "home-analyser.mp4"},
            ],
        },
        # "Earlier work · 2020-2023" group (Content hub, Radically Digital,
        # Diago, Know-all) hidden for now per Maxine's call on 2026-09-06 --
        # the row data is kept in git history, not deleted, if she wants it
        # back later.
    ],

    # The tail group, after the 96px break. No previews — these are not work.
    "tail": {
        "label": "Elsewhere",
        "rows": [
            {"name": "Resume", "desc": "PDF",
             "href": "assets/doc/maxine-zhou-resume.pdf"},
            {"name": "Email", "desc": "maxinezhou0302@outlook.com",
             "href": "mailto:maxinezhou0302@outlook.com"},
            {"name": "LinkedIn", "desc": "in/maxine-z",
             "href": "https://www.linkedin.com/in/maxine-z-90281422b/"},
        ],
    },

    "foot": "© 2026 Maxine Zhou",
}

# ---------------------------------------------------------------------------
# Adding a moving preview to a row
# ---------------------------------------------------------------------------
# The preview renders at 560x350. A hover clip must stay under ~1MB, because
# it is fetched at the moment someone hovers — the reference site eagerly
# loads 11MB of them, which is what we are deliberately not doing.
#
# Pick the 4 seconds that show the interaction, then:
#
#   avconvert --source assets/video/lp-multiselect.mp4 \
#             --output assets/video/home-launchpad.mp4 \
#             --preset Preset960x540 --start 2 --duration 4 --replace
#
# Measured: 960x540 at 4s lands around 690KB; at 6s it is 2.3MB, which is too
# much to fetch on hover. Then add to the row:
#
#   "video": "home-launchpad.mp4",
#
# The existing home-<slug>.jpg stays as the poster, so the frame is filled the
# instant the pointer arrives and the clip starts underneath it.
