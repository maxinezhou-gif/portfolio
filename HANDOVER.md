# Handover — Maxine Zhou portfolio

Written 6 September 2026, at the end of a long session. Read this before
touching anything; it will save you re-deriving decisions that were already
measured and settled.

Companion docs: **README.md** (how the repo works), **DESIGN-SYSTEM.md**
(tokens and components), **MEDIA.md** (preparing images and video),
**CLAUDE.md** (conventions).

---

## 1 · The goal

Maxine is a **product designer looking for work**. She needs a **public
portfolio URL she can put on her CV and send to recruiters**.

Her old site was on Wix. She stopped paying, so Wix disconnected her custom
domain. Everything here was recovered from the still-live free Wix URL and
rebuilt as a static site she owns.

The end state she wants:

1. A homepage, an about page, and case study pages, all in one visual language
2. Hosted on a real domain — **she has not bought one yet, deliberately**;
   she wants the site right first
3. Adding a future case study should be **writing content, not building a page**

---

## 2 · Where things actually stand

**Two designs coexist in this repo.** This is the single most important thing
to understand.

| | Old ("cream") | New (v2) |
|---|---|---|
| Generator | `build.py` | `casestudy.py` |
| Stylesheet | `assets/css/site.css` | `assets/css/case-study.css` |
| Content lives | inside `build.py` | `content/<slug>.py` |
| Pages | `index.html`, `projects.html`, `about.html`, `404.html`, 8 × `work/*.html` | `work/launchpad.html`, `work/design-system-migration.html` |

**Done:** two case studies fully migrated to v2, plus the design system,
generator, template and docs.

**Not done:** home, work index and about are still the old cream design.
Because of that, **Launchpad currently exists at two URLs in two different
styles** — `work/underwriting-efficiency.html` (old) and `work/launchpad.html`
(new). Fine locally, not shippable. Resolving this is the main remaining task.

```bash
cd portfolio
python3 casestudy.py          # rebuild the v2 case studies
python3 -m http.server 8787   # or double-click open-site.command
```

---

## 3 · Decisions already settled — do not re-litigate

### Visual system

Taken from Maxine's Figma frame `4:2` and **audited against it: 14 of 14
spot-checks match exactly**. Eight drifts were found and closed. Full table in
`DESIGN-SYSTEM.md`. Headlines:

- Inter throughout. Display face in the reference is Maison Neue (commercial
  licence) — Inter stands in
- `#FAFAFA` ground, `#111112` ink, accent **`#674FA3`** used *only* on `**bold**`
- One rule that matters: **a heading is always 40px from the body it introduces**
- 1440 frame, 1160 content, 140px gutters

### Deliberate divergences from the Figma file

These came from later instructions and are **newer than the file**. If the
Figma and the build disagree on these, the build is right:

