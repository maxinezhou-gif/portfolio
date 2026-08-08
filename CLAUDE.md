# Working in this repo

Static portfolio site for Maxine Zhou, a product designer. Rebuilt from a Wix site after
the custom domain was disconnected. Read `README.md` for architecture and `HANDOFF.md` for
open decisions and known gaps.

## Critical: the HTML files are generated

`index.html`, `projects.html`, `about.html`, `404.html` and everything in `work/` are
**build output**. Editing them directly gets your work destroyed on the next build.

- Content and page structure → edit `build.py`
- Styling → edit `assets/css/site.css`
- Then run `python3 build.py` to regenerate

## Commands

```bash
python3 build.py                    # regenerate all HTML
python3 -m http.server 8787         # preview at localhost:8787
```

No npm, no dependencies, no install step. Uses only the Python that ships with macOS.

## Conventions

- **Design tokens live in `:root` in `site.css`.** Never hard-code a colour, font family, or
  `--max`-derived width in a rule. Add a token if one is missing.
- **British spelling** in all user-facing copy (organisation, personalised, prioritised,
  tokenisation). The original site used it consistently.
- **Every `<img>` needs meaningful `alt` text.** The generator's `img_tag()` requires it as a
  positional argument, so don't route around it.
- **One `<h1>` per page.** Section titles are `<h2>`.
- Content strings in `build.py` support `**bold**`; everything else is HTML-escaped
  automatically by `rich()`. Do not write raw HTML entities like `&amp;` in content strings —
  write a plain `&` and let the escaper handle it.
- Keep `prefers-reduced-motion` handling intact when adding motion.

## Before saying a change works

Actually verify, don't assume:

1. Re-run `python3 build.py` and confirm it reports 12 pages.
2. Serve the folder and check the affected pages render.
3. For layout or CSS changes, check 390px / 768px / 1280px for horizontal overflow —
   the site was verified clean at all three and should stay that way.

## A restyle is the expected next task

Maxine plans a drastic visual change following a different portfolio UI as reference. It
should be achievable almost entirely in `site.css`. See the "Planned next step: the restyle"
section of `HANDOFF.md` for the class vocabulary and what depends on what.

If the new design genuinely needs different markup, add new block types to `render()` in
`build.py` rather than reshaping existing ones — that keeps the eight existing case study
pages working while you iterate.
