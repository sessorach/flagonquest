# Working on FlagonQuest

Conventions and practices for maintaining this site — read this at the
start of a session to pick the workflow back up without re-deriving it.
For what the project *is* and what's shipped, see `README.md`. For the
data-format mini-syntaxes (Prereq Check, Feature Budget, Builder Notes,
Choice Effects, Base Item Options), see the docstring at the top of
`scripts/convert.py` — that documentation is authoritative and
shouldn't be duplicated here. For the *why* behind a specific rules or
balance decision, see `design/RULES_DESIGN.md` (a human-readable log of
design reasoning as decisions get made — rules content, not workflow
notes) and `design/balance.md` (aggregate balance-approach notes,
building on the value-economy model explained in
`archive/flagonquest_balance_notes_model.md`). This file (`CLAUDE.md`) is
where *my own* working notes belong instead — file-location facts,
standing verification habits, session workflow — not `RULES_DESIGN.md`,
which should stay a clean decision record.

## Architecture

- `index.html`, `rulebook.html`, `glossary.html` are independent, single-file
  React 18 apps — CDN React/ReactDOM/Babel-standalone, JSX compiled in the
  browser, no build step, no shared imports between the three files. Small
  shared helpers (`withGlossary`, `GlossaryTerm`, the header nav) are
  duplicated by hand across them and kept in sync manually — there's no
  build step to share code through. `index.html` also pulls in
  `qrcode-generator` from CDN (the "Show QR code" share overlay) — same
  pattern as React/ReactDOM/Babel, a plain `<script>` tag exposing a
  global, no bundler involved.
