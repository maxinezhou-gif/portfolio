# Case study design system

Everything a case study page is made of. Values come from Maxine's Figma file
(`kZbRLtd614DBU5cWWJLP8O`, frame `4:2`) and were audited against it — 14 of 14
spot-checks match exactly.

**A new case study is a content file, not a page.** Copy
`content/_template.py`, fill it in, run `python3 casestudy.py <slug>`. You
should never need to write HTML or CSS again.

```bash
cp content/_template.py content/my-project.py
python3 casestudy.py my-project        # → work/my-project.html
python3 casestudy.py                   # rebuild everything
```

---

## Tokens

All defined once in `:root` in `assets/css/case-study.css`. Change a token and
the whole system moves with it.

### Colour

| Token | Value | Used for |
|---|---|---|
| `--bg` | `#FAFAFA` | page ground |
| `--surface` | `#F6F6F8` | stat tiles, step cards, media frames |
| `--surface-2` | `#F2F4F5` | inside the media clip |
| `--white` | `#FFFFFF` | question chips, dock, top bar wash |
| `--line` | `#ECECEC` | hairlines |
| `--line-strong` | `#E0E0E0` | pill borders, list rules |
| `--ink` | `#111112` | headings, top bar |
| `--ink-body` | `#3D3D40` | body copy, label headings |
| `--ink-muted` | `#76767B` | captions, stat labels, notes |
| `--ink-faint` | `#A0A0A6` | eyebrows, step numerals |
| `--accent` | `#FF70C1` | **bold** emphasis only |

The accent is the one saturated colour. It appears *only* on `**bold**` text —
that restraint is what makes it read as emphasis rather than decoration.

### Type — Inter throughout

| Style | Size / weight / line-height / tracking | Token |
|---|---|---|
| Eyebrow | 12 / Medium / auto / +9% | `--t-eyebrow` |
| H1 (page title) | 26 / Medium / 33 / −2% | `--t-h1` |
| H2 (section) | 20 / Medium / 33 / −2% | `--t-h2` |
| H3 (label) | 18 / Medium / 33 / −2% | `--t-h3` |
| Body | 16 / Regular / 29 / 0 | `--t-body` |
| Small | 15.5 / Regular / 25 / 0 | `--t-small` |
| Body 2 | 14 / Regular / 33 / −2% | `--t-body2` |
| Numerals | 38 / Semi Bold / 40 / −4% | `--t-num` |
| Project label | 14 / Medium / −2% | `--t-label` |

The display face in the reference site is **Maison Neue**, a commercial
licence. Inter stands in for it. If you licence Maison Neue, add it to the
`--font` stack — nothing else changes.

### Layout

| Token | Value | Meaning |
|---|---|---|
| `--max` | `1440px` | frame width, matching Figma |
| `--content` | `1160px` | inner content width |
| `--reveal-max` | `1600px` | before/after reveal only — see below |
| `--col-text` | `370px` | sticky label column |
| `--col-gap` | `48px` | gap between the two columns |
| `--gutter` | `clamp(20px, 9.72vw, 140px)` | side padding; 140px at 1440 |

Radii: `--r-sm 8` · `--r-md 12` · `--r-lg 16` · `--r-pill 40`. Case study
media is `--r-lg`.

Two components deliberately use **literals, not tokens** — they are one-offs,
and in the preview's case the arithmetic has to stay readable:

| Where | Value | Rule |
|---|---|---|
| About page portrait | `6px` | `.about-photo`, `home.css` |
| Homepage hover preview — card | `12px` | `.home-preview`, `home.css` |
| Homepage hover preview — media | `8px` | `.home-preview .media`, `home.css` |

The preview's two values are **concentric, not arbitrary**: the media sits
inside a 4px white frame (`--prev-pad`), so its radius is the card's minus 4.
Change one and change the other, or the two arcs stop running parallel. The
media's 8px happens to equal `--r-sm`, but leave it written as `8px` — as a
token the `12 − 4` relationship stops being visible to the next reader.
`_prototype/radius-lab.html` is the sandbox for trying values against the real
images — it keeps that 4px relationship locked by default.

**Spacing rules** — measured against Figma's own metadata, not guessed:

