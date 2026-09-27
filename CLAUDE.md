# Working in this repo

Static portfolio site for Maxine Zhou, a product designer looking for work. Rebuilt from a
Wix site after the custom domain was disconnected. **Live at https://maxine-zhou.com** since
6 September 2026, on GitHub Pages from `maxinezhou-gif/portfolio`.

Read `HANDOVER.md` for context, decisions and gotchas, and `DESIGN-SYSTEM.md` for the case
study system. `HANDOFF.md` is from the original cream-design rebuild and is **superseded** —
ignore it.

## Two designs coexist. Know which one you are in.

| | v2 — the live site | Cream — retired |
|---|---|---|
| Pages | `index.html`, `about.html`, `work/{launchpad,design-system-migration,analyser}.html` | `404.html`, 7 × `work/*.html` |
| Generator | `casestudy.py` · `home.py` · `about.py` | `build.py` |
| Content | `content/<slug>.py` · `content/_home.py` · `content/_about.py` | inside `build.py` |
| Stylesheet | `case-study.css` (+ `home.css`) | `site.css` |

The 7 cream case studies still build but **nothing links to them** — they are reachable only
by typing the exact URL, and `robots.txt` excludes them. Maxine chose to leave them folded
away rather than delete them. Don't reintroduce links to them.

## Critical: the HTML is generated

`index.html`, `about.html`, `404.html` and everything in `work/` is **build output**.
Editing it directly gets your work destroyed on the next build.

- A case study → `content/<slug>.py`, then `python3 casestudy.py <slug>`
- The homepage → `content/_home.py`, then `python3 home.py`
- The about page → `content/_about.py`, then `python3 about.py`
- Styling → `assets/css/case-study.css` (tokens + everything) or `home.css` (homepage/about
  layout only)

**A new case study is a content file, not a page.** Copy `content/_template.py`. You should
never need to write HTML.

**Two generators must never target the same file.** `build.py` keeps a `MIGRATED` set of
slugs that `casestudy.py` owns, and skips them. It currently holds
`design-system-migration`, the only slug both generators know about — the other v2 pages use
slugs the cream design never had. If you migrate a page that already exists in `build.py`,
add its slug to `MIGRATED` immediately. Skipping this silently overwrites a v2 page with a
cream one; it has happened.

## Commands

```bash
python3 casestudy.py <slug>    # one case study
python3 casestudy.py           # all of them
python3 home.py                # index.html
python3 about.py               # about.html
python3 build.py               # the cream pages — reports 8
```

No npm, no dependencies, no install step. Uses only the Python that ships with macOS.

**To preview, use the Browser pane tools, not Bash.** There is a `.claude/launch.json`
config named `portfolio` on port 8787. Never start a dev server with `python3 -m
http.server`.

## Conventions

- **Design tokens live in `:root` in `case-study.css`**, which is loaded site-wide including
  by the homepage — its name undersells it. Never hard-code a colour or font family; add a
  token if one is missing. Sizes local to a single component may be literals, and a few
  deliberately are (see the radius table in `DESIGN-SYSTEM.md`).
- **British spelling** in all user-facing copy (organisation, personalised, tokenisation).
- **Every `<img>` needs meaningful `alt` text.** The generators require it.
- **One `<h1>` per page.** Section titles are `<h2>`, sub-labels `<h3>`. Heading level is
  semantic — never pick a tag to get a size.
- Content strings support `**bold**`; everything else is HTML-escaped by `rich()`. Write a
  plain `&`, never `&amp;`.
- Keep `prefers-reduced-motion` handling intact when adding motion.
- `_prototype/*.html` are sandboxes for trying values against real assets. They are not
  published — there is no `.nojekyll`, so GitHub Pages skips underscore directories.

## Before saying a change works

Actually verify, don't assume:

1. Re-run the right generator and confirm it reports the page.
2. Open the affected page in the Browser pane and look at it.
3. For layout or CSS changes, check 390px / 768px / 1280px for horizontal overflow — the
   site was verified clean at all three and should stay that way.
4. Browsers cache the stylesheet hard. If a CSS change doesn't appear, bust the cache before
   concluding it didn't work.

## How Maxine wants this worked on

- **Incrementally.** One thing at a time, shown to her, then the next. She asked for this
  explicitly after a session that built too much at once. Don't run ahead into adjacent work.
- **Commit, but never push.** She reviews on `localhost:8787` first and pushes herself with
  GitHub Desktop. There is no GitHub credential on the command line, and she must not paste
  a token into chat. Tell her which commits are waiting.
- **Ask for copy rather than inventing it.** Don't write claims about her projects she
  hasn't made. Flag genuine grammar errors in her wording — she wants them fixed — but apply
  her words, not your rewrite of them.
