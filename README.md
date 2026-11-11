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

### 2026-11-11 — Debuffs pushed to the limit, and a tidier simulator

Tried every rule change for Crippled and Slowed we could think of, and none makes one Wing Clip or Hamstring worth a skill rank; the two best (Crippled stops an enemy attacking at 3 stacks, Slowed also lowers Dodge) get to about half. Also cleared out the simulator: one enemy builder instead of four, finished studies archived, every result checked unchanged against fixed-seed runs.

### 2026-11-10 — What a few more XP buy

Measured every effect over whole adventuring days made threatening with an extra enemy or two, and what 3 or 6 more XP buy when the party loses a quarter of its days: a skill rank or a Stat saves more days than a debuff Battle Maneuver, at Level 2 and Level 3.

### 2026-11-09 — Potions in the simulator

Gave the sample parties two Healing Potions each (worth a lot, mostly drunk between fights or fed to a Downed friend, which the [Potion] tag now allows) and rebuilt the enemy table around firm targets for how often each side hits and how hard. The simulator now plays a whole adventuring day as one pool of cards, enemies attack once a turn, an audit fixed a handful of places where it didn't follow the rules, and every test now fights the monster manual's enemies.

### 2026-11-08 — Heavy armor from Level 3, a flatter enemy curve

Enemies only wear Heavy armor from Level 3, which made the slow armored fights at Levels 1-2 shorter and safer; then pencilled in a flatter enemy table from Level 2, a little less Defense and Resist paid back in Health, which lets a party at the bottom of its XP band win far more days. Re-measured every enemy Ability, gave monsters area attacks and pushes, and pencilled in harder enemy hits (fewer, two to three times as big).

### 2026-11-07 — Elites and debuffs

Elites and solo bosses can no longer buy their way out of debuffs, which was most of what made a heavily armored elite knight such a slog, and two of the sample characters now carry Fire weapons, the game's answer to heavy armor; a point more enemy budget, now the default, wins back the notch of danger those took off. Every enemy's armor and gear now comes out of its Ability budget with nothing paid out of Health, and Heavy armor costs more, which trims the slowest armored fights.

### 2026-11-06 — Bigger budgets for elites and bosses

