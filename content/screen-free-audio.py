# Screen-free audio — content only. No markup, no CSS.
# Run `python3 casestudy.py screen-free-audio` from the portfolio folder.
#
# Copy is "case study copy .rtf" (Desktop, 11 Nov 16:29), kept as close to
# her sentences as grammar allows. Where a line needed fixing it was fixed in
# place, not rewritten.
#
# NO DASHES. 11 Nov, her instruction: no hyphen or dash punctuation anywhere
# in the copy. Em dashes are gone; the sentences are split or joined with
# commas instead. Hyphens INSIDE her own compound words are kept, because
# they are hers: screen-free, low-tech, nice-to-have, drag-to-reorder,
# one-time, lo-fi. Don't reintroduce "—" when editing this file.
#
# NO CAPTIONS. 11 Nov, her instruction: every figure runs without a
# figcaption. The generator still supports them; this page does not use them.
#
# ANONYMISATION. The product, the client and the mechanism stay at category
# level. Her source names "kids story book" in the Prototype section; that is
# the one phrase paraphrased rather than corrected. "nursery educators" is
# her own wording and is kept.

CASE_STUDY = {
    "slug":    "screen-free-audio",
    "project": "Connected learning device",
    "title":   "Screen-free audio player for kids",
    "summary": "An app to manage the player devices, set up customised audio "
               "content, browse the library and receive important alerts.",

    # The hero meta lines, as pills: emphasised first, then the quiet ones.
    #
    # "iOS & Android" is kept, but her copy says the MVP was tested on iOS
    # while principle 2 is about being native on both. One of the two wants
    # changing. Flagged, not guessed.
    "tags_key": ["Client work", "Pre-launch", "Details anonymised"],
    "tags":     ["Product Designer", "iOS & Android", "2026"],

    # Labels kept short: the dock clips to a scrolling track, and a wider set
    # pushes the last pill out of sight at 390px.
    "dock": [("Intro", "intro"), ("Principles", "principles"),
             ("Flows", "flows"), ("Testing", "testing"),
             ("Prototype", "prototype")],
    "next": ("Next", "launchpad.html"),

    # Every figure loses the card and gets an 8px corner and a soft shadow
    # instead. Chosen 11 Nov 2026 off explore/container-styles.html, where
    # six treatments were compared against this page's own media. The other
    # case studies keep the card.
    "media": "plain",

    "sections": [

        # ---------------------------------------------------- Hero loop
        # Held to the content column, not the viewport: its edges land exactly
        # under "Maxine Zhou" and "About", because the top bar uses the same
        # .wrap. "media": "plain" is what makes the media's own edges the
        # figure's edges; the default card would inset it 21px and lose it.
        #
        # The source fills its frame edge to edge, no letterbox, so `ar` is
        # simply the file's own 1600x944.
        {
            "blocks": [
                ("fig", {"video": "sfa-hero.mp4", "poster": "sfa-hero-poster.jpg",
                         "ar": "1600 / 944", "op": "center"}),
            ],
        },

        # ---------------------------------------------------- Intro
        {
            "id": "intro", "classes": ["pad-lg"],
            "blocks": [
                ("prose", [
                    ("p", "A client is rethinking what a screen-free interactive "
                          "learning experience for kids can be."),
                    ("p", "I designed a mobile app for nursery educators and parents "
                          "to set up the device and customise the audio content, "
                          "before letting kids have a go."),
                    ("p", "Because the device never needs the app, and only "
                          "communicates with a few light signals, I had to make sure "
                          "every message that cannot be communicated through the "
                          "hardware is delivered via this app."),
                    ("p", "I was the sole product designer, taking the app from the "
                          "first workshop with the client to a tested MVP on iOS, "
                          "covering the PM work and collaborating closely with the "
                          "industrial design, firmware and engineering partners."),
                ]),
            ],
        },

        # ---------------------------------------------------- Principles
        {
            "id": "principles", "classes": ["pad-lg"],
            "blocks": [
                ("head", [("eyebrow", "Principles"), ("h2", "App principles")]),
                ("prose", [
                    ("p", "**The app shows what the device can't.** The hardware has "
                          "only a few light signals, so status, battery, sync and "
                          "errors live in the app."),
                    ("p", "**Native on both platforms.** iOS and Android differ "
                          "wherever the operating system expects them to, especially "
                          "for edge scenarios relating to connections and statuses, "
                          "so I prepared different UX copy for both."),
                    ("p", "**The app is designed for low-tech users.** It needs to be "
                          "simple enough for nursery educators to complete setup and "
                          "audio content preparation on their own, even in a loud "
                          "classroom with many distractions."),
                ]),

                # Same kind of Figma export as the hero, so the same treatment:
                # `ar` is the file's own 1600x774 and it fills its frame edge
                # to edge, no letterbox.
                ("fig", {"video": "sfa-principles.mp4",
                         "poster": "sfa-principles-poster.jpg",
                         "ar": "1600 / 774", "op": "center"}),
            ],
        },

        # ---------------------------------------------------- The two flows
        # Not in her copy file: she asked for this section separately, and the
        # body text is DRAFT, the only copy on the page that is not hers.
        # Built from the sheet behaviour visible in the demos and her own line
        # about the key experience taking more than 10 stepped actions with
        # multiple handovers. No number is quoted, because that line counts
        # actions, not pages.
        #
        # BOTH rows are (text, fig). 11 Nov, her instruction: the two blocks
        # share one layout, text left and media right, so the two text columns
        # start on the same line down the page. Do not alternate these.
        #
        # "rows-flush" puts that text on the page's own left margin instead of
        # 96px in from it, which is where a centred feature row lands. See the
        # rule of that name in case-study.css.
        #
        # The media is a recording of each hero demo, not the demo itself.
        # Embedding them live worked, but Netlify injects a "Powered by
        # Netlify" badge into every page it serves on the free plan, and it
        # cannot be turned off from the account, so the badge rode along
        # inside both blocks. Recordings carry no host.
        #
        # SETTLED 11 Nov 2026, Maxine's call: the record demo shows "Link
        # tag" on a button, which names the mechanism the rest of the page
        # keeps at category level. It stays. Re-recording costs more than the
        # leak is worth, and the word carries no product name. Don't raise
        # this again or quietly re-cut the video.
        #
        # `ar` is the recordings' own 1200x1500 rather than the 4/5 it
        # reduces to: if a re-record ever comes back a different size, the
        # mismatch is visible here instead of silently letterboxing.
        #
        # "fit": "contain" so neither the cover crop nor the 1.021 scale that
        # hides screenshot corner-rounding can take a slice off the phone.
        {
            "id": "flows", "classes": ["pad-lg", "gap-lg", "rows-flush"],
            "blocks": [
                ("head", [("eyebrow", "The app"), ("h2", "Two flows")]),

                ("features", [
                    (
                        [("h3", "Recording a page"),
                         ("p", "Educators record one piece of audio per page, "
                               "several in a row. The sheet opens over the list "
                               "rather than on its own screen, so a finished "
                               "recording drops into place and the next one starts "
                               "without leaving the list. Fewer taps, and fewer "
                               "handovers between the phone and the device.")],
                        {"video": "sfa-flow-record.mp4",
                         "poster": "sfa-flow-record-poster.jpg",
                         "ar": "1200 / 1500", "fit": "contain"},
                    ),
                    (
                        [("h3", "Reordering pages"),
                         ("p", "The list is the playback order, not just "
                               "housekeeping: whatever sits second is what plays "
                               "second. Pages can be dragged into place afterwards, "
                               "so recording one page's audio onto another doesn't "
                               "mean recording it again.")],
                        {"video": "sfa-flow-reorder.mp4",
                         "poster": "sfa-flow-reorder-poster.jpg",
                         "ar": "1200 / 1500", "fit": "contain"},
                    ),
                ]),
            ],
        },

        # ---------------------------------------------------- Testing
        # "fit": "contain" on the figure: a flat composite on a cream ground,
        # with labels close to the edge and no baked-in rounded corner to
        # hide. The default 1.021 scale would shave ~2% off every edge and
        # take the top of "Tooltip as a..." with it.
        {
            "id": "testing", "classes": ["pad-lg", "gap-lg"],
            "blocks": [
                ("head", [
                    ("eyebrow", "Testing"),
                    ("h2", "What user testing sessions changed"),
                    ("small", "Remote sessions with the founder and four educators, "
                              "aged 26 to 52, using the coded prototype and Figma."),
                ]),

                ("fig", {"img": "sfa-testing-changes.jpg", "fit": "contain",
                         "alt": "Three screens side by side: the recording sheet "
                                "before testing with an icon-only control, the same "
                                "sheet afterwards with a labelled text button, and "
                                "the tile list showing a tooltip that reads “Hold and "
                                "drag to reorder”"}),

                ("findings", [
                    "**Universal icon is not very clear.** 4 out of 5 educators "
                    "couldn't tell how to redo a recording, so I changed the icon to "
                    "a labelled “Redo” button.",

                    "**Give nice-to-have features a hint.** No one found "
                    "drag-to-reorder, they'd re-record instead. It mainly helps "
                    "experienced users, so I added a one-time tooltip to introduce "
                    "it, rather than a louder control.",
                ]),
            ],
        },

        # ---------------------------------------------------- Prototype
        # "kids story book" in her source is paraphrased here: it is the one
        # line where the copy would otherwise name the format.
        #
        # The CTA is a real link again. The 9 Nov decision to leave it as
        # plain text is SUPERSEDED by her 11 Nov instruction for a pill
        # button, which is what the new `cta` block in casestudy.py is for.
        {
            "id": "prototype", "classes": ["pad-lg"],
            "blocks": [
                ("head", [("eyebrow", "Prototype"),
                          ("h2", "Explored and tested in code, refined in Figma")]),
                ("prose", [
                    ("p", "The key experience requires users to make stepped actions "
                          "more than 10 times, and multiple handovers (between the "
                          "phone, the player device and the object in the child's "
                          "hands), so I built the lo-fi prototype in code with Claude "
                          "Code to do experiments and find the flow with fewer taps "
                          "and handovers."),
                    ("p", "I also built a prototype index page so that I can pull out "
                          "the flows I want to test with people and get their "
                          "feedback quickly."),
                ]),
                ("cta", {"label": "Try prototype",
                         "href": "https://maxine-potato.netlify.app/"}),
            ],
        },

        # ---------------------------------------------------- Closing
        # Left aligned, 11 Nov, her instruction. It used to sit in a "centred"
        # section; a plain prose column puts it on the same left edge as every
        # other line on the page.
        {
            "classes": ["pad-lg"],
            "blocks": [
                ("prose", [
                    ("note", "Product name, brand and visuals have been changed. The "
                             "flows, research and decisions are from the real "
                             "project. Happy to walk through the original work in "
                             "interview."),
                ]),
            ],
        },
    ],
}