- `index.html`'s tab is deep-linkable via a `?tab=<build|techniques|
  items|sheet|notes>` query param, read once by a lazy `useState`
  initializer (`initialViewFromUrl`/`VALID_VIEWS`) — deliberately the
  query string, not the URL hash, since the hash is already reserved for
  share-link `#build=<encoded>` character data. `rulebook.html`/
  `glossary.html`'s header nav links point at `index.html?tab=...` so
  "back to the Builder/Techniques/Items/..." from another page lands on
  the right tab instead of always defaulting to the Character Sheet. The
  query param's own naming matches the tab labels users see
  ("techniques", not the `view` state's old internal "browse") — a
  second effect strips `?tab=...` back off the URL right after that
  initial render consumes it, since it's a one-time landing instruction,
  not a live mirror of which tab is open (same reasoning as dropping the
  live `#build=` mirroring below).
- Game content lives in `scripts/*.csv` (plus `scripts/rulebook.md` and
  `scripts/glossary.md` for hand-written prose) and is compiled to
  `data/*.json` by `scripts/convert.py`. **Never hand-edit `data/*.json`**
  — it's generated output, and edits will be silently blown away next time
  someone runs the converter. Run `python scripts/convert.py` from
  anywhere (it resolves paths off its own file location) after any CSV
  change, and commit the regenerated JSON alongside the CSV.
- `items.csv` has an **`Archetype`** column (Potions only, so far) purely
  for my own reference during balance work — informal groupings like
  "Buff", "Healing/Protection", "Resource", "Utility" that don't
  correspond to anything the site displays. `convert.py`'s `ITEM_MAP`
  has no entry for it on purpose, so it's silently dropped during
  conversion and never reaches `data/items.json` — confirmed empty diff
  on `data/items.json` when this column was added. Keep it that way;
  if a grouping like this ever needs to actually show up in the app, it
  should get folded into the real `Tags` column instead, not this one.
- **The data should be the source of truth, not prose.** Whenever the
  site needs a fact at runtime that could reasonably live as a real CSV
  column/JSON field, put it there instead of deriving it by
  regex-scraping free text. A prose-derived shortcut looks like it works
  right up until the prose it depends on gets reworded, moved to a
  different column, or just doesn't quite match the pattern anymore —
  and then it tends to fail *silently*, not loudly. (This is exactly how
  Feature Budget broke: `parsePointBudget()`'s fallback regexed the
  "Points: Level 1: 3 basic; ..." sentence out of `Effects`, but that
  sentence had since moved into the `Building` column (since renamed to
  `Builder Notes` — see Design conventions below) — the regex kept
  matching nothing, `budgetMap` came back `null`, and the Feature-builder
  quietly stopped enforcing point limits at all, for months, with no
  error anywhere.) When adding something that could be derived from
  prose, prefer a real column from the start. When you come across an
  existing derive-from-prose shortcut, prefer migrating it to real data
  over patching the derivation — see `Prereq Check` and `Feature Budget`
  in `scripts/convert.py`'s docstring for the two this project has
  already done this for.
- `archive/` holds genuinely dead files — an old prototype, stale one-off
  outputs from completed migrations, and historical source documents
  (old design docs, the designer's balance-notes spreadsheet, and its
  reading-guide companion `flagonquest_balance_notes_model.md`, which
  explains the value-economy model in that spreadsheet) kept for
  reference. Nothing in it is read by the site or by `convert.py`.
- `design/` holds living design documentation — `RULES_DESIGN.md` (a
  human-readable log of rules-design reasoning, growing as decisions get
  made), `balance.md` (aggregate balance-approach notes),
  `balance_weights_notes.md` (the full derivation behind every current
  THE TABEL weight), and `IDEAS_BACKLOG.md` (loose not-yet-drafted ideas
  for items/abilities/content — a holding pen, not a commitment; move an
  idea out once it's actually drafted into the real CSVs and given a
  proper writeup, don't leave it duplicated in both places) — plus
  `balance_weights.csv`, a fast-lookup index of the same weights (current
  value, Locked/Pencil status, which markdown section has the derivation)
  for quick reference without scanning prose. Unlike `archive/`, this is
  meant to be read and extended, not
  just kept for the record.

## Quick reference

- The full 25-skill list with its governing Stat lives in `index.html`'s
  `STAT_SKILLS` constant (~line 488), not as a single table anywhere in
  the rulebook prose — cross-check there, not from memory, if the skill
  list ever seems off.
- Skill descriptions (flavor + mechanical blurb) are `####` headers
  under each Stat's `###` section in `rulebook.md`, roughly lines
  13–151.
- Common Effects keyword definitions (Bleeding, Crippled, Frightened,
  Harried, Hasted, Necrotic, Protected, Slowed, Taunted, Vulnerable,
  Ward) are in `glossary.md` under "# Common Effects", ~line 121–176.
  The `[Stance]` rules tag is ~line 113.
- `parse_markdown_sections` in `convert.py` (~line 596) treats every
  non-blank, non-heading line in `rulebook.md`/`glossary.md` as literal
  rendered body text — no HTML-comment stripping exists. Never leave
  draft/review markers inside those files; draft in chat first, commit
  clean. Since a marker can't live inline, track "the designer still
  wants to read this over" separately instead: append an entry to
  `design/PROSE_REVIEW_QUEUE.md` (file/section/one-line summary/commit
  hash) whenever a `rulebook.md`/`glossary.md` prose section gets
  written or edited — a running checklist the designer deletes entries
  from as they review them, not a permanent log (git history is that).
- **Verify, don't assert, especially on any math** (crafting formulas,
  worked examples, balance-model calculations) — standing instruction
  from an explicit correction earlier in this project's history: a
  worked example was presented with more confidence than had actually
  been verified, and it took the user's correction to catch it, not a
  self-check. When a claim involves arithmetic, actually compute it and
  check the result is internally consistent before presenting it — don't
  write plausible-looking numbers and trust they work out.
- **Old-term translations to apply on sight, from earlier eras of this
  project**: "Bodily Defense" → **Vital Defense** (found live in
  `items.csv`'s own schema and `index.html` until this got fixed, not
  just an archive-only artifact — worth a second look if it turns up
  anywhere else), "Soak" → **Resist**. When reading `archive/` source
  material or old drafts, translate these automatically rather than
  treating them as a different mechanic.

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
- Every content table (`techniques.csv`, `items.csv`, `backgrounds.csv`,
  `features.csv`) splits flavor text from rules text into two columns —
  `Description (Fluff)` (italicized, hidden on the read-only Character
  Sheet) and `Effects` (always shown). This is a schema-level rule, not
  a per-row judgment call: every table gets both columns even if a
  given row's Fluff ends up blank (most `features.csv` rows will, since
  a Feature is a small modular snippet with little room for its own
  flavor — that's fine, blank Fluff is a normal, common state, not a
  gap to fill in). When adding a new row, if the text has a genuine
  flavor lead-in (scene-setting, in-fiction "why," no rules content) put
  that in Fluff and the actual rule in Effects, rather than leaving the
  two blended into one column. If existing rows still have them blended
  when you're touching that content for another reason, split them out
  while you're in there instead of leaving the exception in place.
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

