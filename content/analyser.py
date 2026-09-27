# Analyser — content only. No markup, no CSS.
# Copy sourced verbatim from maxinezhou03024.wixsite.com/mysite/projects/analyser
# Videos from ~/Downloads/Analyser (the high-res source recordings).
# Run `python3 casestudy.py analyser` from the portfolio folder to rebuild.

CASE_STUDY = {
    "slug":    "analyser",
    "project": "Analyser",
    "title":   "AI-Augmented Contract documents Analysis Platform",
    "summary": "Owned end-to-end design of an AI-assisted contract analysis "
               "platform, bringing workflows scattered across 5+ tools into one "
               "product. The product has since been white-labelled and sold as a "
               "service by the AI development partner.",

    "tags_key": ["AI / ML", "B2B SaaS", "Workflow", "InsurTech"],
    "tags":     [],

    "dock": [("Context", "context"), ("Research", "research"),
             ("Insight", "insight"), ("Design", "design")],
    "next": ("Next", "launchpad.html"),

    "sections": [

        # ---------------------------------------------------- Context
        {
            "id": "context", "classes": ["pad-lg"],
            "blocks": [
                ("head", [("eyebrow", "Context"), ("h2", "Overview")]),
                ("overview", [
                    ("My Role", ["Product Designer (Sole Designer)"]),
                    ("Key Outcomes", [
                        "Streamlined contract review during critical renewal periods",
                        "Designed Continuous AI Training in workflow that felt natural to users",
                        "Built user trust through transparent AI verification design",
                    ]),
                    ("Additional Complexity", [
                        "Remote collaboration with a dev team in France",
                        "Tech constraints: LLM latency and inability to build a specific layout",
                        "Ecosystem consistency: aligned with two products and fed insights "
                        "into a core product",
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
                          "faster and more confident decisions"),
                ]),
            ],
        },

        # ---------------------------------------------------- The Problem
        {
            "blocks": [
                ("head", [
                    ("eyebrow", "The Problem"),
                    ("h2", "Fragmented, High-Stakes Workflows"),
                    ("p", "During busy renewal periods, underwriters analyse hundreds of "
                          "reinsurance and insurance contracts under tight deadlines. Their "
                          "workflow is chaotic—constantly switching between:"),
                ]),
                ("bullets", [
                    "Contract PDFs",
                    "Email chains",
                    "Notes documents",
                    "Slack conversations",
                    "Dropbox files",
                ]),
                ("head", [("h3", "Need a solution that could")]),
                ("bullets", [
                    "Make contract review instantaneous, not time-consuming",
                    "Simplify checking against complex underwriting rules",
                    "Reduce compliance risk and financial exposure",
                ]),
                ("pull", "How might we accelerate contract analysis without compromising "
                         "thoroughness, accuracy, or user confidence in AI-generated insights?"),
            ],
        },

        # ---------------------------------------------------- Research
        {
            "id": "research", "classes": ["pad-lg"],
            "blocks": [
                ("head", [
                    ("eyebrow", "Research"),
                    ("h2", "Research and Discovery"),
                    ("p", "I conducted stakeholder interviews with underwriters and "
                          "product managers to understand their workflows, pain points, "
                          "and needs during high-pressure renewal periods."),
                ]),
                ("head", [("h3", "Key Insights that shaped design")]),
                ("bullets", [
                    "Navigation must be instantaneous and mirror document’s natural flow",
                    "Users question AI accuracy, design should communicate transparency "
                    "and verifiable sources",
                    "AI assistance should feel like productive work, not extra overhead",
                ]),
            ],
        },

        # ---------------------------------------------------- Insight (Design Evolution)
        {
            "id": "insight", "classes": ["pad-lg"],
            "blocks": [
                ("head", [
                    ("h2", "Design Evolution"),
                    ("p", "I went through three distinct layout approaches, testing each "
                          "with PMs and users to land on the optimal information hierarchy "
                          "that also fit within the dev team's technical constraints."),
                ]),
                ("steps", [
                    {"title": "Early Prototype",
                     "text": "This is what the UI looked like when I first joined "
                             "the project.\n#Christmas tree #Unclear IA #Long scroll "
                             "#Content gets lost",
                     "img": "an-evo1.jpg",
                     "alt": "The early prototype layout for the contract analysis "
                            "screen, before the redesign"},
                    {"title": "Explored Modal-Based Details (users’ fav)",
                     "text": "Rebalanced the information hierarchy across multiple "
                             "layers of detail\nConsolidated all detailed information "
                             "in a modal to minimise visual noise\n(blocked by dev "
                             "team due to tech constrains)",
                     "img": "an-evo2.jpg",
                     "alt": "The explored modal-based details layout, consolidating "
                            "information in a modal"},
                    {"title": "Hybrid Tabs + Accordion (final)",
                     "text": "Parent accordions organised by document section "
                             "(mirroring contract order)\nEnable users to do "
                             "side-by-side comparison with one click",
                     "img": "an-evo3.jpg",
                     "alt": "The final hybrid tabs and accordion layout, organised "
                            "by document section"},
                ]),
            ],
        },

        # ---------------------------------------------------- Design
        {
            "id": "design", "classes": ["pad-lg"],
            "blocks": [
                ("head", [
                    ("eyebrow", "Design"),
                    ("h2", "Design Decision"),
                    ("p", "Detected wording is compared against preferred language in a "
                          "clear side-by-side view with concise risk summaries, enabling "
                          "decisions in seconds."),
                ]),
                # AI-Powered Comparison -- stacked full-width in Figma, not a
                # side-by-side row: heading+body first, then a full-bleed video.
                ("h3", "AI-Powered Comparison with Source Verification"),
                ("fig", {"video": "an-comparison.mp4", "poster": "an-comparison-poster.jpg",
                         "ar": "1920 / 1280", "op": "center",
                         "alt": "Contract clause compared against criteria, with detected "
                                "text linked back to the source PDF"}),

                # Human-in-the-Loop -- also stacked full-width: heading+body,
                # then a video + a static image side by side, not a single
                # text+media row.
                ("head", [
                    ("h3", "Human-in-the-Loop Machine Training"),
                    ("p", "Underwriters can quickly verify or relink AI-detected text "
                          "within the “Text” view, embedding feedback directly "
                          "into their normal review workflow."),
                ]),
                ("div", {"classes": ["media-pair"], "blocks": [
                    ("fig", {"video": "an-feedback.mp4", "poster": "an-feedback-poster.jpg",
                             "ar": "1758 / 1000", "op": "bottom",
                             "alt": "Rating an AI-detected result to feed accuracy "
                                    "back into the model"}),
                    ("fig", {"img": "an-relink-empty.jpg",
                             "alt": "The relink empty state, prompting the underwriter "
                                    "to select text from the PDF to teach the system"}),
                ]}),

                ("features", [
                    (
                        [("h3", "Natural Review Workflow"),
                         ("p", "Key validation actions are surfaced at the point of "
                               "review, enabling one-step decisions and preserving "
                               "underwriters’ analytical flow.")],
                        {"video": "an-verify.mp4", "poster": "an-verify-poster.jpg",
                         "ar": "1920 / 1280", "op": "center",
                         "alt": "Working through a list of flagged exclusion clauses, "
                                "each with its own verification status"},
                    ),
                ]),

                # Action List repeats as its own full-width hero shot in Figma --
                # the compact row above, then this dedicated close-up.
                ("head", [
                    ("h3", "Action List for Faster Collaboration"),
                    ("p", "Instead of jumping between components to recall what needs "
                          "discussion, underwriters get a consolidated view of every "
                          "flagged item, suggested alternative, and comment at a glance. "
                          "When everything checks out, a single 'Finish Validation' "
                          "click closes the loop."),
                ]),
                ("fig", {"img": "an-action-list.jpg",
                         "alt": "Action List showing every flagged clause with its "
                                "suggested replacement, and a single Finish Validation "
                                "action to close out the review"}),
            ],
        },
    ],
}