- 40px heading-to-body everywhere (Figma's section gaps vary 32/40/56)
- Design direction as four cards
- "Why Back button dominance?" centred
- Captions **below** media
- Section intros lifted **out** of sticky columns (see §4)
- "Launchpad" spelling corrected — the Figma reads "Lauchpad"

---

## 4 · Interactions — agreed, with exact values

Three interactions were prototyped, measured and chosen. Each has a lab file
if it needs retuning.

### 4.1 Sticky label swap — `("scrolly", …)` · SHIPPED

Left label column pins; as each image reaches the pin line its label replaces
the previous one.

| | |
|---|---|
| Chosen | **fade + rise, 600ms** (variant B in the lab) |
| Tokens | `--swap-dur: 600ms` · `--swap-rise: 6px` · `--swap-ease: cubic-bezier(.2,.7,.3,1)` |
| Pin | `top: 80px` (clears the 55px top bar) |
| Collapses | below 1040px |
| Lab | `_prototype/sticky-lab.html` — six variants, live drift readout |

**Two rules this depends on. Break either and it visibly jumps:**

1. **Keep the section intro OUT of the scrolly.** Put it in a `head` block
   above. Originally the first label block also carried the intro, so its
   heading sat ~180px lower than the others and the swap leapt.
2. **Give every label the same shape** — `h3` + one `small`, or `h3` +
   `questions`. Verified: heading offset **0px** in every block, so the label
   changes in place.

Exactly one label is ever visible — JS marks the active one and hides the rest.
An opaque backdrop was tried first and **was not sufficient**: the blocks pin
and unpin at different moments, so a transiting block left the previous one
exposed. Don't go back to that.

### 4.2 Before/after reveal — `("reveal", …)` · JUST ADDED, NEEDS A LOOK

Two full-viewport frames; the AFTER crossfades in over the BEFORE as you
scroll, and uncovers on the way back.

| | |
|---|---|
| Chosen | **fade variant at 100vh** |
| Mechanism | both panes `position: sticky; top: 0`, after has higher z-index |
| Driver | `--reveal-p` (0→1) set per section in `case-study.js` |
| Lab | `_prototype/reveal-lab.html` — cover / card / wipe / fade |

**Verification status — read this.** Static properties are confirmed on the
built page: both panes `sticky`, z-index 1/2, pane height 900 = viewport,
full-bleed 1440, after opacity `0` at rest, tags present. The **scroll-driven
fade was not exercised** — the preview pane stopped scrolling (see §7).
The identical sticky mechanism *was* measured working in the lab across ten
scroll positions. **Please open `work/design-system-migration.html` in a real
browser and confirm the fade before shipping.**

Currently using `ds-before.jpg` / `ds-after.jpg`. Maxine has made **two
full-screen frames in Figma (`76:11851`)** intended for this — swapping them in
is two filenames in `content/design-system-migration.py`.

### 4.3 Homepage row hover — EXPLORED, NOT BUILT

Reference: **niklas.space**. Analysed in detail (§5).

Agreed direction: a **travelling dot + hover preview**, in Maxine's tokens.
Nothing built yet.

---

## 5 · Reference sites — what was measured, and what to take

### jasonspielman.com/notebooklm → the case study shell

Source of the current page architecture. Measured: `#FAFAFA` ground,
`#F6F6F8`/`#F2F4F5` surfaces, `#ECECEC`/`#E0E0E0` hairlines, radii 8/12/16/40.
Sticky "Panel States" section: flex row, **gap 48**, `align-items: flex-start`,
left column **379px** sticky at `top: 0`, right column **733px**. That became
the scrolly at 370/742.

### jasonspielman.com/huxe → the DS migration structure

A **reverse-chronological changelog**, and — the surprising bit — **zero sticky
behaviour** (measured `stickyCount: 0`, against NotebookLM's 5).

Feature row measured: text **384** / gap **64** / media **520**,
`align-items: center`, rows 48px apart. The feature heading is deliberately
**larger** than the chapter heading.

Adopted for DS migration because that story is chronological, unfinished
("three in progress" — Huxe's "Coming soon" chapter handles that as momentum),
and made of many small artefacts. **It also fixed a real flaw**: full-width
figures were rendering a 1316×680 Slack screenshot enormously. Media is now
488px, and the page went from 13,309px to 9,775px.

Sizes use Maxine's tokens (26/16) not Huxe's (28/17).

### niklas.space → the homepage

**Read this before designing the homepage — the first analysis was wrong and
the correction matters.**

Structure:

| | |
|---|---|
| Column | `max-w-screen-sm` + `px-6` → **600px max, 552px of text**, centred |
| Top bar | fixed, 58px, `bg-white/80` + `backdrop-blur(24px)`, name only |
| Font | **system stack** — no webfont at all |
| Type | **one size for the whole page: 17px / 1.5** |
| Colours | **two**: `#09090b` names, `#a1a1aa` descriptions, on white |
| Images | zero |
| Row | `flex flex-col py-3`, name over description, 71px tall, rows butting together, 96px break before "About" |
| Body | carries `lowercase` and `select-none` |

**The hover interaction — initially reported as absent. It is not.**

The CSS contains **0 occurrences of `hover`** in 12KB, and a real pointer on a
row changes no computed style. That led to a wrong conclusion. It is entirely
**React state**, and the elements **only exist in the DOM while hovering**. A
before/after **pixel comparison** is what caught it. Lesson: for JS-driven
hover, diff pixels, not the DOM.

What actually happens:

1. **A blue dot marks the row** — 16×16, round,
   `oklch(60.39% 0.23045 259.474)` ≈ `#3B82F6`, sitting **24px to the left** of
   the row and 15px down. At rest it sits beside his name in the top bar, so it
   reads as **one travelling indicator**.
2. **A muted video preview appears to the right** — `.webm`, rendered
   **672×437** (source 1660×1080), **4px** radius, two-layer grey shadow
   `rgba(186,186,186,0.5)`, 4px padding frame, `autoplay muted loop playsinline`,
   no controls. Offset **+296px right, −183px up** from the hovered row.

Nothing else moves. Two moving parts on an otherwise inert page.

**Cost:** ~11 MB across five previews with `preload="auto"` (futures 4.6 MB,
intents 3.3 MB). Two rows 404 and have no preview. **If we adopt this, use
`preload="none"` and keep clips under ~1 MB.**

**Recommendation on record:** take the structure and restraint, express them in
Maxine's existing tokens rather than importing his — so home and case studies
read as one site. A narrower homepage column (600 vs 1160) is normal.

**Open question for Maxine:** the forced `lowercase`. It is a big part of why
his page reads as it does, but it is a personality choice and her case studies
are sentence case. Default to sentence case; it is a one-line change.

---

## 6 · Figma

File **`kZbRLtd614DBU5cWWJLP8O`**.

| Node | What |
|---|---|
| `0:1` | Page "Launchpad — case study" — frame `4:2`, the audited source of truth |
| `50:10126` | Page "DS migration — case study" — built from this repo, 1440 × 9354 |
| `76:11851` | The two full-screen before/after frames for §4.2 |

Variable collection **"Case study tokens"** (18 vars) and text styles
**H1 / H2 / H3 / body / Body 2 / Eyebrow** exist and are used. Reuse them —
do not invent new ones.

**The MCP gotcha that cost time in this session:** the write-capable Figma
plugin server disconnected mid-session. Re-authorising via `/mcp` in another
terminal **did not restore it**, because MCP servers are registered when a
session starts. It needs a **new session**. The read-only Dev Mode server is a
different thing and needs the Figma **desktop app** with Preferences →
*Enable Dev Mode MCP Server*, plus a Claude restart.

If you have the plugin server, you can read `76:11851` directly. If not,
**ask Maxine to export the frames as PNG 2x into `assets/img/`** — faster than
fixing the connection, and you need the rendered pixels anyway.

---

## 7 · Verification — what this environment can and cannot prove

Hard-won. Do not waste time rediscovering it.

**Works reliably:** computed styles, geometry, `elementFromPoint`, layout
measurement at any viewport (via an offscreen iframe), link/asset integrity,
alt-text checks.

**Does not work when the Browser pane is hidden** (it reports
`document.hidden: true`, so the page never composites):

- **Scroll events do not fire** — verified with a fresh probe listener
- **IntersectionObserver never fires** — not even its initial callback
- **CSS transitions do not run**, so timing measurements are meaningless
- **Screenshots come back blank**
- Late in a session, even `scrollTo` stops moving the page

So: **anything scroll-driven, animated, or video-related cannot be confirmed
here.** Verify structure and geometry by measurement, then ask Maxine to check
motion in a real browser. Say plainly which is which — she is fine with the
limitation, but not with it being glossed over.

**Two traps that produced wrong conclusions in this session:**

- **Stylesheet caching.** After editing CSS, the browser served the old file
  and the new component appeared to do nothing. Cache-bust the *CSS*, not just
  the HTML.
- **Unrevealed `.rv` elements.** They carry `translateY(14px)`, which silently
  poisons any spacing measurement. Add `.in` and let the transition finish
  (~700ms) before measuring.

---

## 8 · Next steps, in the order I would do them

1. **Confirm the before/after fade** in a real browser (§4.2), and swap in the
   Figma frames from `76:11851`.
2. **Build the homepage** on the niklas.space structure in Maxine's tokens
   (§5). She has media ready: five Launchpad clips with measured crop values,
   plus the DS before/after stills.
3. **Migrate about + work index** to v2.
4. **Retire the old design** — delete the cream entries from `build.py`, point
   the work index at the new slugs, remove `work/underwriting-efficiency.html`.
   This is what clears the two-URLs problem.
5. **Then** buy the domain and deploy once, cleanly. Netlify — it serves
   private repos on the free tier; GitHub Pages does not (§ README).
6. Set `BASE_URL` in the generators to switch on canonical tags, OG tags,
   sitemap and robots.

---

## 9 · Things that need Maxine's judgement, not yours

Raised with her; she has not ruled. **Do not quietly change them.**

- **Slack screenshots.** Seven across the two case studies show colleagues'
  names, photos and messages from client work. Strong evidence, already public
  on the old Wix site — but internal comms, and worth a conscious decision.
- **A work email is baked into the pixels** of the DS cover image
  (`maxine@pangaea.co.uk`). Needs an image editor to remove.
- **ConvexAI** (`content/` has no file; old page at
  `work/workplace-ai-assistant.html`) has a real content problem: roughly
  two-thirds of its copy is duplicated verbatim from the contract analysis case
  study. It is deliberately unlinked. It needs original writing before it
  should be linked.
- **Two Wix pages were never rebuilt** — "Learning JBE" and "Digital content
  design" — because they had images but essentially no writing. All their
  images are downloaded and the contact sheets in `_reference/contact-sheets/`
  show what each one is.
- **Earlier work is now visible.** The Wix site hid four finished case studies
  behind "Stay Tuned" placeholders; they are now linked. Reversible via the
  `earlier=True` flags in `build.py`.

---

## 10 · Assets

- 108 images downloaded from Wix at full resolution (202 MB), resized to max
  2000px and converted PNG→JPEG where transparency was not needed → **25 MB**
- **Untouched originals are at `../original-assets/`** (195 MB), outside the
  repo. Do not delete — only copy if Wix goes down
- Maxine's own source recordings for Launchpad live in `~/Desktop/launchpad`;
  the DS before/after exports in `~/Downloads/DS`. Neither is committed
- Video crop values (`ar` / `op`) are measured per clip — see `MEDIA.md`.
  **The bar detector reads dark UI chrome as a letterbox bar**; it produced a
  false positive on the DS "after" screen (a dark teal app header). Check
  before cropping.