- **Mobile is a first-class target, not a scaled-down desktop.** This is
  a tabletop companion app, and a lot of players run it from a phone at
  the actual table, not a desk — a component that reads fine on desktop
  but cramps, overflows, or wastes space on a phone is a real gap to
  close, not optional polish to get to eventually. The sitewide mobile
  zoom bump (see Type scale below) covers "everything reads a bit
  bigger" for free, but a component with real mobile-specific needs —
  its own layout, its own spacing, a size that isn't just desktop's
  number times a fixed ratio — should reach for the design tokens (see
  below) instead of fighting zoom with one-off `!important` overrides.
  Expect more of these over time, not fewer; build new mobile-aware
  components against the token pattern from the start rather than
  bolting a workaround on after the fact.
- **Skill Total**, not the raw skill value, is used for every calculation
  that references a skill — Accuracy, all Defenses, Reflex, Might
  Requirement checks. `skillTotalValue(statPoints, skillPoints, skill)` is
  the one formula for this. The raw skill *value* (skill points alone) is
  used only for technique prerequisites.
- Techniques can carry a machine-checkable `Prereq Check` column (see the
  PREREQ CHECK doc in `convert.py`) alongside the free-text `Prereqs
  (Full)` — a small mini-syntax of Skill/Stat-and-threshold and
  Technique-name clauses, ANDed together. `meetsPrereqCheck` in
  `index.html` evaluates it against the current build and renders a
  red/green "✓ Met"/"✗ Not met" badge next to the Prereqs line, same
  colors as the Might Requirement badge. Not every technique has one —
  "(Based on option chosen)"-style prereqs genuinely can't be expressed
  in the syntax, so those stay blank and just show the plain text with
  no badge. `Craft 2 (if Smithing/Carving/...)`-style School-conditional
  text *can* now be expressed, via Choice clauses — see below. A
  level-scaling threshold (`[Level]`,
  `[Level]+1`) only evaluates when the technique itself has one fixed
  Level — for a Buildable technique with a Level range, which Level
  you'd build it at isn't chosen yet while just browsing, so
  `meetsPrereqCheck` returns `null` (no badge) rather than guessing —
  same "flag readiness, don't guess" rule the crafting School-matching
  already follows. When adding a new technique, fill in `Prereq Check`
  whenever the Prereqs text is expressible in the syntax; don't leave it
  blank just because it's extra work.
- The Builder tab has a prereq summary panel (between the XP tracker and
  the Stats & Skills grid, `StatsPanel`'s `prereqSummary` prop) that
  rolls up every technique currently in the build's `Prereq Check`
  clauses into one deduplicated list — two clauses naming the same
  Skill/Stat/OR-group collapse to a single entry at the higher
  threshold, since meeting the higher one always satisfies the lower.
  `summarizeBuildPrereqs` (`index.html`) does the merge; `App()` memoes
  it and passes it down, following the same "computed value lives in
  `App()`, component just renders what it's given" split as `knownXP`/
  `unknownCount`. It reuses `configs[uid].level` to resolve a
  level-scaling threshold per build-instance (the same lookup
  `needsLevelPicker` already gates elsewhere) rather than adding new
  tracking, and only the Builder's `<StatsPanel>` call site gets the
  prop — the read-only Character Sheet's does not, since "what does my
  build still need" is a build-time concern, not a reference one.
- A technique that makes you choose something when you learn it
  (Artisanal Training's School, Soulblade's weapon type) uses the same
  per-copy `notes[uid]` a plain free-text note would, just with a
  `<select>` swapped in for the `<textarea>` — see `Free Text` in
  `convert.py`'s `TECHNIQUE_MAP` comment and `choiceOptions` in
  `TechCard`. `Free Text` is `TRUE` for a genuinely open-ended pick
  that doesn't fit a fixed list (Temper Soulblade's GM-approved
  Masterwork power), or a specific value (`"School"`, `"Weapon"`)
  naming which dropdown to render and which existing data to populate
  it from — `CREATION_SCHOOLS` for School, Base Game `Category:
  "Weapon"` items for Weapon, `PROFESSIONS` for Profession,
  `eligibleBackgrounds(...)` for Background. No new state, no new
  storage — a dropdown is just a pickier textarea. When a technique
  needs a new kind of structured pick, prefer this pattern (reuse
  `notes[uid]`, add one more `Free Text` value, source the options from
  data that already exists) over inventing a parallel per-technique
  state map.
