# FlagonQuest

FlagonQuest is a browser-based companion site for the FlagonQuest tabletop
RPG — a beer-and-pretzels TTRPG for the modern gamer. It's a technique/item
browser, character builder, and printable character sheet, all in a single
static HTML file with no build step, deployed via GitHub Pages. Game
content (techniques, items, backgrounds, and so on) is maintained as
spreadsheets under `scripts/` and converted to the JSON the site reads via
`scripts/convert.py`.

## Changelog

Notable changes, newest first. Each entry is a summary — see `git log` for
the full commit-by-commit detail behind any of these.

### 2026-08-17 — Choice-based prereqs, Grants Technique

- **Artisanal Training** and **Profession** now use a real dropdown to
  pick their School/Profession when you learn them, instead of a plain
  free-text note — the same mechanism as Soulblade's weapon-type picker.
  Artisanal Training's prereq badge now correctly checks Craft/Mixology/
  Survival based on which School you picked, instead of showing no
  badge at all.
- **Profession**'s full original text — each of the ten options'
  specific Good Luck benefit and prereq (Apothecary, Artisan, Busker,
  Fisher, Gatherer, Grifter, Merchant, Sailor, Tactician, Theologian) —
  had gone missing from the data at some point; restored it, and wired
  up its prereq badge the same way as Artisanal Training's. Several
  options (Apothecary, Artisan, Fisher, Merchant, Sailor) need more than
  one skill at once, which needed a small extension to the Prereq Check
  syntax to express.
