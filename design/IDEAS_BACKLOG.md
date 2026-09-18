# Ideas backlog

Loose ideas for items, abilities, and other content that came up during
design/balance sessions but weren't acted on immediately — a holding pen,
not a commitment. Move an idea out of this file (delete it here) once
it's actually been drafted into `items.csv`/`techniques.csv` and given a
real writeup in `RULES_DESIGN.md`/`balance_weights_notes.md`; don't leave
a stale duplicate sitting in both places.

## Reviewed and declined

A running log of ideas that got a real look and were explicitly decided
against — distinct from the rest of this file, which is ideas still
queued to draft. Kept rather than deleted: "decided against for now"
isn't the same as "never revisit" (see the Cloth/Leather section below
for two ideas that got exactly that treatment, on material grounds
only). New entries append here going forward whenever something gets
cut, not just backfilled at a point in time.

- **Immaculate Spice Rack** (Masterwork) — cut; the game has too few
  Craft flips in actual play for a cooking-specific Good Luck bonus to
  matter, and Placeholder's Wondrous Workspace already covers the
  "waive tool requirements" niche.
- **Choker of Silent Whispers** (Neck) — cut; a strictly worse reskin
  of Headband of Telepathy (Head) — half the range, a single message
  instead of a standing channel, plus a visible tell the original
  doesn't have.
- **Cape of Many Pockets** (Belt) — cut; a clean duplicate of
  Bottomless Belt/Sash of Deep Pockets' own "carrying items" lane, no
  real differentiation.
- **Cloak of Faces** (Masquerade) — cut; sourced from the old design
  doc's own rejected-ideas dump ("THE BIN"), not the real item list,
  and mechanically an outlier — an unconditional, no-check
  transformation with no precedent among the Masquerade family's
  disguise-CHECK shape.
- **Ring of Charming, Assertive, or Bold Statements** (Ring) — cut;
  exact same shape as the Head slot's social-hat family (Confident
  Cap etc.), no differentiation beyond which slot it's worn on.
- **Returning Knives** / **Weapon of Sending** (Held) — both cut;
  thrown weapons are meant to be an abstracted "you have enough to
  fight with" collection recovered after the encounter, not tracked
  square-by-square — so "return a thrown weapon mid-fight" doesn't
  solve a real problem under that design call.
- **Staying Gauntlets** (Hands) — cut; redundant with Bounty Hunter's
  Blade, which solves the same "remove the risk of an accidental
  kill" problem via the same mechanism (bypassing the Non-Lethal
  Attacks penalty).
- **Elemental Bloodletter** (Held) — cut; the Bleeding-conversion half
  loses badly (~−77 Net) once checked against Bleeding's own capped
  curve versus guaranteed Health loss — a structural finding, not a
  tuning miss. Superseded by the Held slot's existing
  elemental-conversion options.
- **Sorcerer's Gloves** (Hands) — cut; superseded by Sorcerer's Bow,
  which covers the same "Sorcery Skill Total drives a weapon-style
  attack" niche.
- **Apprentice's Dueling Catalyst** (Held) — cut as obsolete; predates
  the Implement tag existing, which already makes Bounty Hunter's
  Blade's non-lethal waiver apply to spell attacks channeled through
  it.
- **Spiritlink Scepter** (Held) — cut; strictly obsolete once Reaching
  Weapon (same Range bonus, broader scope) existed.
- **Scepter of Evocation** (Held) — cut; an earlier, narrower draft of
  what became Thrumming Focus.
- **Stoic Skullcap** (Head) — retired from the Head social-hat family
  (its "resisting others' persuasion" flavor doesn't fit that
  family's own-Skill-buff shape); name/fluff reserved for a future
  Neck item instead — see "Neck slot — reserved flavor" below.
- **Bloodshard Ring** (Ring) — cut as an item (no usage cap made it
  impossible to price cleanly); the mechanic itself was sound and
  moved to a Technique idea — see "Spend-Health-for-damage Technique"
  below.
- **Flamefist's Approach** (Ring) — cut as an item (the Brawl/Spell
  interplay fits a toggled Form better than a passive Ring); moved to
  a Technique idea — see "'Flamefist' Form Technique" below.
- **Assassin's Undetectable Arms** (Held) — cut as a standalone item;
  the concealment mechanic works better folded into another item as
  an accessory effect. Partial pricing sketch (~1.53 raw Value, a real
  shortfall either way) preserved in case a home for it comes up.
- **True-Seeing Lenses** (Head) — cut; per the designer, Invisibility
  and illusion magic are intentionally not mechanics in this game, so
  a detection tool built around piercing them has nothing real to
  detect. Too niche to earn a slot, not a balance problem — draft
  read at 27% funded (Good Luck on a disguise-detection check, ⅓
  niche tier) before the designer called it.
