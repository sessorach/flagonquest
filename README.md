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

### 2026-08-14 — Rulebook cleanup, material pricing

- Removed Jokers from the rulebook — the deck is now a standard 52-card
  deck of playing cards throughout.
- Materials (catalog and custom) are now priced at their Level in Gold
  rather than a flat 1 Gold regardless of grade, matching the rule that
  a material is baseline worth its Level.
- Light formatting pass on the Rulebook, from "The Basics" onward:
  clusters of short parallel sentences (difficulty factors, creation
  Schools, Material Types, and others) are now bulleted instead of
  reading as a run of one-line paragraphs, and worked examples render
  italicized and indented to set them apart from the surrounding rules
  text.
- The header's brand and tab nav now stay centered on mobile once they
  wrap onto their own line, instead of sitting flush against the left
  edge.
- **Crafting browser overhaul**: each item now shows once, with a School
  picker if it can be made more than one way (a Weapon via Carving or
  Smithing), instead of a separate row per School. Recipes gained a
  **Kind** switch (Slots or Value) so the Gold-value model isn't
  Masterwork/Alchemy-only anymore — generic fallback recipes now cover
  Potions, Poisons, Grenades, Food, and Masterwork items that don't have
  their own hand-authored recipe yet, so browsing shows the full catalog
  instead of only the handful of items with detailed data. Masterwork
  items with a base-item choice get an actual picker instead of static
  "X or Y" text (reference only — it doesn't check inventory yet).
  Artisanal Training can now grant School training too, read from its
  free-text note. Filters are checkboxes/chips now: Skill ready and
  Materials ready independently, plus Base/Masterwork/Alchemy/Food type
  toggles.
- Two new Goblin Game techniques: **Spacious Gut** and **Gorger**,
  raising a Goblin's maximum Fullness and changing what happens when
  they're Too Full. Techniques now have a **Supplement** column (like
  items/backgrounds already did) so the Sources panel gates which ones
  show up to pick, rather than every technique always being available.
- **Goblin Game Food System**: a new Rulebook chapter overhauling
  cooking and food for Goblins around a Fullness resource — how much
  food they need per day, what happens when they don't get it or eat
  too much (**Too Full**, new in the Glossary), the five Food Material
  varieties, and the updated Meal-crafting recipe. The Rulebook and
  Glossary can now be tagged and filtered by supplement — a level-1
  heading like `# Goblin Game {Goblin Game}` tags that whole chapter,
  and both pages show a supplement tab row (All / Base Game / Goblin
  Game) above the table of contents whenever more than one exists.
- More Goblin Game rules content, pulled from the full player doc:
  Goblin Traits (Illiteracy, Loving Fire, Fear of Horses, Cannibalism,
  Hate Sunlight/Darkvision, Hungry), Gems as the Goblin equivalent of
  Gold, **Bingus and Golden Bingus** (a small Good-Luck reward for good
  roleplay or a successful/foiled scheme), The Great Game (sanctioned
  PvP scheming, character death and replacement), and Deeds (Goblins'
  reputation-by-story system in place of literacy). **Bingus**,
  **Golden Bingus**, and **Fullness** are now in the Glossary too.
  Gorger's Prereqs now include Spacious Gut, matching the source doc.
- The Rulebook and Glossary links in the header no longer open in a new
  tab — they navigate in place, like every other nav link.
- Techniques gained an **Excluded By** column for the case where an
  enabled supplement makes a *different* technique nonsensical even
  though that technique's own supplement is still on — used to hide
  Pranic Nourishment and Land's Bounty (not available in the Goblin
  Game's food economy) and to swap the standard Street Runner for a new
  Goblin Game-supplement version that grants Food Material instead of a
  day's nutrition, once Goblin Game is enabled in Sources.
- The header is pinned to the top of the screen again on desktop, so
  the nav and character switcher stay reachable while scrolling — but
  only at the width where it's a single compact row; on narrow screens
  where it can wrap onto several rows it still scrolls away normally,
  same as before, so it can't eat a large chunk of a small screen
  permanently.
- Exported files are named after their contents now instead of generic
  `build.json`/`flagonquest-all-characters.json`: a single character's
  export is `<character name>-<date>.json`, and Backup all characters
  is `FlagonQuest-export-<date>.json`.
