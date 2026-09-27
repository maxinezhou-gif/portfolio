# ============================================================================
# Motorverse — NOT YET LINKED ANYWHERE. Local preview only, per Maxine:
# built for her to check against Figma (kZbRLtd614DBU5cWWJLP8O, node 80:836)
# before it goes into home.py's card list or any dock/nav.
#
# Copy is hers, pulled verbatim from the Figma file via get_design_context.
# Colours come from get_variable_defs (assets/css/motorverse-dark.css).
# Images are her own exports from ~/Desktop/Motorverse assets/, except
# mv-momentum.jpg, which has no matching export there yet -- see HANDOVER.
#
# The hero video slot is still empty: two candidate clips sit in
# ~/Desktop/Motorverse assets/ (video.mov, Screen Recording ....mov) and
# neither has been transcoded yet -- her call on which one and what portion.
# ============================================================================

CASE_STUDY = {
    "slug":    "motorverse",
    "project": "The Motorverse",
    "title":   "Redesigning a Web3 racing app for web and mobile",
    "summary": "Motorverse is an ecosystem built around digital vehicle ownership "
               "and community, where players own a digital car and drive it "
               "across many games and experiences.",

    "tags_key": ["UX/UI", "WEB 3", "Website"],
    "tags":     ["Mobile", "2024/25"],

    # Figma's own dock only carries "All work" + "Next" -- no section jump
    # links -- so the middle nav row is left empty rather than invented.
    "dock": [],
    "next": ("Next", "launchpad.html"),

    # A dark case study: adds class="theme-dark" to <body> and loads the
    # override stylesheet below, which redefines just colour + the framed-
    # figure and section-background rules Motorverse's Figma diverges on.
    # Everything else (type scale, spacing, the .rv reveal, the dock, the
    # pill system) is untouched case-study.css.
    "dark": True,
    "extra_css": ["motorverse-dark.css"],

    "sections": [

        # ---------------------------------------------------- Overview
        {
            "id": "overview", "classes": ["pad-lg"],
            "blocks": [
                ("head", [("eyebrow", "Overview"), ("h2", "Overview")]),
                ("overview", [
                    ("Our Design Team", ["UX/UI Designer (me)", "Design Manager"]),
                    ("Timeline", ["April 2024 – February 2025"]),
                    ("My Core Deliverables",
                     ["Research · Wireframes · Prototypes · UI design · "
                      "Developer handoff documentation"]),
                ]),
            ],
        },

        # ---------------------------------------------------- The Project
        {
            "blocks": [
                ("head", [("h2", "The Project")]),
                ("prose", [
                    ("p", "The goal was to transform Motorverse's main website and "
                          "app to align with its new motorsport and gaming brand "
                          "identity, while building anticipation for the minting "
                          "event of its first Lamborghini digital car, the "
                          "Revuelto. The Showroom and Garage pages were designed "
                          "specifically to carry that launch."),
                    ("p", "The result: over 1,000 cars minted in 26 minutes."),
                ]),
            ],
        },

        # ---------------------------------------------------- Hero video
        # ~/Desktop/Motorverse assets/video.mov, transcoded whole (41s, no
        # letterbox bar in the source, so no ar/op crop is needed beyond
        # matching its real frame ratio).
        {
            "id": "hero-video",
            "blocks": [
                ("fig", {"video": "motorverse-hero.mp4",
                         "poster": "mv-hero-poster.jpg",
                         "ar": "2940 / 1912",
                         "alt": "Screen recording of the Motorverse site"}),
            ],
        },

        # ---------------------------------------------------- The Process
        {
            "id": "process",
            "blocks": [
                ("features", [
                    (
                        [("eyebrow", "The Process"),
                         ("h2", "Started from UI style exploration"),
                         ("p", "We started with a thorough review of the client's "
                               "expectations and requirements, then audited the "
                               "existing Motorverse platform and explored several "
                               "UI directions for sign-off before committing to a "
                               "full UI set.")],
                        {"img": "mv-process.jpg",
                         "alt": "Grid of early Motorverse UI style explorations "
                                "in different colour treatments"},
                    ),
                ]),
            ],
        },

        # ---------------------------------------------------- Design
        # pad-b: 56px trailing space before the black "accent" section right
        # after it -- otherwise the paragraph butts straight against the
        # colour change with no breathing room.
        {
            "classes": ["pad-b"],
            "blocks": [
                ("head", [("h2", "Design")]),
                ("prose", [
                    ("p", "With a clear picture of what users and the business "
                          "needed, I moved into redesigning the existing product. "
                          "The aim was to align the platform with the new brand "
                          "identity, improve how information was structured and "
                          "surfaced, translate Web3 terminology so that "
                          "non-crypto-native users could follow it, and deliver a "
                          "responsive experience across desktop, tablet and "
                          "mobile."),
                ]),
            ],
        },

        # ---------------------------------------------------- Challenge: accent colour
        {
            "id": "accent", "classes": ["on-black"],
            "blocks": [
                ("features", [
                    (
                        {"img": "mv-accent-colour.jpg",
                         "alt": "Motorverse mobile screens showing green, yellow "
                                "and pink accent colours applied across plate "
                                "customisation UI"},
                        [("h2", "Multiple accent colours, applied as a system"),
                         ("p", "Brand colours were used as the accent across all "
                               "utility components, with primary buttons kept "
                               "visually consistent between web and mobile so "
                               "that the same action always looks the same, "
                               "wherever it appears.")],
                    ),
                ]),
            ],
        },

        # ---------------------------------------------------- Challenge: gradients
        {
            "id": "gradients", "classes": ["on-black"],
            "blocks": [
                ("head", [
                    ("h2", "Gradients as a brand signature"),
                    ("p", "Gradients were used throughout the pages to create a "
                          "sense of energy and movement, giving Motorverse a "
                          "distinct visual presence among other Web3 sites."),
                ]),
            ],
        },
        {
            "id": "collage", "classes": ["on-black"], "full": True,
            "blocks": [
                ("fig", {"img": "mv-gradient-collage.jpg",
                         "alt": "Two Motorverse plate-selection and rewards "
                                "screens shown with multicolour gradient "
                                "backgrounds"}),
            ],
        },

        # ---------------------------------------------------- Challenge: momentum
        {
            "id": "momentum", "classes": ["on-black"],
            "blocks": [
                ("features", [
                    (
                        [("h2", "Designing momentum into the launch"),
                         ("p", "Countdown timers, leaderboards and supporting UI "
                               "elements were used to build urgency around the "
                               "mint and drive engagement in the run-up to "
                               "launch.")],
                        {"img": "mv-momentum.jpg",
                         "alt": "Motorverse mint page showing a countdown timer, "
                                "rewards panel and the Lamborghini Revuelto "
                                "prize car"},
                    ),
                ]),
            ],
        },

        # ---------------------------------------------------- Multi-screens banner
        {
            "id": "screens", "classes": ["on-black"], "full": True,
            "blocks": [
                ("fig", {"img": "mv-screens.jpg",
                         "alt": "Collage of five Motorverse homepage and app "
                                "variants shown across desktop and mobile"}),
            ],
        },
    ],
}