- **Circlet of Clarity** (Head) — cut; "resistance to Charm/domination/
  mind-control" turns out to already be what Mental Defense itself
  represents (`rulebook.md:310`'s own flavor text: "resist fear,
  compulsion, and other mental manipulations"). No separate
  Charmed-style keyword exists to grant resistance *against* the way
  Cowl of Tranquility hooks into the real, live Taunted/Frightened
  keywords — so this wasn't a distinct gap, just an already-covered
  Stat doing its job.
- **Comprehend Languages Circlet** (Head) — cut; this game doesn't
  have a language system at all beyond Goblins' illiteracy *flavor*
  trait — no language list, no "you don't speak this" friction for
  any Skill to gate. Nothing for the item to actually remove. Third
  candidate in a row to hit this exact wall (see True-Seeing Lenses,
  Circlet of Clarity above) — worth remembering as a pattern before
  reaching for another "detect/pierce/understand X" Head concept:
  check whether X is a real mechanic in this game first.

## Techniques with stale "Social Contest"-era mechanics, need real rework

Found while doing the Social Contest → Social Encounter terminology
rename across the codebase (see `scripts/rulebook.md`'s Pressure/Social
Encounter sections, `design/balance_weights_notes.md`'s Social Encounter
Baseline). These four `techniques.csv` rows got the plain text rename
("social contest" → "social encounter") since that much is unambiguous,
but each also references a mechanic that no longer exists in the
current Statement/Support/Pressure system — a real design decision, not
a find-and-replace, so flagging here instead of guessing:

- **T058 Challenge, T062 Cry of Victory, T067 Exert Pressure** all key
  their social-encounter Interrupt off "while in the front, when you
  succeed on a Charismatic statement." Neither "front" positioning nor
  a "Charismatic" statement type exists anywhere in the current rules —
  Support doesn't require "back" positioning, and statements aren't
  typed Charismatic/Strategic/etc. in the current text (Strategic shows
  up elsewhere, e.g. T054/T057/T068, so that half might still map, but
  "front" doesn't map to anything). These three all currently read as
  combat Techniques with a bolted-on social side-effect (Taunt/Frighten
  a target once) gated on a condition that can't currently be
  satisfied. Needs a decision on what the trigger should actually be —
  maybe "when your Statement succeeds" with no positioning clause, maybe
  something else entirely — before these are usable as written.
- **T061 A Perfectly Good Explanation**: "Whenever your party would
  gain Concessions in a social encounter, as many times as you like you
  may discard a card and reduce those Concessions by 3 (or 4 if you
  discarded a Heart)." This predates the Pressure rework entirely —
  "Concessions" was the old mechanic Pressure replaced. The shape of
  the effect (discard a card to blunt the party's rising social cost)
  actually maps reasonably well onto "discard a card to remove some
  Pressure," but that's a judgment call on the conversion rate, not a
  literal rename, so it's flagged here rather than silently converted.

## Source material to mine: cut FlagonQuest content in `archive/`

Distinct from the dice-game import below — this is old *FlagonQuest's
own* design work that never made it into the current ruleset, sitting
in `archive/flagonquest_site_techniques.md`/`flagonquest_site_items.md`
and similar old site exports. Distraction (`T144`) is the first real
case of pulling one of these back in: found in an old draft, rebuilt
against a current-ruleset sibling (Vanish, `T052`) rather than revived
as-is, since old mechanics/terminology/Level assignments don't
necessarily still fit. Worth treating as the template for future
pulls — find the old draft, find its closest live analogue, rebuild
against that rather than trusting the archived numbers directly.

**Full sweep completed** across all three `archive/flagonquest_site_*.md`
files (items, techniques, other/rules — ~23,000 lines combined),
cross-checked against current `items.csv`/`techniques.csv` and this
whole file, so nothing from past versions should be sitting
unaccounted-for. Coverage turned out very high already — both catalogs
are direct ancestors of their current counterparts, and most named
old items/techniques already exist live, often under the same name.
The lists below are what's left: genuinely new, not-yet-addressed
material, organized by theme. Old terminology throughout is already
translated to current (Soak→Resist, Elementalism→Sorcery, etc.).

- **Placeholder's Sneaky Storage** (old Level 2 General Spell,
  `(Elementalism or Theurgy) 3` + `Stealth 2` or `Legerdemain 2`,
  three slightly different drafts in `archive/flagonquest_site_techniques.md`)
  — grants a small extradimensional storage space (old text: "Weight
  of 2," the archive's own pre-cubic-meters capacity system), always
  an easily-accessible location, ends if the caster loses
  consciousness (contents dump into adjacent spaces). Cut during
  development; doesn't exist in `techniques.csv`/`features.csv`
  currently. Surfaced while reviewing the Storage item family
  (`balance.md`'s Open Balance Work) — per the designer, leave it
  archived for now, but it's the natural next candidate once there's
  a settled Storage-capacity value model to price it against and
  appetite for another archive-recovery pass like Distraction's.

### Items and Consumables (from `flagonquest_site_items.md`)

No new equipment-slot (Head/Neck/Torso/Hands/Feet/Ring/Held/Belt/Other)
concepts survived the cross-check — that catalog is fully mined and
already live. The gap is entirely in Potions/Grenades:

- **Skill-cluster "reflip" Potions.** The current game only has this
  pattern twice (Energizing Brew/Reflex, Liquid Charisma/Presence-
  Persuasion-Rapport); the old doc had one per cluster. **Bottled
  Wit** (Legerdemain/Awareness/Disguise/Insight/Survival, 1 hour),
  **Profound Potion** (Academics/Craft/Sorcery-non-Spell/Medicine/
  Mixology, 1 hour — check this name isn't already spoken for; the
  Wizardly Hat/Alcohol-suite writeup in `balance_weights_notes.md`
  references a potion by this name as what prompted that whole line
  of work), **Strongbrew** (Athletics/Might/Centering/Intimidate, 1
  hour), **Steady Heart** (reflip Acrobatics/Stealth + Good Luck on
  Reflex + reduces the first Forceful social attack each encounter —
  more complex, multi-part).
- **"Extra Action" Potions** — no current potion grants a flat extra
  action (Swiftblade Vial's Hasted+reposition is a different shape).
  **Extra Heartbeat** (extra Main action this turn), **Coursing
  River** (extra Move action for the rest of the scene). A strong
  pair; needs real balance scrutiny before drafting given how big an
  extra action is.
- **Heaven's Kiss** — ignore all Wounded stacks until end of scene.
  Kiss of the Earth/Predator's Cry cover Bleeding/Crippled-Slowed;
  Wounded itself isn't covered by any current Potion.
  **Essence-Infused Bauble** — restores 1 Focus (old "Willpower"
  term) on use; no current Potion restores a resource point like
  this (only the deferred Crown of Glory capstone touches it).
- **Lower priority / needs real reframing, not just translation:**
  Quartz Tincture (damage + old "Off-Balance"/"Prone," neither a
  current keyword), Reaper's Mist (Shadow damage + old "Weakened,"
  also redundant with Bonemelter/Harrowing Ichor already covering
  that niche), a second Hellfire Bomb variant (repeating/unavoidable
  attack, name conflict with the current item), Cobblestone Boots
  (walk the sea floor at full Speed — Swim Flippers already covers
  Feet's water-utility niche from a different angle), Orb of the
  Weave/Wand (cast a spell you don't know via the item — corroborates
  the already-logged Tome of Mana Bolt gap, not a new finding).

### Techniques and Spells (from `flagonquest_site_techniques.md`)

By far the largest source of unmined material — this file is ~12,000
lines and several whole old families (Battle Magic→War Magic, Blessing
Magic→Spirit Blessing, Healing Magic, Social Contest Techniques→Social
Maneuver, Martial Strikes→Battle Maneuver) already got a full
systematic redesign into today's Feature-Budget techniques. What's
below is what's left after checking each family's current Feature list
against the old drafts — genuinely missing mechanics, not just
unported flavor text.

**Sorcery spells**: Force Barrier (Counter an attack targeting Parry —
roll Sorcery and substitute for Dodge instead, ignoring Harried — no
current "roll to dodge" reactive spell exists), Bindings of Force
(ranged magical grapple — no ranged-grapple mechanic exists anywhere
currently), Elemental Storm (spell attack leaves a delayed hazard zone
that keeps attacking), Shadowfrost Bolt (capstone; attacks whichever
of Fire/Frost/Shadow the target resists least — a novel "targets your
weakest Resist" mechanic), Concentrate Arcana (spend Focus as a
Counter right as you cast, to boost that cast).

**Theurgy/Nature spells** — a large, mostly-untouched vein even though
Sculpt Stone/Weatherworking/Earthquake/Cloak of Awe made it in: Wild
Shape (full animal transformation — classic archetype, absent
currently), Control Weather, Alarm Ward (12-hour perimeter alarm),
Birdsight (bird familiar, see through its eyes), Windweaving
(breathable-air bubble, or Counter a fall to land safely), Door of
Respite (extradimensional rest shelter — distinct from Sneaky
Storage's item-storage niche above), Fog Cloud (steerable obscuring
fog), Mark of Smiting (mark an ally; their next hit converts some
damage to Spirit), Ring of Entropy (Weakens anyone entering/starting
their turn in a rune-trap zone), Commune With Nature (wilderness
divination, 15km), Curse of Mortality (Necrotic + strips temporary
Health), Dust to Dust (disintegrates dead organic matter, ignores
Armor Soak), Entangle (vine zone, Snares), Heat Metal (remotely heat a
metal weapon/armor), Plague Cloud (disease-miasma zone), Step Into the
Earth (meld into solid earth to move through it, blind), Interdict
(Snare + Off-Balance).

**General Spells** (school-neutral utility "cantrip" magic) — a whole
layer that didn't make it in at all: Identify Magic, Minor Illusion
(known-fake image/sound), Sympathetic Sight (see through a linked
creature's eyes), Telepathic Sending (one-way single-sentence, distinct
from the current group Telepathic Link), Wisps (persistent following
candlelight), Freeze/Scorch (heat/chill a small object), Glittering
Trail (party-only visible trail), Quick Sober, Placeholder's Accurate
Artistry (instant perfect sketch), Placeholder's Covert Conclave
(eavesdropping/scrying ward), Placeholder's Instantaneous Instrument
(Conjure Armament variant for musical instruments), Placeholder's
Meticulous Mending (repair/clean a mundane object), Blood Magic (spend
Health, Interrupt, any time, to regain a Spell Encounter Technique use),
Prepared Magic (pre-load a spell to cast free next turn), Counterspell
/ Spell-Rending Arcanology (Counter a creature starting to cast, spell-
attack to negate it — a genuine counterspell mechanic, nothing like it
exists currently), Sudden Abjuration (expend spell uses reactively for
temp Health when hit), Infuse Summon (extra turn for a summoned
creature), Swordsoul (the mirror of the already-live Spellblade —
expend a *Martial* Encounter Technique to fuel a magic attack instead
of the other way around).

**Martial reactive/defensive tricks** — checked directly, nothing in
`techniques.csv` lets you substitute a roll for your Defense or negate/
redirect an attack outright: the Flashing Steel/Lucky Dodge/Tumble
family (Counter an attack, substitute a fresh roll or a discarded
card's value for Parry/Dodge, ignoring Harried), Cleave Magic (melee
Counter against a spell attack — weapon-attack roll as Defense,
redirect the spell back on a miss), Veil of Dispersing Shadows /
Unbreakable Stone Anchor / Unmovable Stone Anchor (capstone "ignore
this attack" defenses), Parry Cover / Intervene (redirect an attack
from an adjacent ally onto yourself), Final Feint Strikes the Heart
(3-attack combo, first two are damage-less setup, third bypasses Armor
Soak with guaranteed Hearts), Deadeye Shot (unlimited-range called
shot), Hammer and Anvil (shield bash Push + free ally follow-up),
Obliterating Smash (two-handed cleave, chip damage even on a Dodge/
Parry), Shield Slam (Stunning bash), Adaptive Style (Martial's own
Channel Ki/Warmage's Reserves — expend one Encounter Technique to
regain another), Moment of Celerity (spend Soul for a genuine extra
Main action — no current technique grants one).

**Combat Stances** (general Martial, not tied to a named Style) — a
whole unported family, ~20 tradeoff-based postures. Representative
sample: Alacritous Posture (Main/Move as Extra/Counter if unused),
Half-Guard/Drunken Brawling/Shifting Ground (Speed-for-defense),
Breaching Blows/Earthen Fist Posture (offense-for-defense, two-
handers), Doubleshot (double ranged attack as a Full action), Group
Bulwark/Lend Bulwark (share your shield's Defense with an adjacent
ally), Sentinel (shadow an adjacent enemy's movement), Iron Vanguard
(shield-tank, Bad Luck to attackers), Raptor's Precision/Swashbuckler's
Focus (accuracy/speed or single-target tradeoffs), Earthen Mantle
Approach (elemental Resist for defense).

**Discipline/Martial-Arts Styles** — only 1-4 techniques per Style
made it in; the rest of each tier ladder didn't. **Great Old Oak
Style** and **Ki Style** are entirely absent (0 ported) — Oak is a
defensive/endurance style (ignore Harried, counter-and-heal, remove
debuffs mid-swing, regen on hit, deflect as a Counter); Ki is a
teleport/chakra-disruption style (teleport-then-strike, Spirit-damage
unarmed, disintegration finishers, Weakened strikes). **Bear**, **Demon**,
**Shugen**, and **Snake** each have several tier-ladder entries still
unported (defensive-mauling Parries, Bleed-on-Parry, disarm Counters,
AoE knockdowns, Vulnerable-on-hit stances, self-sacrifice strikes,
disintegration/chain-binding/teleport-swap/mind-shatter/shuriken
options, trip-Counters, Slowed dual-wield stances, Parry-redirect).

**Card/luck-economy techniques** — nothing currently manipulates cards
beyond Grim Resolve's "spend Health, draw a card": Intuitive Maneuver
(swap a played card for deck-top), Lucky (passive card draw after a
rest), Minor Oracle (peek/cull your own top cards), Focus and
Conviction/Strength and Conviction/Words of Encouragement/Roll the
Dice (spend Soul or Focus to draw 2 discard 1, self or ally), Font of
Inspiration (nearby allies reflip low cards when you spend Soul),
Morning's Determination (keep 1 card through the rest-discard),
Primal Intuition (cull top cards on demand, but must reshuffle your
discard pile every rest — real risk/reward), Mastermind (capstone,
permanent +1 max Focus — no current technique raises a resource cap).

**Battle Maneuver leftovers** (old Features with no current match):
Riposte/Counterstrike (counter-attack on a Parry/Dodge), Opportunist
(punish a retreating target), Pinpoint Flash (teleport into range
before attacking), Hemorrhage (bypass Armor Soak, convert lost Health
to Bleeding), Shockwave/Scattershot (splash to an adjacent target or
ranged cone), Inescapable Claw (miss → free second attack), Stagger
(deny a Move each round), Execute (finishing Bleed scaled to missing
Health), Fighting Spirit/Ten Ton Hammer (spend extra Willpower for a
bonus).

**Social Maneuver leftovers** (same idea, social side): Gritty
Countenance-style Defense-swap-for-front-member, Corner and Interrogate
(force the same front members next turn), Bow Out (remove yourself,
negate a Demerit), Fast Talker (extra turn in the contest), Logos
Overwhelming (Disadvantage on the opponent's next Statement), Instill
Emotion (crowd mood-shifting outside a formal contest), Storied
Adventurer/"Impressive" Reputation (reputation-based Good Luck on a
first social flip with a stranger).

**Craft/Mixology utility**: Immaculate Saucepan Methodology/Stately
Tailoring (reflavor a dish/restyle a garment), Deploy Mounted Launcher
(summon a temporary turret from materials), Scraptrops (scatter
material caltrops), Essence Admixture/Catalytic Activation (buff a
Potion/Grenade you personally crafted), Inspirited Armaments
(temporarily grant a Masterwork enhancement to gear you crafted),
Reactant Brewing (transmute one alchemical good you know into
another), Saboteur (rig a disabled trap/device), Vessel of Belief
(bank committed Soul/Focus in an item, released to whoever uses it),
Philosopher's Metallurgy (convert materials up/down a Level).

**Alcohol-cost techniques** — direct hits for the already-queued
"Alcohol-cost Technique suite" below: Flamebreath (drink, breathe fire),
For Medicinal Purposes (drink to heal/reduce a poison, scaled to the
drink's Level), Victory Swig (drink on a kill, Frighten onlookers).
Worth reusing as worked examples when that suite gets drafted.

**Misc Skill/Utility**: Hunter's Mark (Survival — mark + Slowed on
next hit), Speak With Animals, Assert Dominance (Survival —
intimidate a wild animal), Hidden Meaning/Secret Cant (Streetwise
coded speech), Dark Powers of Commerce (fair-value trading + market
research), Encrypt Letter, Perfect Poise (Integrity — immune to
Insight reads except lying, ignores appearance penalties), Perfect
Visual Analysis (eidetic memory, instant estimation), Trivia Master
(Academics, Daily — recall a fact on demand), Animal Companion: Combat
Training/War Training (a missing mid/high progression tier — current
game only has base + one Trick tier), Spider Climb, Overbear (double
Carrying Capacity/ignore Might for backpacks), Hulking Hurl (Might —
throw a heavy object as improvised ranged), Tavern Brawler
(improvised weapons count as real; destroying one on a kill Bleeds
nearby enemies), Plaguebearer (a Corrupted Blood sibling using disease
instead of poison).

No additional storage-granting spell drafts turned up beyond the three
already logged for Sneaky Storage above.

### Rules and GM notes worth reviewing (from `flagonquest_site_other.md`)

This file turned out to be overwhelmingly superseded material — an
export from at least three distinct earlier rules eras, over a third
of it sitting in the designer's own explicit "Quarantine" (deprecated)
section. Checked systematically against current `rulebook.md`/
`glossary.md`/`design/RULES_DESIGN.md`/`design/GM_GUIDE_NOTES.md`;
confirmed already-superseded (not re-flagged as findings): the old
Rules Tags/Common Effects/Type Tags glossary (all current except
Bolstered, already documented as deliberately cut), two old Stat/Skill
taxonomies (5-Stat and 7-Stat, both superseded by the current 4-suit
system), old Summoned-creature rules, the DM Notes item-tier math
(already incorporated, see `balance.md`'s "Common/Uncommon/Rare/
Extraordinary tiers" section), old "Stunting" (superseded by Bingus/
Golden Bingus), and old movement/climb/swim/jump formulas (superseded
by the current Athletics budget rules). A large fraction of the file's
bulk is also just old Technique/Item text blocks belonging with the
sweeps above, not separate rules content.

What's actually left, worth a look:

- **A "Destroying Objects" rule** — a compact, complete mechanic for
  breaking scenery/objects: four Soak(→Resist) tiers by material
  category (Delicate/Normal/Sturdy/Impenetrable) crossed with three
  Health tiers by size (Small/Medium/Large). Confirmed no equivalent
  exists anywhere in current `rulebook.md`/`glossary.md` (no hits for
  break/shatter/smash/inanimate/construct). The one candidate here
  with real teeth — a ready-made starting point if formal
  object-destruction rules are ever wanted.
- **Legend Binding** / **Palhalla** — binds a chosen item to you
  permanently (unlosable, always retrievable), old-costed in "Glory"
  (a resource that no longer exists). The underlying concept — a
  signature item that can never be stolen or lost — has no current
  analogue; would need a real cost mechanism designed fresh.
- **Meta Book** ("Basics of Roleplaying") — no-metagaming guidance,
  keeping character politics separate from the table, a plain
  GM/player gameplay-loop description. Current `rulebook.md` only has
  a one-line "GM has final say" note; this is fuller onboarding-style
  framing that may or may not fit a rules-only rulebook's scope.
- **Skill-rating flavor text** — narrative description of what Skill
  ratings 0-5 feel like in-fiction ("a base level of competency,"
  "among the elite," etc.). The specific numbers reference the old
  dice-pool scale so wouldn't port directly, but the framing device
  itself could be adapted.
- **Design philosophy fragments**, repeated across several old
  sections: a "Variety / Distinct / Obvious / Prune" four-point design
  checklist, and a "Barrier vs. Justification" framing for why prereqs
  exist. Not tied to any specific current mechanic — generic design
  wisdom — but could fold into `RULES_DESIGN.md`'s own meta-principles
  if useful as a standing checklist.

## Source material to mine: the dice game's item list

A large batch of items from a separate dice-based tabletop game (its own
Mana/Range-in-spaces/dice-damage system, not this game's AP/meters/card-
flip one) was handed over as inspiration for FlagonQuest items across any
slot — real per-item translation work, not reskinning, since the
underlying mechanics don't map 1:1. Full source list, organized by what
they'd likely translate as once someone sits down with a specific one:

**Consumables** (candidates for Potion/Grenade/Poison, or a Food-adjacent
category): Blade Poison, Blink Potion, Bottled Sunlight, Elixir of Might,
Lucky Coin, Goop Jar, Grave Jar, Healing Potion, Hero's Potion, Mana
Potion (no direct Mana-analogue in this game — would need reframing
around AP/cards/a resource this game actually has), Shockwave Jar, Tile
of Escape, Deadly Poison (+), Earthen Potion (+), Elixir of Precision
(+), Inferno Jar (+), Restoration Potion (+).

**Permanent Consumes**: Tome of Mana Bolt (would need a real spell-
granting mechanic analogue).

**Charms** (likely Ring or Neck candidates — small always-available
triggered effects): Blink Charm, Charm of Ambition, Deflecting Charm,
Gambler's Charm, Goading Charm, Hunter's Handbook,
Repelling Charm, Restoring Charm, Ring of the Skull Oath,
Shielding Charm, Thug's Shiv, Thunderstone Bracelet, Weighted Pommel,
Wizard's Earring, Crab Demon Figurine (+), Lifeforce
Shard (+), Regrowth Amulet (+), Shockwave Talisman (+), Vampire's Fang
(+), Venomstone Pendant (+). (Pillar Talisman, Ring of Comets, and
Dryad's Mantle drafted and priced — see Pillar Ring, `I255`, Ring of
Comets, `I256`, and Dryad's Mantle, `I257`.)

**Equipment** (Feet/Held/Torso/Belt candidates mostly, a few Head-shaped
by name but combat-mechanical rather than mental/vision — see the Head
slot note below): Belt of Stanching, Berserker's Helmet, Blazing Boots,
Coward's Shoes, Cursed Mask, Dark Sash, Eagle Claw Bracer, Earthen
Girdle, Flask of the Moon, Flask of the Sun, Gauntlets of Wrath,
Gladiator's Crown, Hermit's Pouch, Lodestone Bracers, Orb of Purity,
Ranger's Bracers, Sandals of Travel, Sanguine Illusionist's Mantle,
[Type]slayer (+), Cape of Needles (+), Cloak of Shifting Sand (+),
Fortress Shield (+), Leyline Orb (+), Sundering Sledge (+), Zephyr
Greaves (+).

Note on the Head-shaped ones specifically (Berserker's Helmet,
Gladiator's Crown, Cursed Mask): these are combat-attack modifiers
(reroll-and-keep mechanics, bonus damage against a prior target), not
mental/vision effects — Head's established lane (`RULES_DESIGN.md:129`).
They'd need real reflavoring to fit this slot rather than a straight
port. Cursed Mask's "choose an enemy, you both reroll certain results"
has a genuine mental/curse-link angle that could become a symmetric
Good-Luck/Bad-Luck effect on wearer and target. Hunter's Handbook's
"learn a fact about an enemy, gain a bonus" has a nice knowledge/analysis
hook, though the attack-bonus half reads more Ring-lane than Head-lane.

## Artisan's Eye — undocumented "analyze" mechanic

Surfaced while drafting Third Eye (`I258`) off Artisan's Eye (`T046`)
as a precedent. Artisan's Eye's Effects text reads "as though you had
flipped a 13 to analyze it," but no "analyze" check is actually
documented anywhere in `rulebook.md` — the only baseline rule found is
a plain, rollless "a character can determine [a Masterwork item's
effects] in full by examining the item for an hour" line (Equipment
section). Since that baseline already reads as automatic success with
no roll involved, Artisan's Eye's real value-add is likely just
collapsing the hour down to instant (1 AP), not removing some failure
chance that may never have existed. Worth a look whenever Techniques
get a dedicated review pass — either the "analyze" check needs to
actually get written into the rulebook, or Artisan's Eye's own text
should stop implying a flip that doesn't exist.

## Crown of Glory — capstone redesign, deferred

Original mechanic (once/day, wearer + up to 4 allies each draw a card)
set aside rather than rebalanced — see `balance_weights_notes.md`. Not
just a Level-scaling problem (a "wearer + up to 2×Level allies" formula
fit the numbers cleanly); the real concern is that generic party-wide
card generation doesn't fit Head's "mental, vision" lane at all and
reads more like a capstone-tier effect. Revisit once the rest of the
equipment slots have had a first pass — figure out what a genuinely
capstone-appropriate Head effect looks like, rather than patching the
current mechanic's Level or scaling formula.

## Neck slot — reserved flavor

**Stoic Skullcap**'s name and fluff ("these caps provide the wearer a
sense of calm and clarity when dealing with others, a feeling that
intensifies the more another tries to menace or win them over with raw
charisma") were retired from the Head slot's social-hat consolidation
(see `balance_weights_notes.md`) specifically to be reused for a future
**Neck**-slot item dealing with Pressure directly, once the Neck slot
gets its own pass — matches Neck's "niche, boring, passive utility"
lane (`RULES_DESIGN.md:129`) better than an offensive Skill-buff family
did anyway.

## Alcohol-cost Technique suite

A planned suite of Techniques that use Alcohol as an additional cost,
prompted by revisiting Wizardly Hat of Tam the Tipsy. Real anchors
established while pricing that item, worth reusing when this suite gets
drafted: `Gold = 1.5` raw Value (Locked, `balance_weights.csv`), so
Alcohol's own Value by Level is `1.5 × Level` (1.5, 3.0, 4.5, 6.0, 7.5
for Levels 1-5); and the working (unverified) assumption that a Level-N
Technique effect is worth about the same `Level × 3` a same-Level item
would be. See the Wizardly Hat writeup in `balance_weights_notes.md` for
the full accounting, including why a 2 AP activation cost read as a net
loss at low Levels and why 0 AP reads much better.

## Spend-Health-for-damage Technique, pulled from Bloodshard Ring

Original Ring mechanic (`I081`, Level 2, cut from `items.csv`): "Before
making a spell attack that deals damage, the wearer may spend X Health.
If they do, the spell attack deals its damage as Fire, and deals an
extra X damage. If the spell attack only has one target, then instead
it deals an extra [twice X] damage." Worked through during the
Ring-slot balance pass — the raw Health-for-damage trade is close to a
wash, not a trap: break-even at 1-2 targets hit (`Net = 2X(N−2)` for N
targets, since the bonus damage applies per target on an AoE, priced at
`X × 2` per target against a flat `4X` Health cost), genuinely
profitable at 3+ targets and scaling with however much Health the
player risks. The flat "deals its damage as Fire" conversion adds a
consistent `~2.0` (same "1 point of average soak bypassed" logic as
Ring of Pure Elements/Worry Token's Diamonds branch) on top, regardless
of target count.

Pulled rather than priced as an item because the original text has no
stated usage cap ("before making a spell attack" reads as usable on
every qualifying attack) — hard to price cleanly without a realistic
usage-frequency assumption the model can't supply on its own. Checked
both `items.csv` and `techniques.csv`: no other spend-Health-for-damage
mechanic exists anywhere in the game currently, so a Technique version
would be genuinely new ground. Worth drafting later — Sorcery-flavored
given the Fire-conversion, or School-neutral as a "sacrifice your own
vitality for raw power" theme — reusing the break-even-at-1-2/
profitable-at-3+ shape already worked out above as a starting point,
and deciding a real per-encounter usage cap as part of that draft
rather than leaving it open-ended the way the ring did.

## "Flamefist" Form Technique, pulled from Flamefist's Approach

Original Ring mechanic (`I086`, Level 4, cut from `items.csv`): two
powers, both once/encounter (uncappable by discarding a card) — a
Brawl hit grants a free Sorcery Spell cast (≤2 AP, targeting a Brawl
target); a Sorcery hit within `[Meditation Skill Total]` meters grants
a free Teleport into a space adjacent to that creature. Broken into
components during the Ring-slot balance pass before pricing finished
(Power 1 as a hit-gated Autoswing; Power 2 as an attack-enabler, once
it became clear `[Meditation Skill Total]` was just the trigger's range
gate, not the teleport distance — the destination is always
"adjacent").

Pulled rather than priced as an item because the whole
Brawl-enables-Spell/Spell-enables-Brawl-closing interplay — a genuine
martial-arts/spellcasting hybrid combat style — reads as a much more
natural fit for a `[Form]` Technique (a stance entered/left at the
start of a turn, per `glossary.md`) than an always-on passive Ring.
Worth drafting later as a Form: the toggled, turn-scoped nature of a
Form suits "while in this stance, landing one kind of hit unlocks a
follow-up of the other kind" far better than a Ring ever could, and a
Technique draft can build in a real once/encounter (or Form-scoped)
cap from the start instead of needing the discard-a-card escape valve
the ring used. The component breakdown above (hit-gated Autoswing for
the Brawl→Spell half, attack-enabler for the Spell→Brawl-closing half)
is a reusable starting point for pricing whichever Level this ends up
drafted at.

## Masterwork recipes as a learned/collected resource, not universally known

Right now any character with the right School and Craft Skill Total
can attempt any Masterwork item's recipe — the only gates are Skill,
materials, tools, and (per the rulebook's own Tools section) *"special
items like Masterwork creations require you to find a specific recipe
for them"*, which isn't currently backed by any mechanic. Per the
designer, base (non-Masterwork) items make sense as broadly known —
a Smithing Kit or similar already implies "you know the basic
recipes" — but Masterwork recipes could be their own acquired,
collectible resource: found, bought, or otherwise earned individually,
the same way a specific magic item is.

One shape floated: standardized recipe-collection items bundling
"all the Level 1 Masterwork recipes" (and so on per Level), while
Level 4-5 recipes stay individual, rarer finds — reflecting that the
most powerful enchantments shouldn't come as part of a convenient
starter bundle. Not drafted at all yet — needs a real pass on how
recipe acquisition actually works mechanically (a new item category?
a Technique? pure GM narrative?) before this goes anywhere. Flagged
here rather than acted on now.

## More Cooking recipes

Per the designer, the Food catalog (currently just Hearty Meal,
Muscular Feast, Power Snack, Soul Soup, Travel Rations — 5 items) is
worth expanding with more Food items at some point, giving Cooking a
bigger direct catalog rather than staying this narrow. Not scoped yet
— just a flagged reminder, no direction on what the new items should
do.

## Two mechanics pulled from the Cloth/Leather gap-filling pass

Both liked mechanically, both rejected on material/slot-lane grounds
(Cloth/Leather is Tailoring's own domain, not a fit for either of
these) — see `balance.md`'s writeup of Quilted Overcoat/Sure-Grip
Boots/Dancing Shoes/Gloves of Misdirection for the pass these came out
of. Worth reviving on a properly-fitting material if either comes up
again, not as Cloth/Leather items.

- **Barbed weapon, Bleeding on hit** — a Leather-wrapped/barbed weapon
  enchantment, "when an attack with this weapon hits, the target gains
  1 stack of Bleeding." Per the designer, Leather doesn't fit how
  weapon enchantments work in this system (that's Carving/Smithing's
  job) — a genuine niche for a future Held item on the right material
  (Bone reads as the more natural fit for a barbed/claw-flavored
  weapon than Leather ever did). Also worth a second look at the
  pricing convention before reviving: the draft used Battering
  Armament's own "priced at a single occurrence/encounter" L1
  convention, but per the designer this likely underprices an "on
  hit" trigger that would actually fire multiple times a fight —
  worth a real hits-per-encounter derivation (the Numbing Edge/
  Fanged Guard precedent) instead of reusing that shortcut as-is.
- **Cord-and-Crippled Ring** — a braided cord ring, "once per
  encounter, for 2 AP, throw a length of cord at a creature within 6
  meters — an attack against Dodge Defense; on hit, Crippled a number
  of times," with a `[Clubs]` suit bonus (Crippled's own suit per the
  portfolio table). Full math was worked out: 4 stacks Crippled
  (Value 15, from the established stacks table) + suit bonus (1.5) +
  Universal Harried credit (1) − Autoswing (5.5) = Value 12.0 against
  a Level 3 Target of 9, Net +3.0 (133% funded) — same "portable War
  Magic"-style shape as Chillstrike Band, just built on Crippled
  instead of Slowed. Rejected purely on material grounds (Cloth/
  Leather doesn't fit Ring's own jewelry-precedent lane), not the
  mechanic itself — the math above is ready to reuse directly once a
  fitting material/slot comes up (Ring on a real Jewelry material is
  the obvious first option, since the mechanic was built for Ring's
  own "active ability" lane specifically).
