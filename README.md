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

### 2026-09-21 — More player-drafted PCs, a Heavy Bow fix, and a more readable combat log

Fixed Heavy Bow's Might Requirement (was 6, now 4 - Light Bow already had none). Added two more player-drafted characters to the simulator (Sable and Hanforth, a dedicated healer), and made the combat log actually name what's happening - which weapon or technique produced each attack/heal, and how far a unit moved - instead of just numbers.
- Swapped in Sable, Deadeye's real build and corrected the simulator's own Light Bow Range to match the actual craftable item (19m, not the abstract category's 15m).
- Added Hanforth, a dedicated Theurgy healer, and generalized the simulator's healer logic to read a build's actual Healing Magic Level and Vitality bonus from the CSV instead of one hardcoded number - his own heal comes out to 5 Health a cast, not the old flat 2. Gave him a Heal Range and a "go after the isolated enemy, not the main clump" targeting preference instead of always closing on whoever's nearest.
- Every attack and heal in the combat log now says what did it (a weapon name, or "Second Wind"/"Bottled Fire"/etc.), and every move shows how far the unit actually went - much easier to spot-check a replay against the real rules.
- Gave the simulator real turn order - a Reflex flip for every PC and enemy at the start of a fight, rolled once and interleaved for the whole fight, instead of "all 4 PCs act, then all enemies act" every round. It's a real balance swing, not just cosmetic: enemies sometimes acting first now costs the party noticeably more at low Tiers (a Tier 1 party's win rate against Level 2 enemies drops from the low 30s to around 5-6%). Also modeled Sable's Hand of Chaos (a flat 1-in-4 chance of +1 damage, standing in for real suit-pool tracking this simulator doesn't have) and gave her Good Luck on her own initiative roll from One Eye Behind You. Fixed Light Two-Handed Melee to allow Brawl as well as Melee, matching its already-flexible Body-or-Cunning damage.
- Dropped Healing Potion from Jackal's Bottomless Bottles kit and worked out a real number for Bottled Fire instead of a guess: her Cards Per Day (10), spending 2/3 of them on the Technique's own Gold budget, buying Bottled Fires at a price inferred from its balance-ledger Value (no Grenade or Potion actually has a listed Gold cost yet - a real gap worth knowing about), landing on 6 a day and 3 per fight. Alchemy items without their own listed price are now all filled in at the designer's own general rule, 2x Level Gold.
- Checked the enemy Roster against real drafted PCs for the first time - on-level fights read far too easy (99%+ win rate, versus the original ~50% design target), confirming the "recalibration is due" note from a few days back. Worked out a real target instead of guessing at one: the design's own combat-assumptions math puts the party finishing an average fight around 72% Health, so aiming for the simulator to read twice as pessimistic lands on ~44%. Drafted 5 new Level 1 enemy archetypes with deliberately mixed Fighting Styles (only one double-attacker, kept as a direct comparison case) instead of defaulting every enemy to Flurry, and found that a flat Accuracy/Damage bump on the shared Level curve was far too blunt an instrument - it swings win rate from ~90% to under 10% over a couple of points, because it inflates enemies' own Resist at the same time as their damage. Added a cleaner `DamageBonus` field that only touches attack damage, which behaved far more predictably. Landed on real numbers - most compositions now win ~65-90% of the time at 55-65% Health remaining - short of the literal 44% target, but that turned out to hit a real ceiling: pushing harder just converts close wins into losses rather than deepening chip damage on the wins that remain.
- Promoted 4 of those 5 archetypes (Hedge Knight, Marsh Archer, Skulking Footpad, Fen Warden) to the actual Level 1 baseline, replacing the old 4x-clone Marsh Viper Scout - a real varied encounter instead of one archetype fought four times. Also switched the simulator's movement from a continuous ruler to the real rule: whole spaces only, and diagonal movement costs the same as orthogonal - checked it barely moved the numbers, as expected, but it's now actually correct instead of coincidentally close.
- Went back to that Level 1 calibration once its win-rate numbers stopped holding up - the check that landed on DamageBonus+4 hadn't been run through the simulator's official method, and once it was, on-level fights read far too hard, not too easy. Also found the whole Roster's validated win-rate table (from a few days back) has gone stale since - several mechanics landed after it was measured (Card Techniques, the real AP/Armor economy, real turn order) and nobody re-checked it against them, so most Levels now read close to 100% instead of ~50%. Only Level 1 got fixed today. Added two new retune knobs alongside DamageBonus - AccuracyBonus and DefenseBonus - and found DefenseBonus (an enemy's own Parry/Dodge/Bodily/Mental, moved together) is the cleanest of the three for landing a win rate and a "Health left on a win" at the same target together, since it changes how fast the party kills the enemy instead of how hard the enemy hits back. Level 1's four archetypes now land around 68% win, about 4-5 rounds, and 68% party Health remaining on a win.

