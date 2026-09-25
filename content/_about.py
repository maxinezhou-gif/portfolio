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
    # Sits above the bio on the About page. Remove this key to drop the photo.
    "photo": {
        "file": "about-maxine.jpg",
        "alt": "Maxine Zhou outdoors on a hillside trail at dusk, laughing, "
               "with wooded mountains behind her",
    },

    "bio": [
        "I’m Maxine, a London-based product designer who designs complex "
        "products. I’ve designed enterprise AI tools, design systems and a "
        "0 to 1 hardware product. I spent two years designing B2B tools for "
        "Convex Insurance, including an AI contract analysis product, an "
        "insurance platform (used by 18 underwriting teams), and a design "
        "system shared by 10 designers across 3 agencies.",

        "I’m comfortable with ambiguity. I’d rather form a point of view "
        "and test it than wait for certainty, and I like owning work from the "
        "first question to launch. My background in fine art and product "
        "design is why I care about both craft and how things actually get "
        "built.",
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
