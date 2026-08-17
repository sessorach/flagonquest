# Working on FlagonQuest

Conventions and practices for maintaining this site — read this at the
start of a session to pick the workflow back up without re-deriving it.
For what the project *is* and what's shipped, see `README.md`. For the
data-format mini-syntaxes (Prereq Check, Feature Budget, Building text,
Base Item Options), see the docstring at the top of `scripts/convert.py`
— that documentation is authoritative and shouldn't be duplicated here.

## Architecture

- `index.html`, `rulebook.html`, `glossary.html` are independent, single-file
  React 18 apps — CDN React/ReactDOM/Babel-standalone, JSX compiled in the
  browser, no build step, no shared imports between the three files. Small
  shared helpers (`withGlossary`, `GlossaryTerm`, the header nav) are
  duplicated by hand across them and kept in sync manually — there's no
  build step to share code through.
- Game content lives in `scripts/*.csv` (plus `scripts/rulebook.md` and
  `scripts/glossary.md` for hand-written prose) and is compiled to
  `data/*.json` by `scripts/convert.py`. **Never hand-edit `data/*.json`**
  — it's generated output, and edits will be silently blown away next time
  someone runs the converter. Run `python scripts/convert.py` from
  anywhere (it resolves paths off its own file location) after any CSV
  change, and commit the regenerated JSON alongside the CSV.
- `archive/` holds genuinely dead files — an old prototype, stale one-off
  outputs from completed migrations. Nothing in it is read by the site or
  by `convert.py`.

## Editing content

- Small tweaks: just describe the change and make the CSV edit directly.
- Bulk content from an external source (a doc, a spreadsheet, a big pasted
  block of lore): parse it and turn it into proper CSV rows rather than
  asking the user to reformat it first.
- If the user hand-edits a CSV themselves, that should happen in a real
  spreadsheet app (Excel/Google Sheets), not a plain text editor — fields
  with embedded commas, quotes, or multi-line dialogue (several technique
  descriptions are two or three paragraphs) are easy to corrupt outside a
  tool that understands CSV quoting.
