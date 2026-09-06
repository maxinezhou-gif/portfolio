# Enterprise design system migration — content only.
# Copy sourced from maxinezhou03024.wixsite.com/mysite/projects/designsystemmigration
# Before/after screens from ~/Downloads/DS (the "no corner radius" exports).
# Rebuild:  python3 casestudy.py design-system-migration

CASE_STUDY = {
    "slug":    "design-system-migration",
    "project": "Convex Design System",
    "title":   "Enterprise design system migration",
    "summary": "Led a design system migration across a 16-product insurance ecosystem, "
               "cutting custom components by **94%** and establishing governance across "
               "three design agencies.",

    "tags_key": ["Design System", "Design Ops", "InsurTech"],
    "tags":     ["Strategy", "2025"],

    "dock": [("Context", "context"), ("Challenge", "challenge"),
             ("Approach", "approach"), ("Impact", "impact")],
    "next": ("Next", "launchpad.html"),

    "sections": [

        # ---------------------------------------------------- Context
        {
            "id": "context", "classes": ["pad-lg"],
            "blocks": [
                ("head", [("eyebrow", "Overview"), ("h2", "Overview")]),
                ("overview", [
                    ("Our Design Team", [
                        "Design System Designer (me)",
                        "Design Manager",
                    ]),
                    ("Timeline", ["March – December 2025 (10 months)"]),
                    ("My Core Deliverables", [
                        "Four products migrated, three in active progress",
                        "Design library fully built, aligned with Storybook",
                        "Documentation and governance frameworks established",
                        "Design team culture transformed from siloed to collaborative",
                        "Client set up to scale the system independently",
                    ], True),
                ]),
            ],
        },

        {
            "blocks": [
                ("head", [("h2", "The Product")]),
                ("prose", [
                    ("p", "An internal underwriting application for insurance teams to "
                          "review and triage submissions, manage workflows, and make "
                          "faster and more confident decisions."),
                ]),
            ],
        },

        {
            "blocks": [
                ("head", [("h2", "Impacts")]),
                ("stats", [
                    ("49",        "components with full tokenisation and documentation"),
                    ("35% → 2%",  "reduction in custom components (core product pilot)"),
                    ("10",        "designers across three agencies aligned"),
                    ("7",         "products migrated or in progress"),
                ]),
            ],
        },

        # ---------------------------------------------------- The Challenge
        {
            "id": "challenge", "classes": ["pad-lg"],
            "blocks": [
                ("head", [
                    ("eyebrow", "Challenge"),
                    ("h2", "The Challenge"),
                    ("p", "The client operated **16+ products** built by multiple "
                          "contractors, with significant operational challenges:"),
                ]),
                ("bullets", [
                    "**83%** of design work required custom components, due to the "
                    "limitations of the existing design system",
                    "Three separate design agencies worked in **silos**, with "
                    "inconsistent practices",
                    "Designers skipped collaboration meetings and worked independently",
                    "**Fragmented user experiences** across the product portfolio",
                    "**No clear governance** on when or how to extend the design system",
                ]),
            ],
        },

        {
            "classes": ["pad-b"],
            "blocks": [
                ("head", [("h2", "What my role brought")]),
                ("bullets", [
                    "Build and organise the design library and documentation",
                    "Provide design system services and support to designers across agencies",
                    "Establish governance processes for consistent adoption",
                    "Lead a pilot migration to demonstrate value and approach",
                    "Transform team culture from siloed to collaborative",
                ]),
            ],
        },

        # ---------------------------------------------------- Before / After
        # No separate intro heading here -- Figma's metadata confirms the
        # reveal section sits directly after "What my role brought" with
        # nothing between them. (The old intro copy lived here before this
        # page was rebuilt against the current Figma file.)

        # Full-bleed crossfade. Swap these two filenames for the Figma frame
        # exports when they land — nothing else needs to change.
        {
            "full": True,
            "blocks": [
                ("reveal", {
                    "before": {"img": "ds-before.jpg", "label": "Before",
                               "body": "Ad-hoc components, inconsistent spacing, and a "
                                       "narrower activities panel with no tab structure.",
                               "alt": "Submission detail screen before migration, with a "
                                      "light header and a two-tab activities panel"},
                    "after":  {"img": "ds-after.jpg", "label": "After",
                               "body": "Design system components throughout, semantic "
                                       "tokens, and a fuller Activities Hub with five tabs.",
                               "alt": "The same submission detail screen after migration, "
                                      "using design system components and a five-tab "
                                      "Activities Hub"},
                }),
            ],
        },

        # ---------------------------------------------------- Approach
        {
            "id": "approach", "classes": ["pad-lg", "gap-lg"],
            "blocks": [
                ("head", [
                    ("eyebrow", "Approach"),
                    ("h2", "Four phases over ten months"),
                ]),

                ("features", [
                    (
                        [("h2", "Phase 1\nFoundation building"),
                         ("numbered", [
                             "Built the Design Library covering the full product ecosystem",
                             "Tokenised design foundations and component documentation",
                             "Established a cleaned-up **Storybook** as the single "
                             "source of truth",
                             "Provided designer support infrastructure across all "
                             "three agencies",
                         ])],
                        {"img": "ds-support.jpg",
                         "alt": "The assembled design library, showing components, "
                                "variants and typography documentation across the "
                                "product ecosystem"},
                    ),
                ]),

                ("features", [
                    (
                        {"img": "ds-phase2.jpg",
                         "alt": "Flow diagram of the component contribution process, "
                                "from an ad-hoc request through to a light, medium or "
                                "heavy contribution",
                         "caption": "Phase 2 · Governance & quality assurance"},
                        [("h2", "Phase 2\nGovernance & Quality Assurance"),
                         ("numbered", [
                             "Conducted UX audits and regular design check-ins across "
                             "agencies to identify drift",
                             "Documented an **Exception Framework** for when deviations "
                             "make sense, balancing system integrity with design flexibility",
                             "Hosted pattern workshops across agencies to identify "
                             "reusable patterns",
                         ])],
                    ),
                ]),

                # Folded into Approach rather than a standalone dock section --
                # this is where the conflict actually happened in the narrative.
                # Plain sequential text, left-aligned, 880px column (extra
                # .inset on top of the normal 1160) -- Figma has no callout box
                # here. Only the heading + sticker row is centred, per Maxine.
                ("div", {"classes": ["inset", "stack-40"], "blocks": [
                    ("div", {"classes": ["insight-heading"], "blocks": [
                        ("h2", "The Challenge I faced at Phase 2"),
                        ("raw", '<span class="conflict-sticker-slot">'
                                '<span class="conflict-sticker" aria-hidden="true">Conflicts</span>'
                                '</span>'),
                    ]}),
                    ("head", [
                        ("eyebrow", "What happened?"),
                        ("p", "While reviewing mockups I noticed many components were heavily "
                              "customised — spacing, padding and text weights all differed "
                              "from the design system."),
                    ]),
                    ("head", [
                        ("eyebrow", "The tension"),
                        ("p", "Product designers wanted to preserve user familiarity.\n"
                              "The design system manager questioned the purpose of "
                              "migration if the visuals stayed unchanged."),
                    ]),
                    ("head", [
                        ("eyebrow", "What I did to solve it"),
                        ("numbered", [
                            "Clarified intent:\n**Migration means technical adoption and "
                            "gradual alignment, not forced visual conformity.**",
                            "Defined a path forward:\nPhase 1 — design system components "
                            "with overrides;\nPhase 2 — reassess after research and user "
                            "acceptance testing.",
                            "Process improvement:\nProposed an Exception Framework to "
                            "document justified divergences from the system.",
                        ]),
                    ]),
                    ("fig", {"img": "ds-exception.jpg",
                             "alt": "Message to the design team proposing the Exception Framework",
                             "caption": "Taking the proposal to the whole team, in the open."}),
                ]}),

                ("features", [
                    (
                        [("h2", "Phase 3\nStrategic Migration"),
                         ("p", "We ran a low-risk pilot on a simple product to validate "
                               "the process and build team confidence, then migrated "
                               "the essential product to showcase impact."),
                         ("p", "During migration, we fixed some UX issues, applied "
                               "semantic tokens, and improved predictability with a "
                               "unified visual language."),
                         ("h3", "Result: 35% → 2% custom components")],
                        {"img": "ds-phase3.jpg",
                         "alt": "A UX audit table listing issues, notes, effort and priority "
                                "found during the migration"},
                    ),
                ]),

                ("features", [
                    (
                        {"img": "ds-phase4.jpg",
                         "alt": "A calendar of recurring design system rituals — design "
                                "catchups, critiques and office hours — alongside a dev "
                                "handoff checklist"},
                        [("h2", "Phase 4\nScaling & Enablement"),
                         ("numbered", [
                             "Transformed siloed agencies into a collaborative community",
                             "Completed four product migrations, three in progress, "
                             "planned completion by the end of the year",
                             "Client equipped to continue independently with "
                             "established processes",
                         ])],
                    ),
                ]),
            ],
        },

        # ---------------------------------------------------- Impact
        {
            "id": "impact", "classes": ["pad-lg"],
            "blocks": [
                # Figma nests this inside the Approach frame and narrows it to
                # 880px (extra .inset), left-aligned, numbered not bulleted.
                # Kept as its own top-level section rather than moved inside
                # Approach's markup: the dock-nav highlighting relies on
                # IntersectionObserver watching a full section's worth of
                # scroll height, which a nested anchor point can't give it.
                ("div", {"classes": ["inset"], "blocks": [
                    ("head", [("eyebrow", "Impact"), ("h2", "Impact for the business")]),
                    ("numbered", [
                        "Drastic reduction in design and handoff time as system coverage grew",
                        "A migration approach proven through a pilot that other teams can replicate",
                        "The team now owns and evolves the design system together",
                    ]),
                ]}),
            ],
        },

        # Collapsed by default -- click "My reflects" to open.
        {
            "classes": ["pad-lg"],
            "blocks": [
                ("collapsible", {
                    "toggle": "My reflects",
                    "panel_id": "reflect-panel",
                    "blocks": [
                        ("head", [("eyebrow", "Reflects"), ("h2", "Reflection and learnings")]),
                        ("bullets", [
                            "Design system migration is as much about **people and process** as "
                            "components. Building trust by supporting designers proactively is the key.",
                            "I came to understand the importance of **change management**: "
                            "balancing consistency against designers' real needs.",
                            "Stakeholder communication and systems thinking are essential.",
                            "Finally, I learnt to **choose the battle**. We paused migration on one "
                            "product with fewer than 10 active users — its designers were reluctant "
                            "to migrate our way, and re-onboarding them at every check-in was "
                            "costing more than it returned.",
                        ]),
                        ("features", [
                            (
                                [("h3", "Weekly updates kept adoption visible"),
                                 ("p", "Release notes in the open, every week. Designers stopped "
                                       "being surprised by a change, which is most of what "
                                       "trust in a design system actually is.")],
                                {"img": "ds-weekly.jpg",
                                 "alt": "Weekly design system update posted to the team channel, "
                                        "listing new and updated components"},
                            ),
                            (
                                [("h3", "The real signal of success"),
                                 ("p", "Designers coming to the system **before** building "
                                       "around it. Nobody asked them to — the question simply "
                                       "became easier than the workaround.")],
                                {"img": "ds-sorting.jpg",
                                 "alt": "A designer asking for guidance on which sorting "
                                        "pattern to use"},
                            ),
                        ]),
                    ],
                }),
            ],
        },
    ],
}
