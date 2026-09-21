# FlagonQuest

FlagonQuest is a browser-based companion site for the FlagonQuest tabletop
RPG — a beer-and-pretzels TTRPG for the modern gamer. It's a technique/item
browser, character builder, and printable character sheet, all in a single
static HTML file with no build step, deployed via GitHub Pages. Game
content (techniques, items, backgrounds, and so on) is maintained as
spreadsheets under `scripts/` and converted to the JSON the site reads via
`scripts/convert.py`.

## Changelog

One entry per day, newest first — a quick skim of what happened, not a
full log. See `git log` for the commit-by-commit detail.

### 2026-09-21 — Combat simulator overhaul: turn order, Harried, Armor, movement, and a Level 1 recalibration

Reworked the simulator's fundamentals to actually match the rules - Reflex-based turn order, Harried, worn Armor, multiple attacks a turn, 2D movement, PC/enemy stat blocks moved into CSV tables - then recalibrated the Level 1 enemy Roster against the real drafted party now that all of that's in place. Also added more drafted PCs (Sable, Hanforth) and fixed a couple of small item bugs (Heavy Bow's Might Requirement, Light Bow's Range).
- Turn order and Harried were both missing entirely before today and moved win rates a lot once wired in, so Level 1's four archetypes (Hedge Knight, Marsh Archer, Skulking Footpad, Fen Warden) got retuned against the real party, landing around a 99% win rate and ~72% Health remaining on a win.
- Fixed several other rules gaps along the way - PCs had no Armor, every unit got only one attack a turn regardless of AP, attacks always hit the wrong Defense/Resist for their damage type - and added a 2D movement mode plus Card Techniques (Second Wind, Perfect Strike, Bottomless Bottles) budgeting.
- Gave the combat log real attribution (which weapon/technique produced each hit, how far a unit moved) instead of bare numbers, and used the simulator along the way to spot-check a few Ring items' existing prices.

### 2026-09-19 — Enemy math retuning, abilities wired into the simulator

Rebuilt the PC baseline as an actual named character instead of an abstract number, then retuned the whole enemy roster and combat math to match — including giving enemies the same Armor choices players get.
- Found and fixed two formula bugs along the way (weapon Damage uses Body, not Agility; Resist is raw Essence) and added a missing Gambling option to the fight simulator so PCs have a way through heavy armor.
- Result is the cleanest enemy difficulty curve yet — ~50% fights at your own tier, lockout above it and dominance below.
- Also wired a first batch of the Ability catalog into the simulator (Enhanced Health, Powerful Weapon/Spell, Strike (Crippling)/(Vulnerable), Poison (Bleeding), Durable) — testing it found Powerful Weapon can backfire on a Parry-focused enemy, and Vulnerable has no live target until an Action exists that actually attacks Bodily/Mental.

### 2026-09-18 — Enemy Encounter Design written up and validated

Documented the designer's own point-buy system for building enemies (Level, Encounter Slots, Roles, Defense tiering, Battle Tactics) from an old spreadsheet, then built a combat simulator to check it actually produces five felt power tiers.
- Added a first GM-facing enemy stat block and a practical guide for running Social Encounters at the table.
- Also: Social Contest renamed to Social Encounter with a Pressure fix, an archive sweep that cut a few overreaching Head items and added Third Eye, and three new Masterwork items translated from another game.

### 2026-09-17 — Crafting cleanup, new Technique and items

Fixed several inconsistencies in the crafting rules and added gear to round out material coverage.
- Fixed which base items and Crafting Schools can make what (Neck items off Basic Clothing, Carving up to Medium Armor, Bows Carving-only), and cleaned up ambiguous recipe wording.
- New content: Preserving Larder, the Distraction Technique plus four Cloth/Leather items, and renamed Instinct Defense to Vigilant Defense so it stops getting confused with Insight.

### 2026-09-16 — Crafting Skill Total requirements reorganized

Reworked the Skill Total needed to craft anything into one clean tiered table, and rounded out a few more material/slot combinations.
- New items: Clarion Cord, Kindled Wrap, Numbing Edge, and Chillstrike Band, each covering a Frost or Slot/Level combination that was missing.
- 17 Hands/Feet items can now be crafted via Jewelrymaking as well as Tailoring.

### 2026-09-15 — Crafting recipes for the rest of Pack/Gear and Tools

Gave every remaining basic adventuring item (Tools, Kits, Packs, Wagons, Alcohol) a proper crafting recipe instead of a generic placeholder, and added 15 new basic tool items.
- Retired Adventurer's Kit in favor of Rope, Firestarter, and Camping Kit as separately priced items.
- New Masquerade Bad Luck/Good Luck rule for disguises, a new shared "Vigor" keyword, and a Food-item retune to fix a couple of items that had landed under their Value target.

### 2026-09-14 — Weapons and Armor balance pass

First balance pass on base Weapons and Armor, plus new upgrade-path recipes for Armor.
- Reworked Armor from two tiers to three (added Medium), tightened Might Requirements, and adjusted a couple of Bow/Thrown numbers.
- Armor can now be upgraded in place (pay just the difference) instead of only built fresh.

### 2026-09-13 — Held slot closed out