- New content packs get tagged by `Supplement` (e.g. "Base Game", "Goblin
  Game") on items/backgrounds/techniques. `enabledSupplements` (the
  Builder tab's Sources panel) gates what's *offered* for new picks —
  it must never retroactively hide or remove content already in a build.
- Techniques also have `Excluded By` (comma-separated supplement names)
  for the reverse case — a technique whose own Supplement is enabled but
  that a *different* enabled supplement makes obsolete or nonsensical.
  Used when a supplement replaces a Base Game technique outright: tag
  the original "Excluded By: Goblin Game" and add a same-named
  Goblin-Game-supplement row with the replacement text, rather than
  building conditional per-supplement effect text on one row. Same
  non-retroactive rule as Supplement — only gates the browse list, never
  a build already holding the excluded technique.
- The Rulebook/Glossary get the same idea via Markdown: a level-1
  heading can end with `{Supplement Name}` (e.g. `# Goblin Game {Goblin
  Game}`) to tag that whole chapter — untagged chapters default to
  "Base Game". `rulebook.html`/`glossary.html` show a supplement tab row
  (All / one per distinct tag) above the Contents sidebar when there's
  more than one; see the MARKDOWN SOURCES doc in `convert.py` for the
  exact syntax. Put a new supplement's rules content in its own tagged
  chapter (or a tagged subsection within an existing chapter, for a rule
  that specifically overrides a Base Game one) rather than scattering it
  untagged — otherwise it silently reads as Base Game and never shows up
  under its own tab.
- Writing new Rulebook/Glossary prose (not just fleshing out a stub, but
  a section that has to sound like the rest of the book): read a few
  neighboring sections first and match their shape sentence-by-sentence,
  not just topically. What's been consistent across the existing text:
  a rule paragraph opens with the in-fiction "why would this come up"
  framing before the mechanical rule itself; asides get tacked onto a
  sentence with `- ` rather than parenthesized or split into a separate
  sentence; a worked "Example:" paragraph follows, reusing the existing
  cast of named characters (Browndog, Hilde, Carrick, Jackal, Felix,
  Beornhard...) rather than inventing new ones, and walks through actual
  numbers the way the surrounding examples do (Skill Total + card value
  = result, compared to the difficulty). Apostrophes/quotes in this file
  are curly (’, “ ”), not straight — check with `grep -o "[a-zA-Z][''][a-zA-Z]"`
  if unsure which is more common in the surrounding text before adding a
  large block. Don't reach for bullet-point summaries mid-prose the way
  a fresh-start explanation might — the book's rule sections are written
  as continuous paragraphs, with bullets reserved for actual enumerated
  lists (steps, options, factors). Repeated-count phrasing is always
  spelled out as a word, never a numeral, and never "N times" for small
  N: once (or just the bare effect — "Good Luck", not "1 Good Luck"),
  twice, thrice, then "four times"/"five times"/... from there on. This
  applies both to stacking an effect (Good Luck twice, Protected thrice)
  and to multiplying a value in a formula, bracketed or not (twice your
  Speed, thrice the Level, [four times X]) — same convention either way.

## Design conventions established so far

- **Skill Total**, not the raw skill value, is used for every calculation
  that references a skill — Accuracy, all Defenses, Reflex, Might
  Requirement checks. `skillTotalValue(statPoints, skillPoints, skill)` is
  the one formula for this. The raw skill *value* (skill points alone) is
  used only for technique prerequisites.
- Pass/fail badges are red `#e0645f` (unmet/bad) and green `#6fae5a`
  (met/good) — established by the Might Requirement badge, reused for
  Wounded. Keep using these two colors for any future met/unmet indicator
  rather than inventing new ones.
- "Session-tracking" state (Expended checkboxes, current Health) persists
  to localStorage like everything else, but is deliberately excluded from
  `doExport()`/single-character `doImport()` — sharing or exporting a
  build shouldn't hand off someone else's mid-encounter state. It's
  included in Duplicate and Backup-all/Restore-all, since those are meant
  to be full round-trips of the same character. `currentCharacterData()`
  is the single source of truth for "everything about the active
  character" and feeds the persist effect, Duplicate, and Backup-all —
  extend that one function rather than adding a parallel payload builder.
- Character slots: `localStorage` can hold more than one character
  (`flagonquest-characters` registry + `flagonquest-char-<id>` per
  character). Opening a share link, importing a file, or duplicating
  always lands in a **new** slot and switches to it — never overwrites
  whichever character was already open.
- Comment style throughout the codebase leans on explaining *why*, not
  restating *what* the code does — a hidden constraint, a workaround, a
  non-obvious tradeoff. Match that when adding code; don't pad with
  comments that just narrate the next line.
- Keep design consistent across similar objects rather than styling each
  one from scratch. Text pages (Rulebook, Glossary) share the same prose
  formatting conventions — e.g. `renderBlock`'s bullet-list detection and
  "Example:" italics are duplicated by hand across `rulebook.html` and
  `glossary.html` (same reasoning as the shared-helper note under
  Architecture) so a Markdown convention added to one reads the same way
  on the other. Tiles for items/techniques/materials/etc. share look and
  feel (card background/border, badge shapes, the red/green pass-fail
  colors above) rather than each inventing its own. When adding a new
  convention to one of these families, check whether its siblings should
  pick it up too instead of only fixing the one spot that prompted it.

## Verifying UI changes before committing

There's no CI here, so every UI change gets manually verified in a
sandboxed copy before it's committed:

1. Copy the changed file(s) into a scratchpad `testsite/` directory that
   already has React/ReactDOM/Babel vendored locally (avoids depending on
   CDN access in the sandbox) and `sed`-replace the CDN `<script>` tags
   with the local copies.
2. Serve it with `python3 -m http.server 8123` in the background.
3. Drive it with Playwright (`chromium.launch({ executablePath:
   '/opt/pw-browsers/chromium' })`), screenshot the relevant states, and
   actually look at the screenshots — don't just trust that the code
   "should" render correctly.
4. For print-affected changes, also check `page.emulateMedia({ media:
   'print' })` renders correctly, since the print stylesheet
   (`@media print` in index.html) is a totally separate flattened
   black-on-white layout with its own rules.
5. Only then commit and push.

Two recurring environment quirks worth knowing:
- Combining `pkill -f "http.server 8123"` with starting a new background
  server in the same bash call often reports a spurious "Exit code 144"
  even though it worked — re-run just the server-start command standalone
  afterward and verify with `curl -s -o /dev/null -w "%{http_code}\n"
  http://localhost:8123/index.html` (expect `200`).
- Playwright's `hasText` does substring matching, which can catch an
  unintended element with similar text (e.g. "+ Add" matching both a
  technique's and an unrelated tile's add button, or one card's text
  mentioning another card's name). Prefer an exact match — e.g.
  `.filter({ has: page.locator('span', { hasText: /^Exact Name$/ }) })`
  — whenever a test's pass/fail depends on hitting the right element.

## Git workflow

- Develop on the designated feature branch (check the task/session
  instructions for its current name), never directly on `main`.
- Commit messages explain *why*, matching the existing log — not a
  changelog restating the diff.
- Only merge into `main` when explicitly asked. Fetch both branches first
  and confirm `main` has nothing the feature branch doesn't (a clean
  fast-forward) before merging — if `main` has diverged, that needs a real
  merge/rebase decision, not an assumed fast-forward.
- Add a new dated entry to `README.md`'s changelog section for each
  notable commit — skip pure internal housekeeping (file reorganization,
  a stale comment fix) that doesn't change anything a user would notice.
- Before committing, always check `git status`/`git diff --stat`, and
  fetch + compare against `origin/<branch>` to confirm nothing else
  changed the remote branch since the last push.

## Things considered and deliberately not done

- **Persistent/live character links** (so a shared link always shows the
  latest edit): would need external storage since GitHub Pages is static
  — discussed a GitHub Gist–backed approach (unique ID per character,
  publish via a Personal Access Token, read-only for anyone without one)
  and a Firebase/Supabase-backed real-login alternative. Decided the
  added complexity (token setup, or a new third-party service) isn't
  worth it yet versus just re-sharing a link/file after edits. Worth
  revisiting if this becomes a bigger pain point.
- **Cross-platform "Sign in with Google/GitHub"**: not achievable from a
  static site without a small backend to hold an OAuth secret — noted in
  case it comes up again.