Tested giving elites and the solo boss more Ability points paid for out of their Health (twice the points works if the extra can't buy Defense), then found the solo boss too unpredictable and tested boss fights led by elites instead.

- On a boss, Defense is worth more than its price and offense less, so a boss that spent extra points on Parry and Dodge beat the party over half the time.
- Two problems turned up that no budget fixes: a big Defender in heavy armor can't be beaten, and a ranged boss on its own barely threatens anyone. A cap on enemy Defense like the one on Accuracy, with the Defender's Parry bonus turned into Health, fixes the first; it's now the default, and fights in the monster manual run a little easier and shorter for it.
- Wrote down how to build an enemy in order (archetype, Abilities, then gear and action), with every limit at the Abilities step; only fighters get Parry from a shield.
- Enemy sizes are now one simple table (minions, regular, elites at twice the points spent on offense for a bit less Health, and the rare solo boss with two turns), and boss fights are an elite or two leading regular enemies.
- A boss fight led by one or two stronger elites inside the party's usual four Slots is harder without dragging on; every Slot past four nearly doubles the fight's length.

### 2026-11-05 — A draft monster manual

Built 30 enemy stat blocks the new pen-and-paper way, covering every archetype, weapon loadout and main action, then ran them through a broad test that plays close to the old fights and shows which pieces are over- and underpriced.

- Hexes now land a stack fewer and poisons stop at two stacks, since they outlast the fight.
- Compared the enemy Battle Tactics side by side, fixed Kiting (it now steps back only when someone closes in) and modeled Hold the Line and Vanguard, with a quick GM reference for whom each one attacks; Assassin is still the deadliest by far.
- Hexers became casters whose spells carry heavy debuffs, the solo boss shrank to six regular enemies' worth of Health, and a settled baseline puts the middle of every band at 86-92% of days won.
- The heavily armored walls were the outliers: armor now costs about what it's worth, and the Defender archetype trades its extra Resist for Health, which brings them back in line. Kiting enemies barely hurt anyone and the trimmed hexers now do little, which is where the next round of pricing starts.

### 2026-11-04 — Enemies with debuffs as standard

Tested how to give enemies more debuffs and mechanics without making fights shorter, then built a thinner enemy baseline whose Damage and Accuracy go into an Ability budget instead: spent on loadouts and mechanics, it gives fights of four to five rounds at every Level.

- Health, Resist and Defenses set how long a fight lasts; Damage and Accuracy barely do, so they're the ones to trim and buy back.
- Archetypes now only add, an enemy's weapon is a loadout (sword and shield by default, two-handers, bows, spells), on-hit effects stack a pick at a time up to four, and the budget runs 6 / 7 / 9 / 9 / 9 by Level.
- This is now the simulator's default, set a notch dangerous since real players coordinate and have items: building an enemy is meant to be a few pen-and-paper picks so it can go in a book, and the average party wins 82-90% of days.
- One party mix (Hilde, Sable and Hanforth together) wins nearly every day whatever the enemies get, which is one for the character balance pass.

### 2026-11-03 — Enemies built the way PCs are, and one designer document

Enemies are now built the way PCs are (same Stats, Skill Totals, weapons and armor, Health near a PC's, archetypes as plain bumps) with their Abilities priced in Health, and every design decision is gathered into one designer document.

- `design/DESIGNER_NOTES.md` now holds the rules design, balance basics, enemy design, how the table plays, GM notes and the designer's early notes, most important first; the old docs are kept whole in `archive/`, and the GM guide notes, idea backlog and prose review moved to `design/todo/`.
- The new enemy table is the simulator's default: damage and Resist step up at different Levels like a PC's Stats, the base sits a notch under a PC's, and bigger archetypes make up the rest, so a Defender and a Striker play differently.
- Each enemy Ability was measured in enemy Health and priced at that, with 1 Health of Abilities and armor free per enemy; the middle of each XP band still wins about 95% of days in fights of about 4 rounds.

### 2026-11-02 — Browse mode, a purchase history, and enemy stats per Level

The site can now browse Techniques, Items and Backgrounds without a character, and the Notes tab keeps a dated history of what each character bought. In the simulator, on-level fights at Level 3 turned out much harder than at Levels 1-2, so the enemy base stats got a broad pass, a new table and a repriced kit of archetypes and abilities.

- Browse mode: a Browse button in the header (and a link from the Rulebook and Glossary) opens searchable, filterable lists of every Technique, Item and Background, with no build controls in the way; items can also be narrowed by Level, Gold and what stats they grant, and sorted by price.

- The history covers Stats, Skills, Techniques, Backgrounds, items and gold; changes made in one sitting are grouped into one entry, and it goes along when you export or duplicate a character.
- Scored in parties of other strong builds, or against enemies that hit harder, the soaks fall from the top to below average at Level 3, while the damage builds hold up; at Level 2 Lifeline and Toughened Resolve still look strong.
- Enemy damage climbs every Level while the party's Resist and Health barely do; about 1 less enemy Damage at Level 2 and 2 less at Level 3 gives every Level the same table feel, and one Level up is still a cliff in every version tried.
- The new table (now the default) follows the original's shape out to Level 5, where some enemies reach the player caps; with about twice the enemy Health and a little less damage, fights in the middle of each Level's XP band run 4-5 rounds and the party wins almost every day, while the bottom of the band is a hard day and the top is easy.
- Repriced the enemy archetypes, Abilities and armor against it so they're worth about the same; +1 enemy Damage turned out worth about eight points of Accuracy (enemy hits only get about 1.5 past the party's Resist), so Striker pays 2 Accuracy for it and Bruiser is now the tough, clumsy hitter (Damage +1, Resist +1, Accuracy −3).

### 2026-11-01 — Healing Magic against the other healing

Compared Healing Magic with every other healing Technique on the optimized builds, at the same XP, and searched each build again without it; then tested it as an Encounter Technique. Every build wants healing and Healing Magic beats every alternative; as an Encounter Technique it's still the best and still on almost every build, just with a narrower lead.

- Without it, builds go for Second Wind at Level 3 and Lay On Hands at Level 2; the damage-heavy builds just drop healing and lose the least.
- As an Encounter Technique (a test, not a rules change), the healer loses the most and the strongest builds come down a little; the soak builds stay, since Toughened Resolve and Lifeline are what make them.
- Reorganized the simulator folder: the one-off studies and the regular tools now have their own subfolders.
- Scored in parties of other optimized builds instead of plain fighters, the soak builds drop from near the top to the bottom, and pairs of soaks overlap the most.

### 2026-10-31 — Every party mix, and what the optimizer finds

Played every party of four of the sample characters at the same combat XP, and searched for each character's strongest build from several starting points. Together, the characters as built do worse than four plain fighters; the strongest builds stack Toughened Resolve, Lifeline and a little Healing Magic, or are Sable.

- Three of the best Level 3 builds are pure soaks that deal almost no damage and almost never go down; they're great next to plain fighters, but a party mostly of them can't win.

### 2026-10-30 — New yardsticks, and every character at the same combat XP

Switched to judging builds by days won against enemies a Level up, with every sample character rebuilt to the same 145 XP of combat. At that budget the characters as built come out about even, but an optimizer finds builds for every one of them that win most days a Level up, so the ceiling sits far above the norm.

- With enemies that hit harder instead of having more Health, Essence's edge halves, and an optimizer that gives Health no credit stops stacking Toughened Resolve for three of four characters (finding stronger builds), so the next pass moves to a composite enemy-Level yardstick.
- Started measuring each character against a plain fighter of the same XP, with enemies built a Level up: a party of four plain fighters wins about as often as our sample parties.
- A deep pass put every Technique on every character it fits, by the day; healing between fights is what moves. A synergy scan of 599 pairs found nothing outsized: most pairs just add up, and healing on healing overlaps.
- Fixed the simulator letting Whirlwind work with bows and thrown weapons; its text says close-range only.
- A first scorecard (days won a Level up, damage share, Downs, pairs, whole parties) on optimized builds: Cunning, Essence and Healing Magic on non-healers show up again and again, and the optimized Sable wins 90% of days a Level up with three plain fighters.
- The build optimizer finished both runs, and the first Hall of Fame is in (`design/enemy_sim/hall_of_fame/v1.2/`): 39 of the most broken legal builds, ranked by the toughest day they can win, with a watch list. Nearly all of them stack Toughened Resolve and max Essence.

### 2026-10-29 — A whole day, and a build optimizer

The simulator can now play a whole day (two fights, healing afterwards, a night's rest) and score the party by how much Health it wakes up with. A build optimizer has started looking for the strongest legal build for each sample character.

- By the day, at normal enemy Health, healing is worth nearly six times what a single fight showed: without Healing Magic, Hanforth's party wakes up 11 Health worse off and lasts two fewer days in a row.

- Effect weights were re-measured after the Assassin change. Taunted came out stronger, Physical Resist weaker.
- The optimizer's first find is a Hilde with a huge Health pool who takes her friends' hits through Lifeline. She wakes up a few Health short, but her party wins far more days in a row, so it's on the watch list.

### 2026-10-28 — Proposed builds, and a pass over every Technique

Drafted Level 2 and 3 builds for Felix, Enith, Ashleigh and Sable that level the way the designer's own characters do, then ran every Technique and Feature the simulator plays through a broad test to see how well it can tell what each is worth.

- The proposed builds now sit close to the designer's in a fight (best attack 10, other Defenses about half a point lower).
- The simulator gained Interrupts that cancel, redirect or re-aim an enemy's attack (five Techniques, plus Storm of Blades for a two-weapon striker).
- Each reading repeats well, but a Technique's worth depends a lot on who carries it, and its XP cost barely predicts it. Sanguine on its own costs a caster's party a lot (down for an overhaul); Feint still never pays.
- Assassin enemies now go for the most hurt PC and, all else equal, the one in the lightest armor, instead of whoever happened to be listed first; Level 1-2 fights got rougher. Interrupts are checked to happen before what triggers them.

### 2026-10-27 — What each mechanic is worth, and the whole catalog in the sim

Measured what every combat Feature of every Buildable Technique is worth in a fight, next to THE TABEL's price, then wired the rest of the Technique catalog into the simulator. Damage and healing land close to their weights; most debuff riders land at a tenth to a third, and who carries an effect matters as much as what it is.

- Hilde's and Browndog's Battle Maneuvers got the same broad sweep as Hanforth and Beornhard: Half Guard is the standout Feature, and Viper's Sting is the best addition to Hilde's Level 3 copy.
- The simulator now plays 120 of the 205 Techniques, with 44 out of combat and 41 waiting on something it doesn't have yet; every Encounter use carries its Level, which brought in Vigor, Willow Springs Back, Placeholder's Alacritous Adaptation, Blood-Powered Spirit and Spellblade.
- The party can switch tactics in one setting (all in, cautious, max range, hold the line, bodyguard, focus fire...); playing as built or all in does best, and holding the line costs the most.
- The simulator runs about two and a half times faster, always plays the current CSVs (weapons and armor included), writes out every sample character's sheet, and lists the ones whose exports need a rebuild; every character now holds its AP between turns for Interrupts, per the rules, and a Magehunter bug that gave free attacks to anyone with an Interrupt is fixed; neither moved the numbers much.
- The last two days' sweep tables reported "Health" that was really a share of the party's max Health, about half a point each; they're relabeled, and the comparison tool now counts points.

### 2026-10-26 — Hanforth as built, and how healers scale

Hanforth's own 125 and 175 XP builds are in the simulator, and he heals about once every two fights at every Level. Yesterday's Lifeline numbers came from a made-up Level 2 Hanforth: the real one doesn't take Lifeline, and someone goes Down in 16% of his party's Level 2 fights, not 2%.

- Put in Jackal's seat, the healer starts a step behind her at Level 1 and ends a step ahead by Level 3, mostly by keeping people standing.
- Notes for the Healing and Blessing magic pass: the heal barely grows from Level 1 to 2, cards do more saving a hit than healing, and Spirit Blessing's budget only grows a point a Level.
- Tried 45 other picks for Hanforth. Keeping him standing (Lifeline, Toughened Body) beats any Healing Magic or Spirit Blessing swap, Guardian Angel and Triage beat Vitality, and Shielding is as good as any blessing.
- Did the same for Beornhard's War Magic: plain damage beats every rider, and his Level 4 spell does best as one big Lance shot, since he seldom gets close enough to use a Shape.

### 2026-10-25 — Every Technique and Ability in the simulator

The simulator now plays every combat Technique and Feature a character can pick and every Ability in the enemy catalog, reads the characters straight from their Builder exports, and can swap one character's build for another and show what changed. Hanforth's Lifeline turned out to be the big one: with him in the party, someone goes Down in 2% of Level 2 fights instead of 19%.

- New on the party side: Beornhard's Shadow Jaunt, Gainsay and Wall of Shadows, Hanforth's Gust of Wind, Lifeline and Spirit Blessing, Blinkstep and Parting Shot, and nearly every War Magic, Battle Maneuver, Spirit Blessing and Healing Magic Feature.
- New on the enemy side: grappling, cleaving, Retribution Aura and the rest of the catalog. No sample enemy uses them yet. Retribution Aura looks far stronger than its draft price.
- Drafted 22 alternate builds (a Frost Beornhard, a Flurry Hilde, six different Hanforth blessings and heals...). Most swaps cost the party a little. Giving up spell damage for Slowed or a Push mostly doesn't pay. Flurry and Piercing Elements do.
- Reorganized the simulator so each Technique and Ability lives in one place, and a sheet naming one the simulator doesn't know, or spending past its Feature Budget, stops with an error instead of being skipped.

### 2026-10-24 — The sample characters, as built

The simulator's Hilde, Browndog, Carrick, Jackal and Beornhard now play the way their players built them, at Level 1 and at the designer's new 125 and 175 XP versions. Thrown weapons now hit as hard as the item list says, a point less than the simulator had them.

- Added the Techniques those builds use that the simulator didn't have yet, from Brace and Furious Rage to Beornhard's Level 4 line spell.
- Leveled the right way, the party pulls further ahead of same-Level enemies, not closer: at Levels 2 and 3 it hits close to nine times in ten.
- Light Two-Handed weapons (a spear, a staff) can use Brawl as well as Melee.
- Fixed a rulebook example that called Jackal "he".

### 2026-10-22 — A weak, an average and a strong price

The weights table now gives each buff and debuff three numbers: a weak case (riding whatever you hit), an average one (aimed in an ordinary fight) and a strong one (aimed at a boss in a hard fight), with a short guide to which one to use. The old single number stays until the designer decides whether the average should replace it.

- Filled the missing cases in the simulator: Push turns out to gain the most against a hard-hitting boss, and Necrotic is worth its price once the enemy has Protected to cancel.

### 2026-10-21 — Every buff and debuff, measured

Fixed how the simulator scores fights when it prices things (it was reading Styles and effects 2-6 times too high), then measured every buff and debuff against THE TABEL, in ordinary fights and against enemies tougher than the party. Control riding whatever you hit is worth a fraction of its price, the same control aimed at a big threat is worth about its price or well over it, and new weights are proposed for a look before anything changes.

- In ordinary fights, Crippled, Slowed and Bad Luck are worth about a third of their price for one stack and much less for big doses, since the enemy you just hit rarely lives to feel them.
- Against a 2-slot Brute Chief or a harder-hitting Ogre, the same effects aimed at the boss are worth up to ten or more times as much, and Taunted pays only when the tank aims it.
- On the fixed scoring, Seize the Moment reads like a Level 1 Style again, and Stagger no longer wastes places on the dead.

### 2026-10-20 — What "spend" means, and what Bleeding's worth

The rulebook's section on costs now says what spending something means (it's paid and does nothing else), so an ability can say "spend up to 3 of the target's Bleeding" without spelling out the rest. Bleeding got priced under its new rule, about 1.8 Value for the first stack in a dose and 0.8 for each one after, along with what spending it on other effects would be worth.

### 2026-10-19 — Bleeding's new rule

After a dozen setups in the simulator, Bleeding now loses half its stacks (rounded up) each time it decays, and Protected stops its ticks: big doses pay off without changing what Bleeding costs the party overall, and Protected blunts it rather than shutting it off. Bleeding still hits the party harder than it helps them, so the next step is pricing each side for what it actually lands.

### 2026-10-16 — Bleeding's levers

Tested different ways Bleeding could tick and execute, then a middle road: Bleeding loses half its stacks (rounded up) each turn, and a few techniques cash in the rest the way War Magic's Reign of Blood does. Reign of Blood comes out just under spending the same points on straight damage, and a draft Battle Maneuver version (Open the Wound) speeds fights up more than one that puts Bleeding on.

### 2026-10-11 — Cards from the Character Sheet

A new "Make cards" button on the Character Sheet opens your techniques and items in Card Builder as poker-size cards, ready to download as pictures or as a Tabletop Simulator deck.

### 2026-10-09 — The simulator gets a hand of cards

The simulator now deals every character a hand from their own deck and plays it the way the table does, and the last three sample characters (Felix, Enith and Ashleigh) are in with their own abilities. With cards, Level 1 fights come out close to the table on length, losses, Downs and Wounded.
- Setting up the new characters fixed the Feature builder, which now enforces once-only Features and gives Bare-Handed and Tormenting Curse their extra points. Doubleshot now asks for Acrobatics instead of an old Skill name.
- Once the party has its cards, Bleeding comes out at about 0.9 Value for a first stack, so the simulator's been testing fixes: the best so far drops a creature whose Health falls to half its Bleeding stacks. Fleeting effects now only skip their first removal when gained on your own turn, and Bleeding never skips.
- The glossary's Play entry now matches the rulebook (a played card replaces a flipped card or just adds its suit), and enemies deal +1 damage on a Heart for now.

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
- Each copy of Temper Soulblade now has a dropdown of the Held Masterwork powers at that copy's Level, and the Character Sheet shows what the picked power does.

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
