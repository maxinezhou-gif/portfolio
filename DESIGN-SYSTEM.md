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
| `--accent` | `#674FA3` | **bold** emphasis only |

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
| `--col-text` | `370px` | sticky label column |
| `--col-gap` | `48px` | gap between the two columns |
| `--gutter` | `clamp(20px, 9.72vw, 140px)` | side padding; 140px at 1440 |

Radii: `--r-sm 8` · `--r-md 12` · `--r-lg 16` · `--r-pill 40`.

**Spacing rule:** a heading is always **40px** from the body it introduces.
Sections are 56px apart (`--section`), or 112px with `gap-lg`.

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
| `("centred", [...])` | centred column, text still left-aligned |
| `("stats", [(n, label), …])` | up to 4 tiles; reflows 2→4 |
| `("overview", [(label, [items]), …])` | 3 label/value columns |
| `("findings", […])` | inline-numbered list, 28px apart |
| `("steps", […])` | numbered cards, `01`–`04`; reflows 1→2→4 |
| `("questions", […])` | white question chips |
| `("bullets", […])` | plain bullet list, accent markers |
| `("callout", [...])` | tinted aside; use `("label", "…")` inside for its accent sub-headings |
| `("chapter", "Phase 1 · Foundation building")` | quiet chapter divider, 20px in ink-faint |
| `("features", [(text, fig), …])` | text 384 / gap 64 / media 520, centre-aligned rows |
| `("fig", {…})` | one framed, clipped, captioned figure |
| `("scrolly", [(labels, fig), …])` | **the sticky pattern** |
| `("reveal", {"before": {…}, "after": {…}})` | **full-bleed before/after crossfade** |

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
_prototype/sticky-lab.html  label-swap sandbox
_prototype/reveal-lab.html  before/after sandbox
HANDOVER.md               context, decisions and gotchas — read first
```
