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

### 2026-10-09 — Builder fix for once-only Features

The Feature builder now enforces Features that can only be taken once, and Bare-Handed and Tormenting Curse now add their extra points to spend, the way their text says.

### 2026-10-08 — Teaching the simulator to play like a real table

The simulator now plays more like the designer's table: real Wounded rules, a 6–10 meter start with some line-of-sight trouble, and players who dive in or hang back depending on their character. At Level 1, with the players' own starting characters, it now lands close to how fights actually go at the table.
- First real player build (HOLE, ~90 XP) added for comparison: about a quarter of its XP goes outside combat, and it fits right in with the Level 1 sample characters.
- In that setup, Bleeding comes out at about 1.6 Value for a first stack, well under its current price of 4.

### 2026-10-07 — Active Style on the sheet

Style cards on the Character Sheet now have an Enter Style button, so you can mark which Style you're in and switch with one tap at the table. Furious Rage also lost its "can't Parry" drawback after the simulator showed it cost more than the Style gave back.
- The simulator's party now picks targets more like players do (mostly focus fire, but not perfectly), and a closer look at Bleeding found it's worth well under its current price in ordinary fights.

### 2026-10-06 — Leader, Face and Druid Styles

Leader, Face and Druid got their first real sets of Styles, so every combat archetype now has early and late options.
- Leader: Forward!, Lead by Example, Command the Tempo and Commander's Gambit.
- Face: Intimidating Presence and Dread Reputation. Druid: Grasping Earth, and Pack Leader, which makes every Summoned creature hit more reliably.
- Late Styles for Sorcerer (Twin Spell), Duelist (Exploit the Opening) and Archer (Suppressing Fire); Storm of Blades and Crashing Wave were repriced after a pricing mistake on copied Techniques, and Crashing Wave became a shield charge.
- Ran the turn-order Styles through the simulator: Seize the Moment (renamed from Quick Draw) and Command the Tempo each went up a Level, Lie in Wait went down one, and Ambush Predator now just gives Good Luck against enemies who haven't acted yet.

### 2026-10-05 — Version 1.2 and the last of the old Stances

Started version 1.2, finished turning the archived Stances into Styles, and gave Healer and Scout their first Styles.
- From the old Stances: Deadeye's Shadow, Oppressive Presence, Aura of Death and Adrenaline High.
- Healer got Field Medic and Lifeward, and Scout got Seize the Moment, Lie in Wait and Ambush Predator, which play with turn order.
- Minor Oracle is back as a fortune-telling spell, and card costs now always say discard instead of pitch.

### 2026-10-04 — Keywords, guardian Styles and a social overhaul

Attacks that copy their Technique now share a Repeat keyword, Counterattack became Opportunity Attack, and the social Techniques got rebuilt for the current Statement and Pressure rules.
- Two old Stances came back as Styles: Lend Bulwark takes hits meant for an adjacent ally on your own Parry, and Sentinel follows an enemy every step it takes away from you.
- Every Skill on the Builder and Character Sheet now shows its suit, so you don't have to look up which cards count for Extra Successes.
- Social Maneuver now adds Features to a Statement instead of costing AP, with every Feature priced against a model of a social encounter, and Taunt and Frighten now work in social encounters.

### 2026-10-03 — Oak, drunks and archers get Styles

Great Old Oak, the last School without a Style, got Boughs Unbroken, and two old Stances came back as Styles: Drunken Brawling leaves every enemy you stagger past off-balance, and Doubleshot makes every ranged attack twice.
- Boughs Unbroken: Parrying with your fists doesn't wear you down, and every Unarmed hit shakes off one debuff completely.
- An empty hand now counts as an Unarmed weapon, so monks can use the dual-wield Styles; Flurry of Blows and Dragon's Fang were dropped as repeats of Styles we already have.

### 2026-10-02 — Styles pass: Tiger, Snake and Bear

