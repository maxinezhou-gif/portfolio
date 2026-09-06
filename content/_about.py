"""
About page content.

Same principle as the homepage: this is DATA. `python3 about.py` turns it
into about.html. There is no HTML to write here and no CSS to touch.

Maxine's brief: "a pic of me, a short intro, and links" — the niklas.space
/about pattern, kept deliberately shorter than his (no experience table, no
awards list). See home.py's own header comment for the shared column and
typography this reuses.
"""

LOWERCASE = False

ABOUT = {
    "title": "About — Maxine Zhou",
    "summary": "Product designer working on AI-powered SaaS. Background, "
               "and what I'm looking for next.",

    "heading": "About",
    "bio": [
        "Over the past two years, I’ve designed products for a global "
        "insurance organisation, including an AI contract analysis product, "
        "a design system migration across 10+ designers from multiple "
        "agencies (which reduced custom component work by **94%**), and a "
        "redesigned insurance platform used by **68 underwriters across 18 "
        "teams** (2,700+ monthly sessions).",

        "I particularly enjoy working on AI products where clarity, "
        "consistency and long-term scalability are as crucial as usability.",
    ],

    # Same three as the homepage's tail group — kept in sync by hand, since
    # they rarely change.
    "links": [
        {"name": "Resume", "desc": "PDF",
         "href": "assets/doc/maxine-zhou-resume.pdf"},
        {"name": "Email", "desc": "maxinezhou0302@outlook.com",
         "href": "mailto:maxinezhou0302@outlook.com"},
        {"name": "LinkedIn", "desc": "in/maxine-z",
         "href": "https://www.linkedin.com/in/maxine-z-90281422b/"},
    ],

    "foot": "© 2026 Maxine Zhou",
}