- Land's Bounty's Difficult Terrain now scales with Mind ("up to [Mind]
  levels") instead of a flat single level.
- **Supporting** now has real rules instead of a placeholder: a flat
  difficulty 11 check that grants the target Good Luck on success, with
  prose on when to reach for it — using a Skill you do have to back up
  an ally using one you don't. Moved up next to Skill Checks and
  Gambling, where the rest of "how a check gets resolved" already
  lives, instead of sitting alone in Adventuring.
- Character Creation moved to the end of the Rulebook's chapter list,
  after Creating Items — it only really makes sense once you've read
  the rest of the book anyway.
- Standardized repeated-count phrasing across the Rulebook, techniques,
  items, and features: "twice"/"thrice"/"four times" etc. instead of the
  mix of numerals ("Slowed 4 times", "[3 times X]") and inconsistent
  spelled-out forms ("Good Luck two times") that had crept in.
- Food created items (cooked meals, etc.) now spoil a week after being
  made, matching how long raw Food materials already last — they used
  to spoil after just a day, which didn't make sense next to a week for
  the raw ingredients that went into them.
- **Site-wide consistency pass**, mostly invisible but a bunch of small
  fixes: a glossary tooltip bug where multi-paragraph entries rendered
  as one run-on block on the main app (worked fine on the Rulebook/
  Glossary pages, which is how it went unnoticed); a broken item price
  (Travel Rations) that couldn't resolve a Gold value; several
  unfinished/cut-off Rulebook sentences (Persuasion's skill blurb, the
  Adventuring chapter's intro, a stale rule referencing "Spirit" from
  before it was renamed to Essence); straight quotes/apostrophes
  standardized to curly throughout the Rulebook and Glossary; a handful
  of missed spots from the repeated-count and Food-spoilage passes.
  Also some code-only cleanup with no visible effect: several
  copy-pasted style objects and one-line helpers (filter chip styling,
  collapsible-section buttons, array-toggle logic) that had drifted
  slightly out of sync across the Items/Techniques/Crafting sections
  are now single shared definitions.
- **Consistency pass, round two** — the judgment calls from round one:
  - Split the Pack/Gear "Travel Rations" out from the craftable Food
    one — it's now **Basic Travel Ration**, a plain store-bought staple
    distinct from the Level 1-5 version you cook yourself.
  - Rapport's Rulebook blurb no longer cites specific Social Contest
    terms that are about to be reworked; it's just about making people
    like you now.
  - `techniques.csv`'s `Relevant Skills`/`related_skills` and
    `items.csv`'s `Relevant Skill`/`relevant_skill` — same concept,
    different names — are now both `Relevant Skills`/`relevant_skills`.
  - `backgrounds.csv` and `features.csv` now split flavor text from
    rules text into `Description (Fluff)`/`Effects` columns, matching
    `techniques.csv`/`items.csv` — a handful of backgrounds with a real
    flavor lead-in (Predator, Numb, Sacred Flame, Masters of Safety,
    Scrap Trap) got split out; the rest were already all-mechanics, so
    Fluff is blank for them (and for every Feature, which don't really
    have room for flavor text by design) the same way it already was
    for some Techniques/Items.
  - Filled in three stub/unfinished Rulebook spots: an intro paragraph
    for "The Basics," a full worked example of crafting a Masterwork
    weapon enhancement (Enith's shadow blade) under Creating Items, and
    a resolution for an Example in Damage and Health that set up a
    scenario (a firebolt at Beornhard) but never finished it.
  - The Character Creation chapter's first section no longer repeats
    the chapter's own name — it's "Building a Character" now, matching
    how every other chapter's opening section has its own distinct
    title.
- **Automatic prereq checking**: techniques with a machine-checkable
  `Prereq Check` (Skill/Stat-and-threshold or known-Technique clauses,
  matching most of what "Prereqs (Full)" already says in prose) now show
  a red/green "✓ Met"/"✗ Not met" badge next to their Prereqs line while
  browsing, evaluated against the current build — 140 of 143 techniques
  got one; the 3 that didn't have Prereqs text the syntax genuinely
  can't express (a choice, "None", or a School-conditional OR) and just
  show the plain text with no badge, same as before. A technique whose
  prereq scales with its own Level (`[Level]`, `[Level]+1`) and can be
  learned across a range of Levels doesn't get a badge either, since
  which Level you'd build it at isn't chosen yet while just browsing —
  same "don't guess" spirit as the crafting School-matching.
- **Fixed a live bug**: the Feature-builder (Battle Maneuver, War Magic,
  Healing Magic, Spirit Blessing, Social Maneuver) has been silently
  ignoring its own point budgets — the "Points: Level 1: 3 basic; ..."
  text its fallback regexed out of Effects had moved to the Building
  column at some point, so the regex quietly matched nothing and the
  Feature-builder let you pick unlimited Features with unlimited points
  at any Level. All five now have a real `Feature Budget` data column
  instead (matching Prereq Check's approach), and the fallback regex —
  the thing that broke silently in the first place — is gone rather
  than patched. Data now driving something the site used to derive from
  prose is the new standing rule here; see the "source of truth" note
  added to CLAUDE.md.
- The Rulebook/Glossary header nav can now jump straight to a specific
  tab (`index.html?tab=items`, etc.) instead of always landing on the
  Character Sheet — clicking "Items" from the Rulebook actually takes
  you to Items now.

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