Worked through all 30 Held Masterwork items, the largest slot in the game — cut a handful of redundant or broken ones and repriced the rest against a couple of newly-derived pricing baselines.
- Heartseeker and Blade of Fortune got redesigns; Placeholder's Speedy Scepter had an AP-cost exploit caught and closed before it shipped.

### 2026-09-06 — Ring slot closed out

Finished the Ring Masterwork cluster — cut a couple of duplicate items, swapped two items between Neck and Ring to match their actual design lane, and priced the rest from formulas instead of guesses.
- Backfilled the balance tracking files for Feet/Head/Neck, which had quietly fallen behind during this stretch of work.

### 2026-09-05 — Neck slot closed out

Finished the Neck Masterwork cluster, cutting a few duplicate or unused items and reworking others around a couple of new shared mechanics.
- Named the three steps of a Full Night's Rest as Cycles, which several items now hook into cleanly.

### 2026-08-31 — Torso slot closed out, Resist rate fixed

Finished the Torso Masterwork cluster and fixed a math bug in Resist's pricing that had been double-discounting its value.
- Recomputed every item that depended on the old (wrong) Resist rate.

### 2026-08-30 — Torso Masterwork pass

First balance pass through the Torso slot, plus a slot-design-philosophy reference (Torso = protection, Neck = passive utility, Ring = active ability) recorded for future items.
- Fixed the stale "Bodily Defense" term to "Vital Defense" everywhere it was still live in the code.

### 2026-08-29 — Buff Potions finished, Ward redesigned

Finished the buff-Potion lineup and redesigned Ward around a cleaner absorption mechanic.
- New items: Windrunner's Draught, Thornskin Elixir, Spellblade's Sipper, Fatebinder's Cordial.

### 2026-08-27 — Grenades and Potions rebalanced

Rebalanced the Grenade and healing-Potion families into cleaner Level ladders, and added a few new items to round them out.
- New items: Oozejar, Legbreaker, Harrowing Ichor, Battlemaster's Brew.

### 2026-08-26 — Ward's Resist bonus doubled

Ward now grants +2 Resist per stack instead of +1, after a balance audit found it underpriced relative to Resist's own rate.

### 2026-08-25 — Crafting recipes unified onto one formula

Replaced two incompatible crafting-recipe formats with a single rule — every recipe states its own Total Materials directly, at least half of it a Main Type.
- Masterwork items now name only their own Main Type, so the same enhancement works on any compatible base item without listing every material combination by hand.

### 2026-08-23 – 2026-08-24 — Social Contests and Exploration reworked

Reworked Social Contests into a Pressure-based system replacing the old Concessions/positioning subsystem, and rewrote Exploration around a simpler one-action-per-leg structure.
- Food and Exhaustion moved out of Exploration into their own section, since neither was ever actually wilderness-specific.

### 2026-08-19 — Printed sheet, mobile layout groundwork, a few fixes

Made the printed Character Sheet easier to hand-edit with a pen, laid the groundwork for mobile-specific layout, and fixed a few display bugs.
- Added the first mobile-specific design tokens and a two-column Stats & Skills grid for wider phones.

### 2026-08-18 — Bigger text, consistent styling

Bumped the site's base text sizes up a notch across the board, especially for mobile, and pulled repeated styling into shared constants so it can't drift apart again.
- Added the Fullness tracker (Goblin Game) to the Character Sheet, next to Health.

### 2026-08-17 — Choice-based prereqs, Builder cleanup

Techniques that make you pick something when you learn them (School, Profession, weapon type) now use dropdowns instead of free text, with prereq checking that follows the actual pick.
- Character switching and sharing got an overhaul — one "Manage Characters" list, a QR code option, and much shorter share links.

### 2026-08-14 — Rulebook cleanup, crafting browser overhaul, Goblin Game content

A big cleanup pass across the Rulebook and crafting system, plus a wave of new Goblin Game content.
- Crafting browser rebuilt with working recipes and pickers instead of guesswork; automatic prereq-checking added to most techniques.
- New Goblin Game Food System chapter (Fullness, Too Full, the Meal recipe), plus more content pulled from the full player doc.

### 2026-08-11 — Crafting materials framework

Added the Materials system — a new item category for crafting resources, plus a browser showing what you're eligible to craft.
- Custom materials builder for GM-granted special materials that aren't in the data file.

### 2026-08-04 — Health tracking

The Character Sheet now tracks current Health directly, with a clickable pip readout and automatic Wounded flagging at 0 Shallow Health.

### 2026-08-03 — Character management, flavor text

Added Duplicate/Backup/Restore for characters and a Sources panel to toggle which supplements show up, and restored 66 techniques' original flavor text that had been condensed down to one line somewhere along the way.

### 2026-08-02 — Goblin Game content, combat math fixes

Added 14 new Goblin Game clan Backgrounds and fixed Accuracy/Defenses to consistently use Skill Total instead of the raw skill value.
- Custom weapon builder, item filters, and a few other Builder-tab conveniences.

### 2026-08-01 — Items, Backgrounds, multiple characters

Added Items and Backgrounds pickers, character slots (more than one character per browser), and a proper print layout.

### 2026-07-29 – 2026-07-31 — Foundation

Initial build-out: technique browser, the Builder/Character Sheet split, Stats & Skills point-buy, Feature-built techniques, share links, the Rulebook and Glossary pages, and the site's branding.