Added Good Luck to the fight simulator and used the enemy model to spot-check several Ring items' existing prices, then moved both PC and enemy stat blocks into CSV tables and built out a much wider set of reference builds for future use. Also gave the simulator an optional 2D-movement mode to test how Speed and range actually interact, and closed the day by fixing two rules gaps - PCs had no Armor at all, and everyone only ever got one attack a turn - that had been making every fight swingier than the actual rules allow.
- Good Luck's simulated swing confirmed a real effect but isn't directly comparable to the calculated per-flip value; Pillar Ring and Ring of Comets checked out at their existing price, Flamebinder's Promise turned out more Resist-sensitive than assumed, and Mendicant's Cord's "guess which Defense to protect" has no real risk yet. Logged both open findings in `balance_weights_notes.md`.
- PC stat blocks now live in `sample_pcs.csv` (real named characters - Hilde, Browndog, Carrick, Jackal, Felix - alongside the validated party baseline), and enemy stat blocks gained 20 new archetype touchstones (Neutral/Power-Attack/Max-Damage/Ranged Caster/Tank at every Level).
- Building the Ranged Caster archetype surfaced a real bug: PCs' own attacks were hardcoded to always target an enemy's Parry, never Dodge, which broke badly against an enemy with a deliberately tanked Parry. Fixed to match the actual rule (target picks whichever Defense is better for them).
- New optional `movement=True` sim mode: a bounded 20x20 arena, units closing to their own attack range or kiting away from the nearest threat. Turning it on for the Ranged Caster archetype shows range matters a lot at Tier 3+ (the party's win rate against an on-level kiting caster drops from 42% to 5% by Tier 5); tested from the PC side too with three new ranged reference builds (Sable on a bow, Rook throwing knives, Wren casting War Magic) - a bow's fixed 15m range wins fights outright once movement is on, but War Magic's shorter range (Sorcery Skill Total, ~6m at Level 1) barely helps against an equal-Speed enemy.
- Followed up with a real mixed party instead of 4 clones (`party.make_party_from`), a 2x2 party formation, a random 5-10m starting gap between front lines instead of opposite arena corners, Wren's War Magic now actually dealing Fire damage (drawing on enemies' generally-weaker elemental Resist), and a support reference PC (Beornhard) who fights with a decent Melee attack most rounds and saves a hard-capped handful of Healing Magic uses - based on his card-hand size, not a per-round guess - for whenever someone's actually in trouble. Mixed reference-build parties land well below the Roster's own ~50%, since the Roster was calibrated for 4 identical smoothed PCs; Beornhard's first pass (healing on a per-round guess, fighting weakly the rest of the time) badly underperformed a straight 4th fighter, but once fixed to actually fight in between his rare heals, he closed most of that gap.
- Pulled every unit's targeting/movement/heal-or-attack decision out of the fight loop into two new small files, `tactics.py` and `cards.py` (a card-suit-assumption helper) - each is a `{name: function}` registry from now on, so a new AI rule is one function and one registration, not another `if` in `run_fight`. Also added an optional fight trace and `narrate_fight.py`, which turns one seeded fight into a round-by-round position map and combat log instead of just a win/loss tally - useful for actually seeing what the simulator's doing. Assuming Healing Magic's discarded card is always a Heart (the designer's own call - you're choosing from your hand, not flipping blind) turned out to barely move Beornhard's numbers, since he only ever gets one heal in a fight to begin with.
- Looking at that replay caught two gaps: PCs had no worn Armor at all (bare Essence Resist only), and every unit - PCs included - only ever got a single attack a turn regardless of Action Points. Fixed both to match the actual rules: Armor now adds to Physical Resist (and Dodge/Speed) the same way for PCs and enemies, both sides' attacks now draw on the right Resist pool for their own damage type (a Fire attack used to always hit Physical Resist), and every unit spends its full 4 AP a turn - move as needed, then attack, twice if the AP's there (enemies follow their own Fighting Style's economy - Guarded/Aimed Shot/Skirmisher cap at one attack for a compensating bonus, Flurry doesn't). Also added Slots-based encounter composition (`sample_enemies.build_encounter`, a new Minion archetype at 0.5 Slots) and a `narrate_fight.py --html` option that writes a self-contained graphical replay to open in a browser, no server needed. The fixes swing the win-rate grid hard toward the party (an on-level fight that read ~50% before now reads close to 100% at Tier 1-3) - correct given what was missing, but the enemy Roster hasn't been retuned to match yet, which is its own balance pass for another day.
- Fixed the demo replay to actually use 4 Slots of enemies (one Slot per PC, the standing convention) instead of 2, and added raw damage/Resist detail to the combat log - each hit now shows "6 raw - 2 resist = 4" instead of just the final number, so it's clear Armor's actually being applied.
- Swapped in five player-drafted Level 1 characters (Hilde, Browndog, Carrick, Jackal, Beornhard) for the simulator's own earlier reference versions of those same names, and gave the sim a new Card Techniques mechanic for the handful of techniques whose real cost is a card, not AP - Second Wind's self-heal, Perfect Strike's Good Luck on a Gamble, and Jackal's Bottomless Bottles items, all drawing on a shared "about a third of your hand" budget. This real roster lands close to the smoothed Baseline Roster's own difficulty curve, a decent sign the two aren't wildly out of step.

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
