# Handoff notes

State as of the initial rebuild. Read `README.md` first for how the project works.

---

## Where things stand

The site is **complete and verified**: all content from the Wix site has been recovered
and rebuilt across 12 pages.

Verification actually run (not assumed):

- 275 internal links and asset references resolved — **0 broken**
- **0** images missing `alt` text
- **0** horizontal overflow at 390px / 768px / 1280px
- All 12 pages return 200 and have exactly one `<h1>`
- Only intentional orphan page: `work/workplace-ai-assistant.html` (see below)

---

## Planned next step: the restyle

The next task is a **drastic visual change**, following a different portfolio UI as
reference.

**Do the restyle in `assets/css/site.css`, not `build.py`.** The generated HTML is
semantic and class-based specifically so the CSS can be swapped wholesale. Useful things
to know before starting:

- **Tokens first.** Everything derives from the custom properties in `:root`. Changing
  those five or six colour values and the two font families gets you most of the way to a
  different feel without touching a single rule.
- **The class vocabulary is small and stable.** Roughly: `.wrap` / `.narrow` (layout),
  `.hero*`, `.section` / `.section-head` / `.eyebrow`, `.work-card` / `.tags` /
  `.card-more`, `.cs-hero` / `.cs-cover` / `.overview` / `.cs-body`, `.block`,
  `.stats` / `.stat`, `.insights`, `.questions`, `.pull`, `.callout`, `.fig-pair`,
  `.sequence`, `.video-block`, `.contact`, `.site-footer`, `.reveal`.
- **If the reference UI needs different markup** (say, a horizontal-scrolling project
  rail, or a two-column case study), the block renderers in `build.py` → `render()` are
  where the HTML shapes are defined. Each block type is ~3 lines. Add new block types
  rather than reshaping existing ones, so old pages keep working.
- **`.reveal`** is the scroll-in animation hook, applied by the generator. It's driven by
  a small IntersectionObserver in the inline `SCRIPT` string in `build.py`. Removing the
  class from CSS disables the effect safely (elements stay visible — the `opacity: 0` only
  applies when the observer is running).
- **`prefers-reduced-motion` is respected** throughout. Keep that if you add motion.
- **`.wide` figures** break out of the narrow reading column on screens ≥1000px. That
  trick relies on `--max`; if you change the layout system, check those.

---

## Decisions I made that you may want to reverse

**1. Earlier work is now visible.** On the Wix site, the "Old works (2022–2023)" section
showed only *"Stay Tuned"* placeholders — the four older case study pages existed but
nothing linked to them. I built them properly and linked them under "Earlier work
(2020–2023)", on the reasoning that finished work helps more than a placeholder.

To go back to hiding them: remove the `earlier=True` flag from those four `P(...)` entries
in `build.py`, or delete the "Earlier work" `<section>` from `build_home()` and
`build_projects()`.

**2. ConvexAI / workplace AI assistant is left unlinked.** It was an orphan on the Wix site
too, so I matched that. **It also has a real content problem**, which is why it probably
shouldn't be linked as-is: roughly two-thirds of that page's copy is duplicated verbatim
from the contract analysis case study (the "Design Evolution", "Early Prototype", "Hybrid
Tabs + Accordion", and "Action List" sections are the same text about contract review,
which doesn't apply to a chat assistant). I only carried across the sections genuinely
about that product. If you want it in the portfolio, it needs original copy written for it
— that's a writing task, not a code task.

**3. Two Wix pages were not rebuilt**, because they had essentially no written content —
only images and a couple of stray labels:

| Wix page | What was on it |
|---|---|
| `/general-4` ("Learning JBE") | 27 images, and the text *"Task 1 / Equipment setting guidance and breath training"* |
| `/s-projects-side-by-side-1` ("Digital content design") | 11 images, plus team/timeline/tools labels only |

**All of their images are downloaded and present** in `assets/img/`, and the contact sheets
in `_reference/contact-sheets/` show what each one is. If you want these as case studies,
the images are ready and waiting — they just need copy.

---

## Known gaps

**The self-introduction video could not be recovered.** The Wix "About me" page had a
personal intro video ("Who am I outside of university/work?"). Wix loads that player via a
runtime API call rather than putting the file in the page source, so it isn't in the
scraped HTML and I couldn't find the file. The seven videos that *were* recovered are all
product demos.

If Maxine still has the original video file, drop it in `assets/video/` and add a
`("video", "filename.mp4", "caption")` block to `build_about()` in `build.py`. Otherwise
the About page reads fine without it.

---

## Things worth flagging to Maxine before this goes on a CV

These are her calls, not mine — I left everything as it was on the live site:

1. **Client Slack screenshots.** The design system case study includes five screenshots of
   internal Slack conversations, showing her colleagues' names, profile photos and
   messages. They're genuinely good evidence of how she works, and they were already public
   on the Wix site — but they are internal client communications, and worth a conscious
   decision rather than an inherited one. Files: `429fa4_81783366…`, `429fa4_46c62b14…`,
   `429fa4_d79c6c6e…`, `429fa4_dbe8db9a…`, `429fa4_934a0060…`.
2. **Two colleague testimonials on the About page** are also Slack screenshots
   (`429fa4_d495b40f…`, `429fa4_11e39adf…`). Same consideration.
3. **A work email address is visible inside the design system cover image** (a Figma
   mockup with `maxine@pangaea.co.uk` rendered in it). It's baked into the image pixels,
   not the HTML, so it would need editing in an image editor to remove.
4. **Contact email is `maxinezhou0302@outlook.com`** throughout — taken from the Wix site's
   mailto link. Change `EMAIL` at the top of `build.py` if that's not the right address for
   job applications.
5. **The insurance client is never named** anywhere in the copy (it's consistently "a
   global insurance organisation"), but product UI screenshots do show real interface
   details. Presumably already cleared, since it was public — just noting it.

---

## Reference material

`_reference/` holds the raw material the rebuild came from. Not part of the site; safe to
delete once you're confident nothing else is needed.

| File | What it is |
|---|---|
| `wix-extracted-content.txt` | All text from every Wix page, tagged by heading level. The source of truth for wording. |
| `wix-raw-html.tar.gz` | The original scraped Wix HTML for all 14 pages. Ultimate fallback. |
| `contact-sheets/*.jpg` | Labelled thumbnail grids of every image per page — the fastest way to see what an image filename actually is. |
| `page_images.json` | Which images appeared on which Wix page, in order. |
| `flow.json` | Interleaved text + image order, where Wix server-rendered it. |
| `image_ids.json` | Original Wix media filenames before renaming. |

**Note on image filenames:** originals were `429fa4_<hash>~mv2.png`. They're now
`429fa4_<hash>.jpg` (or `.png` where transparency was needed). Hashes are unchanged, so
you can always match a file back to the Wix source.

---

## Recovering the source site again

The Wix site was still live at the free URL when this was built:

```
https://maxinezhou03024.wixsite.com/mysite
```

Case study pages are nested at `/mysite/projects/<slug>` — `/mysite/<slug>` returns an
empty shell, which is a trap worth knowing about. Content is server-rendered into the HTML,
so `curl` with a normal browser user-agent is enough; images come from
`https://static.wixstatic.com/media/<original-filename>` at full resolution.
