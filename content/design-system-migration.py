# Enterprise design system migration — content only.
# Copy sourced from maxinezhou03024.wixsite.com/mysite/projects/designsystemmigration
# Before/after screens from ~/Downloads/DS (the "no corner radius" exports).
# Rebuild:  python3 casestudy.py design-system-migration

CASE_STUDY = {
    "slug":    "design-system-migration",
    "project": "Design System 2.0",
    "title":   "Enterprise design system migration",
    "summary": "Led a design system migration across a 16-product insurance ecosystem, "
               "cutting custom components by **94%** and establishing governance across "
               "three design agencies.",

    "tags_key": ["Design System", "Design Ops", "InsurTech"],
    "tags":     ["Strategy", "2025"],

    "dock": [("Context", "context"), ("Challenge", "challenge"),
             ("Approach", "approach"), ("Conflict", "conflict"), ("Impact", "impact")],
    "next": ("Next", "launchpad.html"),

    "sections": [

        # ---------------------------------------------------- Context
        {
            "id": "context", "classes": ["pad-lg"],
            "blocks": [
                ("head", [("eyebrow", "Context"), ("h2", "Overview")]),
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
                    ]),
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
        {
            "blocks": [
                ("head", [
                    ("h2", "The same screen, before and after"),
                    ("p", "Migration was never meant to be a visual redesign. The value "
                          "shows in consistency, tokenisation and predictability rather "
                          "than a dramatic before-and-after. Scroll to cross-fade between "
                          "the two."),
                ]),
            ],
        },

        # Full-bleed crossfade. Swap these two filenames for the Figma frame
        # exports when they land — nothing else needs to change.
        {
            "full": True,
            "blocks": [
                ("reveal", {
                    "before": {"img": "ds-before.jpg", "label": "Before",
                               "alt": "Submission detail screen before migration, with a "
                                      "light header and a two-tab activities panel"},
                    "after":  {"img": "ds-after.jpg", "label": "After",
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
                    ("p", "Migration was not a single project. It ran as four phases, "
                          "each one earning the trust the next depended on."),
                ]),

                ("chapter", "Phase 1 · Foundation building"),
                ("features", [
                    (
                        [("h3", "A design library for the whole ecosystem"),
                         ("p", "Built the library covering all 16 products, tokenised "
                               "the foundations, and established a cleaned-up "
                               "**Storybook** as the single source of truth.")],
                        {"img": "429fa4_1c3a8c2e3fb5442bb06d134f647be1cf.jpg",
                         "alt": "The assembled design library, showing components "
                                "across the product ecosystem"},
                    ),
                    (
                        [("h3", "Support, not just artefacts"),
                         ("p", "A library nobody knows how to use is shelfware. I ran "
                               "critiques, pattern workshops and a standing office "
                               "hour across all three agencies.")],
                        {"img": "429fa4_35d8c4aab5bb4b30a2c00b58c163b781.jpg",
                         "alt": "Cards for design critique, pattern workshops and a "
                                "design system office hour"},
                    ),
                ]),

                ("chapter", "Phase 2 · Governance & quality assurance"),
                ("features", [
                    (
                        [("h3", "Audits to catch drift early"),
                         ("p", "Regular UX audits and design check-ins across agencies, "
                               "so divergence surfaced in weeks rather than quarters.")],
                        {"img": "429fa4_2aece0e687e544a0b895414de8f9772f.jpg",
                         "alt": "UX audit documents from 2025"},
                    ),
                    (
                        [("h3", "A contribution process, made explicit"),
                         ("p", "A **3–4 week prioritisation pipeline** and a documented "
                               "path for proposing components, so extending the system "
                               "stopped being a matter of who you asked.")],
                        {"img": "429fa4_d861706d33a4423b95920f6aa3351b15.jpg",
                         "alt": "Flow diagram of the component contribution process"},
                    ),
                ]),
            ],
        },

        # ---------------------------------------------------- The conflict
        {
            "id": "conflict", "classes": ["pad-lg"],
            "blocks": [
                ("head", [
                    ("eyebrow", "Conflict"),
                    ("h2", "The challenge I faced at Phase 2"),
                ]),
                ("callout", [
                    ("label", "What happened"),
                    ("p", "While reviewing mockups I noticed many components were heavily "
                          "customised — spacing, padding and text weights all differed "
                          "from the design system."),
                    ("label", "The tension"),
                    ("p", "Product designers wanted to preserve user familiarity. The "
                          "design system manager questioned the purpose of migration if "
                          "the visuals stayed unchanged."),
                    ("label", "What I did to resolve it"),
                    ("bullets", [
                        "**Clarified intent:** migration means technical adoption and "
                        "gradual alignment, not forced visual conformity.",
                        "**Defined a path forward:** Phase 1 — design system components "
                        "with overrides; Phase 2 — reassess after research and user "
                        "acceptance testing.",
                        "**Improved the process:** proposed an Exception Framework to "
                        "document justified divergences from the system.",
                    ]),
                ]),
                ("fig", {"img": "429fa4_81783366317148b9af57efeb531cf56d.jpg",
                         "alt": "Message to the design team proposing the Exception Framework",
                         "caption": "Taking the proposal to the whole team, in the open."}),
            ],
        },

        {
            "classes": ["gap-lg"],
            "blocks": [
                ("chapter", "Phase 3 · Strategic migration"),
                ("prose", [
                    ("p", "We ran a low-risk pilot on a simple product to validate the "
                          "process and build team confidence, then migrated the "
                          "essential product to showcase impact. Along the way we fixed "
                          "UX issues, applied semantic tokens, and improved "
                          "predictability with a unified visual language."),
                ]),
                ("pull", "35% → 2% custom components."),

                ("chapter", "Phase 4 · Scaling & enablement"),
                ("features", [
                    (
                        [("h3", "Weekly updates kept adoption visible"),
                         ("p", "Release notes in the open, every week. Designers stopped "
                               "being surprised by a change, which is most of what "
                               "trust in a design system actually is.")],
                        {"img": "429fa4_46c62b14bcb44e5d97ceb07d58778ec3.jpg",
                         "alt": "Weekly design system update posted to the team channel"},
                    ),
                    (
                        [("h3", "The real signal of success"),
                         ("p", "Designers coming to the system **before** building "
                               "around it. Nobody asked them to — the question simply "
                               "became easier than the workaround.")],
                        {"img": "429fa4_dbe8db9a448b4e6e9d7e10cb47d11eb9.jpg",
                         "alt": "A designer asking for guidance on the sorting pattern"},
                    ),
                ]),
            ],
        },

        {
            "blocks": [
                ("chapter", "Three products · In progress"),
                ("prose", [
                    ("p", "Four products are migrated and three are in flight, with "
                          "completion planned by the end of the year. The client now "
                          "runs the process without me — which was the actual goal."),
                ]),
            ],
        },

        # ---------------------------------------------------- Impact
        {
            "id": "impact", "classes": ["pad-lg"],
            "blocks": [
                ("head", [("eyebrow", "Impact"), ("h2", "Impact for the business")]),
                ("bullets", [
                    "Drastic reduction in design and handoff time as system coverage grew",
                    "A migration approach proven through a pilot that other teams can replicate",
                    "The team now owns and evolves the design system together",
                ]),
            ],
        },

        {
            "blocks": [
                ("head", [("h2", "Reflection and learnings")]),
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
            ],
        },
    ],
}
