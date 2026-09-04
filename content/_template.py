# ============================================================================
# NEW CASE STUDY — copy this file, rename it to your slug, fill it in.
#
#   cp content/_template.py content/design-system-migration.py
#   ...edit...
#   python3 casestudy.py design-system-migration
#
# The leading underscore keeps this file out of the build. Delete any section
# you do not need — nothing here is required except slug/project/title/summary.
# Every block type is listed in the docstring at the top of casestudy.py.
# ============================================================================

CASE_STUDY = {
    # ---- identity -----------------------------------------------------------
    "slug":    "design-system-migration",          # becomes work/<slug>.html
    "project": "Design System",                    # small label above the title
    "title":   "Enterprise design system migration",
    "summary": "One sentence under the title. **Bold** shows in the accent colour.",

    # ---- pills: emphasised first (ink border), then quiet -------------------
    "tags_key": ["Design System", "Design Ops"],
    "tags":     ["Strategy", "2025"],

    # ---- floating dock: (label, section id) --------------------------------
    "dock": [("Context", "context"), ("Research", "research"),
             ("Insight", "insight"), ("Design", "design"), ("Impact", "impact")],
    "next": ("Next", "contract-analysis.html"),

    "sections": [

        # ---------------------------------------------------- Context
        {
            "id": "context", "classes": ["pad-lg"],
            "blocks": [
                ("head", [("eyebrow", "Context"), ("h2", "Overview")]),
                ("overview", [
                    ("My Role", ["Design System Designer"]),
                    ("Responsibilities", [
                        "First responsibility",
                        "Second responsibility",
                        "Third responsibility",
                    ]),
                    ("The Product", ["What the product actually is, in one sentence."]),
                ]),
            ],
        },

        # A stat row. Four reads best; two or three also work.
        {
            "blocks": [
                ("head", [("h2", "Impact at a glance"), ("note", "(In ten months)")]),
                ("stats", [
                    ("49",       "components tokenised"),
                    ("35% → 2%", "custom components"),
                    ("10",       "designers aligned"),
                    ("7",        "products migrated"),
                ]),
            ],
        },

        # ---------------------------------------------------- Research
        # `gap-lg` gives 112px between blocks, for a long section.
        {
            "id": "research", "classes": ["pad-lg", "gap-lg"],
            "blocks": [
                ("head", [
                    ("h2", "Section heading"),
                    ("p", "Intro paragraph. Keep this OUT of the scrolly below — the "
                          "sticky labels must be parallel or the swap will jump."),
                ]),

                # The sticky pattern: one label per image, label swaps as you scroll.
                # Give each label the same shape (h3 + one small paragraph, or
                # h3 + questions) so the heading sits at the same height in each.
                ("scrolly", [
                    (
                        [("h3", "First label"),
                         ("small", "One line describing this screen.")],
                        {"img": "your-image.jpg",
                         "alt": "Describe what is in the image, for screen readers",
                         "caption": "Caption sits below the image."},
                    ),
                    (
                        [("h3", "Second label"),
                         ("small", "One line describing this screen.")],
                        {"img": "your-other-image.jpg",
                         "alt": "Describe what is in the image",
                         "caption": "Caption sits below the image."},
                    ),
                ]),

                # A single full-width figure.
                ("head", [
                    ("eyebrow", "Research"),
                    ("h2", "Another heading"),
                    ("p", "Body copy."),
                ]),
                ("fig", {"img": "wide-image.jpg", "alt": "...",
                         "caption": "What this shows."}),
            ],
        },

        # ---------------------------------------------------- Insight
        {
            "id": "insight", "classes": ["pad-lg"],
            "blocks": [
                ("head", [("eyebrow", "Insight"), ("h2", "What the data revealed")]),
                ("findings", [
                    "First finding, with **the number** emphasised",
                    "Second finding",
                    "Third finding",
                ]),
            ],
        },

        # The centred pull-quote moment. Use once per case study at most.
        {
            "classes": ["centred"],
            "blocks": [
                ("head", [("h2", "The question this answers")]),
                ("pull", "The one line you want remembered."),
                ("centred", [
                    ("p", "Why it matters, in a paragraph."),
                    ("p", "And the consequence."),
                ]),
            ],
        },

        # ---------------------------------------------------- Design
        {
            "id": "design", "classes": ["pad-lg"],
            "blocks": [
                ("head", [("eyebrow", "Design"), ("h2", "Design direction")]),
                ("steps", [
                    "First move.",
                    "Second move.",
                    "Third move.",
                    "Fourth move.",
                ]),
            ],
        },

        # Video. `ar` and `op` crop out any black letterbox bar in the source —
        # see MEDIA.md for how to measure them for a new recording. Without
        # them a bar will show as a dark edge inside the rounded corner.
        {
            "blocks": [
                ("head", [
                    ("h2", "A thing you designed"),
                    ("p", "What it does and why."),
                ]),
                ("fig", {"video": "your-clip.mp4", "poster": "your-clip-poster.jpg",
                         "ar": "1500 / 853", "op": "bottom",
                         "caption": "What to watch for in the clip."}),
            ],
        },

        # ---------------------------------------------------- Impact
        {
            "id": "impact", "classes": ["pad-lg"],
            "blocks": [
                ("head", [("eyebrow", "Impact"), ("h2", "Impact")]),
                ("prose", [
                    ("p", "What changed, with a number if you have one."),
                    ("p", "What happened next, honestly — including what did not ship."),
                ]),
            ],
        },
    ],
}