Went back to estimating Styles on paper after the simulator couldn't read them well, and added Styles for Snake and Bear.
- Styles that copy or boost your other Techniques are now priced off the Level 2 Techniques you'd actually have, so Storm of Blades moves to Level 3.
- New Styles: Infinite Coiling for Snake (your grapples don't leave you open) and Furious Swipes for Bear (every Unarmed hit shoves, then Bleeds or Slows).

### 2026-10-01 — Enemy stat blocks get a price list

Priced every enemy ability and archetype in the simulator, then turned enemy building into a step-by-step process: a Level baseline, an archetype, a main Action, one strong Defense, and a set of Upgrades.
- One Upgrade is worth about one point of enemy Health, so the old spreadsheet's abilities got re-costed on that scale and +1 Health is just another Upgrade.
- Every enemy now has an archetype, and Medium or Heavy Armor and heavy weapons cost picks; Defender is a plain shield (Parry +2).
- Minions stay at a third of a normal enemy's Health, and Horde swapped its Hexer for a second caster so the fight costs the party some Health.

### 2026-09-30 — More Styles, and enemies rebuilt like players

Finished another batch of Styles, then rebuilt the simulator's enemies from the same Stats, weapons and armor players use, and started a quick way for GMs to build enemy stat blocks by hand.
- New Styles: Rending Claws for dual-wielders, Hands of Defilement for Demon School, and Spirit Hands reworked; Follow Through, Eagle Eyes, Inexhaustible Guardian and Indomitable Phalanx got cleaned up.
- Enemies now come in more kinds (casters, hexers, healers, shield-bearers, minions), and the sample party is Level 2, with Browndog taunting.
- The by-hand enemy build is in the GM guide notes: a Level table, archetypes priced against each other in the simulator, and heavier gear paid for out of the enemy's budget.
- The simulator's party can now attack Vital and Mental (Felix is back as a monk), fights use two or three kinds of enemy like a real table, and Level 2 enemies got a little tougher.

### 2026-09-29 — Styles pass started, Barbarian gets two Styles

Started going through every Style one at a time, repricing them against a proper Style budget and giving Barbarian a Level 2 and a Level 4 Style that do different jobs.
- Lawman's Hand is now a Level 2 Style that Slows the first target you hit each turn and lets you leave anyone you Down alive, and Hand of Chaos and Ritual Magic got clearer wording.
- Disciple of the Flowing Hand moved to Level 3.
- Furious Rage is now just "can't Parry, and anything you hit or that Parries you Bleeds", built for grinding down armored enemies, and the new Level 4 Warpath ignores fear, taunts and wounds and gives you Vigor every time you Down something.

### 2026-09-28 — Great Old Oak finished, "Updated" badges

Finished Great Old Oak: Snake now needs Insight instead of Acrobatics, and Oak's older Meditation Techniques got new names and new jobs.
- Iron Skin is now Bark Turns the Blade, Channel Ki is now Willow Springs Back (Level 3), Ignore Pain is now Oak Sheds Its Leaves (spend cards to block incoming debuffs), and Harmonious Mending is now Sap Seals the Wound (spend cards to heal over a few turns).
- Seasons Pass the Forest moved to Oak's Unarmed Techniques.
- Went through the old martial drafts in the backlog, declined the ones made redundant by the School split, and turned three into new Techniques: Gaze of Pale Moonlight (Level 2), a ranged curse that Cripples and Frightens, Arrow Finds Only Mist (Level 3), which teleports you out of an attack's way, and one into Demon: Blood Answers Blood (Level 3), which makes an attacker Bleed as much as they hurt you.
- Techniques and items whose rules changed since the last release now carry a blue "Updated" badge, and the Techniques and Items tabs each have a "Recently updated" filter — an easy way to see everything this batch of changes touched.

### 2026-09-27 — Shugen and Demon reworked, Oak started

Reworked Shugen and Demon under the new School split, filled out Demon's Meditation Techniques, and started on Great Old Oak.
- Swallow Skims the Water now deals Brilliant damage and moved from Level 2 to Level 3, Hand Rings the Bell became a 2 AP Brilliant punch that Slows, Fist of the Third Dragon became Dawn Wind Bends the Grass, a cone that Slows, and Tide Rolls Back the Shore now targets Mental Defense.
- Added two Level 4 Shugen School Techniques: Lantern Gutters in the Wind, a Brilliant punch that Cripples, and Great Wind Scatters the Leaves, which blows everyone around you in one direction.
- Reworked Demon to fit the split and renamed its older Techniques in the new style: Plague Fist is now Sickness Takes the Flock and targets Vital Defense, Ripjaw Gambit costs 1 Health, Hand of Defilement is now Shepherd Opens the Gate and leaves targets Harried and Vulnerable, and Wasting Claw is now Circling Vulture with a cap on its Health loss.
- Started Demon's pure Meditation Techniques, named to mock Shugen's: Firefly Dies in the Hand (Level 1), a Shadow touch, Thief Empties the Vessel (Level 2), which lets you discard a card to heal on a hit, Bell Tolls a Dirge (Level 2), a ranged curse, Dusk Wind Withers the Grass (Level 3), a cone that makes everything in it Bleed, and Fawn Left to the Wolves (Level 4), which hits harder the more a target is bleeding.
- Started Great Old Oak's Unarmed Techniques, which target Vigilant Defense and protect you on a hit, with Tree Withstands the Storm (Level 2) and Oak Draws the Lightning (Level 3), which Taunts the target and keeps your Defense from wearing down, and Old Growth Digs Deep (Level 4), which shakes off your debuffs and hits back with them, plus Seasons Pass the Forest (Level 2), a reaction that Parries a spell and wards you against fire and frost.

### 2026-09-26 — Demon School finished, Shugen started

Finished Demon School, split the in-combat Meditation Techniques between the three supernatural Schools, and started on Shugen, which now gets poetic names.
- Added Demon School - Hand of Defilement (Level 3), a Shadow punch that Cripples and Slows, and Wasting Claw (Level 4), a follow-up that strips every debuff off the target and makes it lose 1 Health per stack.
- Added three Shugen School Techniques: Swallow Skims the Water (Level 2), which teleports you to a target and punches it for 1 AP; Hand Rings the Bell (Level 2), a 1 AP punch that drops the target's Dodge and Parry for your follow-up; and Tide Rolls Back the Shore (Level 3), a Brilliant punch that knocks the target back.
- Split the in-combat Meditation Techniques into Demon (offense), Shugen (control), and Great Old Oak (defense), and started a pass over Shugen: Spirit Bolt is now Firefly Leaves the Hand, and Through the Void is now Water Fills the Empty Vessel with a Slowed rider on its swap.

### 2026-09-25 — Demon School: Ripjaw Gambit rebuilt

Rebuilt Demon School's Ripjaw Gambit as a Level 3 attack where you bleed yourself for a big Shadow hit to the target's Vital Defense, since all three old drafts priced out far below budget.

### 2026-09-24 — Snake and Bear Schools finished

Finished the Snake and Bear martial-arts Schools, and wrote down that spell attacks can't be Gambled on, which was always intended but never in the rulebook.
- Added Snake School - Chainbreaker, a Level 2 punch that breaks you out of a grapple and shakes off Bleeding, Crippled, and Slowed before it lands.
- Added three Bear School Techniques: Shattering Slam (Level 2), a body-slam that trades damage for Bleeding and Slows the target; Swatting Paw (Level 3), which bats aside an attack you see coming and Frightens the attacker; and The Grizzly Awakens (Level 4), the Slam as a shockwave cone.
- Snake and Bear scale on Brawl, while the more supernatural Schools (Demon, Shugen, Great Old Oak) scale on Meditation, and Bear's Bleeding now grows with Extra Successes so it can be Gambled on.

### 2026-09-23 — Unarmed martial-arts Schools: backlog rebuilt, first new Technique

Pulled every unported martial-arts School Technique out of the old archive into the ideas backlog, set pricing rules for unarmed fighting, and reworked the Snake School.
- Snake School: added Striking Constrictor (Level 1, turns a landed punch into a grapple with Good Luck), gave Turn the Tables a better parry, and rebuilt Chainbreaker as Slithering Hands (Level 4, deflect an attack you see coming into one of the attacker's friends).
- Unarmed now gets a small skill discount for Brawl, and monk Techniques that need empty hands or no armor can carry a little extra value to make up for what they give up.

### 2026-09-22 — Martial Technique cluster priced, "Style" freed up for the martial-arts Technique families

Worked through the Martial Technique cluster (Magehunter, Parting Shot, Blinkstep, Perfect Strike, Cloak and Dagger, Boulder Toss, Plague Fist) pricing each one against THE TABEL, then renamed the `[Form]` rules tag to `[Style]` and the Bear/Snake/Demon/Shugen/Lion/Tiger Technique families from "X Style" to "X School" to make room for it.
- Modeled Magehunter, Parting Shot, and Blinkstep's off-turn/free-movement mechanics for the first time, catching two bugs in the process (Magehunter's AP-refresh timing, then its missed Encounter tag) and adding a Kiting enemy archetype (Bog Skirmisher) so Parting Shot has something to trigger against.
- Priced Perfect Strike and Cloak and Dagger, both already implemented but never checked — Cloak and Dagger turned up a rules bug (Unaware drops Defense to 8, not an auto-hit) and needed an EV-gate fix so the simulator only spends a card when it's actually worth it.
- Hand-priced Boulder Toss, Plague Fist, the three Snake School Techniques (Heelbiter, Chainbreaker, Turn the Tables), and Spellblade against THE TABEL's own weights instead of building new simulator mechanics for each — Boulder Toss reads very differently depending on whether the throw is set up deliberately or attempted on the fly, Plague Fist turned up a real bug (Vulnerable wasn't dropping Vigilant Defense) plus a modest overshoot on budget, Chainbreaker's defense-into-offense swap checks out close to on-budget, and Turn the Tables checks out strong for a build that actually leans into Brawl.
- Spellblade's ten options turned out badly uneven (Crippled and Protected massively over-delivering, Ward initially miscounted as a trap pick when it wasn't) — rebalanced against a clearer design target (each option worth roughly what the spell it replaces was already worth, plus a small premium) and shipped: `[6×X]`→`[7×X]` on the range/Push/Shift options, `[3×X]`→`[2×X]` on Slowed/Vulnerable/Necrotic, and Protected/Crippled both reworked to a flat `X+1+suit` shape instead of scaling with X at all.
- Renamed the `[Form]` rules tag to `[Style]`, and the martial-arts Technique family names ("Bear Style", "Snake Style", etc.) to "School" to free up the word.

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