- `Prereq Check` also supports a literal `None` cell — parses to `[]`
  (an empty-but-present clause list, trivially met, distinct from a
  genuinely blank cell which parses to `null`/no badge) — for a
  technique whose Prereqs text really is "None" and should still show
  a green "✓ Met" badge rather than no badge at all.
- `Prereq Check` also supports Choice clauses —
  `ChoiceField{value1|value2=Skill:N; value3=Skill:N&OtherSkill:N}` —
  for a technique whose actual prereq depends on its own `Free Text`
  pick (Artisanal Training's School decides whether it's Craft 2 or
  Mixology 2; Profession's ten options each carry their own prereq,
  several of them multiple ANDed skills — Apothecary needs Survival 1
  *and* Medicine 1 *and* Mixology 1). `ChoiceField` matches the
  technique's `Free Text` column value (e.g. `School`); branches are
  `;`-separated (not `,`, so the syntax survives the top-level
  comma-split), each `when-values=<clauses>` — one or more
  Skill:N/(Skill1|Skill2):N/AnySkill:N clauses, `&`-separated (not `,`,
  same reason) if there's more than one, ANDed within that branch.
  Parsed branch shape is `{when, clauses}` (always a list, even for a
  single clause) — `meetsPrereqClause`'s choice-type branch resolves
  all of a branch's clauses and ANDs the results the same three-state
  way `meetsPrereqCheck` ANDs top-level clauses (`null` if any clause is
  ambiguous, otherwise `every(Boolean)`); `summarizeBuildPrereqs`
  flattens a resolved branch's `clauses` array the same way it iterates
  top-level ones. `meetsPrereqClause`/`meetsPrereqCheck` take a `choice`
  param (the build-copy's own picked value) to resolve which branch applies,
  returning `null` (no badge) if the choice hasn't been made yet — same
  "flag readiness, don't guess" rule as level-scaling thresholds.
  TechCard's single aggregate badge only reflects the *first* instance's
  choice (a known, accepted simplification); the Builder's Prereq
  Checker summary panel (`summarizeBuildPrereqs`, which already takes a
  `notes` param) resolves each build entry's choice correctly since it
  iterates per-instance anyway.
- **Choice Effects**: for a technique whose Free Text options each do
  something genuinely different (Profession's ten options each grant a
  distinct Good Luck benefit) rather than the same effect worded once
  regardless of pick (Artisanal Training's Schools all just say "you're
  trained in crafting using the chosen School"), an optional `Choice
  Effects` column holds one "Option Name: effect text" line per option
  — real structured data (`choice_effects` in the JSON), not a regex
  slice of the shared Effects prose, per the data-over-prose principle
  above. TechCard collapses its Effects display down to only the
  option(s) actually picked once *every* copy has a choice made —
  every *distinct* pick across every instance (`madeChoices`), not just
  the first, so a repeatable technique learned twice for two different
  options (Profession for both Sailor and Apothecary) shows both lines,
  not only whichever was learned first. On the Builder, falls back to
  showing every option (the full unfiltered list) while browsing, or
  while *any* copy is still sitting on its default "Choose a ___…"
  (`anyChoicePending`) — e.g. adding a second copy of an already-picked
  repeatable technique — so there's always a way to compare the
  remaining options instead of the list vanishing the moment one copy
  is picked; same "don't guess" rule as everywhere else this pattern
  shows up. The read-only Character Sheet skips that fallback entirely
  (`anyChoicePending` is forced `false` there) — it's a reference for
  what's actually been picked, not a picker, so a copy that hasn't been
  assigned a choice yet shows nothing for that copy instead of the full
  list, and the block drops out completely once `madeChoices` is empty.
  The Prereqs
  *line* stays tied to `firstChoice` like the badge next to it always
  has been (not `madeChoices`) so the text and the badge on that one
  line never describe two different picks — `formatResolvedChoicePrereq`
  swaps a vague "(Based on option chosen)" Prereqs text for the concrete
  resolved one ("Survival 1, Medicine 1, Mixology 1") once a choice is
  made, built straight from the same Prereq Check data the badge
  already resolves against rather than a second hand-typed copy of the
  same facts. Choice Effects (unlike the Prereqs line) still shows on
  the read-only Character Sheet, since it IS the technique's actual
  effect, just picked — Prereqs/the badge stay hidden there like they
  always have, a build-time concern rather than a reference one. The
  per-copy Free Text block (the "Copy 1: Sailor" / "School: Smithing"
  static record under Effects) is hidden on the Sheet specifically when
  the technique has Choice Effects — that prose already says what was
  picked, so a flat "Copy 1: Sailor" underneath would just repeat it in
  a plainer form. A `choiceOptions` technique with no Choice Effects
  data (Artisanal Training's School, Soulblade's Weapon type) still
  shows this block on the Sheet, since it's the only record of the pick
  that exists there.
- **Grants Technique**: a background can auto-grant a technique the
  moment it's selected — `grants_technique` on `backgrounds.json`
  (Creator → Artisanal Training, Professional → Profession) — free of
  XP, not manually removable, but its own choice dropdown (School,
  Profession, ...) still works normally. A `useEffect` in `App()` near
  `toggleBackground` syncs `build` to match `selectedBackgrounds`,
  materializing/removing entries with `granted: true`. It uses a
  **deterministic uid** (`granted-${backgroundId}`, not `makeUid()`) so
  the existing uid-keyed `notes`/`configs` state transparently preserves
  the chosen School/Profession across refreshes and re-selecting the
  same background — no separate persistence needed. `granted: true` is
  threaded through: excluded from XP (`knownXP`/`unknownCount`/
  `totalXP` filter to `chargeable = buildEntries.filter(e => !e.granted)`
  first), excluded from single-character `doExport()`'s techniques list
  (re-derived automatically on import via the same sync effect — including
  it would double-add on `doImport()`), and passed down as a `grantedUids`
  Set so `TechCard`/`BuildPanel` lock the Remove/Duplicate controls on a
  granted copy while leaving its choice dropdown editable. Whole-browser
  Backup/Restore-all and Duplicate-character round-trip raw state
  directly and don't need this special-casing.
- A technique can also let a player pick an *additional* background
  beyond their normal two Builder-tab slots (Extensive Background, via
  `Free Text: "Background"`) — the pick lives in the same per-copy
  `notes[uid]` as any other choice dropdown, sourced from
  `eligibleBackgrounds(backgrounds, backgroundType, enabledSupplements)`
  (a shared helper, also used by `BackgroundsSection`'s own picker grid,
  following the chipStyle/collapseBtnStyle "reach for the shared helper"
  precedent). It only feeds the read-only Character Sheet's background
  display, via `effectiveBackgroundIds` in `App()` (`selectedBackgrounds`
  plus any Background-type Free Text picks, deduped) — the editable
  Builder-tab picker grid still shows only the normal two slots, since
  the extra pick's own UI lives on the granting technique's card.
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
  whichever character was already open. The header's "Manage
  Characters" button (`CharacterManagerOverlay`) is the one place that
  lists every slot at once — switch/duplicate/delete/reorder, plus "New
  Character" as the last row in the same list rather than a separate
  toolbar button, so it reads as "the next slot." Reordering
  (`moveCharacter`) just splices the `characters` array itself, same
  drag-and-drop pattern as `moveTechniqueGroup`/`moveSheetSection`
  elsewhere in the file — there's no separate order field to keep in
  sync. `duplicateCharacter`/`deleteCharacter` both take an explicit id
  (not just "the active one") so the overlay can act on any row, not
  only whichever character happens to be open. Backup/Restore-all (and
  their localStorage-only warning note) live in this overlay too, below
  a divider under the character list — they act on every character in
  the browser at once, not the one open on the Builder tab, so they
  belong with the other whole-browser actions instead of competing for
  space with the single-character Export/Import buttons there.
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
- Within `index.html` specifically (one file, so no import to share
  through — everything just has to live at top level), a few small
  helpers exist precisely so per-tab code doesn't reinvent them:
  `chipStyle(active)` for any toggle-able filter chip button (Items'
  Keyword/Supplement, Techniques' Related skills/Tags, Crafting's type
  filters all use it), `collapseBtnStyle` for a collapsible section's
  Show/Hide button (Sources, Backgrounds, Crafting), and
  `toggleInArray(setter, value)` for flipping a value in/out of an
  array-backed multiselect filter's state. These used to be copy-pasted
  three-plus times each, one per component that needed them, some
  acknowledged in a comment ("same look as X's chips") and some not;
  reach for the shared one before writing a new local copy.
- Share links (`encBuild`/`decBuild`) encode as a positional array —
  `[ids, name, stats, skills]` with technique IDs as bare integers and
  Stats/Skills as fixed-order arrays keyed off `STATS`/`ALL_STAT_SKILLS`
  — instead of a `{ids, name, stats, skills}` object with quoted keys,
  since the quoted keys were most of a link's length, not the actual
  data. `decBuild` still accepts the old object shape too (checks
  `Array.isArray`), so links generated before this existed keep working
  — encode compact, decode both. `buildShareUrl()` is the one place that
  turns the current build into a URL; both "Copy share link" and the
  "Show QR code" overlay call it, so they can never encode two different
  things. The QR overlay itself (`qrModuleGrid` + `QRCodeOverlay`) draws
  the code as plain SVG `<rect>`s from the module grid rather than a
  canvas/image, so it's just more React output — themable, no extra
  asset-loading step, no library dependency beyond the tiny CDN encoder.
- Full-screen modals (`QRCodeOverlay`, `CharacterManagerOverlay`) share
  actual code, not just a matching look: `ModalBackdrop` renders the
  `position: fixed; inset: 0` backdrop and the click-swallowing card
  wrapper (`e.stopPropagation()`) that every modal's content goes
  inside; `useEscapeToClose(onClose)` wires up the Escape-key listener;
  `modalCloseBtnStyle` is the × button's style. A future modal should
  reuse these three instead of copy-pasting the pattern again — that's
  exactly how QRCodeOverlay and CharacterManagerOverlay ended up with
  byte-identical backdrop/Escape/× code before this got pulled out.
- The `Building` column (Feature-built techniques' "When you learn
  this, choose features that apply..." reference text) was renamed to
  `Builder Notes` and generalized — it's now the place for any short
  reference note on how a technique's own card behaves mechanically,
  not just Feature-building instructions (e.g. Profession/Artisanal
  Training's note that the card narrows down once a choice is picked —
  see Choice Effects above). Still free text, still shown alongside
  whatever picker it explains on the Techniques/Builder tabs, still
  left off the read-only Character Sheet. Use it going forward for
  this kind of "how this card works" note on any technique whose
  behavior isn't obvious from Effects text alone, not just Buildable
  ones — that's the whole point of the more general name.
- **Fullness** (Goblin Game): a supplement-gated tracker on the
  Character Sheet's Derived Stats row, alongside Health — the first
  case of a whole sheet section (not just which items/techniques/
  backgrounds are offered) being gated by `enabledSupplements`, so if a
  second supplement-specific mechanic like this comes up, check whether
  it should follow the same `{enabledSupplements.includes("X") && (...)}`
  pattern rather than inventing a new one. Base 15 max / Too Full above
  10 per the rulebook, raised by Spacious Gut/Gorger's `Fullness Bonus`/
  `Fullness Threshold Bonus` technique columns — same known-technique-
  sum pattern as Shallow/Deep Health Bonus, all four now summed by one
  renamed `techniqueMaxBonuses` (was `techniqueHealthBonuses`) since it
  covers more than Health now. `HealthTrack` (the ❤️/🤍 pip widget) is
  now the generalized `PipTrack`, taking `fullIcon`/`emptyIcon` props
  (🍖/🍽️ for Fullness) — same "generalize once a second real use shows
  up" reasoning as the Building/Builder Notes rename above — plus two
  more props for Fullness's own needs: `step` (pip granularity — Hunger
  Debt below is `step={5}`, so its 30-point span is 6 clickable pips
  instead of 30) and `markAfter` (draws a small `┃` divider right after
  the pip reaching that value, so a threshold like Too Full or Starving
  reads at a glance on the track itself, not just from the badge once
  actually crossed). Fullness can go negative too (Hunger Debt, down to
  -30, a starvation mechanic distinct from Too Full, badged/captioned
  the same visibility-reserved way as Too Full/Wounded) — rather than
  stretch `PipTrack` to one-pip-per-point for that whole span (30 empty
  icons sitting there for a state that's rare in play), Hunger Debt is
  its own `PipTrack` at `step={5}`/`markAfter={10}` (10 being its own
  Starving threshold), fed the negated value. `currentFullness` stays
  one signed number under the hood; the two PipTracks are just two
  differently-scaled views/controls onto it, split at zero (Fullness
  clamps display to `Math.max(0, ...)`, Hunger Debt to
  `Math.max(0, -...)`, and each writes back through its own sign). Same
  session-tracking-state treatment as `currentHealth` (persists to
  localStorage, excluded from single-character Export/Import, included
  in Duplicate/Backup-all) — `currentFullness: null` in
  `emptyCharacterData` means "hasn't eaten yet" (0), not "full," the
  opposite default logic from Health's null-means-max, since a fresh
  character hasn't had a meal. `PipTrack`'s pips are `no-print` — color
  emoji don't render reliably across print engines/OSes and were
  clipping — with a `print-only` row of plain bordered boxes standing
  in instead, blank rather than reflecting current fill state, since
  the value/max text above already states the number and a fresh
  printout is meant to be checked off by hand as play happens, same as
  the boxes on a paper character sheet.
- **Type scale** (`index.html`): text runs in a few consistent px tiers
  rather than one-off sizes per component — 12 (formula lines, table
  headers, captions), 13 (buttons, Prereqs line, notes, tag/skill-chip
  text — bolded a touch heavier than the tier around it, since those
  chips are meant to read as "important rules info" someone's scanning
  for, not filler), 14 (the main reading tier — Effects/Special/Fluff
  text, most body copy), 16 (secondary UI chrome one notch above body
  text — nav tabs, modal titles, gold/XP-adjacent readouts, the Sources
  header), and 17 bold (the "this is the number/name that matters" tier
  — Skill Total's glowing badge, Derived Stats' computed values,
  Health/Fullness's own pip-track readout, and every MedievalSharp card
  title — technique/item/background/material names — unified into one
  size rather than each drifting to whatever felt right at the time).
  When adding a new piece of UI text, reach for the closest existing
  tier instead of picking a fresh number — that's what keeps a "bump
  the base sizes" pass like this one from being needed again piecemeal
  later. Two fixed-width elements (`PointStepper`'s inline count box,
  the read-only Skill grid's point-value box) had their `width` bumped
  alongside their tier's font so a 2-digit number still fits; the ⠿
  drag-handle icon and single-glyph ×/+/− buttons were deliberately left
  alone, since they're icons, not reading text, and don't need to scale
  with it. `overflow-wrap: break-word` on `body` is a new, low-risk
  safety net alongside this — larger text (and the mobile zoom below)
  means a long unbroken run in some technique's Effects text is more
  likely to actually exceed a narrow card's width than it used to,
  even though the surrounding paragraph wraps fine at spaces.
  A **mobile bump** on top of all this lives at `@media (max-width:
  639px) { .app-root { zoom: 1.08; } }` (reset to 1 under `@media
  print`, so it can't compound with the print stylesheet's own existing
  `.sheet-box`/`.tech-card` zoom values). `zoom` — not a font-size
  rule — is deliberate: every size above is a literal px number in an
  inline `style` object (no build step here to route them through
  rem/CSS custom properties), and a stylesheet `font-size` cascade
  rule only reaches elements that don't set their own — which is
  almost everything in this file. `zoom` sidesteps inheritance
  entirely and uniformly multiplies an element's already-computed
  render size, reaching inline styles a cascading rule couldn't; it's
  also already how this file's print stylesheet shrinks `.sheet-box`/
  `.tech-card`, so this isn't a new technique, just the same one aimed
  at the opposite end (narrow screens, scaling up) instead of print.
  Zoom is a blanket multiplier, though — it can't give one component a
  size that isn't some fixed ratio of its desktop value. A component
  that needs a genuinely different mobile size (not just "the same
  number, bigger") reaches for the design tokens below instead.
- **Design tokens (`--fq-text-*`)**: five CSS custom properties at
  `:root`, one per Type scale tier above (`--fq-text-caption` 12,
  `--fq-text-chip` 13, `--fq-text-body` 14, `--fq-text-ui` 16,
  `--fq-text-important` 17) — the tier system given a name a style
  object can actually reference (`fontSize: "var(--fq-text-body)"`)
  instead of retyping a literal number. This is the escape hatch the
  mobile-zoom bullet above points to: a component with real
  mobile-specific sizing needs opts its own subtree out of the ambient
  zoom (`zoom: 1`, same "reset so it can't compound" trick the print
  rule already uses) and redefines whichever token(s) it needs a
  different value for, scoped to itself via plain CSS custom-property
  inheritance rather than a `!important` override block re-deriving
  every number from scratch. See `sheet-stat-grid` below for the first
  real adopter. Adopted incrementally, same "generalize once a second
  real case shows up" bar as every other shared pattern here (see the
  first bullet in this section on why mobile work specifically should
  expect to keep needing this) — nothing sitewide gets retrofitted onto
  these just because they exist; a call site only switches from a
  literal number to `var(--fq-text-*)` once it actually needs to.
- Three more shared style constants, same "reach for the shared one"
  precedent as `chipStyle`/`collapseBtnStyle`/`toggleInArray`:
  `cardBoxStyle` (`background:"#161b27", border:"0.5px solid
  #2d3555", borderRadius:8` — the base look for a technique/item/
  background card, a Stats & Skills or Derived Stats block, an XP
  tile, and similar boxed sections; was retyped at over a dozen call
  sites), `modalCardStyle` (the same colors at `borderRadius:12`, for
  a full-screen modal's own inner card — QRCodeOverlay/
  CharacterManagerOverlay), and `statBadgeStyle` (the amber `#e8c46a`/
  `#20180a`/`#6b5423` "granted bonus" badge — an item's flat stat
  bonus, a material's type tags). Spread into each call site's own
  style object (`{ ...cardBoxStyle, padding: "10px 12px" }`) rather
  than replacing it outright, since padding/layout still varies per
  use — only the shared visual identity (color/border/radius) moved.
  `className="sheet-box"` stays on top of `cardBoxStyle` wherever it
  was already there — that class is a separate, print-only concern
  (see the `.sheet-box` print rule), not something this constant
  replaces.
- **`sheet-stat-grid`**: below the `.stat-grid` breakpoints' 560px
  cutoff, the read-only Character Sheet's Stats & Skills grid (not the
  editable Builder one — `StatsPanel` only adds this second class
  alongside `stat-grid` when `readOnly`) can still fit more than one
  box per row on a wide-enough phone, since there's no `PointStepper`
  eating column width there, just a name and a couple of plain
  numbers. Rather than a hand-picked "2 columns below Xpx" breakpoint
  (which either overflows or forces a skill name like "Performance"/
  "Masquerade" to wrap mid-letter the moment real content doesn't
  quite fit that guess), it uses `grid-template-columns: repeat(auto-fit,
  minmax(min(174px, 100%), 1fr))` — 174px is a measured worst case
  (longest skill name + the Skill Total badge + the point number + this
  rule's own tightened padding, all at once) plus a few px of headroom,
  not a guess, so the grid itself decides the column count from what
  actually fits at any given width rather than a fixed rule risking
  overflow at some width nobody tested. This is also the first real
  adopter of the design tokens above: the grid opts out of the ambient
  mobile zoom (`zoom: 1`) and redefines `--fq-text-important` to 15px
  on its own subtree, so `skill-badge`/`stat-name`/`stat-value` (all
  three already written as `fontSize: "var(--fq-text-important)"` in
  StatsPanel) just pick up the smaller size for free — no `!important`
  font-size override needed, unlike the padding/gap/width trims below
  it, which stay direct `!important` overrides since spacing isn't
  part of the token system (only text tiers are). In practice this
  means most phones in portrait (~375-414px) still render one column
  here; only wider phones/phablets/small tablets clear two — verified
  by screenshotting both the just-under and just-over side of that
  transition (~414px vs ~430px) rather than assuming the math holds.
  Worth noting since it was a genuine surprise during development: the
  `zoom: 1` reset did *not* move that crossover further down (measured
  identically before and after, both at a true content-need of 170px)
  — resetting zoom bought cleaner, `!important`-free font-size handling
  and the reusable token pattern, not extra room on top of what the
  padding/gap/width trims already gained. Two more pieces make the
  safeguard actually hold: `min-width: 0` on the box (grid items
  default to a `min-width: auto` floor of their own min-content, which
  would silently override the track size above) and the skill-name
  span's own `minWidth: 0` (same idea one level down inside the row's
  flex layout) as a last-resort wrap if some future skill name ends up
  longer than the 174px measurement assumed — better a rare wrapped
  line than a silent reintroduction of the overflow this exists to
  prevent.

## Verifying UI changes before committing

There's no CI here, so every UI change gets manually verified in a
sandboxed copy before it's committed:

1. Copy the changed file(s) into a scratchpad `testsite/` directory that
   already has React/ReactDOM/Babel (and, for `index.html`, qrcode-
   generator — the "Show QR code" overlay's dependency) vendored locally
   (avoids depending on CDN access in the sandbox) and `sed`-replace the
   CDN `<script>` tags with the local copies.
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
- For rules/design prose specifically: draft in chat, matching voice per
  this file's Rulebook/Glossary prose guidance, get confirmation, then
  commit — one focused commit per section. No in-file review markers;
  git diffs/commits are the review record.

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