- **Profession**'s and (going forward) any similar technique's card now
  narrows down to just the option(s) you've actually picked instead of
  always showing the full list — pick Apothecary and only its benefit
  and prereq show, learn a second copy for Sailor too and both show,
  side by side. The old catch-all "Building" column (Feature-built
  techniques' behind-the-scenes build instructions) has been renamed to
  the more general "Builder Notes" and picked up a short explainer on
  Profession/Artisanal Training's cards about how this narrowing works.
- **Extensive Background** now has its own dropdown to pick an
  additional Background you qualify for, and correctly shows a green
  "Prereqs: None — ✓ Met" badge instead of no badge. The extra
  Background you pick shows up on the Character Sheet alongside your
  normal two.
- **Creator** and **Professional** backgrounds now automatically grant
  you Artisanal Training / Profession the moment you select them — free
  of XP, with their own School/Profession dropdown, but not manually
  removable (deselect the background to remove the granted technique
  instead). The Builder's XP totals, and single-character Export/
  Import, correctly treat these as free and don't double them up.

### 2026-08-17 — Prereq summary panel, share-link cleanup

- The Builder's prereq summary panel is now labeled "Prereq Checker."
- The URL no longer mirrors the current build in a `#build=...` hash
  during normal use — that only ever served refresh persistence, which
  character slots/localStorage already handle.
- Share links are now much shorter (a typical build's link is roughly a
  third of its old length) — same data, just packed more efficiently
  instead of as a quoted-key JSON object. Older links still open fine.
- Added a **"Show QR code"** button next to Copy share link — pops up
  the current build's share link as a scannable code, so someone else
  at the table can open it on their phone without typing a URL.
- "Copy share link" no longer puts the link in the address bar either —
  it only ever copies to the clipboard now (falling back to a native
  copy-this-text prompt if that's blocked).
- **Character switching overhauled**: the header's character dropdown
  plus separate "+ New"/"Duplicate" buttons are now one "Manage
  Characters" button that opens a list of every character with
  Switch/Duplicate/Delete on each, drag-to-reorder, and a "New
  Character" row at the end of the list. Also removed "Clear build"
  from the Builder tab — Delete (or just starting a new character)
  covers that now.
- The Rulebook/Glossary header's Techniques link now says `?tab=
  techniques` when you hover it, matching the tab's actual name
  (it used to read `?tab=browse`, an old internal name). The `?tab=`
  query string also disappears from the address bar right after it
  lands you on the right tab, instead of sitting there — stale — once
  you switch to a different one.
- **Builder tab tidy-up**: Export/Import/Share/QR code are now a small
  button grid to the right of the Character name/Concept fields
  (wrapping below them on narrow screens) instead of a full-width row
  underneath. Backup/Restore all characters, and the localStorage
  warning note, moved into the Manage Characters overlay — they act on
  every character in the browser, not just the one open here. The
  Sources header is bolder and brighter than its neighbors now, since
  it's the one section that starts collapsed.
- Fixed wrapped header/Builder-row elements landing off-center on
  narrow-but-not-mobile screens (roughly 500-900px) — a real
  double-checked layout issue, not just an eyeballing quirk: two items
  sharing a line and then centered as a *pair* still reads as lopsided
  when one of them (the page title) is a much wider box than its
  visible text. Each piece now gets its own row below the breakpoint
  where they'd otherwise unevenly pair up.
- Code cleanup pass after this stretch of changes: pulled the QR/
  Manage-Characters overlays' identical backdrop, Escape-key handling,
  and × button styling into shared helpers instead of two copies drifting
  apart, and swept for dead code/stale docs left over from the changes
  above. No visible behavior change.

### 2026-08-14 — Rulebook cleanup, material pricing

- Removed Jokers from the rulebook — the deck is now a standard 52-card
  deck throughout.
- Materials are now priced at their Level in Gold instead of a flat 1
  Gold regardless of grade.
- Formatting pass on the Rulebook: parallel-sentence clusters bulleted,
  worked examples italicized/indented.
- Header brand and tab nav stay centered on mobile once wrapped.
- **Crafting browser overhaul**: one row per item with a School picker
  instead of a duplicate row per School; recipes gained a Kind switch
  (Slots or Value) so generic fallback recipes now cover Potions,
  Poisons, Grenades, Food, and un-authored Masterwork items; Masterwork
  base-item choices get a real picker; Artisanal Training can grant
  School training; filters are now independent checkboxes/chips.
- Two new Goblin Game techniques, **Spacious Gut** and **Gorger**
  (raise max Fullness, change what happens when Too Full; Gorger
  requires Spacious Gut). Techniques gained a **Supplement** column,
  gated by Sources like items/backgrounds already were.
- **Goblin Game Food System**: new Rulebook chapter on Fullness, daily
  food needs, **Too Full**, the five Food Material varieties, and the
  Meal recipe. Rulebook/Glossary chapters can now be supplement-tagged
  and filtered via a tab row when more than one supplement exists.
- More Goblin Game content from the full player doc: Goblin Traits,
  Gems, **Bingus**/**Golden Bingus**, The Great Game, Deeds — added to
  the Glossary where relevant.
- Rulebook/Glossary header links navigate in place instead of opening a
  new tab.
- Techniques gained an **Excluded By** column for when a different
  enabled supplement makes a technique nonsensical — hides Pranic
  Nourishment and Land's Bounty and swaps in a Goblin Game version of
  Street Runner once Goblin Game is enabled.
- Header is pinned again on desktop at the compact single-row width;
  still scrolls away normally on narrower/wrapped layouts.
- Exported files are named after their contents (`<character
  name>-<date>.json`, `FlagonQuest-export-<date>.json`) instead of
  generic filenames.
- Land's Bounty's Difficult Terrain now scales with Mind ("up to
  [Mind] levels") instead of a flat single level.
- **Supporting** now has real rules: a flat difficulty 11 check that
  grants Good Luck on success, moved next to Skill Checks and Gambling.
- Character Creation moved to the end of the Rulebook's chapter list.
- Standardized repeated-count phrasing ("twice"/"thrice"/"four times")
  across the Rulebook, techniques, items, and features.
- Food-created items now spoil a week after being made, matching raw
  Food materials (previously just a day).
- **Site-wide consistency pass**: fixed a glossary tooltip bug with
  multi-paragraph entries, a broken Travel Rations price, several
  unfinished Rulebook sentences, and straight quotes/apostrophes
  standardized to curly; deduped a few copy-pasted style helpers in
  the code with no visible effect.
- **Consistency pass, round two**: split out **Basic Travel Ration** as
  a plain store-bought Pack/Gear item, distinct from the craftable
  Food-category version; rewrote Rapport's blurb ahead of the Social
  rework; unified `Relevant Skills`/`relevant_skills` naming across
  techniques and items; split `backgrounds.csv`/`features.csv` into
  `Description (Fluff)`/`Effects` columns; filled in three stub
  Rulebook spots; renamed Character Creation's opening section to
  "Building a Character."
- **Automatic prereq checking**: techniques with a machine-checkable
  `Prereq Check` show a red/green "✓ Met"/"✗ Not met" badge on their
  Prereqs line while browsing, evaluated against the current build
  (140 of 143 techniques; the rest stay plain text where the syntax
  can't express them).
- **Fixed a live bug**: the Feature-builder (Battle Maneuver, War
  Magic, Healing Magic, Spirit Blessing, Social Maneuver) was silently
  ignoring its own point budgets after its prose-scraping fallback
  broke; now driven by a real `Feature Budget` data column instead.
- Rulebook/Glossary header nav can jump straight to a specific Builder
  tab (`index.html?tab=items`, etc.) instead of always landing on the
  Character Sheet.
- **Artisanal Training and Soulblade get real pickers**: School and
  weapon type are now dropdowns instead of free text.
- **Builder prereq summary panel**: a new panel between the XP tracker
  and Stats & Skills grid lists every Skill/Stat/Technique the current
  build requires, collapsed to the highest threshold, with the same
  red/green Met badge as the per-technique Prereq Check line.

### 2026-08-11 — Crafting materials framework

- New **Material** item category for crafting resources, tagged with one
  or more Material Types (Metal, Wood, Fire, and so on) — seeded a
  starter catalog of the 12 canonical Types.
- **Custom materials**: a lightweight builder (name, Level, toggle any
  number of Types) for GM-granted special materials that aren't in the
  data file, e.g. one that's both Metal and Fire.
- Materials get their own section on the Items tab and Character Sheet,
  separate from the gear grid.
- **Crafting browser** (draft): a collapsible section on the Items tab
  listing every item with a resolvable recipe, showing whether the
  current character is trained/skilled enough and has the materials for
  it, with a filter for either or both. Recipes now explicitly declare
  which items they cover (`crafting_recipes.csv`'s new "Applies To"
  column) instead of relying on eyeballing text, and Masterwork items'
  base-item requirement (if any) is shown for reference. No craft action
  yet — this is the eligibility browser, not the spend-materials step.
- Weapons/Armor/Tools recipes rebuilt around fixed **Primary/Leeway
  material slots** (e.g. 2 Metal + 1 Cloth/Leather) instead of the
  Gold-derived Base/Extra percentage split, with a separate recipe row
  per crafting School (Carving vs. Smithing, etc.) so the browser shows
  each way to make an item on its own line. Masterwork/Alchemy items
  keep the original Gold-value formula, since materials being worth
  their Level in Gold is what lets that side scale without hand-authored
  recipes.
- Items tab: **Keyword** and **Supplement** filters are checkbox
  multi-selects now, so you can show e.g. both Base Game and Goblin Game
  at once instead of picking one at a time; the custom item and material
  builders moved to sit side by side under the search bar, above the
  inventory grid.
- Catalog materials now carry a **Level** (1–5), editable per stack —
  picking a different Level splits a unit off into its own stack instead
  of reclassifying the whole pile, so you can hold e.g. both Level 1 and
  Level 3 Metal at once; crafting eligibility checks each stack's Level
  against the item being made.
- Custom material builder reworked to match the buildable-technique
  pattern: a fresh one opens straight into the name/Level/Type form, and
  "Done" collapses it down to look like a stock material tile (name, Lv
  badge, only the Types you turned on) — "Edit" reopens the form. Also
  fixes the name field clipping outside the tile.

### 2026-08-04 — Health tracking

- Character Sheet's Health box now tracks current Shallow/Deep Health, not
  just the max: a heart-pip readout you can click directly, plus a
  −/+ stepper for one-at-a-time changes.
- Hitting 0 Shallow Health auto-flags **Wounded**: a badge on the Health
  box, an automatic −2 applied to Speed and all five Defenses (called out
  in red on each), and a reminder to also apply Bad Luck to flips by hand.

### 2026-08-03 — Character management, flavor text, content sources

- **Duplicate** a character into a new slot; **Backup/Restore all**
  characters at once (everything lives in browser storage only, so this is
  the only way to back up more than one at a time).
- Removing a technique or item now shows a brief "Removed X — Undo" toast.
- Restored the full original flavor text for 66 techniques that had been
  condensed down to a single line somewhere before this repo's history —
  cross-checked against the source content document.
- **Sources** panel on the Builder tab: toggle which supplements (Base
  Game, Goblin Game) show up when picking new content, without touching
  anything already in a build.
- Un-stuck the header bar (scrolls away normally instead of staying
  pinned); Rulebook/Glossary nav links now wrap together as a pair.

### 2026-08-02 — Goblin Game content, combat math, item filters

- 14 new Goblin Game clan Backgrounds (Bloody Banner, Rockbiters,
  Black-Ear, Dampfoot, Firebug, Fardown, Troll-Food); Backgrounds and
  Techniques sections are drag-reorderable on the Character Sheet.
- Advanced filters on the Items tab (Slot, keyword, Supplement);
  Techniques default-sorted by Level then name.
- Permanent max-Health bonuses from techniques (Toughened Body/Resolve/
  Spirit) now flow through to the sheet automatically.
- Accuracy/Defenses/Reflex consistently use Skill **Total** (stat + skill
  points), not just the raw skill value; Unarmed requires a free hand.
- Custom weapon builder for freeform items; Goblin Game firearms and bomb
  variants added.
- Auto-calculated Parry Defense and weapon damage; dual-mode Thrown
  weapons (melee + thrown stats together); drag-reorder inventory.
- Masterwork base-item picker with per-level pricing; custom items with
  their own stats and stacked powers.

### 2026-08-01 — Items, Backgrounds, multiple characters

- Items and Backgrounds pickers added, with equip/parry tracking.
- Character **slots** — the browser can hold more than one character, with
  a switcher in the header.
- Print layout overhaul: compact header box, pinned footer, alternating
  row shading that actually survives most browsers' print settings.

### 2026-07-29 – 2026-07-31 — Foundation

- Initial build-out: technique browser and search, the Builder/Character
  Sheet split, Stats & Skills point-buy with XP budget, Feature-built
  techniques (Battle Maneuvers, Spells, etc.) with their point budgets,
  share links, the Rulebook and Glossary pages, and the site's branding
  and print styling.