| From → to | Gap | Where it lives |
|---|---|---|
| Eyebrow → H2 → an intro line, all within one `head` group | **12px** | `.sec-head > * + *` |
| A whole `head` group → whatever comes after it | **40px** | `.section > .sec-head + *` |
| A `bullets`/`numbered` list → whatever comes after it | **40px** | `.section > :is(.numbered,.bullets) + *` |
| Everything else between two blocks in a section | **56px** | `.section > * + *` |
| One eyebrow-bearing section → the next (`pad-lg`) | **96px** | `.section.pad-lg { padding-top }` |
| A section with no eyebrow (`Impacts`, `The Product`…) | **56px** | `.section { padding-top }` — default |
| Feature heading → its paragraph/list, inside Approach | **24px** | `.feature-text > * + *` |

**A collapsible section's content still needs all of the above** — the
`.collapse-panel` between a `section` and its blocks is invisible to these
rules unless the selector explicitly reaches through it (see
`.section > .collapse-panel > …` variants in the CSS). Forgetting this is
what breaks a collapsible's spacing silently.

**Heading levels are semantic, not just visual size:**
- A section's own title (`Overview`, `The Challenge`, a Phase heading) is
  always a real `<h2>`, whatever size it's styled at.
- A sub-label under it (`Our Design Team`, a stat's caption) is `<h3>`.
- Never reach for a bigger/smaller *tag* to get a bigger/smaller *look* —
  set the font-size on that context instead (e.g. `.feature-text h3` used
  to fake H1 size on an h3; that's gone, because it silently re-inflated
  any h3 dropped into a feature, like a "Result:" line, that was never
  meant to be that large).

### Elevation

| Token | Used by |
|---|---|
| `--shadow-media` | the `plain` figure frame — **Figure frames** below |

The only shadow token on the site. The dock pills write their own inline, and
nothing else is raised off the page at all, so treat a new shadow as a
decision to discuss rather than a value to pick.

### Motion

| Token | Value |
|---|---|
| `--swap-dur` | `600ms` |
| `--swap-rise` | `6px` |
| `--swap-ease` | `cubic-bezier(.2, .7, .3, 1)` |

Reveals fade only — they never translate. A translate would leave media
sitting below its paired sticky text until the reveal fired, i.e. misaligned
exactly while being read. `prefers-reduced-motion` disables all of it.

---

## Components

Each is a block type in the content file. Full list in the docstring at the top
of `casestudy.py`.

| Block | Renders |
|---|---|
| `("head", [...])` | heading group; 40px to whatever follows |
| `("h2" / "h3" / "p" / "note" / "small")` | the type styles above |
| `("pull", "…")` | 26px centred quote |
| `("prose", [...])` | 680px reading column |
| `("centred", [...])` | alias for `prose` — only reads as *centred* when the section itself also carries `"classes": ["centred"]`, which centres everything and lets `.centred .prose` override back to a left-aligned 680px column. Used alone, it's just `prose`. |
| `("div", {"classes": […], "blocks": […]})` | generic wrapper for a utility class — `inset` (extra `--gutter` of side padding, e.g. an 880px column inside the usual 1160), `center-block` (true `text-align: center`, for a block that's genuinely centred throughout — rare), `stack-40` (40px between children, for a wrapper that isn't itself a `section`) |
| `("stats", [(n, label), …])` | up to 4 tiles; reflows 2→4 |
| `("overview", [(label, [items]), …])` | 3 label/value columns; add a 3rd element `True` to a column's tuple for a numbered list instead of bulleted |
| `("findings", […])` | inline-numbered list, 28px apart |
| `("steps", […])` | numbered cards, `01`–`04`; reflows 1→2→4 |
| `("questions", […])` | white question chips |
| `("bullets", […])` | plain bullet list, accent markers |
| `("numbered", […])` | plain numbered list, same weight as `bullets` — use whenever the source content is a real ordered list, not a bulleted one |
| `("collapsible", {"toggle": "…", "panel_id": "…", "blocks": […]})` | collapsed by default; a dock-pill-styled button reveals it on click. No animation — it's a visibility toggle, not scroll-driven, so nothing for `prefers-reduced-motion` to disable. **Spacing rules need to explicitly reach through `.collapse-panel`** — see the Spacing rules table above |
| `("callout", [...])` | tinted aside; use `("label", "…")` inside for its accent sub-headings |
| `("chapter", "Phase 1 · Foundation building")` | quiet chapter divider, 20px in ink-faint. Not currently used anywhere — a phase-style heading is just a two-line `h2` (`"Phase 1\nFoundation building"`, one literal `\n`, which `rich()` turns into a `<br>`) directly in a `features` row |
| `("features", [(text, fig), …])` | text 384 / gap 64 / media 520, centre-aligned rows. Swap the pair to `(fig, text)` to put the media on the **left** instead — both the column widths and the DOM order flip together |
| `("fig", {…})` | one framed, clipped, captioned figure — see **Figure frames** below for the two frame variants |
| `("cta", {"label": "…", "href": "…"})` | pill-shaped link, sharing the `.dock-pill` rule. The **only** block that emits an `<a>` — `rich()` escapes everything else, so a link cannot be written as copy. An `http` href opens in a new tab |
| `("scrolly", [(labels, fig), …])` | **the sticky pattern** |
| `("reveal", {"before": {…}, "after": {…}})` | **full-bleed before/after crossfade** |

### Figure frames — `card` and `plain`

Two variants. The frame is chosen **per case study, not per figure**: a page
that mixes them reads as an oversight rather than a decision.

| | `card` (default) | `plain` |
|---|---|---|
| Panel | `--surface` fill, 1px `--line`, 20px padding | none |
| Media corner | `--r-lg` (16px) | `--r-sm` (8px) |
| Edge | the panel's hairline | `--shadow-media` |
| Media edges sit | 21px inside the text column | **on** the text column |

**`card`** is the default and needs nothing in the content file. The inset is
the point of it: the media is a specimen on a tray, which suits a dense
interface shot that would otherwise bleed into the page.

**`plain`** drops the panel and raises the media instead. Opt in with one key
on the case study dict, beside `slug` and `title`:

```python
"media": "plain",
```

That puts `class="media-plain"` on `<body>`; the overrides live under
`.media-plain` in `case-study.css`. No other case study is affected, and
leaving the key out is how every existing one stays on `card`.

Use it when the case study is carrying mostly full-screen recordings and
device shots, where the tray competes with the screen inside it. Because the
media's own edges become the figure's edges, a full-width figure then lines up
exactly with the text column — and so with the top bar's name and About link.

**Why 8px and not 16px.** A large corner on a photograph of a screen fights
the device's own rounded corner inside it. 8px is `--r-sm`, already in the
scale, so this borrows a step rather than inventing one.

**`--shadow-media`** is five stacked shadows, not one. A single large blur
reads as grey haze; short layers stacked read as a soft edge. It is grey
(`186,186,186`) rather than black, so it tints `--bg` instead of dirtying it,
and is offset slightly right as well as down. Values measured from
`niklas.space/canvas`.

> Overriding `.clip` needs **`.media-plain .fig .frame > .clip`**, matching the
> shape of the rule it beats. A shorter selector loses to the three-class
> default whatever the source order — the same trap as `.feature.rev`.

### Chapter + feature rows

Taken from `jasonspielman.com/huxe`, measured: a dated chapter heading acting
as a quiet divider, then rows of text 384 / gap 64 / media 520, centred on the
cross axis, 48px apart. Note the deliberate inversion — the **feature heading
is larger than the chapter heading**, because the chapter is a marker and the
feature is the content.

Use this when a case study is **chronological** and made of many small
artefacts. The compact 520px media column suits Slack threads, cards and
audit documents, which look absurd at full width. Use `fig` instead when a
screen deserves the whole column.

Huxe's own sizes are 28/17; this system uses 26/16 so the page stays inside
Maxine's tokens. The tracks are `minmax(0, …)` so they shrink rather than
overflow between the two-column breakpoint and the 1248px at which
384 + 64 + 520 genuinely fits.

#### `rows-flush`

A feature row is 384 + 64 + 520 = 968, centred in the 1160 column, so it sits
96px in from each side. Under a full-width heading that reads as a
misalignment rather than an indent.

Add `rows-flush` to the **section's** `classes` and the row keeps both track
widths but spends the slack on the gap instead, putting the text on the page's
left margin and the media on its right:

```python
"classes": ["pad-lg", "gap-lg", "rows-flush"],
```

Opt-in, because the published case studies are laid out against the centred
version. Below 1040px the rows are a single `1fr` track with no slack to
distribute, so it stops applying on its own.

### Before / after reveal

Two full-viewport frames. Both pin at `top: 0`; the AFTER frame is later in the
DOM with a higher stacking order and crossfades in as it rises, covering the
BEFORE frame and uncovering it on the way back up. Chosen from
`_prototype/reveal-lab.html`: the **fade** variant at **100vh**.

Put it in a section marked `"full": True` so it loses the gutter and runs
full-bleed. `--reveal-p` (0→1) is set per section in `case-study.js`; everything
else is CSS. Both panes release together at the end of the section, so the
reader is never scroll-trapped, and `prefers-reduced-motion` drops it to two
stacked static images.

**The media is `object-fit: contain`, and must stay that way.** The pane is
`100vh` with no ceiling while its width is capped, so viewport height alone
decides the media box's shape. On a tall display that box turns portrait
against these 1.6 landscape frames, and `cover` fills the height and crops the
sides away — at 1700x1150 that was about half the width gone. The same fault
at the other end of the range is what the 1040px fallback below exists for: a
390x844 pane showed a 29% vertical slice. `contain` is the fix at both ends.

**It is capped at `--reveal-max` (1600px), not `--content`.** This block is
full-bleed, so holding it to the 1160px *text* column made the frame far
smaller than the space available, which `contain` then surrounded with dead
space. 1600px is the single dial: lower it for a tighter frame, raise it for a
bigger one.

### The scrolly pattern

The signature interaction. The left label column pins while the media scrolls
past; as each image reaches the pin line its label replaces the previous one.

Two rules keep it working:

1. **Keep the section intro OUT of the scrolly.** Put it in a `head` block
   above. If one label block also carries the intro, its heading sits lower
   than the others and the swap visibly jumps.
2. **Give every label the same shape** — `h3` + one `small`, or `h3` +
   `questions`. Then the heading offset is 0px in each and the label changes
   in place.

Exactly one label is ever visible: JS marks the active one and hides the rest,
so nothing bleeds through in either scroll direction. It pins at 80px, clearing
the 55px top bar, and collapses to a stacked single column below 1040px —
where source order is already text, image, text, image, so it reads correctly.

`_prototype/sticky-lab.html` isolates this with six transition variants and
live drift instrumentation, if it ever needs retuning.

---

## Media

See `MEDIA.md` for preparing images and video — this is the fiddliest part of
adding a case study, and getting `ar` / `op` wrong is what produces a dark
corner.

---

## Files

```
casestudy.py              the generator — you should rarely touch this
content/<slug>.py         one file per case study: pure content
content/_template.py      copy this to start a new one
assets/css/case-study.css the design system
assets/js/case-study.js   reveals, sticky swap, video autoplay, dock spy
work/<slug>.html          generated — never hand-edit

home.py                   homepage generator -> index.html
content/_home.py          homepage content
about.py                  about generator -> about.html; imports home.py
content/_about.py         about content; the optional "photo" key drives
                          the portrait — delete it and the photo goes
assets/css/home.css       homepage layout only; case-study.css still owns
                          every token, the reset and the top bar
assets/js/home.js         the travelling dot and the hover preview

_prototype/sticky-lab.html  label-swap sandbox
_prototype/reveal-lab.html  before/after sandbox
_prototype/radius-lab.html  corner-radius sandbox (sliders, real images)
HANDOVER.md               context, decisions and gotchas — read first
```

**`case-study.css` is now loaded site-wide**, including by the homepage, so
its name undersells it — it is the token layer for everything. Worth renaming
once the cream design is retired, not before.

**Two generators must never target the same file.** `build.py` keeps a
`MIGRATED` set of slugs that `casestudy.py` owns; add a slug to it the moment
its content file exists. Skipping this silently overwrites a v2 page with the
cream one.
