# Launchpad — content only. No markup, no CSS.
# Run `python3 casestudy.py launchpad` from the portfolio folder to rebuild.

CASE_STUDY = {
    "slug":    "launchpad",
    "project": "Launchpad",
    "title":   "Improving underwriting efficiency through behaviour-driven design",
    "summary": "Turning user data into a smarter navigation model + dynamic viewport "
               "to provide a better decision environment.",

    # emphasised pills first, then the quiet ones
    "tags_key": ["B2B SaaS", "UX/UI", "InsurTech"],
    "tags":     ["Product Design", "2025"],

    "dock": [("Context", "context"), ("Research", "research"),
             ("Insight", "insight"), ("Design", "design"), ("Impact", "impact")],
    "next": ("Next", "design-system-migration.html"),

    "sections": [

        # ---------------------------------------------------- 01 Context
        {
            "id": "context", "classes": ["pad-lg"],
            "blocks": [
                ("head", [("eyebrow", "Context"), ("h2", "Overview")]),
                ("overview", [
                    ("My Role", ["Product Designer (Sole Designer)"]),
                    ("Responsibilities", [
                        "Next version of this product",
                        "UX analysis & insight synthesis",
                        "Interaction design",
                        "Information architecture",
                        "Stakeholder alignment",
                    ]),
                    ("The Product", [
                        "An internal underwriting application for insurance teams to "
                        "review and triage submissions, manage workflows, and make "
                        "faster and more confident decisions."
                    ]),
                ]),
            ],
        },

        {
            "blocks": [
                ("head", [("h2", "Usage at a glance"), ("note", "(In a typical month)")]),
                ("stats", [
                    ("2,720",  "Review sessions per month"),
                    ("224h",   "Total active usage"),
                    ("26min",  "Average session length"),
                    ("18",     "Teams actively using"),
                ]),
            ],
        },

        # ---------------------------------------------------- 02 Research
        {
            "id": "research", "classes": ["pad-lg", "gap-lg"],
            "blocks": [
                ("head", [
                    ("h2", "Two pages, one workflow"),
                    ("p", "Underwriters work in a high-volume, high-stakes environment "
                          "where speed and accuracy are essential. The application's "
                          "workflow centered around two primary pages:"),
                ]),
                ("scrolly", [
                    (
                        [("h3", "Pipeline View"),
                         ("small", "A table-based workspace for filtering, triaging and "
                                   "updating submissions.")],
                        {"img": "429fa4_4e748c80fe2f43b29017c32d9d3b0fa5.jpg",
                         "alt": "Pipeline view showing a table of insurance submissions "
                                "with filters and grouping",
                         "caption": "Pipeline View: the triage workspace."},
                    ),
                    (
                        [("h3", "Submission Detail"),
                         ("small", "A deep-dive view with full context, documents, "
                                   "analysis and activity history.")],
                        {"img": "429fa4_d416b84ddeca45fc8e1cf939f55f68a8.jpg",
                         "alt": "Submission detail page showing summary, ranking and "
                                "activity panels",
                         "caption": "Submission Detail: the deep-dive view."},
                    ),
                ]),

                ("head", [
                    ("eyebrow", "Research"),
                    ("h2", "Start at the UX audit"),
                    ("p", "As the sole product designer on the next version, I began "
                          "with a structured UX audit to find where the interface was "
                          "costing people time."),
                ]),
                ("fig", {"img": "429fa4_cb15cf892bcf444488324e341f870dbc.jpg",
                         "alt": "UX audit findings clustered into themes across the "
                                "product screens",
                         "caption": "Identify and prioritise UX issues by conducting "
                                    "UX Audit."}),

                ("head", [
                    ("h2", "Understanding real usage"),
                    ("p", "I analysed funnel behaviour, heat maps, feature usage and "
                          "session data to understand how underwriters actually worked."),
                ]),
                ("scrolly", [
                    (
                        [("h3", "Questions for funnel analysis"),
                         ("questions", ["Where does decision-making actually happen?",
                                        "What information do users need during triage?"])],
                        {"img": "429fa4_184c0642d417480f8554f3bb6d79b93e.jpg",
                         "alt": "Funnel chart showing session drop-off between pipeline "
                                "and submission detail",
                         "caption": "Funnel analysis across 7.09K sessions."},
                    ),
                    (
                        [("h3", "Questions for heat map"),
                         ("questions", ["Are users navigating efficiently, or "
                                        "compensating for missing context?",
                                        "How can the interface support comparison "
                                        "across submissions?"])],
                        {"img": "429fa4_a8c14759cdd74c84822e9e887ffc0a65.jpg",
                         "alt": "Annotated analysis of which areas of the submission "
                                "screen users engage with",
                         "caption": "Heat map to understand what contents users care "
                                    "the most."},
                    ),
                ]),
            ],
        },

        # ---------------------------------------------------- 03 Insight
        {
            "id": "insight", "classes": ["pad-lg"],
            "blocks": [
                ("head", [("eyebrow", "Insight"), ("h2", "What the data revealed")]),
                ("findings", [
                    "Only **46.1%** of users entered the submission detail page",
                    "The **Back button** was the most-used interaction on submission detail",
                    "Users frequently **looped** between pipeline and submission detail",
                    "Submission detail was used selectively to access specific context, "
                    "especially **summaries and notes**",
                ]),
            ],
        },

        {
            "classes": ["centred"],
            "blocks": [
                ("head", [("h2", "Why Back button dominance?")]),
                ("pull", "Fast comprehension first, depth on demand."),
                ("centred", [
                    ("p", "The pipeline view functioned as the **true decision "
                          "workspace**, while the submission detail page acted as a "
                          "short-term inspection layer."),
                    ("p", "Underwriters relied on the pipeline page for orientation and "
                          "comparison, opening submission detail primarily to "
                          "**verify context** before returning to continue their review."),
                ]),
            ],
        },

        # ---------------------------------------------------- 04 Design
        {
            "id": "design", "classes": ["pad-lg"],
            "blocks": [
                ("head", [("eyebrow", "Design"), ("h2", "Design direction")]),
                ("steps", [
                    "Rebalanced hierarchy to surface key signals closer to the pipeline.",
                    "Cut navigation overhead with pre-filtered views and filters-on-demand.",
                    "A contextual Details drawer for files, AI insights, history and notes.",
                    "An adaptive viewport for dense analysis without losing context.",
                ]),
            ],
        },

        {
            "blocks": [
                ("fig", {"img": "lp-design-decision.jpg",
                         "alt": "Set of redesigned Launchpad screens showing the new "
                                "navigation model"}),
            ],
        },

        {
            "blocks": [
                ("head", [
                    ("h2", "Reducing noise, preserving control"),
                    ("p", "I designed a 'filters-on-demand' system that reduced visual "
                          "complexity while maintaining flexibility. Frequently used "
                          "filters were prioritised, and reusable filter presets allowed "
                          "underwriters to quickly re-establish context across sessions."),
                    ("p", "I then consolidated key submission information into a "
                          "contextual drawer, reachable without leaving the pipeline."),
                ]),
                ("fig", {"video": "lp-filters.mp4", "poster": "lp-filters-poster.jpg",
                         "ar": "1500 / 853", "op": "bottom",
                         "caption": "Filters-on-demand: surfacing only what's needed, "
                                    "when it's needed."}),
                ("fig", {"img": "launchpad-details-drawer.png",
                         "alt": "Details drawer showing Notes, Activities, Files, "
                                "Synthesis and Contract tabs beside the pipeline",
                         "caption": "The Details drawer: files, synthesis, activities "
                                    "and notes in one place."}),
                ("fig", {"video": "lp-multiselect.mp4",
                         "poster": "lp-multiselect-poster.jpg",
                         "ar": "1500 / 937", "op": "center",
                         "caption": "Multi-select: acting on several submissions in a "
                                    "few clicks."}),
            ],
        },

        {
            "blocks": [
                ("head", [
                    ("h2", "Adaptive viewport for high-density data"),
                    ("p", "To accommodate dense tables, I designed an adaptive viewport "
                          "that supports uninterrupted analysis while preserving quick "
                          "access to workflow context and collaboration tools."),
                ]),
                ("fig", {"video": "lp-adaptive-detail.mp4",
                         "poster": "lp-adaptive-detail-poster.jpg",
                         "ar": "1500 / 882", "op": "bottom",
                         "caption": "The adaptive detail view, expanding to suit the "
                                    "task in hand."}),
                ("fig", {"video": "lp-dynamic-viewport.mp4",
                         "poster": "lp-dynamic-viewport-poster.jpg",
                         "ar": "1500 / 882", "op": "bottom",
                         "caption": "Dynamic viewport: the workspace adapting as the "
                                    "underwriter moves between comparison and detail."}),
            ],
        },

        # ---------------------------------------------------- 05 Impact
        {
            "id": "impact", "classes": ["pad-lg"],
            "blocks": [
                ("head", [("eyebrow", "Impact"), ("h2", "Impact")]),
                ("prose", [
                    ("p", "With over 224 hours of monthly usage, even small improvements "
                          "could scale quickly. Reducing just one minute per session "
                          "could save over 45 hours per month across underwriting teams."),
                    ("p", "Due to roadmap priorities, this work was positioned as a "
                          "future optimisation, establishing a clear, data-backed "
                          "direction for improving underwriting efficiency at scale."),
                ]),
            ],
        },
    ],
}
